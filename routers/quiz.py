from typing import List

from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from sqlalchemy.orm import Session

from db.database import get_db
from models.quizResult import QuizResult
from schema import QuizSubmission, QuizResultOut
from services.quiz_service import get_categories, get_questions_by_category, evaluate_answers, \
    evaluate_answers_from_submission

router = APIRouter(prefix="/quiz", tags=["Quiz"])

@router.get("/categories")
def list_categories():
    return get_categories()

@router.get("/questions/{category}")
def get_questions(category: str):
    questions = get_questions_by_category(category)
    if not questions:
        raise HTTPException(status_code=404, detail="Category not found")
    return questions

@router.post("/submit", response_model=QuizResultOut)
def submit_quiz(submission: QuizSubmission, db: Session = Depends(get_db)):
    result = evaluate_answers_from_submission(submission)

    # Only save if all questions answered
    if result["total_questions"] == len(submission.answers):
        quiz_result = QuizResult(
            user_id=submission.user_id,
            category=submission.category,
            total_questions=result["total_questions"],
            correct_answers=result["correct_answers"],
        )
        db.add(quiz_result)
        db.commit()
        db.refresh(quiz_result)

    return result

@router.get("/results/{user_id}", response_model=List[QuizResultOut])
def get_user_quiz_results(user_id: UUID, db: Session = Depends(get_db)):
    results = db.query(QuizResult).filter(QuizResult.user_id == user_id).all()
    return results