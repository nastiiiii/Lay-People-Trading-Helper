from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, Enum, UUID, ForeignKey, DateTime, Float, Integer
from sqlalchemy.orm import declarative_base, relationship

from db.database import Base
from models.enums import TradeTypeEnum


class Trade(Base):
    __tablename__ = "trades"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    stock_symbol = Column(String, nullable=False)
    trade_type = Column(Enum(TradeTypeEnum), nullable=False)
    trade_date = Column(DateTime, default=datetime.utcnow)
    quantity = Column(Integer, nullable=False)
    price_per_share = Column(Float, nullable=False)
    resulting_portfolio_value = Column(Float, nullable=True)

    user = relationship("User", back_populates="trades")
    biases = relationship("Bias", back_populates="trade")
