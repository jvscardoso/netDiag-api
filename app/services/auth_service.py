import os
import bcrypt
import jwt
from datetime import datetime, timedelta
from sqlalchemy import text
from app.database.database import SessionLocal

# Autenticação do usuário
def authenticate_user(email, password):
    session = SessionLocal()
    try:
        query = text("SELECT id, name, password_hash, role FROM users WHERE email = :email")
        result = session.execute(query, {"email": email})
        user = result.fetchone()

        if not user:
            return None

        user_id, name, password_hash, role = user

        if not bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
            return None

        payload = {
            'sub': user_id,
            'name': name,
            'email': email,
            'role': role,
            'exp': datetime.utcnow() + timedelta(hours=6)
        }

        token = jwt.encode(payload, os.environ.get('SECRET_KEY'), algorithm='HS256')
        return token, name, role
    finally:
        session.close()

# Criação de usuário
def create_user(name, email, password, role='user'):
    session = SessionLocal()
    try:
        query = text("SELECT id FROM users WHERE email = :email")
        result = session.execute(query, {"email": email})
        if result.fetchone():
            return False, "E-mail já cadastrado"

        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()

        insert_query = text("""
            INSERT INTO users (name, email, password_hash, role)
            VALUES (:name, :email, :password_hash, :role)
        """)

        session.execute(insert_query, {
            "name": name,
            "email": email,
            "password_hash": password_hash,
            "role": role
        })
        session.commit()
        return True, "Usuário criado"
    finally:
        session.close()

# Obter detalhes do usuário
def get_user(user_id):
    session = SessionLocal()
    try:
        query = text("""
            SELECT id, name, email, role, created_at, updated_at
            FROM users
            WHERE id = :user_id AND deleted_at IS NULL
        """)
        result = session.execute(query, {"user_id": user_id})
        user = result.fetchone()

        if not user:
            return None

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None
        }
    finally:
        session.close()
