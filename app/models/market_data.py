from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal
from typing import Optional


class Ticker(BaseModel):
    """Ticker data"""
    symbol: str = Field(..., description="Trading pair")
    last_price: Decimal = Field(..., description="Last price")
    bid: Optional[Decimal] = Field(None, description="Best bid price")
    ask: Optional[Decimal] = Field(None, description="Best ask price")
    high_24h: Optional[Decimal] = Field(None, description="Maximum 24h")
    low_24h: Optional[Decimal] = Field(None, description="Minimum 24h")
    volume_24h: Optional[Decimal] = Field(None, description="Volume 24h")
    change_24h: Optional[float] = Field(None, description="Change % 24h")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "BTC/USDT",
                "last_price": 45000.00,
                "bid": 44998.50,
                "ask": 45001.50,
                "high_24h": 46500.00,
                "low_24h": 44000.00,
                "volume_24h": 2500.50,
                "change_24h": 2.5,
                "timestamp": "2025-10-07T18:00:00"
            }
        }