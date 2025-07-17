from datetime import datetime, date
from typing import Optional, List
from uuid import UUID

from models.enums import ExperienceLevelEnum, TradeTypeEnum, DeliveryTypeEnum, UserResponseEnum
from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    experience_level: ExperienceLevelEnum

class UserRead(BaseModel):
    id: UUID
    username: str
    email: str
    experience_level: ExperienceLevelEnum
    created_at: datetime
    total_trades: int

    class Config:
        from_attributes = True

class TradeCreate(BaseModel):
    user_id: UUID
    stock_symbol: str
    trade_type: TradeTypeEnum
    trade_date: datetime
    quantity: int
    price_per_share: float
    resulting_portfolio_value: float

class TradeRead(BaseModel):
    id: UUID
    user_id: UUID
    stock_symbol: str
    trade_type: TradeTypeEnum
    trade_date: datetime
    quantity: int
    price_per_share: float
    resulting_portfolio_value: float

    class Config:
        from_attributes = True

class StockCreate(BaseModel):
    stock_symbol: str
    company_name: str
    sector: str
    historical_prices: Optional[List[float]] = None

class StockRead(BaseModel):
    stock_symbol: str
    company_name: str
    sector: str
    historical_prices: Optional[List[float]]

    class Config:
        from_attributes = True

class BiasCreate(BaseModel):
    bias_type: str
    user_id: UUID
    trade_id: UUID
    detected_at: datetime
    severity_score: float

    class Config:
        from_attributes = True

class BiasRead(BaseModel):
    id: UUID
    bias_type: str  # or BiasTypeEnum
    user_id: UUID
    trade_id: UUID
    detected_at: datetime
    severity_score: float

    class Config:
        from_attributes = True

class NudgeCreate(BaseModel):
    bias_id: UUID
    user_id: UUID
    message_content: str
    delivery_type: DeliveryTypeEnum
    user_response: UserResponseEnum
    delivered_at: datetime

class NudgeRead(BaseModel):
    id: UUID
    bias_id: UUID
    user_id: UUID
    message_content: str
    delivery_type: DeliveryTypeEnum
    user_response: Optional[str]
    delivered_at: datetime

    class Config:
        from_attributes = True

class BehaviorProfileCreate(BaseModel):
    user_id: UUID
    total_bias_events: int
    most_frequent_bias: str
    bias_score_history: List[float]
    last_updated: datetime

class BehaviorProfileRead(BaseModel):
    id: UUID
    user_id: UUID
    total_bias_events: int
    most_frequent_bias: str
    bias_score_history: List[float]
    last_updated: datetime

    class Config:
        from_attributes = True

class SandboxTradeBase(BaseModel):
    stock_symbol: str
    action: str
    quantity: float
    timestamp: date
    reason: Optional[str] = None

class SandboxTradeCreate(SandboxTradeBase):
    session_id: UUID

class SandboxTradeRead(SandboxTradeBase):
    trade_id: UUID
    session_id: UUID

    class Config:
        orm_mode = True

class SandboxSessionBase(BaseModel):
    start_date: date
    current_date: date
    initial_balance: float = 100.0
    current_balance: float = 100.0
    is_active: bool = True

class SandboxSessionCreate(SandboxSessionBase):
    user_id: UUID

class SandboxSessionRead(SandboxSessionBase):
    session_id: UUID
    user_id: UUID
    trades: List[SandboxTradeRead] = []

    class Config:
        orm_mode = True

class SandboxDecisionCreate(BaseModel):
    trade_id: UUID
    user_reason: str

class SandboxDecisionRead(SandboxDecisionCreate):
    decision_id: UUID
    detected_biases: Optional[str]

    class Config:
        orm_mode = True
