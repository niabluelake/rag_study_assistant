from flask import Flask
from routes.main_routes import main_bp
from routes.chat_routes import chat_bp
from routes.health_routes import health_bp

app = Flask(__name__)
app.json.ensure_ascii = False
app.register_blueprint(health_bp)
app.register_blueprint(main_bp)
app.register_blueprint(chat_bp)

if __name__ == "__main__":
    app.run(debug=True)