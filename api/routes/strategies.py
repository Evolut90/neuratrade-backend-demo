from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.services.strategy_service import strategy_service
import urllib.parse
 
router = APIRouter(prefix="/strategies", tags=["Strategies"])


@router.get("/compare-all")
async def compare_all_strategies_endpoint(
    symbol: str = Query(..., description="Trading pair (ex: BTC/USDT)"), 
    timeframe: str = Query("1h", description="Timeframe (1m, 5m, 15m, 1h, 4h, 1d)")
):
    """
    Compare all available strategies for a symbol
    """
    try: 
        comparison = await strategy_service.compare_all_strategies(symbol, timeframe)
        return {
            "success": True,
            "data": comparison
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao comparar estratégias: {str(e)}"
        )