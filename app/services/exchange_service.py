from app.models.market_data import Ticker
from decimal import Decimal
from datetime import datetime
from app.core.config import settings
import ccxt
from typing import List
from app.models.market_data import Candle
from typing import Dict, Any, Optional


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
    
    async def get_ticker(self, symbol: str) -> Ticker:
        """
        Get ticker data for a symbol
        
        Args:
            symbol: Trading pair (ex: BTC/USDT)
            
        Returns:
            Ticker object with the data
        """
        try:
            ticker_data = self.exchange.fetch_ticker(symbol)
            
            return Ticker(
                symbol=symbol,
                last_price=Decimal(str(ticker_data['last'])),
                bid=Decimal(str(ticker_data['bid'])) if ticker_data.get('bid') else None,
                ask=Decimal(str(ticker_data['ask'])) if ticker_data.get('ask') else None,
                high_24h=Decimal(str(ticker_data['high'])) if ticker_data.get('high') else None,
                low_24h=Decimal(str(ticker_data['low'])) if ticker_data.get('low') else None,
                volume_24h=Decimal(str(ticker_data['quoteVolume'])) if ticker_data.get('quoteVolume') else None,
                change_24h=ticker_data.get('percentage'),
                timestamp=datetime.now()
            )
        except Exception as e:
            raise Exception(f"Erro ao buscar ticker: {str(e)}")



    async def get_ohlcv(self, symbol: str, timeframe: str = '1h', limit: int = 100) -> List[Candle]:
        """
        Get OHLCV (candlestick) data for a symbol
        
        Args:
            symbol: Trading pair (ex: BTC/USDT)
            timeframe: Timeframe (1m, 5m, 15m, 1h, 4h, 1d)
            limit: Number of candles
        """
        try:
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

    async def get_balance(self) -> Dict[str, Any]:
            """
            Get the balance of the account
            
            Returns:
                Dictionary with the balance of each currency
            """
            try:
                balance = self.exchange.fetch_balance()
                
                # filter only balances with value
                filtered_balance = {}
                for currency, amount in balance['total'].items():
                    if amount > 0:
                        filtered_balance[currency] = {
                            'total': amount,
                            'free': balance['free'].get(currency, 0),
                            'used': balance['used'].get(currency, 0)
                        }
                
                return filtered_balance
            except Exception as e:
                raise Exception(f"Erro ao buscar saldo: {str(e)}")      


    async def create_order(
        self,
        symbol: str,
        side: str,
        amount: float,
        price: Optional[float] = None,
        order_type: str = "limit"
    ) -> Dict[str, Any]:
        """
        Create an order in the exchange
        
        Args:
            symbol: Trading pair
            side: buy ou sell
            amount: Amount
            price: Price (None for market order)
            order_type: limit or market 
            
        Returns:
            Data of the created order
        """
        try:
            if order_type == "market":
                order = self.exchange.create_market_order(symbol, side, amount)
            else:
                if price is None:
                    raise ValueError("Price is required for limit order")
                order = self.exchange.create_limit_order(symbol, side, amount, price)
            
            return order
        except Exception as e:
            raise Exception(f"Error creating order: {str(e)}")


             
# Instância global do serviço
exchange_service = ExchangeService(exchange_name="binance", testnet=True)            