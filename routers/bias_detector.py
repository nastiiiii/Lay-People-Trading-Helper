from fastapi import APIRouter
from pydantic import BaseModel

from services.bias_detector import predict_bias

router = APIRouter(prefix="/bias", tags=["Bias Detection"])

class BiasInput(BaseModel):
    reason: str

@router.post("/detect")
def detect_bias(data: BiasInput):
    prediction = predict_bias(data.reason)
    return {"bias": prediction}
