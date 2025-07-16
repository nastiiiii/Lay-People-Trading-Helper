from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud import crud_trade
from db.database import get_db
from schema import UserRead, TradeRead, TradeCreate

router = APIRouter(prefix="/trades", tags=["Trades"])

@router.post("/", response_model=TradeRead)
def create_trade(trade: TradeCreate, db: Session = Depends(get_db)):
    return crud_trade.create_trade(db, trade)

@router.get("/{trade_id}", response_model=TradeRead)
def get_trade(trade_id: UUID, db: Session = Depends(get_db)):
    trade = crud_trade.get_trade(db, trade_id)
    if trade is None:
        raise HTTPException(status_code=404, detail="Trade not found")
    return trade

@router.get("/", response_model=list[TradeRead])
def list_trades(db: Session = Depends(get_db)):
    return crud_trade.get_all_trades(db)

@router.delete("/{trade_id}")
def delete_trade(trade_id: UUID, db: Session = Depends(get_db)):
    return crud_trade.delete_trade(db, trade_id)