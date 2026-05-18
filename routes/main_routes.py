from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    return "LLM Project Server Running"


@main_bp.route("/health")
def health():
    return {
        "status": "ok",
        "message": "LLM Project Flask server is running"
    }


@main_bp.route("/chat")
def chat_page():
    return render_template("chat.html")