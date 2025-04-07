import os
from flask import Flask
from app.api import register_routes
from app.core.config import Config
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, supports_credentials=True)

    app.config['JSON_SORT_KEYS'] = False

    register_routes(app)

    return app
