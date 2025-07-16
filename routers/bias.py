from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud import crud_bias
from db.database import get_db
from schema import BiasCreate, BiasRead

router = APIRouter(prefix="/biases", tags=["Biases"])

@router.post("/", response_model=BiasRead)
def create_bias(bias: BiasCreate, db: Session = Depends(get_db)):
    return crud_bias.create_bias(db, bias)

@router.get("/{bias_id}", response_model=BiasRead)
def get_bias(bias_id: UUID, db: Session = Depends(get_db)):
    bias = crud_bias.get_bias(db, bias_id)
    if bias is None:
        raise HTTPException(status_code=404, detail="Bias not found")
    return bias

@router.get("/", response_model=list[BiasRead])
def list_biases(db: Session = Depends(get_db)):
    return crud_bias.get_all_biases(db)
