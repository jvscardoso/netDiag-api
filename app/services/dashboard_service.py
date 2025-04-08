from sqlalchemy.sql import text
from app.database.database import SessionLocal

def get_general_metrics():
    query = """
        SELECT
            COUNT(*) AS total_diagnostics,
            AVG(latency_ms) AS avg_latency,
            AVG(packet_loss) AS avg_packet_loss,
            AVG(quality_of_service) AS avg_qos
        FROM diagnostics;
    """

    session = SessionLocal()
    try:
        result = session.execute(text(query)).fetchone()
        return {
            "total_diagnostics": result.total_diagnostics,
            "avg_latency": round(result.avg_latency or 0, 2),
            "avg_packet_loss": round(result.avg_packet_loss or 0, 2),
            "avg_quality_of_service": round(result.avg_qos or 0, 2)
        }
    finally:
        session.close()
