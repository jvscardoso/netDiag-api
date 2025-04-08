from flask import Flask
from app.api.routes import auth, diagnostics, users, dashboard


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def hello():
        return "Hello, netDiag"

def register_routes(app):
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(diagnostics.diag_bp)
    app.register_blueprint(users.users_bp)
    app.register_blueprint(dashboard.dashboard_bp)
    return app
