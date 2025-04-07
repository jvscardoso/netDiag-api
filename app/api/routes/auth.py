from flask import Blueprint, request, jsonify, g
from app.services.auth_service import authenticate_user, create_user, get_user
from app.middlewares.auth_middleware import token_required

auth_bp = Blueprint('auth', __name__)

# LOGIN
@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "E-mail e senha são obrigatórios"}), 400

    result = authenticate_user(email, password)

    if not result:
        return jsonify({"error": "Credenciais inválidas"}), 401

    token, name, role = result
    return jsonify({
        "access_token": token,
        "name": name,
        "role": role
    })

# REGISTER
@auth_bp.route('/auth/register', methods=['POST'])
@token_required
def register():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'user')

    if not all([name, email, password]):
        return jsonify({"error": "Nome, email e senha são obrigatórios"}), 400

    success, message = create_user(name, email, password, role)
    if not success:
        return jsonify({"error": message}), 400

    return jsonify({"message": "Usuário criado com sucesso"}), 201

# USER DETAILS
@auth_bp.route('/me', methods=['GET'])
@token_required
def get_me():
    user_id = g.user.get("sub")  # Usando g.user aqui
    user = get_user(user_id)

    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    return jsonify(user), 200