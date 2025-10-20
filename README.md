# NeuraTrade Backend Demo

AI-powered automated trading system with multiple strategy comparison and technical analysis.

## Features

- **Multiple Trading Strategies**: Conservative and Scalping
- **Technical Analysis**: RSI, MACD, Bollinger Bands, EMA, SMA, Stochastic RSI, Williams %R, CCI, MFI, Parabolic SAR, Aroon, Keltner Channels, ADX, ATR
- **Strategy Comparison**: Real-time comparison of all strategies with consensus analysis
- **FastAPI Backend**: RESTful API with automatic documentation
- **Binance Integration**: Real-time market data and trading capabilities
- **🎭 Mock Data Support**: Test without API keys using realistic fake market data

## Prerequisites

- Python 3.11 (recommended) or Python 3.12
- Binance API keys (optional - system works with mock data)
- Linux/macOS/Windows

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd neuratrade-backend-demo
```

### 2. Create Virtual Environment with Python 3.11
```bash
# Create virtual environment with Python 3.11
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies
```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

### 4. Configure Environment Variables (Optional)
Create a `.env` file in the root directory:
```env
# Binance API Configuration (OPTIONAL - leave empty to use mock data)
BINANCE_API_KEY=your_binance_api_key_here
BINANCE_SECRET_KEY=your_binance_secret_key_here

# API Settings
API_TITLE=AI Trading Bot - NeuraTrade
API_VERSION=1.0.0
DEBUG=true 
```

**Note:** If you don't have Binance API keys or leave them empty, the system will automatically use **mock data** for testing. This allows you to test all strategies without needing real API access!

## Testing Strategies

### Direct Strategy Testing (Recommended)

Test strategies directly without running the server:

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run strategy comparison test (works with or without API keys)
python3 test_strategies_compare.py
```

**🎭 Mock Data Mode:** If you don't have Binance API keys configured, the system automatically generates realistic fake market data for testing. This includes:
- Realistic price movements with different trends (bullish, bearish, sideways)
- Proper OHLCV data structure
- Volatility based on timeframe
- Consistent results for the same symbol

#### Test Options:
1. **Test BTC/USDT (1h)** - Quick test with Bitcoin
2. **Test ETH/USDT (1h)** - Quick test with Ethereum  
3. **Test all symbols and timeframes** - Comprehensive test
4. **Customized** - Enter custom symbol and timeframe

#### Example Output:
```
🔍 ANALYSING: BTC/USDT (1h)
================================================================================

⏳ Searching for data and calculating indicators...

💰 Current Price: $45,230.50
⏰ Timestamp: 2024-01-15T10:30:00

📊 TECHNICAL INDICATORS:
  📈 MOMENTUM:
    RSI:        45.23 (Neutro)
    Stoch RSI:  52.10 / 48.30
    Williams %R: -47.80

  📊 TREND:
    MACD:       125.45
    MACD Sinal: 118.20
    ADX:        28.50

🎯 RESULT OF STRATEGIES:
  Conservative       → BUY             (confidence: 50.0%)
  Scalping           → BUY             (confidence: 50.0%) 

📈 CONSENSUS:
  🟢 Buy:  2/2 strategies
  🔴 Sell: 0/2 strategies
  ⚪ Hold: 0/2 strategies

💡 FINAL RECOMMENDATION:
  Action:      🟢 BUY
  Confidence:  50.0%
  Agreement:   2/2 strategies
```

### Command Line Testing

You can also test specific symbols directly:

```bash
# Test specific symbol and timeframe
python3 test_strategies_compare.py BTC/USDT 1h
python3 test_strategies_compare.py ETH/USDT 4h
```

## Running the API Server

If you want to run the full API server:

```bash
# Start the server
python3 main.py

# Or with uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Strategy Comparison
```bash
# Compare all strategies for a symbol
GET /strategies/compare-all?symbol=BTC/USDT&timeframe=1h
```
 

### Trading
```bash
# Get account balance
GET /trading/balance

# Create order
POST /trading/orders
```

## Strategy Types

1. **Conservative**: Only trades when multiple indicators agree
2. **Scalping**: Quick trades based on momentum and extremes

## Technical Indicators

- **Momentum**: RSI, Stochastic RSI, Williams %R, CCI, MFI
- **Trend**: MACD, EMA, SMA, Parabolic SAR, Aroon, ADX
- **Volatility**: Bollinger Bands, Keltner Channels, ATR
- **Volume**: MFI (Money Flow Index)
- **Patterns**: Candlestick pattern recognition

## Troubleshooting

### Python Version Issues
If you have Python 3.12 and encounter numpy installation errors:
```bash
# Use Python 3.11 instead
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Binance API Issues
- **No API Keys?** No problem! The system automatically uses mock data when API keys are not configured
- **Want real data?** Ensure you have valid Binance API keys (You can generate at [Binance Testnet](https://testnet.binance.vision/))
- Check API permissions (spot trading enabled)

### Virtual Environment Issues
```bash
# Remove existing venv and recreate
rm -rf venv
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
 
## License

This project is for educational and demonstration purposes.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues and questions, please check the troubleshooting section or create an issue in the repository.
