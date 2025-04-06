from datetime import datetime
from sqlalchemy import text
from app.database.database import SessionLocal

# LIST
def list_users(filters):
    session = SessionLocal()
    try:
        base_query = """
            SELECT id, name, email, role, created_at, updated_at, deleted_at
            FROM users
        """
        conditions = []
        values = {}

        all_param = filters.get("all", False)
        if isinstance(all_param, str):
            include_all = all_param.lower() == "true"
        else:
            include_all = bool(all_param)

        if not include_all:
            conditions.append("deleted_at IS NULL")

        if filters.get("name"):
            conditions.append("name ILIKE :name")
            values["name"] = f"%{filters['name']}%"
        if filters.get("email"):
            conditions.append("email ILIKE :email")
            values["email"] = f"%{filters['email']}%"
        if filters.get("role"):
            conditions.append("role = :role")
            values["role"] = filters["role"]

        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)

        base_query += " ORDER BY created_at DESC"

        result = session.execute(text(base_query), values)
        users = result.fetchall()

        return [
            {
                "id": row.id,
                "name": row.name,
                "email": row.email,
                "role": row.role,
                "created_at": row.created_at.isoformat(),
                "updated_at": row.updated_at.isoformat() if row.updated_at else None,
                "deleted_at": row.deleted_at.isoformat() if row.deleted_at else None,
            }
            for row in users
        ]
    finally:
        session.close()

# DELETE
def delete_user(user_id):
    session = SessionLocal()
    try:
        query = text("""
            UPDATE users
            SET deleted_at = CURRENT_TIMESTAMP
            WHERE id = :user_id AND deleted_at IS NULL
            RETURNING id
        """)
        result = session.execute(query, {"user_id": user_id})
        session.commit()
        if result.fetchone():
            return {"message": "Usuário deletado com sucesso"}
        else:
            return {"error": "Usuário não encontrado ou já foi deletado"}
    finally:
        session.close()

# UPDATE
def update_user(user_id, data):
    session = SessionLocal()
    try:
        fields = []
        values = {}

        if "name" in data:
            fields.append("name = :name")
            values["name"] = data["name"]

        if "email" in data:
            fields.append("email = :email")
            values["email"] = data["email"]

        if "role" in data:
            fields.append("role = :role")
            values["role"] = data["role"]

        if not fields:
            return {"error": "Nenhum campo fornecido para atualização"}

        fields.append("updated_at = :updated_at")
        values["updated_at"] = datetime.utcnow()
        values["user_id"] = user_id

        query = f"""
            UPDATE users
            SET {', '.join(fields)}
            WHERE id = :user_id AND deleted_at IS NULL
            RETURNING id
        """

        result = session.execute(text(query), values)
        session.commit()

        if result.fetchone():
            return {"message": "Usuário atualizado com sucesso"}
        else:
            return {"error": "Usuário não encontrado ou já foi deletado"}
    finally:
        session.close()
