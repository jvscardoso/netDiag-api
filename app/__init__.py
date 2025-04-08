from flask import Flask
from app.api import register_routes
from app.core.config import Config
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(
        app, origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",],
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )
    app.config['JSON_SORT_KEYS'] = False

    register_routes(app)

    return app
