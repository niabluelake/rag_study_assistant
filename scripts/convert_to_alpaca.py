import argparse
import json
import random
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT_DIR / "data" / "raw" / "health_export.json"
DEFAULT_OUTPUT_DIR = ROOT_DIR / "data" / "processed"

def normalize_space(text: str) -> str:
    return " ".join(text.split())

def load_records(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8-sig") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError(f"Expected a JSON list: {path}")

    return data


def value(record: dict, key: str, default: str = "정보 없음") -> str:
    item = record.get(key)
    if item is None or item == "":
        return default
    return str(item)


def build_input(record: dict) -> str:
    fields = [
        ("나이", "age", "세"),
        ("성별", "sex", ""),
        ("BMI", "bmi", ""),
        ("총콜레스테롤", "total_chol", "mg/dL"),
        ("일일 섭취 열량", "kcal", "kcal"),
        ("당류", "sugar", "g"),
        ("나트륨", "na", "mg"),
        ("포화지방", "sfa", "g"),
        ("식이섬유", "tdf", "g"),
        ("수면", "sleep", "시간"),
        ("흡연", "smoke", ""),
        ("음주", "alcohol", ""),
        ("유산소 운동", "aerobic", ""),
        ("위험군", "cluster_name", ""),
    ]

    parts = []
    for label, key, unit in fields:
        raw_value = record.get(key)
        if raw_value is None or raw_value == "":
            continue
        parts.append(f"{label}: {raw_value}{unit}")

    return ", ".join(parts)


def build_output(record: dict) -> str:
    cluster = value(record, "cluster_name")
    message = value(record, "message", "")

    advice = []
    bmi = record.get("bmi")
    sodium = record.get("na")
    fiber = record.get("tdf")
    sleep = record.get("sleep")
    smoke = value(record, "smoke", "")
    aerobic = value(record, "aerobic", "")

    if isinstance(bmi, (int, float)) and bmi >= 25:
        advice.append("체중 관리를 위해 섭취 열량을 조절하고 규칙적인 운동을 늘리는 것이 좋습니다.")
    if isinstance(sodium, (int, float)) and sodium >= 2300:
        advice.append("나트륨 섭취가 높으므로 국물, 가공식품, 짠 반찬 섭취를 줄이세요.")
    if isinstance(fiber, (int, float)) and fiber < 20:
        advice.append("식이섬유 섭취가 부족할 수 있으니 채소, 과일, 통곡류를 늘리세요.")
    if isinstance(sleep, (int, float)) and sleep < 7:
        advice.append("수면 시간이 부족하므로 하루 7시간 안팎의 수면을 목표로 하세요.")
    if smoke == "예":
        advice.append("흡연은 심혈관 질환 위험을 높일 수 있어 금연이 필요합니다.")
    if "0" in aerobic or "거의" in aerobic:
        advice.append("가벼운 걷기부터 시작해 주 3회 이상 유산소 운동을 권장합니다.")

    if not advice:
        advice.append("현재 생활습관을 유지하면서 정기적인 건강검진을 이어가세요.")

    return normalize_space(
        f"사용자는 {cluster}으로 분류됩니다. {message} " + " ".join(advice)
    )

def to_alpaca(record: dict) -> dict:
    return {
        "instruction": "사용자의 건강검진 및 생활습관 정보를 바탕으로 건강 위험 요인과 개선 방향을 설명하세요.",
        "input": build_input(record),
        "output": build_output(record),
    }


def split_dataset(items: list[dict], eval_ratio: float, seed: int) -> tuple[list[dict], list[dict]]:
    shuffled = items[:]
    random.Random(seed).shuffle(shuffled)

    if len(shuffled) <= 1:
        return shuffled, []

    eval_size = max(1, round(len(shuffled) * eval_ratio))
    eval_size = min(eval_size, len(shuffled) - 1)
    return shuffled[eval_size:], shuffled[:eval_size]


def save_json(path: Path, data: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.write("\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert health export records to Alpaca training data.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="Raw health export JSON path.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Directory for train/eval JSON.")
    parser.add_argument("--eval-ratio", type=float, default=0.2, help="Evaluation split ratio.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for deterministic split.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not 0 <= args.eval_ratio < 1:
        raise ValueError("--eval-ratio must be greater than or equal to 0 and less than 1.")

    records = load_records(args.input)
    alpaca_items = [to_alpaca(record) for record in records]
    train_items, eval_items = split_dataset(alpaca_items, args.eval_ratio, args.seed)

    save_json(args.output_dir / "train.json", train_items)
    save_json(args.output_dir / "eval.json", eval_items)

    print(f"Converted {len(alpaca_items)} records")
    print(f"train: {len(train_items)} -> {args.output_dir / 'train.json'}")
    print(f"eval: {len(eval_items)} -> {args.output_dir / 'eval.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
