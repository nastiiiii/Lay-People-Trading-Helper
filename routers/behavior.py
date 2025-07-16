from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud import crud_behaviour
from db.database import get_db
from schema import BehaviorProfileRead, BehaviorProfileCreate

router = APIRouter(prefix="/behavior", tags=["Behavior Profiles"])

@router.post("/", response_model=BehaviorProfileRead)
def create_behavior_profile(profile: BehaviorProfileCreate, db: Session = Depends(get_db)):
    return crud_behaviour.create_profile(db, profile)

@router.get("/{profile_id}", response_model=BehaviorProfileRead)
def get_behavior_profile(profile_id: UUID, db: Session = Depends(get_db)):
    profile = crud_behaviour.get_profile(db, profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Behavior profile not found")
    return profile


@router.get("/", response_model=list[BehaviorProfileRead])
def list_profiles(db: Session = Depends(get_db)):
    return crud_behaviour.get_all_profiles(db)
