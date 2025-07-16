from sqlalchemy.orm import Session

from models.bias import Bias

def create_bias(db: Session, bias_data):
    db_bias = Bias(**bias_data.dict())
    db.add(db_bias)
    db.commit()
    db.refresh(db_bias)
    return db_bias

def get_bias(db: Session, bias_id):
    return db.query(Bias).filter(Bias.id == bias_id).first()

def get_biases_by_user(db: Session, user_id):
    return db.query(Bias).filter(Bias.user_id == user_id).all()

def get_all_biases(db: Session):
    return db.query(Bias).all()

def delete_bias(db: Session, bias_id):
    bias = db.query(Bias).filter(Bias.id == bias_id).first()
    db.delete(bias)
    db.commit()