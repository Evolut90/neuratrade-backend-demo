from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class StrategyBase(BaseModel):
    """Modelo base para estratégias de trading"""
    name: str = Field(..., min_length=3, max_length=100, description="Nome da estratégia")
    description: Optional[str] = Field(None, description="Descrição da estratégia")
    symbols: List[str] = Field(..., min_length=1, description="Pares de trading")
    timeframe: str = Field(default="1h", description="Timeframe (1m, 5m, 15m, 1h, 4h, 1d)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "RSI Oversold",
                "description": "Compra quando RSI < 30, vende quando RSI > 70",
                "symbols": ["BTC/USDT", "ETH/USDT"],
                "timeframe": "1h"
            }
        }


class StrategyCreate(StrategyBase):
    """Modelo para criar uma nova estratégia"""
    parameters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Parâmetros da estratégia"
    )
    is_active: bool = Field(default=False, description="Se a estratégia está ativa")


class Strategy(StrategyBase):
    """Modelo completo de uma estratégia"""
    id: str = Field(..., description="ID único da estratégia")
    parameters: Dict[str, Any] = Field(default_factory=dict)
    is_active: bool = Field(default=False)
    performance: Optional[Dict[str, Any]] = Field(
        None,
        description="Métricas de performance"
    )
    total_trades: int = Field(default=0, description="Total de trades executados")
    win_rate: Optional[float] = Field(None, ge=0, le=100, description="Taxa de acerto (%)")
    total_profit: Optional[float] = Field(None, description="Lucro total")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "strategy_123",
                "name": "RSI Oversold",
                "description": "Compra quando RSI < 30",
                "symbols": ["BTC/USDT"],
                "timeframe": "1h",
                "parameters": {
                    "rsi_period": 14,
                    "oversold_level": 30,
                    "overbought_level": 70
                },
                "is_active": True,
                "total_trades": 45,
                "win_rate": 65.5,
                "total_profit": 1250.50,
                "created_at": "2025-10-01T10:00:00",
                "updated_at": "2025-10-07T18:00:00"
            }
        }


class StrategyUpdate(BaseModel):
    """Modelo para atualizar uma estratégia"""
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    symbols: Optional[List[str]] = None
    timeframe: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class StrategySignal(BaseModel):
    """Sinal gerado por uma estratégia"""
    strategy_id: str
    symbol: str
    signal: str = Field(..., description="buy, sell, hold")
    confidence: float = Field(..., ge=0, le=1, description="Confiança no sinal (0-1)")
    indicators: Dict[str, Any] = Field(default_factory=dict, description="Valores dos indicadores")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "strategy_id": "strategy_123",
                "symbol": "BTC/USDT",
                "signal": "buy",
                "confidence": 0.85,
                "indicators": {
                    "rsi": 28.5,
                    "macd": -120.5,
                    "price": 45000.00
                },
                "timestamp": "2025-10-07T18:00:00"
            }
        }

