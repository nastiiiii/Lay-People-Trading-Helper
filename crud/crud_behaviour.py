from uuid import UUID

from sqlalchemy.orm import Session

from models.behaviourProfile import BehaviourProfile


def create_profile(db: Session, profile_data):
    db_profile = BehaviourProfile(**profile_data.dict())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def get_profile(db: Session, profile_id: UUID):
    return db.query(BehaviourProfile).filter(BehaviourProfile.id == profile_id).first()

def get_all_profiles(db: Session):
    return db.query(BehaviourProfile).all()

def get_profile_by_user(db: Session, user_id):
    return db.query(BehaviourProfile).filter(BehaviourProfile.user_id == user_id).first()

def update_profile(db: Session, user_id, updates):
    profile = get_profile_by_user(db, user_id)
    for key, value in updates.items():
        setattr(profile, key, value)
    db.commit()
    db.refresh(profile)
    return profile