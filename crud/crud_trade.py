from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from models.trade import Trade
from models.user import User
from schema import TradeCreate


def create_trade(db: Session, trade_data: TradeCreate):
    db_trade = Trade(
        user_id=trade_data.user_id,
        stock_symbol=trade_data.stock_symbol,
        trade_type=trade_data.trade_type,
        quantity=trade_data.quantity,
        price_per_share=trade_data.price_per_share,
        resulting_portfolio_value=trade_data.resulting_portfolio_value,
        trade_date=trade_data.trade_date,
    )
    db.add(db_trade)

    # Update total trades count for user
    user = db.query(User).filter(User.id == trade_data.user_id).first()
    if user:
        user.total_trades += 1

    db.commit()
    db.refresh(db_trade)
    return db_trade

def get_trade(db: Session, trade_id: UUID):
    return db.query(Trade).filter(Trade.id == trade_id).first()


def get_all_trades(db: Session):
    return db.query(Trade).all()


def delete_trade(db: Session, trade_id: UUID):
    trade = get_trade(db, trade_id)
    if trade:
        db.delete(trade)
        db.commit()


def get_trades_by_user(db: Session, user_id: UUID):
    return db.query(Trade).filter(Trade.user_id == user_id).all()

def get_trades_by_session(db: Session, session_id: UUID):
    return db.query(Trade).filter(Trade.id == session_id).all()