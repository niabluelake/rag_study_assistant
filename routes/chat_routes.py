from flask import Blueprint, request, jsonify
from services.llm_service import generate_answer

chat_bp = Blueprint("chat", __name__, url_prefix="/api")


@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({
            "success": False,
            "error": "message field is required"
        }), 400

    answer = generate_answer(user_message)

    return jsonify({
        "success": True,
        "message": user_message,
        "answer": answer
    })