import os
import bcrypt
import jwt
from datetime import datetime, timedelta
from app.database.connection import get_db

# User authentication
def authenticate_user(email, password):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, password_hash, role FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

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

# User Creation
def create_user(name, email, password, role='user'):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    if cursor.fetchone():
        return False, "E-mail já cadastrado"

    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()

    cursor.execute(
        "INSERT INTO users (name, email, password_hash, role) VALUES (%s, %s, %s, %s)",
        (name, email, password_hash, role)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return True, "Usuário criado"

# USER DETAILS
def get_user(user_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, email, role, created_at, updated_at
        FROM users
        WHERE id = %s AND deleted_at IS NULL
    """, (user_id,))
    
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user:
        return None

    return {
        "id": user[0],
        "name": user[1],
        "email": user[2],
        "role": user[3],
        "created_at": user[4].isoformat() if user[4] else None,
        "updated_at": user[5].isoformat() if user[5] else None
    }