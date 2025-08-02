
from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

import uuid
import enum

from db.database import Base


class MarketType(str, enum.Enum):
    bull = "bull"
    bear = "bear"
    sideways = "sideways"
    volatile = "volatile"

class MarketSimulationConfig(Base):
    __tablename__ = "market_simulation_configs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    market_type = Column(Enum(MarketType), nullable=False)
    shock_frequency = Column(String, default="medium")  # low, medium, high
    noise_level = Column(Float, default=0.1)
    include_user_trader = Column(Boolean, default=False)

    agents = relationship("MarketAgentDefinition", back_populates="config")
