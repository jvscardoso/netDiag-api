import jwt
import datetime
import os
from functools import wraps
from flask import request, jsonify

SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")

def generate_token(user_id, role):
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    

def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].replace("Bearer ", "")

        if not token:
            return jsonify({"error": "Token não fornecido"}), 401

        data = decode_token(token)
        if not data:
            return jsonify({"error": "Token inválido ou expirado"}), 401

        request.user = data  # attach user data
        return f(*args, **kwargs)
    
    return wrapper

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not hasattr(request, "user"):
                return jsonify({"error": "Usuário não autenticado"}), 403

            if request.user["role"] != required_role:
                return jsonify({"error": "Permissão negada"}), 403

            return f(*args, **kwargs)
        return wrapper
    return decorator

