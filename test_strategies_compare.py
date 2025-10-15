#!/usr/bin/env python3
"""
Script to test the comparison of all strategies
"""

import requests 
from datetime import datetime
import urllib.parse

# Settings
BASE_URL = "http://127.0.0.1:8000"
SYMBOLS = ["BTC/USDT", "ETH/USDT"]
TIMEFRAMES = ["15m", "1h", "4h"]
  


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


def test_compare_strategies(symbol, timeframe="1h"):
    """Test all strategies"""
    print_separator()
    print(f"🔍 ANALYSING: {symbol} ({timeframe})")
    print_separator()
    
    try:
        # Make request using query parameters
        url = f"{BASE_URL}/strategies/compare-all"
        params = {"symbol": symbol, "timeframe": timeframe}
        
        print(f"\n⏳ Searching for data and calculating indicators...")
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get("success"):
            print("Error in API response")
            return
        
        result = data["data"]
        
        # Mostrar informações básicas
        print(f"\n💰 Current Price: ${result['current_price']:,.2f}")
        print(f"⏰ Timestamp: {result['timestamp']}")
        
        # Mostrar indicadores técnicos
        print(f"\n📊 TECHNICAL INDICATORS:")
        indicators = result["market_indicators"]
        
        # Basic Indicators
        print(f"  📈 MOMENTUM:")
        print(f"    RSI:        {indicators['rsi']:.2f} {'(Sobrevendido)' if indicators['rsi'] < 30 else '(Sobrecomprado)' if indicators['rsi'] > 70 else '(Neutro)'}")
        if indicators.get('stoch_rsi_k'):
            print(f"    Stoch RSI:  {indicators['stoch_rsi_k']:.2f} / {indicators['stoch_rsi_d']:.2f}")
        if indicators.get('williams_r'):
            print(f"    Williams %R: {indicators['williams_r']:.2f}")
        
        print(f"  📊 TREND:")
        print(f"    MACD:       {indicators['macd']:.2f}")
        print(f"    MACD Sinal: {indicators['macd_signal']:.2f}")
        if indicators.get('adx'):
            print(f"    ADX:        {indicators['adx']:.2f}")
        if indicators.get('parabolic_sar'):
            print(f"    Parabolic SAR: ${indicators['parabolic_sar']:,.2f}")
        
        print(f"  📉 MOVING AVERAGES:")
        print(f"    EMA 20:     ${indicators['ema_20']:,.2f}")
        print(f"    EMA 50:     ${indicators['ema_50']:,.2f}")
        print(f"    SMA 200:    ${indicators['sma_200']:,.2f}")
        
        print(f"  📏 VOLATILITY:")
        print(f"    Bollinger:")
        print(f"      Upper: ${indicators['bb_upper']:,.2f}")
        print(f"      Middle:    ${indicators['bb_middle']:,.2f}")
        print(f"      Lower: ${indicators['bb_lower']:,.2f}")
        if indicators.get('kc_upper'):
            print(f"    Keltner:")
            print(f"      Upper: ${indicators['kc_upper']:,.2f}")
            print(f"      Middle:    ${indicators['kc_middle']:,.2f}")
            print(f"      Lower: ${indicators['kc_lower']:,.2f}")
        
        print(f"  💰 VOLUME & FORCE:")
        if indicators.get('mfi'):
            print(f"    MFI:        {indicators['mfi']:.2f}")
        if indicators.get('cci'):
            print(f"    CCI:        {indicators['cci']:.2f}")
        if indicators.get('atr'):
            print(f"    ATR:        {indicators['atr']:.2f}")
        
        print(f"  🎯 DIRECTIONAL:")
        if indicators.get('aroon_up') and indicators.get('aroon_down'):
            print(f"    Aroon:      Up {indicators['aroon_up']:.2f} / Down {indicators['aroon_down']:.2f}")
        
        # Mostrar resultado de cada estratégia
        print(f"\n🎯 RESULT OF STRATEGIES:")
        print()
        
        strategies = result["strategies"]
        print_strategy_result("Conservative", strategies["conservative"])
        print()
        print_strategy_result("Scalping", strategies["scalping"])
        print()
        print_strategy_result("Trend Following", strategies["trend_following"])
        print()
        print_strategy_result("Reversal", strategies["reversal"])
        print()
        print_strategy_result("Hybrid", strategies["hybrid"])
        if "score" in strategies["hybrid"]:
            print(f"  {'':20}    Score: {strategies['hybrid']['score']}/10")
        print()
        
        print_strategy_result("Advanced", strategies["advanced"])
        if "indicators_used" in strategies["advanced"]:
            print(f"  {'':20}    Indicators: {strategies['advanced']['indicators_used']}")
        print()
        
        print_strategy_result("Intelligent", strategies["intelligent"])
        if "external_data" in strategies["intelligent"]:
            print(f"  {'':20}    External Data: {', '.join(strategies['intelligent']['external_data'])}")
        if "analysis_sources" in strategies["intelligent"]:
            print(f"  {'':20}    Analysis: {', '.join(strategies['intelligent']['analysis_sources'])}")
        
        # Show consensus
        print(f"\n📈 CONSENSUS:")
        consensus = result["consensus"]
        print(f"  🟢 Buy:  {consensus['buy']}/7 strategies")
        print(f"  🔴 Sell:   {consensus['sell']}/7 strategies")
        print(f"  ⚪ Hold: {consensus['hold']}/7 strategies")
        
        # Mostrar recomendação final
        print(f"\n💡 FINAL RECOMMENDATION:")
        final = result["final_recommendation"]
        action_text = {
            "buy": "🟢 BUY",
            "sell": "🔴 SELL",
            "hold": "⚪ HOLD"
        }
        
        print(f"  Action:      {action_text.get(final['action'], final['action'])}")
        print(f"  Confidence: {final['confidence'] * 100:.1f}%")
        print(f"  Agreement:    {final['agreement']}")
        
        print_separator()
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Unable to connect to the server.")
        print("   Ensure the server is running at http://localhost:8000")
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def test_multiple_symbols_and_timeframes():
    """Test multiple symbols and timeframes"""
    print("\n" * 2)
    print_separator()
    print("🤖 TEST OF STRATEGIES COMPARISON - NeuraTrade")
    print_separator()
    
    for symbol in SYMBOLS:
        for timeframe in TIMEFRAMES:
            test_compare_strategies(symbol, timeframe)
            print("\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Se passou símbolo como argumento
        symbol = sys.argv[1]
        timeframe = sys.argv[2] if len(sys.argv) > 2 else "1h"
        test_compare_strategies(symbol, timeframe)
    else:
        # Teste interativo
        print("STRATEGIES TEST - NeuraTrade")
        print("Options:")
        print("1. Test BTC/USDT (1h)")
        print("2. Test ETH/USDT (1h)")
        print("3. Test all symbols and timeframes")
        print("4. Customized")
        print()
        
        choice = input("Choose an option (1-4): ").strip()
        
        if choice == "1":
            test_compare_strategies("BTC/USDT", "1h")
        elif choice == "2":
            test_compare_strategies("ETH/USDT", "1h")
        elif choice == "3":
            test_multiple_symbols_and_timeframes()
        elif choice == "4":
            symbol = input("Enter the symbol (ex: BTC/USDT): ").strip()
            timeframe = input("Enter the timeframe (ex: 1h, 4h, 1d): ").strip() or "1h"
            test_compare_strategies(symbol, timeframe)
        else:
            print("Invalid option!")

