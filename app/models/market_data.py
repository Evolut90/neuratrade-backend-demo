from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from decimal import Decimal


class Ticker(BaseModel):
    """Dados de ticker de mercado"""
    symbol: str = Field(..., description="Par de trading")
    last_price: Decimal = Field(..., description="Último preço")
    bid: Optional[Decimal] = Field(None, description="Melhor preço de compra")
    ask: Optional[Decimal] = Field(None, description="Melhor preço de venda")
    high_24h: Optional[Decimal] = Field(None, description="Máxima 24h")
    low_24h: Optional[Decimal] = Field(None, description="Mínima 24h")
    volume_24h: Optional[Decimal] = Field(None, description="Volume 24h")
    change_24h: Optional[float] = Field(None, description="Variação % 24h")
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


class OrderBook(BaseModel):
    """Livro de ofertas (Order Book)"""
    symbol: str = Field(..., description="Par de trading")
    bids: List[List[float]] = Field(..., description="Ofertas de compra [[price, amount], ...]")
    asks: List[List[float]] = Field(..., description="Ofertas de venda [[price, amount], ...]")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "BTC/USDT",
                "bids": [
                    [44998.50, 0.5],
                    [44997.00, 1.2],
                    [44995.50, 0.8]
                ],
                "asks": [
                    [45001.50, 0.6],
                    [45003.00, 1.1],
                    [45005.50, 0.9]
                ],
                "timestamp": "2025-10-07T18:00:00"
            }
        }


class MarketIndicators(BaseModel):
    """Indicadores técnicos calculados"""
    symbol: str = Field(..., description="Par de trading")
    timeframe: str = Field(..., description="Timeframe dos indicadores")
    
    # Basic Indicators
    rsi: Optional[float] = Field(None, ge=0, le=100, description="RSI (Relative Strength Index)")
    macd: Optional[float] = Field(None, description="MACD")
    macd_signal: Optional[float] = Field(None, description="MACD Signal Line")
    macd_histogram: Optional[float] = Field(None, description="MACD Histogram")
    bb_upper: Optional[Decimal] = Field(None, description="Bollinger Band Superior")
    bb_middle: Optional[Decimal] = Field(None, description="Bollinger Band Média")
    bb_lower: Optional[Decimal] = Field(None, description="Bollinger Band Inferior")
    ema_20: Optional[Decimal] = Field(None, description="EMA 20 períodos")
    ema_50: Optional[Decimal] = Field(None, description="EMA 50 períodos")
    sma_200: Optional[Decimal] = Field(None, description="SMA 200 períodos")
    
    # Advanced Indicators
    stoch_rsi_k: Optional[float] = Field(None, ge=0, le=100, description="Stochastic RSI %K")
    stoch_rsi_d: Optional[float] = Field(None, ge=0, le=100, description="Stochastic RSI %D")
    adx: Optional[float] = Field(None, ge=0, le=100, description="ADX (Average Directional Index)")
    atr: Optional[float] = Field(None, ge=0, description="ATR (Average True Range)")
    williams_r: Optional[float] = Field(None, ge=-100, le=0, description="Williams %R")
    cci: Optional[float] = Field(None, description="CCI (Commodity Channel Index)")
    mfi: Optional[float] = Field(None, ge=0, le=100, description="MFI (Money Flow Index)")
    parabolic_sar: Optional[float] = Field(None, description="Parabolic SAR")
    aroon_up: Optional[float] = Field(None, ge=0, le=100, description="Aroon Up")
    aroon_down: Optional[float] = Field(None, ge=0, le=100, description="Aroon Down")
    kc_upper: Optional[Decimal] = Field(None, description="Keltner Channel Superior")
    kc_middle: Optional[Decimal] = Field(None, description="Keltner Channel Média")
    kc_lower: Optional[Decimal] = Field(None, description="Keltner Channel Inferior")
    
    # Pattern Recognition
    candlestick_patterns: Optional[Dict[str, bool]] = Field(None, description="Padrões de candlestick detectados")
    pattern_signal: Optional[str] = Field(None, description="Sinal dos padrões (bullish/bearish/neutral)")
    pattern_strength: Optional[float] = Field(None, ge=0, le=1, description="Força dos padrões (0-1)")
    
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "BTC/USDT",
                "timeframe": "1h",
                "rsi": 45.5,
                "macd": 125.50,
                "macd_signal": 130.20,
                "macd_histogram": -4.70,
                "bb_upper": 46000.00,
                "bb_middle": 45000.00,
                "bb_lower": 44000.00,
                "ema_20": 45100.00,
                "ema_50": 44800.00,
                "sma_200": 43500.00,
                "stoch_rsi_k": 65.2,
                "stoch_rsi_d": 58.7,
                "adx": 32.1,
                "atr": 1250.5,
                "williams_r": -35.8,
                "cci": 45.2,
                "mfi": 58.3,
                "parabolic_sar": 44500.0,
                "aroon_up": 75.0,
                "aroon_down": 25.0,
                "kc_upper": 46200.00,
                "kc_middle": 45000.00,
                "kc_lower": 43800.00,
                "timestamp": "2025-10-07T18:00:00"
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

