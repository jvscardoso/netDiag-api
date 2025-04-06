from sqlalchemy import text
from app.database.database import SessionLocal

def get_diagnostics(page, limit, filters):
    offset = (page - 1) * limit
    query = "SELECT * FROM diagnostics"
    where_clauses = []
    params = {}

    for key, value in filters.items():
        if key in ["page", "limit"]:
            continue
        where_clauses.append(f"{key} = :{key}")
        params[key] = value

    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)

    query += " ORDER BY date DESC LIMIT :limit OFFSET :offset"
    params["limit"] = limit
    params["offset"] = offset

    session = SessionLocal()
    try:
        result = session.execute(text(query), params)
        diagnostics = [dict(row._mapping) for row in result]
        return diagnostics
    finally:
        session.close()

def get_diagnostics_aggregated(filters=None):
    base_query = """
        SELECT 
            DATE(date) AS day,
            AVG(latency_ms) AS avg_latency,
            AVG(packet_loss) AS avg_packet_loss,
            AVG(quality_of_service) AS avg_qos,
            COUNT(*) AS total
        FROM diagnostics
        WHERE 1=1
    """

    where_clauses = []
    params = {}

    if filters:
        for key, value in filters.items():
            where_clauses.append(f"{key} = :{key}")
            params[key] = value

    if where_clauses:
        base_query += " AND " + " AND ".join(where_clauses)

    base_query += " GROUP BY day ORDER BY day DESC"

    session = SessionLocal()
    try:
        result = session.execute(text(base_query), params)
        rows = result.fetchall()

        return [
            {
                "day": row.day.isoformat(),
                "avg_latency": round(row.avg_latency, 2),
                "avg_packet_loss": round(row.avg_packet_loss, 2),
                "avg_quality_of_service": round(row.avg_qos, 2),
                "total": row.total
            }
            for row in rows
        ]
    finally:
        session.close()
