from decimal import Decimal
from datetime import datetime
from app.core.config import settings
import ccxt
from typing import List
from app.models.market_data import Candle 
from app.services.mock_data_service import MockDataService


class ExchangeService:
    def __init__(self, exchange_name: str = "binance", testnet: bool = True):
        """ 
        Intialize the connection with the exchange
        
        Args:
            exchange_name: Name of exchange (binance, coinbase, etc)
            testnet: If should use the testnet (True for development)
        """
        self.exchange_name = exchange_name
        self.testnet = testnet
        self.exchange = self._init_exchange()
        self.use_mock_data = self._should_use_mock_data()
    
    def _should_use_mock_data(self) -> bool:
        """Verifica se deve usar dados fictícios (quando não há API keys)"""
        api_key = settings.binance_api_key
        secret_key = settings.binance_secret_key
        
        # Use mock if keys are not set or are empty
        if not api_key or not secret_key or api_key.strip() == "" or secret_key.strip() == "":
            return True
        
        return False
    
    def _init_exchange(self) -> ccxt.Exchange:
        """Initialize the exchange with the settings"""
        try:
            exchange_class = getattr(ccxt, self.exchange_name)
            
            config = {
                'apiKey': settings.binance_api_key,
                'secret': settings.binance_secret_key,
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'spot' if self.testnet else 'spot',
                }
            }
             
                
            exchange = exchange_class(config)
            
            # For testnet of Binance
            if self.testnet and self.exchange_name == 'binance':
                exchange.set_sandbox_mode(True)
            
            return exchange
            
        except Exception as e:
            print(f"Erro ao inicializar exchange: {e}")
            # Return exchange without authentication for public queries
            exchange_class = getattr(ccxt, self.exchange_name)
            return exchange_class({'enableRateLimit': True})
    
 
    async def get_ohlcv(self, symbol: str, timeframe: str = '1h', limit: int = 100) -> List[Candle]:
        """
        Get OHLCV (candlestick) data for a symbol
        
        Args:
            symbol: Trading pair (ex: BTC/USDT)
            timeframe: Timeframe (1m, 5m, 15m, 1h, 4h, 1d)
            limit: Number of candles
        """
        try:
            if self.use_mock_data:
                # Mock data already returns Candle objects
                return MockDataService.generate_ohlcv(symbol, timeframe, limit)
            else:
                # Real API data needs to be converted to Candle objects
                ohlcv_data = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
                candles = []
                for candle_data in ohlcv_data:
                    candles.append(Candle(
                        timestamp=datetime.fromtimestamp(candle_data[0] / 1000),
                        open=Decimal(str(candle_data[1])),
                        high=Decimal(str(candle_data[2])),
                        low=Decimal(str(candle_data[3])),
                        close=Decimal(str(candle_data[4])),
                        volume=Decimal(str(candle_data[5]))
                    ))
            return candles
        except Exception as e:
            raise Exception(f"Erro ao buscar OHLCV: {str(e)}")    
 
             
# Instância global do serviço
exchange_service = ExchangeService(exchange_name="binance", testnet=True)            