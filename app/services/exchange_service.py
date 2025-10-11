from app.models.market_data import Ticker
from decimal import Decimal
from datetime import datetime
from app.core.config import settings
import ccxt

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
                    'defaultType': 'future' if self.testnet else 'spot',
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


# Instância global do serviço
exchange_service = ExchangeService(exchange_name="binance", testnet=True)            