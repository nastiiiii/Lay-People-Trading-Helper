from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, UUID, ForeignKey, Integer, String, JSON, DateTime
from sqlalchemy.orm import declarative_base, relationship

from db.database import Base


class BehaviourProfile(Base):
    __tablename__ = "behaviour_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    total_bias_events = Column(Integer, default=0)
    most_frequent_bias = Column(String)
    bias_score_history = Column(JSON, nullable=True)
    last_updated = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="behaviour_profile")
