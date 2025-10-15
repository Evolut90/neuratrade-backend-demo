"""Routes for trading operations"""

from fastapi import APIRouter, HTTPException 
from app.services.exchange_service import exchange_service
from app.models.trade import Trade, TradeCreate, TradeResponse
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


@router.post("/orders", response_model=TradeResponse)
async def create_order(trade: TradeCreate):
    """
    Cria uma nova ordem de trading
    
    - **symbol**: Par de trading (ex: BTC/USDT)
    - **side**: buy ou sell
    - **amount**: Quantidade a comprar/vender
    - **price**: Preço (opcional para market orders)
    """
    try:
        # Determinar tipo de ordem
        order_type = "market" if trade.price is None else "limit"
        
        # Criar ordem na exchange
        order_result = await exchange_service.create_order(
            symbol=trade.symbol,
            side=trade.side,
            amount=float(trade.amount),
            price=float(trade.price) if trade.price else None,
            order_type=order_type
        )
        
        # Criar objeto Trade
        trade_obj = Trade(
            id=order_result.get('id', 'unknown'),
            symbol=trade.symbol,
            side=trade.side,
            amount=trade.amount,
            price=trade.price,
            status="executed" if order_result.get('status') == 'closed' else "pending",
            executed_price=order_result.get('price'),
            executed_amount=order_result.get('filled'),
            fee=order_result.get('fee', {}).get('cost')
        )
        
        return TradeResponse(
            success=True,
            message="Ordem criada com sucesso",
            trade=trade_obj
        )
        
    except Exception as e:
        return TradeResponse(
            success=False,
            message="Erro ao criar ordem",
            error=str(e)
        )        