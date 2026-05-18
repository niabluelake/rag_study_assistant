from flask import Blueprint, request, jsonify

from services.llm_service import generate_answer

health_bp = Blueprint("health", __name__, url_prefix="/api")


@health_bp.route("/health-advice", methods=["POST"])
def health_advice():
    data = request.get_json(silent=True) or {}

    if not data:
        return jsonify({
            "success": False,
            "error": "health data is required"
        }), 400

    prompt_input = build_health_input(data)
    answer = generate_answer(prompt_input)

    return jsonify({
        "success": True,
        "input": prompt_input,
        "answer": answer
    })


def build_health_input(data: dict) -> str:
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
        value = data.get(key)

        if value is None or value == "":
            continue

        parts.append(f"{label}: {value}{unit}")

    return ", ".join(parts)
