from uuid import UUID

from sqlalchemy.orm import Session

from models.nudge import Nudge


def create_nudge(db: Session, nudge_data):
    db_nudge = Nudge(**nudge_data.dict())
    db.add(db_nudge)
    db.commit()
    db.refresh(db_nudge)
    return db_nudge

def get_nudges_by_user(db: Session, user_id):
    return db.query(Nudge).filter(Nudge.user_id == user_id).all()

def get_nudges_by_bias(db: Session, bias_id):
    return db.query(Nudge).filter(Nudge.bias_id == bias_id).all()

def get_nudge(db: Session, nudge_id: UUID):
    return db.query(Nudge).filter(Nudge.id == nudge_id).first()

def get_all_nudges(db: Session):
    try:
        return db.query(Nudge).all()
    except Exception as e:
        print("Error during get_all_nudges:", e)
        raise