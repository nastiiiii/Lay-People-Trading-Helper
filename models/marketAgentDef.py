import enum

from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

import uuid

from db.database import Base


class TraderType(str, enum.Enum):
    emotional = "emotional"
    rule_based = "rule_based"
    ai = "ai"
    contrarian = "contrarian"
    passive = "passive"

class MarketAgentDefinition(Base):
    __tablename__ = "market_agent_definitions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    config_id = Column(UUID(as_uuid=True), ForeignKey("market_simulation_configs.id"))
    trader_type = Column(Enum(TraderType), nullable=False)
    count = Column(Integer, nullable=False)
    aggressiveness = Column(Float, default=1.0)
    reaction_speed = Column(Float, default=1.0)

    config = relationship("MarketSimulationConfig", back_populates="agents")
