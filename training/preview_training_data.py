import json, argparse
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
TRAIN_PATH = ROOT_DIR / "data" / "processed" / "train.json"
EVAL_PATH = ROOT_DIR / "data" / "processed" / "eval.json"

def parse_args():
    parser = argparse.ArgumentParser(description="Preview formatted training prompts.")
    parser.add_argument("--limit", type=int, default=3, help="Number of samples to preview.")
    return parser.parse_args()

def load_json(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {path}")

    with path.open("r", encoding="utf-8-sig") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError(f"JSON 최상위 구조는 list여야 합니다: {path}")

    return data


def format_prompt(example: dict) -> str:
    instruction = example.get("instruction", "").strip()
    input_text = example.get("input", "").strip()
    output = example.get("output", "").strip()

    if input_text:
        return f"""### Instruction:
{instruction}

### Input:
{input_text}

### Response:
{output}"""

    return f"""### Instruction:
{instruction}

### Response:
{output}"""


def preview_dataset(name: str, dataset: list[dict], count: int = 3) -> None:
    print(f"\n========== {name} ==========")
    print(f"데이터 개수: {len(dataset)}")

    for index, example in enumerate(dataset[:count], start=1):
        prompt = format_prompt(example)

        print(f"\n----- sample {index} -----")
        print(prompt)
        print("-" * 60)


def main() -> None:
    args = parse_args()

    train_data = load_json(TRAIN_PATH)
    eval_data = load_json(EVAL_PATH)

    preview_dataset("train", train_data, count=args.limit)
    preview_dataset("eval", eval_data, count=args.limit)

if __name__ == "__main__":
    main()