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


class Candle(BaseModel):
    """Dados de candlestick OHLCV"""
    timestamp: datetime = Field(..., description="Data/hora da vela")
    open: Decimal = Field(..., description="Preço de abertura")
    high: Decimal = Field(..., description="Preço máximo")
    low: Decimal = Field(..., description="Preço mínimo")
    close: Decimal = Field(..., description="Preço de fechamento")
    volume: Decimal = Field(..., description="Volume")
    
    class Config:
        json_schema_extra = {
            "example": {
                "timestamp": "2025-10-07T18:00:00",
                "open": 45000.00,
                "high": 45500.00,
                "low": 44800.00,
                "close": 45200.00,
                "volume": 125.50
            }
        }        


class HistoricalDataRequest(BaseModel):
    """Request para dados históricos"""
    symbol: str = Field(..., description="Par de trading")
    timeframe: str = Field(default="1h", description="Timeframe (1m, 5m, 15m, 1h, 4h, 1d)")
    limit: int = Field(default=100, ge=1, le=1000, description="Número de velas")
    
    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "BTC/USDT",
                "timeframe": "1h",
                "limit": 100
            }
        }

