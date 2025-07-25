import threading
from datetime import date

from fastapi import Depends, APIRouter, HTTPException
from uuid import UUID

from openai import OpenAI
from sqlalchemy.orm import Session

from crud import crud_sandbox
from db.database import get_db
from models.sandboxSession import SandboxSession
from schema import SandboxTradeRead, SandboxTradeCreate
from services.sandbox_simulator import run_sandbox_simulation
from utils.sandbox_advice import get_sandbox_advice, get_claude_advice
from utils.simulation_state import SimulationState

router = APIRouter(prefix="/sandbox", tags=["Sandbox"])

@router.post("/start-sandbox/{user_id}")
def start_sandbox(user_id: UUID, db: Session = Depends(get_db)):
    today = date.today()
    session = SandboxSession(user_id=user_id, start_date=today, current_date=today)
    db.add(session)
    db.commit()
    db.refresh(session)

    thread = threading.Thread(target=run_sandbox_simulation, args=(session.session_id, db))
    thread.start()

    return {"msg": "Sandbox started", "session_id": session.session_id}


@router.post("/sandbox/stop/{session_id}")
def stop_sandbox(session_id: UUID, db: Session = Depends(get_db)):
    session = crud_sandbox.close_sandbox_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Sandbox session not found.")
    return {"message": f"Sandbox session {session.session_id} has been stopped."}


@router.post("/sandbox/trade", response_model= SandboxTradeRead)
def perform_trade(trade_data: SandboxTradeCreate, db: Session = Depends(get_db)):
    try:
        trade = crud_sandbox.execute_trade(db, trade_data)
        return trade
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/sandbox/portfolio/{session_id}")
def portfolio_summary(session_id: UUID, db: Session = Depends(get_db)):
    try:
        return crud_sandbox.get_portfolio_summary(db, session_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/sandbox/advice")
def sandbox_advice(
    session_id: UUID,
    stock_symbol: str,
    action: str,
    db: Session = Depends(get_db),
):
    return get_sandbox_advice(db, session_id, stock_symbol, action)


@router.get("/sandbox/ai-advice")
def get_ai_advice(session_id: UUID, stock_symbol: str, action: str, db: Session = Depends(get_db)):
    try:
        current_price = SimulationState().get_price(session_id, stock_symbol)
        if current_price is None:
            raise HTTPException(status_code=404, detail="Current price not found in simulation.")

        # Get portfolio snapshot
        portfolio = crud_sandbox.get_portfolio_summary(db, session_id)

        return get_claude_advice(session_id, stock_symbol, action, current_price, portfolio)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sandbox/predict-next")
def get_predicted_price(session_id: UUID, stock_symbol: str):
    predicted_price = SimulationState().predict_next_price(session_id, stock_symbol)
    if predicted_price is None:
        raise HTTPException(status_code=400, detail="Not enough data to predict yet.")
    return {
        "stock_symbol": stock_symbol,
        "predicted_next_price": round(predicted_price, 2)
    }
