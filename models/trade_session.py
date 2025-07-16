import uuid
from datetime import datetime

from sqlalchemy import Column, ForeignKey, UUID, DateTime, Integer
from sqlalchemy.orm import declarative_base, relationship

from db.database import Base


class TradeSession(Base):
    __tablename__ = "trade_sessions"
    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    total_trades = Column(Integer, default=0)
    total_volume = Column(Integer, default=0)

    user = relationship("User", back_populates="sessions")
    trades = relationship("Trade", back_populates="session")