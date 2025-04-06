from sqlalchemy import Column, Integer, String, Float, TIMESTAMP
from app.database import Base

class Diagnostic(Base):
    __tablename__ = 'diagnostics'

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(50))
    city = Column(String(100))
    state = Column(String(50))
    latency_ms = Column(Float)
    packet_loss = Column(Float)
    quality_of_service = Column(Float)
    date = Column(TIMESTAMP)
