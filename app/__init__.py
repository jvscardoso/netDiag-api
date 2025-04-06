import os
from flask import Flask
from app.api import register_routes
from app.core.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.config['JSON_SORT_KEYS'] = False

    register_routes(app)

    return app
