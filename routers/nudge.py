from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud import crud_nudge
from db.database import get_db
from schema import NudgeRead, NudgeCreate

router = APIRouter(prefix="/nudges", tags=["Nudges"])

@router.post("/", response_model=NudgeRead)
def create_nudge(nudge: NudgeCreate, db: Session = Depends(get_db)):
    return crud_nudge.create_nudge(db, nudge)

@router.get("/{nudge_id}", response_model=NudgeRead)
def get_nudge(nudge_id: UUID, db: Session = Depends(get_db)):
    nudge = crud_nudge.get_nudge(db, nudge_id)
    if nudge is None:
        raise HTTPException(status_code=404, detail="Nudge not found")
    return nudge

@router.get("/", response_model=list[NudgeRead])
def list_nudges(db: Session = Depends(get_db)):
    return crud_nudge.get_all_nudges(db)

