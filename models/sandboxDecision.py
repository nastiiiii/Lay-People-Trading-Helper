import uuid

from sqlalchemy import Column, UUID, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from db.database import Base


class SandboxDecision(Base):
    __tablename__ = 'sandbox_decisions'

    decision_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    trade_id = Column(UUID(as_uuid=True), ForeignKey('sandbox_trades.trade_id'), nullable=False)
    user_reason = Column(String, nullable=False)
    detected_biases = Column(Text, nullable=True)

    trade = relationship("SandboxTrade", back_populates="decision")