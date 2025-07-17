from datetime import timedelta, datetime
import time
import random

from sqlalchemy.orm import Session

from models.sandboxSession import SandboxSession
from models.stock import Stock
from utils.simulation_state import SimulationState


def run_sandbox_simulation(session_id: str, db:Session):
    session = db.query(SandboxSession).filter_by(session_id=session_id).first()
    if not session or not session.is_active:
        return
    stock = db.query(Stock).filter_by(stock_symbol="AAPL").first() #TODO: random stock
    prices = stock.historical_prices
    if not prices or len(prices) < 30:
        return

    #random starting point
    start_idx = random.randint(0, len(prices) - 30)
    current_idx = start_idx

    print(f"[SIM] Starting simulation at index {start_idx}")
    print(f"[{datetime.now()}] Price updated to: {current_idx}")
    sim_state = SimulationState()

    while current_idx < len(prices):
        time.sleep(5)

        session = db.query(SandboxSession).filter_by(session_id=session_id).first()
        if not session or not session.is_active:
            break

        #price progression
        new_date = session.current_date + timedelta(days=1)
        session.current_date = new_date
        db.commit()

        price_now = prices[current_idx]
        sim_state.update_price(session.session_id, stock.stock_symbol, price_now)
        print(f"[SIM] {session.user_id} | Date: {new_date} | Price: {price_now}")

        current_idx += 1
    print(f"[SIM] Simulation ended for session {session_id}") #TODO print summary

