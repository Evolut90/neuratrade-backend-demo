#!/usr/bin/env python3
"""
Script to test the comparison of all strategies
"""

import requests 
from datetime import datetime
import urllib.parse
from app.services.strategy_service import StrategyService
import asyncio
 
  


def print_separator(char="=", length=80):
    """Print a separator line"""
    print(char * length)


def print_strategy_result(name, result):
    """Print the result of a strategy formatted"""
    signal_emoji = {
        "buy": "BUY",
        "sell": "SELL",
        "hold": "HOLD"
    }
    
    signal = signal_emoji.get(result["signal"], result["signal"])
    confidence = result["confidence"] * 100
    
    print(f"  {name:20} → {signal:15} (confidence: {confidence:5.1f}%)")
    print(f"  {'':20}    {result['description']}")


async def test_compare_strategies(symbol, timeframe="1h"):
    """Test all strategies"""
    print_separator()
    print(f"🔍 ANALYSING: {symbol} ({timeframe})")
    print_separator()
    
    try:
        # Make request using query parameters
        #url = f"{BASE_URL}/strategies/compare-all"
        #params = {"symbol": symbol, "timeframe": timeframe}

        print(f"\n⏳ Searching for data and calculating indicators...")
 
        strategy_service = StrategyService()
        result = await strategy_service.compare_all_strategies(symbol, timeframe)

        print_formatted_result(result)
 
    except requests.exceptions.ConnectionError:
        print("❌ Error: Unable to connect to the server.")
        print("   Ensure the server is running at http://localhost:8000")
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


async def test_multiple_symbols_and_timeframes():
    """Test multiple symbols and timeframes"""
    print("\n" * 2)
    print_separator()
    print("🤖 TEST OF STRATEGIES COMPARISON - NeuraTrade")
    print_separator()
    
    symbols = ["BTC/USDT", "ETH/USDT", "ADA/USDT"]
    timeframes = ["1h", "4h"]
    
    for symbol in symbols:
        for timeframe in timeframes:
            await test_compare_strategies(symbol, timeframe)
            print("\n")


def print_formatted_result(result):
    """Format and display strategy results in an organized way"""
    
    print("\n📊 STRATEGY RESULTS")
    print("=" * 60)
    
    # Basic information
    print(f"💰 Symbol: {result.get('symbol', 'N/A')}")
    print(f"⏰ Timeframe: {result.get('timeframe', 'N/A')}")
    print(f"💵 Current Price: ${result.get('current_price', 0):,.2f}")
    print(f"🕐 Timestamp: {result.get('timestamp', 'N/A')}")
    
    # Consensus
    consensus = result.get('consensus', {})
    print(f"\n🎯 CONSENSUS:")
    print(f"   📈 Buy: {consensus.get('buy', 0)}")
    print(f"   📉 Sell: {consensus.get('sell', 0)}")
    print(f"   ⏸️  Hold: {consensus.get('hold', 0)}")
    
    # Final recommendation
    final_rec = result.get('final_recommendation', {})
    print(f"\n🏆 FINAL RECOMMENDATION:")
    print(f"   Action: {final_rec.get('action', 'N/A').upper()}")
    print(f"   Confidence: {final_rec.get('confidence', 0):.1%}")
    print(f"   Agreement: {final_rec.get('agreement', 'N/A')}")
    
    # Individual strategies
    strategies = result.get('strategies', {})
    print(f"\n📋 INDIVIDUAL STRATEGIES:")
    print("-" * 60)
    
    for name, strategy in strategies.items():
        signal = strategy.get('signal', 'N/A')
        confidence = strategy.get('confidence', 0)
        description = strategy.get('description', 'N/A')
        
        # Emoji based on signal
        emoji = "📈" if signal == "buy" else "📉" if signal == "sell" else "⏸️"
        
        print(f"\n{emoji} {name.upper()}:")
        print(f"   Signal: {signal.upper()}")
        print(f"   Confidence: {confidence:.1%}")
        print(f"   Description: {description}")
        
        # Additional information if available
        if 'score' in strategy:
            print(f"   Score: {strategy['score']}")
        if 'indicators_used' in strategy:
            print(f"   Indicators: {strategy['indicators_used']}")
        if 'external_data' in strategy:
            print(f"   External Data: {', '.join(strategy['external_data'])}")
    
    # Market indicators
    indicators = result.get('market_indicators', {})
    print(f"\n📈 TECHNICAL INDICATORS:")
    print("-" * 60)
    
    # Group indicators by category
    basic_indicators = ['rsi', 'macd', 'macd_signal']
    moving_averages = ['ema_20', 'ema_50', 'sma_200']
    bollinger = ['bb_upper', 'bb_middle', 'bb_lower']
    oscillators = ['stoch_rsi_k', 'stoch_rsi_d', 'williams_r', 'cci', 'mfi']
    trend_indicators = ['adx', 'atr', 'parabolic_sar']
    
    print("\n🔵 Basic Indicators:")
    for indicator in basic_indicators:
        value = indicators.get(indicator)
        if value is not None:
            print(f"   {indicator.upper()}: {value}")
    
    print("\n📊 Moving Averages:")
    for indicator in moving_averages:
        value = indicators.get(indicator)
        if value is not None:
            print(f"   {indicator.upper()}: {value}")
    
    print("\n🎯 Bollinger Bands:")
    for indicator in bollinger:
        value = indicators.get(indicator)
        if value is not None:
            print(f"   {indicator.upper()}: {value}")
    
    print("\n🔄 Oscillators:")
    for indicator in oscillators:
        value = indicators.get(indicator)
        if value is not None:
            print(f"   {indicator.upper()}: {value}")
    
    print("\n📈 Trend Indicators:")
    for indicator in trend_indicators:
        value = indicators.get(indicator)
        if value is not None:
            print(f"   {indicator.upper()}: {value}")
    
    # Candlestick patterns
    patterns = indicators.get('candlestick_patterns')
    if patterns:
        print(f"\n🕯️ CANDLESTICK PATTERNS:")
        print("-" * 60)
        for pattern, value in patterns.items():
            status = "✅" if value else "❌"
            print(f"   {status} {pattern}: {value}")
    
    print("\n" + "=" * 60)
    print("✅ Test completed successfully!")            


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # If symbol passed as argument
        symbol = sys.argv[1]
        timeframe = sys.argv[2] if len(sys.argv) > 2 else "1h"
        asyncio.run(test_compare_strategies(symbol, timeframe))
    else:
        # Interactive test
        print("STRATEGIES TEST - NeuraTrade")
        print("Options:")
        print("1. Test BTC/USDT (1h)")
        print("2. Test ETH/USDT (1h)")
        #print("3. Test all symbols and timeframes")
        #print("4. Customized")
        print()
        
        choice = input("Choose an option (1-2): ").strip()
        
        if choice == "1":
            asyncio.run(test_compare_strategies("BTC/USDT", "1h"))
        elif choice == "2":
            asyncio.run(test_compare_strategies("ETH/USDT", "1h"))
        #elif choice == "3":
        #    asyncio.run(test_multiple_symbols_and_timeframes())
        #elif choice == "4":
        #    symbol = input("Enter the symbol (ex: BTC/USDT): ").strip()
        #    timeframe = input("Enter the timeframe (ex: 1h, 4h, 1d): ").strip() or "1h"
        #    asyncio.run(test_compare_strategies(symbol, timeframe))
        else:
            print("Invalid option!")

