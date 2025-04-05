from dataclasses import dataclass
from datetime import datetime

@dataclass
class Diagnostic:
    id: int
    device_id: str
    city: str
    state: str
    latency_ms: float
    packet_loss: float
    quality_of_service: float
    date: datetime
