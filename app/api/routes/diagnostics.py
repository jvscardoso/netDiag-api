from flask import Blueprint, jsonify
from app.utils.jwt import token_required, role_required

diag_bp = Blueprint("diagnostics", __name__, url_prefix="/diagnostics")

@diag_bp.route("/protected", methods=["GET"])
@token_required
@role_required("admin")
def protected_route():
    return jsonify({"message": "Acesso autorizado para admins!"})
