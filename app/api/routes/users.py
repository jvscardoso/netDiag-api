from flask import Blueprint, request, jsonify
from app.middlewares.auth_middleware import token_required, admin_required
from app.services.user_service import update_user

users_bp = Blueprint('users', __name__)

# USER LIST
@users_bp.route('/users', methods=['GET'])
@token_required
def list_users_route():
    from app.services.user_service import list_users

    filters = {
        "name": request.args.get("name"),
        "email": request.args.get("email"),
        "role": request.args.get("role"),
        "all": request.args.get("all") == "true"
    }

    users = list_users(filters)
    return jsonify(users)


# USER UPDATE
@users_bp.route('/users/<int:user_id>', methods=['PATCH'])
@admin_required
@token_required
def update_user_route(user_id):
    data = request.get_json()
    result = update_user(user_id, data)
    if result.get("error"):
        return jsonify(result), 400
    return jsonify(result)

# USER DELETE
@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
@admin_required
@token_required
def delete_user_route(user_id):
    from app.services.user_service import delete_user
    result = delete_user(user_id)
    if result.get("error"):
        return jsonify(result), 400
    return jsonify(result)

