from uuid import UUID

from sqlalchemy.orm import Session

from models.user import User


def create_user (db: Session, user_data):
    db_user = User(**user_data.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id (db: Session, user_id: UUID):
    return db.query(User).filter(User.id == user_id).first()

def get_all_users (db: Session):
    return db.query(User).all()

def update_user (db: Session, user_id: UUID, updates: dict):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        for key, value in updates.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user (db: Session, user_id: UUID):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user