import uuid

from sqlalchemy import UUID, Column, Float, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship

from db.database import Base


class SandboxSession(Base):
    __tablename__ = 'sandbox_sessions'
    session_id = Column(UUID(as_uuid = True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid = True), ForeignKey('users.id'))
    start_date = Column(Date, nullable= False)
    current_date = Column(Date, nullable= False)
    initial_balance = Column(Float, default=500.0)
    current_balance = Column(Float, default=500.0)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="sandbox_sessions")
    trades = relationship("SandboxTrade", back_populates="session")