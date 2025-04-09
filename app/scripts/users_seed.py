# users_seed.py
import os
import bcrypt
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "netdiag")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

users = [
    {
        "name": "Alice Admin",
        "email": "admin@netdiag.com",
        "password": "admin123",
        "role": "admin"
    },
    {
        "name": "Bob Analyst",
        "email": "analyst@netdiag.com",
        "password": "analyst123",
        "role": "analyst"
    },
    {
        "name": "Joe Doe User",
        "email": "user@netdiag.com",
        "password": "user123",
        "role": "user"
    }
]

sql = text("""
    INSERT INTO users (name, email, password_hash, role)
    VALUES (:name, :email, :password_hash, :role)
    ON CONFLICT (email) DO NOTHING
""")

with engine.connect() as conn:
    for user in users:
        password_hash = bcrypt.hashpw(user["password"].encode("utf-8"), bcrypt.gensalt()).decode()
        conn.execute(sql, {
            "name": user["name"],
            "email": user["email"],
            "password_hash": password_hash,
            "role": user["role"]
        })
    conn.commit()

print("Usuários inseridos com sucesso.")
