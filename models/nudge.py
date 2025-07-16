from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, UUID, ForeignKey, String, Enum, DateTime
from sqlalchemy.orm import declarative_base, relationship

from db.database import Base
from models.enums import UserResponseEnum, DeliveryTypeEnum


class Nudge(Base):
    __tablename__ = "nudges"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    bias_id = Column(UUID(as_uuid=True), ForeignKey("biases.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    message_content = Column(String, nullable=False)
    delivery_type = Column(Enum(DeliveryTypeEnum), nullable=False)
    user_response = Column(Enum(UserResponseEnum), nullable=False, default=UserResponseEnum.ignored)
    delivered_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="nudges")
    bias = relationship("Bias", back_populates="nudges")

