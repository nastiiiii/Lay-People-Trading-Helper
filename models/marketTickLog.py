from sqlalchemy import Column, Float, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from db.database import Base


class MarketTickLog(Base):
    __tablename__ = "market_tick_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    simulation_id = Column(UUID(as_uuid=True), ForeignKey("market_simulation_configs.id"))
    tick_number = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
    price = Column(Float)
    buy_pressure = Column(Float)
    sell_pressure = Column(Float)
    sentiment = Column(Float)
