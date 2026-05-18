import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
TRAIN_PATH = BASE_DIR / "data" / "processed" / "train.json"
EVAL_PATH = BASE_DIR / "data" / "processed" / "eval.json"

REQUIRED_KEYS = {"instruction", "input", "output"}


def load_json(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {path}")

    with path.open("r", encoding="utf-8-sig") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError(f"JSON 최상위 구조는 list여야 합니다: {path}")

    return data


def check_dataset(name: str, dataset: list[dict]) -> None:
    print(f"\n[{name}]")
    print(f"데이터 개수: {len(dataset)}")

    if not dataset:
        print("데이터가 비어 있습니다.")
        return

    error_count = 0

    for index, item in enumerate(dataset, start=1):
        if not isinstance(item, dict):
            print(f"{index}번 데이터 오류: dict 형식이 아닙니다.")
            error_count += 1
            continue

        missing_keys = REQUIRED_KEYS - set(item.keys())

        if missing_keys:
            print(f"{index}번 데이터 누락 키: {missing_keys}")
            error_count += 1
            continue

        for key in REQUIRED_KEYS:
            value = item.get(key)

            if value is None or str(value).strip() == "":
                print(f"{index}번 데이터 오류: {key} 값이 비어 있습니다.")
                error_count += 1

    print(f"오류 개수: {error_count}")

    print("\n[샘플 출력]")
    for index, item in enumerate(dataset[:3], start=1):
        print(f"\n--- sample {index} ---")
        print("instruction:", item.get("instruction", ""))
        print("input:", item.get("input", ""))
        output = item.get("output", "")
        print("output:", output[:150] + "..." if len(output) > 150 else output)


def main() -> None:
    train_data = load_json(TRAIN_PATH)
    eval_data = load_json(EVAL_PATH)

    check_dataset("train", train_data)
    check_dataset("eval", eval_data)


if __name__ == "__main__":
    main()