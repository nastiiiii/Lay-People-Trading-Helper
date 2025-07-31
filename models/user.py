import uuid
from datetime import datetime

from db.database import Base

from sqlalchemy.orm import relationship



from sqlalchemy import Column, String, Enum, UUID, Integer, DateTime

from models.enums import ExperienceLevelEnum



class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=True)
    experience_level = Column(Enum(ExperienceLevelEnum), nullable=False, default=ExperienceLevelEnum.novice)
    created_at = Column(DateTime, default=datetime.utcnow)
    total_trades = Column(Integer, default=0)

    trades = relationship("Trade", back_populates="user")
    biases = relationship("Bias", back_populates="user")
    nudges = relationship("Nudge", back_populates="user")
    behaviour_profile = relationship("BehaviourProfile", uselist=False, back_populates="user")
    sandbox_sessions = relationship("SandboxSession", back_populates="user")
    quiz_results = relationship("QuizResult", back_populates="user")
