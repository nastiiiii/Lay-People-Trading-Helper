import threading
from datetime import date

from fastapi import Depends, APIRouter, HTTPException
from uuid import UUID
from sqlalchemy.orm import Session

from crud import crud_sandbox
from db.database import get_db
from models.sandboxSession import SandboxSession
from schema import SandboxTradeRead, SandboxTradeCreate
from services.sandbox_simulator import run_sandbox_simulation

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
