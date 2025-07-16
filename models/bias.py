import uuid
from datetime import datetime

from sqlalchemy import Column, UUID, Enum, ForeignKey, DateTime, Float
from sqlalchemy.orm import declarative_base, relationship

from db.database import Base
from models.enums import BiasTypeEnum


class Bias(Base):
    __tablename__ = "biases"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bias_type = Column(Enum(BiasTypeEnum), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    trade_id = Column(UUID(as_uuid=True), ForeignKey("trades.id"))
    detected_at = Column(DateTime, default=datetime.utcnow)
    severity_score = Column(Float, default=0.0)

    user = relationship("User", back_populates="biases")
    trade = relationship("Trade", back_populates="biases")
    nudges = relationship("Nudge", back_populates="bias")