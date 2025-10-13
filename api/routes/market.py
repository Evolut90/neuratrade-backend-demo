from fastapi import APIRouter, HTTPException, Query 
from app.services.exchange_service import exchange_service
from app.models.market_data import Ticker, Candle
from typing import List
from app.models.market_data import HistoricalDataRequest
 
 
router = APIRouter(prefix="/market", tags=["Market Data"])


@router.get("/ticker/{symbol}", response_model=Ticker)
async def get_ticker(symbol: str):
    """
    Obtém dados de ticker para um símbolo específico
    
    - **symbol**: Par de trading (ex: BTC/USDT)
    
    Retorna preço atual, volume, variação 24h, etc.
    """
    try:
        ticker = await exchange_service.get_ticker(symbol)
        return ticker
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar ticker: {str(e)}")



@router.get("/trending")
async def get_trending_pairs(limit: int = Query(10, ge=1, le=50)):
    """
    Get the most traded pairs (highest 24h volume)
    
    **Note**: Simplified implementation.
    In production, you can use exchange data or calculate based on volume.
    """
    try:
        # Lista de pares populares (exemplo)
        popular_pairs = [
            "BTC/USDT", "ETH/USDT", "BNB/USDT", "XRP/USDT", "ADA/USDT",
            "SOL/USDT", "DOT/USDT", "DOGE/USDT", "AVAX/USDT", "MATIC/USDT"
        ]
        
        trending = []
        for symbol in popular_pairs[:limit]:
            try:
                ticker = await exchange_service.get_ticker(symbol)
                trending.append({
                    "symbol": symbol,
                    "price": float(ticker.last_price),
                    "change_24h": ticker.change_24h,
                    "volume_24h": float(ticker.volume_24h) if ticker.volume_24h else 0
                })
            except:
                continue
        
        # Ordenar por volume
        trending.sort(key=lambda x: x['volume_24h'], reverse=True)
        
        return {
            "success": True,
            "trending_pairs": trending
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")


@router.post("/candles", response_model=List[Candle])
async def get_candles(request: HistoricalDataRequest):
    """
    Obtém dados históricos de candlestick (OHLCV)
    
    - **symbol**: Par de trading
    - **timeframe**: Intervalo (1m, 5m, 15m, 1h, 4h, 1d)
    - **limit**: Número de velas (máximo 1000)
    
    Útil para análise técnica e backtesting
    """
    try:
        candles = await exchange_service.get_ohlcv(
            symbol=request.symbol,
            timeframe=request.timeframe,
            limit=request.limit
        )
        return candles
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar candles: {str(e)}")        