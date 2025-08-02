from uuid import uuid4

from sqlalchemy import Column, UUID, ForeignKey, Float

from db.database import Base


class UserPortfolio(Base):
    __tablename__ = "user_portfolios"
    id = Column(UUID, primary_key=True, default=uuid4)
    simulation_id = Column(UUID, ForeignKey("market_simulation_configs.id"))
    balance = Column(Float, default=100.0)
    holdings = Column(Float, default=0.0)
    last_price = Column(Float, default=0.0)
