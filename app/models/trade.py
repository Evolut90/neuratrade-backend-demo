from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
from decimal import Decimal


class TradeBase(BaseModel):
    """Modelo base para trades"""
    symbol: str = Field(..., description="Par de trading (ex: BTC/USDT)")
    side: Literal["buy", "sell"] = Field(..., description="Tipo da ordem")
    amount: Decimal = Field(..., gt=0, description="Quantidade")
    price: Optional[Decimal] = Field(None, gt=0, description="Preço (None para market order)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "BTC/USDT",
                "side": "buy",
                "amount": 0.001,
                "price": 45000.00
            }
        }


class TradeCreate(TradeBase):
    """Modelo para criar um novo trade"""
    strategy_id: Optional[str] = Field(None, description="ID da estratégia utilizada")


class Trade(TradeBase):
    """Modelo completo de um trade"""
    id: str = Field(..., description="ID único do trade")
    status: Literal["pending", "executed", "cancelled", "failed"] = Field(
        default="pending",
        description="Status da ordem"
    )
    executed_price: Optional[Decimal] = Field(None, description="Preço executado")
    executed_amount: Optional[Decimal] = Field(None, description="Quantidade executada")
    fee: Optional[Decimal] = Field(None, description="Taxa da transação")
    profit_loss: Optional[Decimal] = Field(None, description="Lucro/Prejuízo")
    created_at: datetime = Field(default_factory=datetime.now)
    executed_at: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "trade_123",
                "symbol": "BTC/USDT",
                "side": "buy",
                "amount": 0.001,
                "price": 45000.00,
                "status": "executed",
                "executed_price": 45050.00,
                "executed_amount": 0.001,
                "fee": 0.45,
                "profit_loss": None,
                "created_at": "2025-10-07T18:00:00",
                "executed_at": "2025-10-07T18:00:05"
            }
        }


class TradeResponse(BaseModel):
    """Resposta de operações de trade"""
    success: bool
    message: str
    trade: Optional[Trade] = None
    error: Optional[str] = None

