# routers/bias_router.py

from fastapi import APIRouter
from pydantic import BaseModel

from services.bias_detector import BiasDetector

router = APIRouter(prefix="/bias", tags=["Bias Detection"])

# Load once globally
bias_model = BiasDetector("yiyanghkust/finbert-tone")

class BiasInput(BaseModel):
    reason: str

@router.post("/detect")
def detect_bias(data: BiasInput):
    prediction = bias_model.predict_bias(data.reason)
    return {"bias": prediction}
