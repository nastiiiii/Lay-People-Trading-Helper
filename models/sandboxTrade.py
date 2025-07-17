import uuid

from sqlalchemy import Column, ForeignKey, String, Float, Date, Boolean, UUID
from sqlalchemy.orm import relationship

from db.database import Base


class SandboxTrade(Base):
    __tablename__ = 'sandbox_trades'

    trade_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey('sandbox_sessions.session_id'))
    stock_symbol = Column(String, nullable=False)
    action = Column(String, nullable=False)  # e.g., "buy" or "sell"
    price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    timestamp = Column(Date, nullable=False)

    session = relationship("SandboxSession", back_populates="trades")
    decision = relationship("SandboxDecision", uselist=False, back_populates="trade")