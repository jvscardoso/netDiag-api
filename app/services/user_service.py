from app.database.connection import get_db
from datetime import datetime

# LIST
def list_users(filters):
    conn = get_db()
    cursor = conn.cursor()

    base_query = "SELECT id, name, email, role, created_at, updated_at, deleted_at FROM users"
    conditions = []
    values = []

    all_param = filters.get("all", False)
    if isinstance(all_param, str):
        include_all = all_param.lower() == "true"
    else:
        include_all = bool(all_param)

    if not include_all:
        conditions.append("deleted_at IS NULL")

    if filters.get("name"):
        conditions.append("name ILIKE %s")
        values.append(f"%{filters['name']}%")
    if filters.get("email"):
        conditions.append("email ILIKE %s")
        values.append(f"%{filters['email']}%")
    if filters.get("role"):
        conditions.append("role = %s")
        values.append(filters["role"])

    if conditions:
        base_query += " WHERE " + " AND ".join(conditions)

    base_query += " ORDER BY created_at DESC"

    cursor.execute(base_query, tuple(values))
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    return [
        {
            "id": user[0],
            "name": user[1],
            "email": user[2],
            "role": user[3],
            "created_at": user[4].isoformat() ,
            "updated_at": user[5].isoformat() if user[5] else None,
            "deleted_at": user[6].isoformat() if user[6] else None,
        }
        for user in users
    ]

# DELETE
def delete_user(user_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET deleted_at = CURRENT_TIMESTAMP WHERE id = %s AND deleted_at IS NULL",
        (user_id,)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Usuário deletado com sucesso"}

# UPDATE
def update_user(user_id, data):
    conn = get_db()
    cursor = conn.cursor()

    fields = []
    values = []

    if "name" in data:
        fields.append("name = %s")
        values.append(data["name"])

    if "email" in data:
        fields.append("email = %s")
        values.append(data["email"])

    if "role" in data:
        fields.append("role = %s")
        values.append(data["role"])

    if not fields:
        cursor.close()
        conn.close()
        return {"error": "Nenhum campo fornecido para atualização"}

    fields.append("updated_at = %s")
    values.append(datetime.utcnow())

    values.append(user_id)
    query = f"UPDATE users SET {', '.join(fields)} WHERE id = %s AND deleted_at IS NULL RETURNING id"

    cursor.execute(query, tuple(values))
    updated = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    if updated:
        return {"message": "Usuário atualizado com sucesso"}
    else:
        return {"error": "Usuário não encontrado ou já foi deletado"}
