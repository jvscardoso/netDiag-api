from sqlalchemy import text
from app.database.database import SessionLocal
from datetime import datetime, timedelta

 # INDEX
def get_diagnostics(page, limit, filters):
    offset = (page - 1) * limit
    query = "SELECT * FROM diagnostics"
    where_clauses = []
    params = {}

    qos_filter = filters.pop("qos_filter", None)
    if qos_filter == "good":
        where_clauses.append("quality_of_service >= 0.8")
    elif qos_filter == "regular":
        where_clauses.append("quality_of_service >= 0.5 AND quality_of_service < 0.8")
    elif qos_filter == "bad":
        where_clauses.append("quality_of_service < 0.5")

    date_filter = filters.pop("date", None)
    if date_filter:
        try:
            date_obj = datetime.fromisoformat(date_filter.replace("Z", "+00:00"))
            start_of_day = date_obj.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = start_of_day + timedelta(days=1)

            where_clauses.append("date >= :start_date AND date < :end_date")
            params["start_date"] = start_of_day
            params["end_date"] = end_of_day
        except ValueError:
            pass  

    for key, value in filters.items():
        if key in ["page", "limit"]:
            continue
        if value == "":
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
        diagnostics = []
        for row in result:
            row_dict = dict(row._mapping)
            if "date" in row_dict and isinstance(row_dict["date"], datetime):
                row_dict["date"] = row_dict["date"].isoformat()
            diagnostics.append(row_dict)
        return diagnostics
    finally:
        session.close()


# GROUPED
def get_diagnostics_grouped(filters=None):
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

    VALID_FILTERS = {"state", "city"}

    where_clauses = []
    params = {}

    if filters:
        invalid_keys = [key for key in filters if key not in VALID_FILTERS]
        if invalid_keys:
            raise ValueError(f"Filtro inválido: {', '.join(invalid_keys)}")

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