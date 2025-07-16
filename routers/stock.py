

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud import crud_stock
from db.database import get_db
from schema import StockRead, StockCreate

router = APIRouter(prefix="/stocks", tags=["Stocks"])

@router.post("/", response_model=StockRead)
def create_stock(stock: StockCreate, db: Session = Depends(get_db)):
    return crud_stock.create_stock(db, stock)

@router.get("/{symbol}", response_model=StockRead)
def get_stock(symbol: str, db: Session = Depends(get_db)):
    stock = crud_stock.get_stock(db, symbol)
    if stock is None:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock

@router.get("/", response_model=list[StockRead])
def list_stocks(db: Session = Depends(get_db)):
    return crud_stock.get_all_stocks(db)