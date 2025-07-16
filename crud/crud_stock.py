from sqlalchemy.orm import declarative_base, Session

from models.stock import Stock

Base = declarative_base()

def create_stock(db: Session, stock_data):
    db_stock = Stock(**stock_data.dict())
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock

def get_stock(db: Session, symbol):
    return db.query(Stock).filter(Stock.stock_symbol == symbol).first()

def get_all_stocks(db: Session):
    return db.query(Stock).all()

def update_stock(db: Session, symbol, updates):
    stock = db.query(Stock).filter(Stock.stock_symbol == symbol).first()
    for key, value in updates.items():
        setattr(stock, key, value)
    db.commit()
    db.refresh(stock)
    return stock

def delete_stock(db: Session, symbol):
    stock = db.query(Stock).filter(Stock.stock_symbol == symbol).first()
    db.delete(stock)
    db.commit()