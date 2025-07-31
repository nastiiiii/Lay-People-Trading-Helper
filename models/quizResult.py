from uuid import uuid4

from sqlalchemy import Column, Integer, String, ForeignKey, UUID
from sqlalchemy.orm import relationship

from db.database import Base


class QuizResult(Base):
    __tablename__ = 'quiz_results'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    category = Column(String, nullable=False)
    total_questions = Column(Integer, nullable=False)
    correct_answers = Column(Integer, nullable=False)

    user = relationship("User", back_populates="quiz_results")