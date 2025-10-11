from fastapi import APIRouter, HTTPException, Query 
from app.services.exchange_service import exchange_service
 
 
router = APIRouter(prefix="/market", tags=["Market Data"])


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