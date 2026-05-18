# Ubuntu Training Commands

## 1. Move To Project

```bash
cd ~/rag_study_assistant
```

## 2. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-train.txt
```

If `bitsandbytes` fails on your environment, install the other training packages first and then install a compatible `bitsandbytes` version for your CUDA setup.

## 4. Check Dataset

```bash
python training/check_dataset.py
python training/preview_training_data.py
```

Expected files:

```text
data/processed/train.json
data/processed/eval.json
```

## 5. Optional: Convert Raw Data

Run this only when you want to regenerate the processed dataset from `data/raw/health_export.json`.

```bash
python scripts/convert_to_alpaca.py
python training/check_dataset.py
```

## 6. Login To Hugging Face

Some base models require access approval and authentication.

```bash
huggingface-cli login
```

## 7. Start LoRA Training

Basic run:

```bash
python training/train_lora.py
```

Run with explicit options:

```bash
python training/train_lora.py \
  --model-name meta-llama/Llama-3.2-1B \
  --train-path data/processed/train.json \
  --eval-path data/processed/eval.json \
  --output-dir outputs/health_lora_model \
  --epochs 3 \
  --batch-size 1 \
  --gradient-accumulation-steps 4 \
  --learning-rate 2e-4 \
  --max-seq-length 1024
```

Use 4-bit quantization when your GPU memory is limited:

```bash
python training/train_lora.py \
  --model-name meta-llama/Llama-3.2-1B \
  --output-dir outputs/health_lora_model \
  --use-4bit
```

## 8. Check Output

```bash
ls -lah outputs/
ls -lah outputs/health_lora_model/
```

The LoRA adapter should be saved under:

```text
outputs/health_lora_model/
```

## 9. Run TensorBoard

```bash
tensorboard --logdir outputs/health_lora_model --host 0.0.0.0 --port 6006
```

Open this URL in your browser:

```text
http://localhost:6006
```

If you are connecting to a remote Ubuntu server, forward the port from your local machine:

```bash
ssh -L 6006:localhost:6006 user@server-ip
```
