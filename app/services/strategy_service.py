"""Service for managing and executing trading strategies"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import numpy as np
import logging
from app.models.strategy import Strategy, StrategyCreate, StrategyUpdate, StrategySignal
from app.models.market_data import Candle, MarketIndicators
from app.services.exchange_service import exchange_service
import talib

logger = logging.getLogger(__name__)

class StrategyService:
    """Service for creating, managing and executing trading strategies"""
    
    def __init__(self):
        self.strategies: Dict[str, Strategy] = {} 
  
    def calculate_indicators(self, candles: List[Candle], symbol: str, timeframe: str) -> MarketIndicators:
        """
        Calculate technical indicators from candlestick data
        
        Args:
            candles: List of candles
            symbol: Trading pair symbol
            timeframe: Data timeframe
            
        Returns:
            Object with calculated indicators
        """
        if len(candles) < 200:
            raise ValueError("Minimum of 20 candles required to calculate indicators")
        
        # Extract price arrays
        closes = np.array([float(c.close) for c in candles])
        highs = np.array([float(c.high) for c in candles])
        lows = np.array([float(c.low) for c in candles])
        opens = np.array([float(c.open) for c in candles])
        volumes = np.array([float(c.volume) for c in candles])
        
        # Basic Indicators
        rsi = self._calculate_rsi(closes, period=14)

        macd, signal, histogram = self._calculate_macd(closes)
        bb_upper, bb_middle, bb_lower = self._calculate_bollinger_bands(closes, period=20)
        ema_20 = self._calculate_ema(closes, period=20)
        ema_50 = self._calculate_ema(closes, period=50) if len(closes) >= 50 else None
        sma_200 = self._calculate_sma(closes, period=200) if len(closes) >= 200 else None
        
        # Advanced Indicators
        stoch_rsi_k, stoch_rsi_d = self._calculate_stochastic_rsi(closes)
        adx = self._calculate_adx(highs, lows, closes)
        atr = self._calculate_atr(highs, lows, closes)
        williams_r = self._calculate_williams_r(highs, lows, closes)
        cci = self._calculate_cci(highs, lows, closes)
        mfi = self._calculate_mfi(highs, lows, closes, volumes)
        parabolic_sar = self._calculate_parabolic_sar(highs, lows, closes)
        aroon_up, aroon_down = self._calculate_aroon(highs, lows)
        kc_upper, kc_middle, kc_lower = self._calculate_keltner_channels(highs, lows, closes)
    
        # Pattern Recognition
        try:
            candlestick_patterns = self._detect_candlestick_patterns(opens, highs, lows, closes)
            pattern_analysis = self._analyze_pattern_strength(candlestick_patterns)
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.warning(f"Error detecting patterns: {e}") 
            candlestick_patterns = {}
            
            pattern_analysis = {
                "signal": "neutral",
                "strength": 0.0,
                "description": "Error in pattern analysis",
                "pattern_count": 0
                }
        
        return MarketIndicators(
            symbol=symbol,
            timeframe=timeframe,
            # Basic Indicators
            rsi=float(rsi) if rsi is not None else None,
            macd=float(macd) if macd is not None else None,
            macd_signal=float(signal) if signal is not None else None,
            macd_histogram=float(histogram) if histogram is not None else None,
            bb_upper=float(bb_upper) if bb_upper is not None else None,
            bb_middle=float(bb_middle) if bb_middle is not None else None,
            bb_lower=float(bb_lower) if bb_lower is not None else None,
            ema_20=float(ema_20) if ema_20 is not None else None,
            ema_50=float(ema_50) if ema_50 is not None else None,
            sma_200=float(sma_200) if sma_200 is not None else None,
            # Advanced Indicators (with precision fix)
            stoch_rsi_k=min(100.0, round(float(stoch_rsi_k), 2)) if stoch_rsi_k is not None else None,
            stoch_rsi_d=min(100.0, round(float(stoch_rsi_d), 2)) if stoch_rsi_d is not None else None,
            adx=min(100.0, round(float(adx), 2)) if adx is not None else None,
            atr=round(float(atr), 2) if atr is not None else None,
            williams_r=max(-100.0, min(0.0, round(float(williams_r), 2))) if williams_r is not None else None,
            cci=round(float(cci), 2) if cci is not None else None,
            mfi=min(100.0, round(float(mfi), 2)) if mfi is not None else None,
            parabolic_sar=round(float(parabolic_sar), 2) if parabolic_sar is not None else None,
            aroon_up=min(100.0, round(float(aroon_up), 2)) if aroon_up is not None else None,
            aroon_down=min(100.0, round(float(aroon_down), 2)) if aroon_down is not None else None,
            kc_upper=float(kc_upper) if kc_upper is not None else None,
            kc_middle=float(kc_middle) if kc_middle is not None else None,
            kc_lower=float(kc_lower) if kc_lower is not None else None,
            # Pattern Recognition
           # candlestick_patterns=candlestick_patterns if candlestick_patterns else None,
           # pattern_signal=pattern_analysis.get("signal") if pattern_analysis else None,
           # pattern_strength=pattern_analysis.get("strength") if pattern_analysis else None,
            timestamp=datetime.now()
        )
     
 

    async def compare_all_strategies(
        self,
        symbol: str,
        timeframe: str = "1h"
    ) -> Dict[str, Any]:
        """
        Executes ALL strategies and returns a complete comparison
        
        Args:
            symbol: Trading pair (ex: BTC/USDT)
            timeframe: Timeframe for analysis (1h, 4h, 1d, etc)
            
        Returns:
            Dictionary with results from all strategies and final recommendation
        """
        # Get market data
        candles = await exchange_service.get_ohlcv(symbol, timeframe, limit=200)
        
        if not candles or len(candles) == 0:
            raise ValueError(f"Unable to get market data for {symbol}")
 
        
        # Calculate indicators
        indicators = self.calculate_indicators(candles, symbol, timeframe)
        current_price = float(candles[-1].close)
  
        # Execute all strategies
        results = {}
 
        
        # 1. Conservative Strategy
        signal, confidence = self.conservative_strategy(indicators, current_price)
        results["conservative"] = {
            "signal": signal,
            "confidence": round(confidence, 3),
            "description": "Multiple indicators must agree"
        }
        
        # 2. Scalping Strategy
        signal, confidence = self.scalping_strategy(indicators, current_price)
        results["scalping"] = {
            "signal": signal,
            "confidence": round(confidence, 3),
            "description": "For quick trades (5m-1h)"
        }
        
        # 3. Trend Following Strategy  
        signal, confidence = self.trend_following_strategy(indicators, current_price)
        results["trend_following"] = {
            "signal": signal,
            "confidence": round(confidence, 3),
            "description": "Follows medium-term trends"
        }        

        # 4. Reversal Strategy  
        signal, confidence = self.reversal_strategy(indicators, current_price)
        results["reversal"] = {
            "signal": signal,
            "confidence": round(confidence, 3),
            "description": "Seeks reversal points"
        }

        # 5. Hybrid Strategy  
        signal, confidence, score = self.hybrid_intelligent_strategy(
            indicators, current_price, candles
        )
        results["hybrid"] = {
            "signal": signal,
            "confidence": round(confidence, 3),
            "score": score,
            "description": "Combines all indicators (weighted)"
        }



        # 6. Advanced Multi-Indicator Strategy 
        # 7. Intelligent Strategy (with external data)
  
        
        # Calculate consensus
        buy_count = sum(1 for r in results.values() if r["signal"] == "buy")
        sell_count = sum(1 for r in results.values() if r["signal"] == "sell")
        hold_count = sum(1 for r in results.values() if r["signal"] == "hold")
        
        # Calculate weighted average confidence
        total_confidence_buy = sum(
            r["confidence"] for r in results.values() if r["signal"] == "buy"
        )
        total_confidence_sell = sum(
            r["confidence"] for r in results.values() if r["signal"] == "sell"
        )
        
        # Determine final recommendation
        if buy_count > sell_count and buy_count > hold_count:
            final_recommendation = "buy"
            final_confidence = total_confidence_buy / buy_count if buy_count > 0 else 0.5
        elif sell_count > buy_count and sell_count > hold_count:
            final_recommendation = "sell"
            final_confidence = total_confidence_sell / sell_count if sell_count > 0 else 0.5
        else:
            final_recommendation = "hold"
            final_confidence = 0.5
        
        # Prepare data for return
        signal_data = {
            "symbol": symbol,
            "timeframe": timeframe,
            "current_price": round(current_price, 2),
            "timestamp": datetime.now().isoformat(),
            "strategies": results,
            "consensus": {
                "buy": buy_count,
                "sell": sell_count,
                "hold": hold_count
            },
            "final_recommendation": {
                "action": final_recommendation,
                "confidence": round(final_confidence, 3),
                "agreement": f"{max(buy_count, sell_count, hold_count)}/{len(results)} strategies"
            },
            "market_indicators": {
                "rsi": round(indicators.rsi, 2) if indicators.rsi else None,
                "macd": round(indicators.macd, 2) if indicators.macd else None,
                "macd_signal": round(indicators.macd_signal, 2) if indicators.macd_signal else None,
                "ema_20": round(indicators.ema_20, 2) if indicators.ema_20 else None,
                "ema_50": round(indicators.ema_50, 2) if indicators.ema_50 else None,
                "sma_200": round(indicators.sma_200, 2) if indicators.sma_200 else None,
                "bb_upper": round(indicators.bb_upper, 2) if indicators.bb_upper else None,
                "bb_middle": round(indicators.bb_middle, 2) if indicators.bb_middle else None,
                "bb_lower": round(indicators.bb_lower, 2) if indicators.bb_lower else None,
                "stoch_rsi_k": round(indicators.stoch_rsi_k, 2) if indicators.stoch_rsi_k else None,
                "stoch_rsi_d": round(indicators.stoch_rsi_d, 2) if indicators.stoch_rsi_d else None,
                "adx": round(indicators.adx, 2) if indicators.adx else None,
                "atr": round(indicators.atr, 2) if indicators.atr else None,
                "williams_r": round(indicators.williams_r, 2) if indicators.williams_r else None,
                "cci": round(indicators.cci, 2) if indicators.cci else None,
                "mfi": round(indicators.mfi, 2) if indicators.mfi else None,
                "parabolic_sar": round(indicators.parabolic_sar, 2) if indicators.parabolic_sar else None,
                "aroon_up": round(indicators.aroon_up, 2) if indicators.aroon_up else None,
                "aroon_down": round(indicators.aroon_down, 2) if indicators.aroon_down else None,
                "kc_upper": round(indicators.kc_upper, 2) if indicators.kc_upper else None,
                "kc_middle": round(indicators.kc_middle, 2) if indicators.kc_middle else None,
                "kc_lower": round(indicators.kc_lower, 2) if indicators.kc_lower else None,
                "candlestick_patterns": indicators.candlestick_patterns if indicators.candlestick_patterns else None,
                "pattern_signal": indicators.pattern_signal if indicators.pattern_signal else None,
                "pattern_strength": indicators.pattern_strength if indicators.pattern_strength else None,
                "timestamp": indicators.timestamp if indicators.timestamp else None
            }
        }
         
        return signal_data

     

    def scalping_strategy(self,indicators, current_price):
        """
        Quick trades based on momentum and extremes
        """
        signal = "hold"
        confidence = 0.5
        
        # Scenario 1: Low RSI + MACD turning + touches lower Bollinger
        if (indicators.rsi < 35 and 
            indicators.macd > indicators.macd_signal and 
            current_price <= float(indicators.bb_lower) * 1.01):
            
            signal = "buy"
            confidence = 0.85
            return signal, confidence
        
        # Scenario 2: High RSI + MACD falling + touches upper Bollinger
        if (indicators.rsi > 65 and 
            indicators.macd < indicators.macd_signal and 
            current_price >= float(indicators.bb_upper) * 0.99):
            
            signal = "sell"
            confidence = 0.85
            return signal, confidence
        
        # Scenario 3: MACD crossing + favorable RSI
        macd_crossover = indicators.macd_histogram > 0  # Positive histogram
        
        if macd_crossover and 30 < indicators.rsi < 50:
            signal = "buy"
            confidence = 0.70
        elif not macd_crossover and 50 < indicators.rsi < 70:
            signal = "sell"
            confidence = 0.70
        
        return signal, confidence


    def conservative_strategy(self,indicators, current_price):
        """
        Only buys/sells when MULTIPLE indicators agree
        """
        buy_signals = 0
        sell_signals = 0
        
        # RSI: Oversold/Overbought
        if indicators.rsi < 30:
            buy_signals += 2  # Strong signal
        elif indicators.rsi < 40:
            buy_signals += 1  # Weak signal
        elif indicators.rsi > 70:
            sell_signals += 2
        elif indicators.rsi > 60:
            sell_signals += 1
        
        # MACD: Momentum
        if indicators.macd > indicators.macd_signal:
            buy_signals += 1  # Positive MACD
        else:
            sell_signals += 1  # Negative MACD
        
        # Bollinger Bands: Price extremes
        if current_price < float(indicators.bb_lower):
            buy_signals += 1  # Price too low
        elif current_price > float(indicators.bb_upper):
            sell_signals += 1  # Price too high
        
        # EMAs: Trend
        if indicators.ema_20 > indicators.ema_50:
            buy_signals += 1  # Uptrend
        else:
            sell_signals += 1  # Downtrend
        
        # SMA 200: Long-term trend
        if current_price > float(indicators.sma_200):
            buy_signals += 1  # Bull market
        else:
            sell_signals += 1  # Bear market
        
        # DECISION: Only acts with 4+ agreeing signals
        if buy_signals >= 4:
            return "buy", min(1.0, buy_signals / 6)
        elif sell_signals >= 4:
            return "sell", min(1.0, sell_signals / 6)
        else:
            return "hold", 0.5

    def reversal_strategy(self,indicators, current_price):
        """
        Seeks trend reversal points
        """
        signal = "hold"
        confidence = 0.5
        
        # REVERSAL UP: Multiple bottom signals
        extreme_oversold = indicators.rsi < 25
        touching_lower_band = current_price <= float(indicators.bb_lower)
        macd_turning_up = (indicators.macd_histogram > 0 and 
                        indicators.macd < 0)  # Negative MACD but rising
        
        if extreme_oversold and touching_lower_band:
            signal = "buy"
            confidence = 0.75
            
            if macd_turning_up:
                confidence = 0.90  # Very likely reversal
        
        # REVERSAL DOWN: Multiple top signals
        extreme_overbought = indicators.rsi > 75
        touching_upper_band = current_price >= float(indicators.bb_upper)
        macd_turning_down = (indicators.macd_histogram < 0 and 
                            indicators.macd > 0)  # Positive MACD but falling
        
        if extreme_overbought and touching_upper_band:
            signal = "sell"
            confidence = 0.75
            
            if macd_turning_down:
                confidence = 0.90
        
        return signal, confidence

    def trend_following_strategy(self,indicators, current_price):
        """
        Buys uptrends, sells downtrends
        """
        signal = "hold"
        confidence = 0.5
        
        # Check moving average alignment (clear trend)
        uptrend = (indicators.ema_20 > indicators.ema_50 > indicators.sma_200)
        downtrend = (indicators.ema_20 < indicators.ema_50 < indicators.sma_200)
        
        # BUY: Uptrend + RSI not overbought
        if uptrend and indicators.rsi < 65:
            signal = "buy"
            
            # Confidence increases if:
            # - MACD positive
            # - Price above all moving averages
            conf_boost = 0
            if indicators.macd > indicators.macd_signal:
                conf_boost += 0.15
            if current_price > float(indicators.ema_20):
                conf_boost += 0.15
            
            confidence = 0.70 + conf_boost
        
        # SELL: Downtrend + RSI not oversold
        elif downtrend and indicators.rsi > 35:
            signal = "sell"
            
            conf_boost = 0
            if indicators.macd < indicators.macd_signal:
                conf_boost += 0.15
            if current_price < float(indicators.ema_20):
                conf_boost += 0.15
            
            confidence = 0.70 + conf_boost
        
        # HOLD: Mixed moving averages (no clear trend)
        else:
            signal = "hold"
            confidence = 0.3  # Low confidence = wait
        
        return signal, confidence           


    # methods for different strategies
    def hybrid_intelligent_strategy(self,indicators, current_price, candles):
        """
        Hybrid strategy that analyzes all indicators
        and adjusts weight based on market context
        """
        score = 0
        max_score = 10
        
        # === TREND ANALYSIS (weight: 3) ===
        trend_score = 0
        
        if indicators.ema_20 > indicators.ema_50:
            trend_score += 1
        else:
            trend_score -= 1
        
        if indicators.ema_50 and indicators.sma_200:
            if indicators.ema_50 > indicators.sma_200:
                trend_score += 1
            else:
                trend_score -= 1
        
        if current_price > float(indicators.sma_200):
            trend_score += 1
        else:
            trend_score -= 1
        
        score += trend_score
        
        # === MOMENTUM ANALYSIS (weight: 3) ===
        momentum_score = 0
        
        # RSI
        if indicators.rsi < 30:
            momentum_score += 2
        elif indicators.rsi < 40:
            momentum_score += 1
        elif indicators.rsi > 70:
            momentum_score -= 2
        elif indicators.rsi > 60:
            momentum_score -= 1
        
        # MACD
        if indicators.macd > indicators.macd_signal:
            momentum_score += 1
        else:
            momentum_score -= 1
        
        score += momentum_score
        
        # === VOLATILITY ANALYSIS (weight: 2) ===
        volatility_score = 0
        
        bb_position = (current_price - float(indicators.bb_lower)) / (float(indicators.bb_upper) - float(indicators.bb_lower))
        
        if bb_position < 0.2:  # Near lower band
            volatility_score += 2
        elif bb_position < 0.4:
            volatility_score += 1
        elif bb_position > 0.8:  # Near upper band
            volatility_score -= 2
        elif bb_position > 0.6:
            volatility_score -= 1
        
        score += volatility_score
        
        # === MOVEMENT STRENGTH ANALYSIS (weight: 2) ===
        # Check if price is accelerating
        recent_closes = [float(c.close) for c in candles[-5:]]
        price_momentum = (recent_closes[-1] - recent_closes[0]) / recent_closes[0]
        
        if price_momentum > 0.02:  # Rising more than 2%
            score += 1
        elif price_momentum < -0.02:  # Falling more than 2%
            score -= 1
        
        # MACD histogram growing
        if indicators.macd_histogram > 0:
            score += 1
        else:
            score -= 1
        
        # === FINAL DECISION ===
        if score >= 5:
            signal = "buy"
            confidence = min(1.0, 0.5 + (score / max_score) * 0.5)
        elif score <= -5:
            signal = "sell"
            confidence = min(1.0, 0.5 + (abs(score) / max_score) * 0.5)
        else:
            signal = "hold"
            confidence = 0.3 + (abs(score) / max_score) * 0.2
        
        return signal, confidence, score


 
    # Auxiliary methods for calculating indicators
    
    
    def _calculate_rsi(self,prices: np.ndarray, period: int = 14) -> Optional[float]:
        """Calculate RSI using TA-Lib"""
        try:
            if len(prices) < period:
                return None
            
            rsi = talib.RSI(prices.astype(float), timeperiod=period)
            
            if np.isnan(rsi[-1]):
                return None
            
            return float(rsi[-1])
        except Exception:
            return None

    
    def _calculate_macd(self,prices: np.ndarray, fast=12, slow=26, signal_period=9):
        """Calculate MACD using TA-Lib"""
        try:
            if len(prices) < slow + signal_period:
                return None, None, None
            
            macd, signal, histogram = talib.MACD(prices.astype(float), fastperiod=fast, slowperiod=slow, signalperiod=signal_period)
            
            if np.isnan(macd[-1]) or np.isnan(signal[-1]):
                return None, None, None
            
            return float(macd[-1]), float(signal[-1]), float(histogram[-1])
        except Exception:
            return None, None, None

 
    
    def _calculate_ema(self,prices: np.ndarray, period: int) -> Optional[float]:
        """Calculate EMA using TA-Lib"""
        try:
            if len(prices) < period:
                return None
            
            ema = talib.EMA(prices.astype(float), timeperiod=period)
            
            if np.isnan(ema[-1]):
                return None
            
            return float(ema[-1])
        except Exception:
            return None
    
    
    def _calculate_sma(self,prices: np.ndarray, period: int) -> Optional[float]:
        """Calculate SMA using TA-Lib"""
        try:
            if len(prices) < period:
                return None
            
            sma = talib.SMA(prices.astype(float), timeperiod=period)
            
            if np.isnan(sma[-1]):
                return None
            
            return float(sma[-1])
        except Exception:
            return None
    
 
    
    
    def _calculate_bollinger_bands(self,prices: np.ndarray, period: int = 20, std_dev: float = 2.0):
        """Calculate Bollinger Bands using TA-Lib"""
        try:
            if len(prices) < period:
                return None, None, None
            
            upper, middle, lower = talib.BBANDS(prices.astype(float), timeperiod=period, nbdevup=std_dev, nbdevdn=std_dev)
            
            if np.isnan(upper[-1]) or np.isnan(middle[-1]) or np.isnan(lower[-1]):
                return None, None, None
            
            return float(upper[-1]), float(middle[-1]), float(lower[-1])
        except Exception:
            return None, None, None

    # Advanced Technical Indicators using TA-Lib
    
    
    def _calculate_stochastic_rsi(self,prices: np.ndarray, rsi_period: int = 14, stoch_period: int = 14):
        """Calculate Stochastic RSI using TA-Lib"""
        try:
            if len(prices) < rsi_period + stoch_period:
                return None, None
            
            fastk, fastd = talib.STOCHRSI(prices.astype(float), timeperiod=rsi_period, fastk_period=stoch_period, fastd_period=3)
            
            if np.isnan(fastk[-1]) or np.isnan(fastd[-1]):
                return None, None
            
            return float(fastk[-1]), float(fastd[-1])
        except Exception:
            return None, None

    
    def _calculate_adx(self,high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 14):
        """Calculate ADX (Average Directional Index) using TA-Lib"""
        try:
            if len(high) < period * 2:
                return None
            
            adx = talib.ADX(high.astype(float), low.astype(float), close.astype(float), timeperiod=period)
            
            if np.isnan(adx[-1]):
                return None
            
            return float(adx[-1])
        except Exception:
            return None

    
    def _calculate_atr(self, high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 14):
        """Calculate ATR (Average True Range) using TA-Lib"""
        try:
            if len(high) < period:
                return None
            
            atr = talib.ATR(high.astype(float), low.astype(float), close.astype(float), timeperiod=period)
            
            if np.isnan(atr[-1]):
                return None
            
            return float(atr[-1])
        except Exception:
            return None

    
    def _calculate_williams_r(self,high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 14):
        """Calculate Williams %R using TA-Lib"""
        try:
            if len(high) < period:
                return None
            
            willr = talib.WILLR(high.astype(float), low.astype(float), close.astype(float), timeperiod=period)
            
            if np.isnan(willr[-1]):
                return None
            
            return float(willr[-1])
        except Exception:
            return None

    
    def _calculate_cci(self,high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 14):
        """Calculate CCI (Commodity Channel Index) using TA-Lib"""
        try:
            if len(high) < period:
                return None
            
            cci = talib.CCI(high.astype(float), low.astype(float), close.astype(float), timeperiod=period)
            
            if np.isnan(cci[-1]):
                return None
            
            return float(cci[-1])
        except Exception:
            return None

    
    def _calculate_mfi(self,high: np.ndarray, low: np.ndarray, close: np.ndarray, volume: np.ndarray, period: int = 14):
        """Calculate MFI (Money Flow Index) using TA-Lib"""
        try:
            if len(high) < period:
                return None
            
            mfi = talib.MFI(high.astype(float), low.astype(float), close.astype(float), volume.astype(float), timeperiod=period)
            
            if np.isnan(mfi[-1]):
                return None
            
            return float(mfi[-1])
        except Exception:
            return None

    
    def _calculate_parabolic_sar(self,high: np.ndarray, low: np.ndarray, close: np.ndarray, acceleration: float = 0.02, maximum: float = 0.2):
        """Calculate Parabolic SAR using TA-Lib"""
        try:
            if len(high) < 2:
                return None
            
            sar = talib.SAR(high.astype(float), low.astype(float), acceleration=acceleration, maximum=maximum)
            
            if np.isnan(sar[-1]):
                return None
            
            return float(sar[-1])
        except Exception:
            return None

    
    def _calculate_aroon(self,high: np.ndarray, low: np.ndarray, period: int = 14):
        """Calculate Aroon using TA-Lib"""
        try:
            if len(high) < period:
                return None, None
            
            aroon_down, aroon_up = talib.AROON(high.astype(float), low.astype(float), timeperiod=period)
            
            if np.isnan(aroon_down[-1]) or np.isnan(aroon_up[-1]):
                return None, None
            
            return float(aroon_down[-1]), float(aroon_up[-1])
        except Exception:
            return None, None

    
    def _calculate_keltner_channels(self,high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 20, multiplier: float = 2.0):
        """Calculate Keltner Channels (manual implementation with EMA and ATR)"""
        try:
            if len(high) < period:
                return None, None, None
            
            # Calculate central EMA
            ema = talib.EMA(close.astype(float), timeperiod=period)
            
            # Calculate ATR
            atr = talib.ATR(high.astype(float), low.astype(float), close.astype(float), timeperiod=period)
            
            if np.isnan(ema[-1]) or np.isnan(atr[-1]):
                return None, None, None
            
            middle = float(ema[-1])
            upper = middle + (float(atr[-1]) * multiplier)
            lower = middle - (float(atr[-1]) * multiplier)
            
            return upper, middle, lower
        except Exception:
            return None, None, None

    # Pattern Recognition using TA-Lib
    
    
    def _detect_candlestick_patterns(self,open_prices: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray):
        """Detect candlestick patterns using TA-Lib"""
        try:
            if len(open_prices) < 5:
                return {}
            
            # Convert to float arrays
 
            
            patterns = {}
            
            # Reversal patterns - using TA-Lib
            try:
                doji_result = talib.CDLDOJI(open_prices.astype(float), high.astype(float), low.astype(float), close.astype(float))
                patterns["doji"] = doji_result[-1] if doji_result is not None and len(doji_result) > 0 else 0
            except:
                patterns["doji"] = 0
            
            try:
                inside_result = talib.CDLINSIDE(open_prices.astype(float), high.astype(float), low.astype(float), close.astype(float))
                patterns["inside"] = inside_result[-1] if inside_result is not None and len(inside_result) > 0 else 0
            except:
                patterns["inside"] = 0
            
            try:
                z_result = talib.CDLZ(open_prices.astype(float), high.astype(float), low.astype(float), close.astype(float))
                patterns["z"] = z_result[-1] if z_result is not None and len(z_result) > 0 else 0
            except:
                patterns["z"] = 0
            
            # Patterns that don't exist in TA-Lib - set as False
            patterns["hanging_man"] = False
            patterns["inverted_hammer"] = False
            patterns["shooting_star"] = False
            patterns["engulfing_bullish"] = False
            patterns["engulfing_bearish"] = False
            patterns["harami_bullish"] = False
            patterns["harami_bearish"] = False
            patterns["three_white_soldiers"] = False
            patterns["three_black_crows"] = False
            patterns["morning_star"] = False
            patterns["evening_star"] = False
            patterns["spinning_top"] = False
            patterns["marubozu"] = False
            patterns["hammer"] = False
            
            # Convert to boolean values and remove NaN
            result = {}
            for pattern_name, value in patterns.items():
                try:
                    # Check if it's NaN
                    if np.isnan(value):
                        result[pattern_name] = False
                    else:
                        # Convert to boolean
                        result[pattern_name] = bool(value)
                except Exception as e:
                    print(f"Error processing pattern {pattern_name}: {e}")
                    result[pattern_name] = False
            
            return result
            
        except Exception as e:
            print(f"Error detecting candlestick patterns: {e}")
            import traceback
            traceback.print_exc()
            return {}
    
    
    def _analyze_pattern_strength(self,patterns: dict) -> dict:
        """Analyze the strength of detected patterns"""
        try:
            bullish_patterns = [
                "hammer", "inverted_hammer", "engulfing_bullish", 
                "harami_bullish", "three_white_soldiers", "morning_star"
            ]
            
            bearish_patterns = [
                "hanging_man", "shooting_star", "engulfing_bearish", 
                "harami_bearish", "three_black_crows", "evening_star"
            ]
            
            neutral_patterns = ["doji", "spinning_top"]
            
            bullish_count = sum(1 for pattern in bullish_patterns if patterns.get(pattern, False))
            bearish_count = sum(1 for pattern in bearish_patterns if patterns.get(pattern, False))
            neutral_count = sum(1 for pattern in neutral_patterns if patterns.get(pattern, False))
            
            total_patterns = bullish_count + bearish_count + neutral_count
            
            if total_patterns == 0:
                return {
                    "signal": "neutral",
                    "strength": 0.0,
                    "description": "No significant patterns detected",
                    "pattern_count": 0
                }
            
            # Determine predominant signal
            if bullish_count > bearish_count:
                signal = "bullish"
                strength = bullish_count / total_patterns
                description = f"Bullish patterns detected ({bullish_count}/{total_patterns})"
            elif bearish_count > bullish_count:
                signal = "bearish"
                strength = bearish_count / total_patterns
                description = f"Bearish patterns detected ({bearish_count}/{total_patterns})"
            else:
                signal = "neutral"
                strength = 0.5
                description = f"Mixed patterns detected ({bullish_count} bullish, {bearish_count} bearish)"
            
            return {
                "signal": signal,
                "strength": round(strength, 3),
                "description": description,
                "pattern_count": total_patterns,
                "bullish_patterns": bullish_count,
                "bearish_patterns": bearish_count,
                "neutral_patterns": neutral_count
            }
            
        except Exception as e:
            logger.error(f"Error analyzing pattern strength: {e}")
            return {
                "signal": "neutral",
                "strength": 0.0,
                "description": "Error in pattern analysis",
                "pattern_count": 0
            }


# Global service instance
strategy_service = StrategyService()

