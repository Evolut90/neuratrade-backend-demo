"""Routes for trading operations"""

from fastapi import APIRouter, HTTPException 
from app.services.exchange_service import exchange_service

router = APIRouter(prefix="/trading", tags=["Trading"])


@router.get("/balance")
async def get_balance():
    """
    Get the current balance of the account
    
    Returns the balance of all available currencies
    """
    try:
        balance = await exchange_service.get_balance()
        return {
            "success": True,
            "balance": balance
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))