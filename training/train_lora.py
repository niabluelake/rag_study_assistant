import argparse
from pathlib import Path

from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
)
from peft import LoraConfig
from trl import SFTTrainer


ROOT_DIR = Path(__file__).resolve().parents[1]

DEFAULT_TRAIN_PATH = ROOT_DIR / "data" / "processed" / "train.json"
DEFAULT_EVAL_PATH = ROOT_DIR / "data" / "processed" / "eval.json"
DEFAULT_OUTPUT_DIR = ROOT_DIR / "outputs" / "health_lora_model"


def format_prompt(example: dict) -> str:
    """
    Alpaca 형식 데이터를 LLM 학습용 프롬프트 문자열로 변환한다.
    """

    instruction = example.get("instruction", "")
    input_text = example.get("input", "")
    output = example.get("output", "")

    if input_text:
        prompt = f"""### Instruction:
{instruction}

### Input:
{input_text}

### Response:
{output}"""
    else:
        prompt = f"""### Instruction:
{instruction}

### Response:
{output}"""

    return prompt


def load_alpaca_dataset(train_path: Path, eval_path: Path):
    """
    train.json / eval.json 파일을 Hugging Face Dataset 형식으로 로드한다.
    """

    dataset = load_dataset(
        "json",
        data_files={
            "train": str(train_path),
            "eval": str(eval_path),
        },
    )

    return dataset


def parse_args():
    parser = argparse.ArgumentParser(description="LoRA fine-tuning script for health domain LLM.")

    parser.add_argument(
        "--model-name",
        type=str,
        default="meta-llama/Llama-3.2-1B",
        help="Base model name from Hugging Face.",
    )

    parser.add_argument(
        "--train-path",
        type=Path,
        default=DEFAULT_TRAIN_PATH,
        help="Path to processed train.json.",
    )

    parser.add_argument(
        "--eval-path",
        type=Path,
        default=DEFAULT_EVAL_PATH,
        help="Path to processed eval.json.",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory to save LoRA adapter.",
    )

    parser.add_argument(
        "--max-seq-length",
        type=int,
        default=1024,
        help="Maximum sequence length.",
    )

    parser.add_argument(
        "--epochs",
        type=int,
        default=3,
        help="Number of training epochs.",
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=1,
        help="Per-device train batch size.",
    )

    parser.add_argument(
        "--gradient-accumulation-steps",
        type=int,
        default=4,
        help="Gradient accumulation steps.",
    )

    parser.add_argument(
        "--learning-rate",
        type=float,
        default=2e-4,
        help="Learning rate.",
    )

    parser.add_argument(
        "--use-4bit",
        action="store_true",
        help="Use 4-bit quantization.",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    print("[INFO] Load dataset")
    dataset = load_alpaca_dataset(args.train_path, args.eval_path)

    print(dataset)

    print("[INFO] Load tokenizer")
    tokenizer = AutoTokenizer.from_pretrained(args.model_name, use_fast=True)

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    quantization_config = None

    if args.use_4bit:
        print("[INFO] Use 4-bit quantization")

        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype="float16",
            bnb_4bit_use_double_quant=True,
        )

    print("[INFO] Load base model")
    model = AutoModelForCausalLM.from_pretrained(
        args.model_name,
        quantization_config=quantization_config,
        device_map="auto",
    )

    model.config.use_cache = False

    print("[INFO] Set LoRA config")
    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=[
            "q_proj",
            "k_proj",
            "v_proj",
            "o_proj",
        ],
    )

    print("[INFO] Set training arguments")
    training_args = TrainingArguments(
        output_dir=str(args.output_dir),
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        learning_rate=args.learning_rate,
        logging_steps=1,
        eval_strategy="epoch",
        save_strategy="epoch",
        report_to="tensorboard",
        fp16=True,
        save_total_limit=2,
        remove_unused_columns=False,
    )

    print("[INFO] Create SFTTrainer")
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset["train"],
        eval_dataset=dataset["eval"],
        peft_config=lora_config,
        formatting_func=format_prompt,
        args=training_args,
        max_seq_length=args.max_seq_length,
    )

    print("[INFO] Start training")
    trainer.train()

    print("[INFO] Save LoRA adapter")
    trainer.save_model(str(args.output_dir))

    print(f"[DONE] Model saved to: {args.output_dir}")


if __name__ == "__main__":
    main()