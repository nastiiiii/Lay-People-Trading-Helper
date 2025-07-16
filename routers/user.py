
from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from crud import crud_user
from db.database import get_db
from schema import UserRead, UserCreate

router = APIRouter(prefix="/user", tags=["Users"])

@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud_user.create_user(db, user)

@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/", response_model=List[UserRead])
def list_users(db: Session = Depends(get_db)):
    return crud_user.get_all_users(db)

@router.delete("/{user_id}")
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    return crud_user.delete_user(db, user_id)