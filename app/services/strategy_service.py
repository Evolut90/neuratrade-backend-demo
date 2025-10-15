from app.models.strategy import Strategy
from typing import Dict, Any
from app.services.exchange_service import exchange_service
from datetime import datetime


class StrategyService:
    def __init__(self):
        pass

    async def compare_all_strategies(
            self,
            symbol: str,
            timeframe: str = "1h"
        ) -> Dict[str, Any]:
            """
            Execute all strategies and return a complete comparison
            
            Args:
                symbol: Trading pair (ex: BTC/USDT)
                timeframe: Timeframe for analysis (1h, 4h, 1d, etc)
                
            Returns:
                Dictionary with results of all strategies and final recommendation
            """
            # Buscar dados de mercado
            candles = await exchange_service.get_ohlcv(symbol, timeframe, limit=200)
            
            if not candles or len(candles) == 0:
                raise ValueError(f"Unable to get market data for {symbol}")
            
            # Calculate indicators

             # Dados fictícios para as estratégias
            strategies_data = [
                {
                    "name": "RSI Strategy",
                    "signal": "buy",
                    "confidence": 0.85,
                    "description": "RSI indica sobrevenda, sinal de compra"
                },
                {
                    "name": "MACD Strategy", 
                    "signal": "sell",
                    "confidence": 0.72,
                    "description": "MACD cruzou para baixo, sinal de venda"
                },
                {
                    "name": "Bollinger Bands",
                    "signal": "hold",
                    "confidence": 0.68,
                    "description": "Preço próximo à banda média, aguardar"
                },
                {
                    "name": "Moving Average",
                    "signal": "buy",
                    "confidence": 0.91,
                    "description": "EMA20 acima da EMA50, tendência de alta"
                }
            ]
           
            
            return {
                "symbol": symbol,
                "timeframe": timeframe,
                "current_price": 45234.56,
                "timestamp": datetime.now().isoformat(),
                "strategies": strategies_data,
                "consensus": {
                    "buy": 5,
                    "sell": 1,
                    "hold": 1
                },
                "final_recommendation": {
                    "action": "buy",
                    "confidence": 0.65,
                    "agreement": "7/7 estratégias"
                },
                "market_indicators": {
                    "rsi": 32.45,
                    "macd": -156.78,
                    "macd_signal": -142.33,
                    "ema_20": 44890.12,
                    "ema_50": 44123.89,
                    "sma_200": 43256.78,
                    "bb_upper": 46500.00,
                    "bb_middle": 45000.00,
                    "bb_lower": 43500.00,
                    "stoch_rsi_k": 25.67,
                    "stoch_rsi_d": 28.90,
                    "adx": 45.23,
                    "atr": 1234.56,
                    "williams_r": -75.43,
                    "cci": -125.67,
                    "mfi": 38.92,
                    "parabolic_sar": 44800.00,
                    "aroon_up": 65.43,
                    "aroon_down": 25.67,
                    "kc_upper": 46200.00,
                    "kc_middle": 45200.00,
                    "kc_lower": 44200.00,
                    "candlestick_patterns": ["Hammer", "Doji"],
                    "pattern_signal": "bullish",
                    "pattern_strength": 0.75,
                    "timestamp": datetime.now().isoformat()
                }
            }

 


strategy_service = StrategyService()