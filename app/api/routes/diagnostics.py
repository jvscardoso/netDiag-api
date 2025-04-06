from flask import Blueprint, jsonify, request
from app.utils.jwt import token_required, role_required
from app.services.diagnostics_service import get_diagnostics, get_diagnostics_grouped

diag_bp = Blueprint("diagnostics", __name__, url_prefix="/diagnostics")

# INDEX
@diag_bp.route("/", methods=["GET"])
@token_required
@role_required("admin", "analyst")
def diagnostics_list():
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        filters = request.args.to_dict()
        diagnostics = get_diagnostics(page, limit, filters)
        return jsonify(diagnostics)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# AGGREGATION
@diag_bp.route("/grouped", methods=["GET"])
@token_required
@role_required("admin", "analyst")
def diagnostics_grouped():
    try:
        filters = request.args.to_dict()
        data = get_diagnostics_grouped(filters)
        return jsonify(data), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500
