import uuid

from sqlalchemy import Column, String, JSON, UUID

from db.database import Base


class Stock(Base):
    __tablename__ = 'stock'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    stock_symbol = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    sector = Column (String)
    historical_prices = Column(JSON, nullable=True)