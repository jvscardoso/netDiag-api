from flask import Blueprint, jsonify
from app.services.dashboard_service import get_general_metrics
from app.utils.jwt import token_required, role_required

dashboard_bp = Blueprint("dashboard", __name__,)

@dashboard_bp.route("/dashboard", methods=["GET"])
@token_required
def diagnostics_metrics():
    metrics = get_general_metrics()
    return jsonify(metrics)
