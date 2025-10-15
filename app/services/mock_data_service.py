"""Serviço para geração de dados OHLCV fictícios quando não há API keys"""

import numpy as np
from typing import List
from datetime import datetime, timedelta
from decimal import Decimal
from app.models.market_data import Candle
import logging

logger = logging.getLogger(__name__)


class MockDataService:
    """Generate fake OHLCV data to replace API calls"""
    
    @staticmethod
    def generate_ohlcv(
        symbol: str,
        timeframe: str = '1h',
        limit: int = 100,
        trend: str = 'bullish'  # 'bullish', 'bearish', 'sideways'
    ) -> List[Candle]:
        """
        Generate fake OHLCV data that mimics real exchange data
        
        Args:
            symbol: Trading pair (ex: BTC/USDT)
            timeframe: Timeframe (1m, 5m, 15m, 1h, 4h, 1d)
            limit: Number of candles to generate
            trend: Trend type ('bullish', 'bearish', 'sideways')
            
        Returns:
            List of Candle objects
        """
        logger.info(f"🎭 Generating {limit} fake candles for {symbol} ({trend})")
        
        # Set base price based on symbol
        base_prices = {
            'BTC/USDT': 45000,
            'ETH/USDT': 2500,
            'BNB/USDT': 350,
            'SOL/USDT': 100,
            'ADA/USDT': 0.5,
            'XRP/USDT': 0.6,
            'DOT/USDT': 7.5,
            'DOGE/USDT': 0.08
        }
        
        base_price = base_prices.get(symbol, 1000)
        
        # Base volatility parameters based on timeframe
        volatility_map = {
            '1m': 0.002,   # 0.2% por candle
            '5m': 0.005,   # 0.5%
            '15m': 0.008,  # 0.8%
            '1h': 0.01,    # 1%
            '4h': 0.02,    # 2%
            '1d': 0.03     # 3%
        }
        
        volatility = volatility_map.get(timeframe, 0.01)
        
        # Determine time interval based on timeframe
        time_deltas = {
            '1m': timedelta(minutes=1),
            '5m': timedelta(minutes=5),
            '15m': timedelta(minutes=15),
            '1h': timedelta(hours=1),
            '4h': timedelta(hours=4),
            '1d': timedelta(days=1)
        }
        
        time_delta = time_deltas.get(timeframe, timedelta(hours=1))
        
        # Generate candles
        candles = []
        current_price = base_price
        current_time = datetime.now() - (time_delta * limit)
        
        for i in range(limit):
            # Apply trend
            if trend == 'bullish':
                # Bullish trend with small corrections
                trend_change = base_price * 0.002 * (1 + 0.3 * np.sin(i / 20))
                current_price += trend_change
                
            elif trend == 'bearish':
                # Bearish trend with small corrections
                trend_change = base_price * 0.002 * (1 + 0.3 * np.sin(i / 20))
                current_price -= trend_change
                
            elif trend == 'sideways':
                # Lateral oscillation
                current_price = base_price + base_price * 0.02 * np.sin(i / 10)
            
            # Add noise (volatility)
            noise = current_price * volatility * np.random.randn()
            current_price += noise
            
            # Generate OHLC for candle
            candle_volatility = volatility * 1.5
            
            # Open: price with small variation
            open_price = current_price + current_price * candle_volatility * np.random.randn() * 0.3
            
            # High: always greater than or equal to open and close
            high_price = max(open_price, current_price) + abs(current_price * candle_volatility * np.random.rand())
            
            # Low: always less than or equal to open and close
            low_price = min(open_price, current_price) - abs(current_price * candle_volatility * np.random.rand())
            
            # Close: current price
            close_price = current_price
            
            # Volume: random but realistic
            avg_volume = 1000000
            volume = abs(np.random.normal(avg_volume, avg_volume * 0.3))
            
            # Ensure correct order: low <= open,close <= high
            high_price = max(high_price, open_price, close_price)
            low_price = min(low_price, open_price, close_price)
                
            # Create candle
            candle = Candle(
                timestamp=current_time,
                open=Decimal(str(round(open_price, 2))),
                high=Decimal(str(round(high_price, 2))),
                low=Decimal(str(round(low_price, 2))),
                close=Decimal(str(round(close_price, 2))),
                volume=Decimal(str(round(volume, 2)))
            )
            
            candles.append(candle)
            current_time += time_delta
        
        logger.info(f"✅ Gerados {len(candles)} candles - Preço inicial: ${candles[0].close}, Final: ${candles[-1].close}")
        
        return candles
    
    @staticmethod
    def auto_detect_trend(symbol: str) -> str:
        """
        Auto-detect trend based on symbol hash
        (to get consistent results for the same symbol)
        """
        hash_value = hash(symbol) % 100
        
        if hash_value < 40:
            return 'bullish'
        elif hash_value < 70:
            return 'sideways'
        else:
            return 'bearish'


# Global instance
mock_data_service = MockDataService()

