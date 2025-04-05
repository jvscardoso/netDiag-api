import os
from flask import Flask
from app.api import register_routes
from app.database.connection import init_db

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

    app.config['JSON_SORT_KEYS'] = False

    init_db(app)

    register_routes(app)

    return app
