from collections import defaultdict
from models.stock import Stock
from sqlalchemy.orm import Session

from models.sandboxDecision import SandboxDecision
from models.sandboxSession import SandboxSession
from models.sandboxTrade import SandboxTrade
from schema import SandboxTradeCreate, SandboxDecisionCreate
from utils.simulation_state import SimulationState


def close_sandbox_session (db: Session, session_id):
    session = db.query(SandboxSession).filter_by(session_id=session_id).first()
    if session:
        session.is_active = False
        db.commit()
        db.refresh(session)
    return session

def get_total_shares(db: Session, session_id, stock_symbol):
    trades = db.query(SandboxTrade).filter_by(session_id=session_id, stock_symbol=stock_symbol).all()
    return sum(t.quantity if t.action.lower() == 'buy' else -t.quantity for t in trades)

def execute_trade(db:Session, trade_data: SandboxTradeCreate):
    session = db.query(SandboxSession).filter(
        SandboxSession.session_id == trade_data.session_id,
        SandboxSession.is_active == True
    ).first()

    if not session:
        raise ValueError("No active session found")

    stock = db.query(Stock).filter_by(stock_symbol=trade_data.stock_symbol).first()
    if not stock or not stock.historical_prices:
        raise ValueError("Stock or price data not available")

    current_price = SimulationState().get_price(trade_data.session_id, trade_data.stock_symbol)
    if current_price is None:
        raise ValueError("No current price available for this stock")

    total = current_price * trade_data.quantity


    #BUY
    if trade_data.action.lower() == "buy":
        if session.current_balance < total:
            raise ValueError("Not enough balance")
        session.current_balance -= total

    #SELL
    elif  trade_data.action.lower() == "sell":
        owned = get_total_shares(db, trade_data.session_id, trade_data.stock_symbol)
        if owned < trade_data.quantity:
            raise ValueError(f"Not enough shares to sell. Owned: {owned}, Attempted: {trade_data.quantity}")
        session.current_balance += total

    else: raise ValueError("Invalid action")

    #Record the trade
    trade = SandboxTrade(
        session_id=trade_data.session_id,
        stock_symbol=trade_data.stock_symbol,
        action=trade_data.action,
        price= current_price,
        quantity=trade_data.quantity,
        timestamp=trade_data.timestamp,
    )
    db.add(trade)

    session.current_date = trade_data.timestamp
    db.commit()
    db.refresh(trade)
    return trade


def get_portfolio_summary(db: Session, session_id):
    session = db.query(SandboxSession).filter_by(session_id=session_id).first()
    if not session:
        raise ValueError("Session not found")

    trades = db.query(SandboxTrade).filter_by(session_id=session_id).all()
    portfolio = defaultdict(float)

    for trade in trades:
        if trade.action.lower() == "buy":
            portfolio[trade.stock_symbol] += trade.quantity
        elif trade.action.lower() == "sell":
            portfolio[trade.stock_symbol] -= trade.quantity

    holdings = []
    total_stock_value = 0.0
    for symbol, qty in portfolio.items():
        if qty <= 0:
            continue
        stock = db.query(Stock).filter_by(stock_symbol=symbol).first()
        if not stock or not stock.historical_prices:
            continue
        # Current simulated price
        delta_days = (session.current_date - session.start_date).days
        if delta_days >= len(stock.historical_prices):
            continue
        current_price = stock.historical_prices[delta_days]
        market_value = qty * current_price
        total_stock_value += market_value
        holdings.append({
            "stock_symbol": symbol,
            "quantity": qty,
            "current_price": round(current_price, 2),
            "market_value": round(market_value, 2)
        })

    return {
        "cash_balance": round(session.current_balance, 2),
        "stock_holdings": holdings,
        "total_portfolio_value": round(session.current_balance + total_stock_value, 2)
    }
