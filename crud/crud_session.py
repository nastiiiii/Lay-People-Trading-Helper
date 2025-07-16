from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from models.trade import Trade
from models.trade_session import TradeSession


def start_trade_session(db: Session, user_id: UUID):
    new_session = TradeSession(user_id=user_id, started_at=datetime.utcnow())
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

def end_trade_session(db: Session, session_id: UUID):
    session = db.query(TradeSession).filter(TradeSession.session_id == session_id).first()
    if not session:
        return None

    trades = db.query(Trade).filter(Trade.id == session_id).all()
    session.ended_at = datetime.utcnow()
    session.total_trades = len(trades)
    session.total_volume = sum(trade.quantity for trade in trades)

    db.commit()
    db.refresh(session)
    return session

def get_sessions_by_user(db: Session, user_id: UUID):
    return db.query(TradeSession).filter(TradeSession.user_id == user_id).order_by(TradeSession.started_at.desc()).all()
