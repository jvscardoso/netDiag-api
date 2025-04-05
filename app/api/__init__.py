from flask import Flask
from app.api.routes.auth import auth_bp
from app.api.routes.diagnostics import diagnostics_bp

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(diagnostics_bp, url_prefix='/diagnostics')

    @app.route("/")
    def hello():
        return "Hello, netDiag 👋"

    return app
