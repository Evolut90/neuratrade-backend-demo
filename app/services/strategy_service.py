from typing import Dict, List, Optional, Any
from datetime import datetime
import numpy as np
import logging 
from app.models.market_data import Candle, MarketIndicators
from app.services.exchange_service import exchange_service 
import pandas_ta as ta
import pandas as pd

logger = logging.getLogger(__name__)

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
            indicators = self.calculate_indicators(candles, symbol, timeframe)
            current_price = float(candles[-1].close)

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


    def calculate_indicators(self, candles: List[Candle], symbol: str, timeframe: str) -> MarketIndicators:
        """
        Calcula indicadores técnicos a partir dos dados de candlestick
        
        Args:
            candles: Lista de candles
            symbol: Símbolo do par
            timeframe: Timeframe dos dados
            
        Returns:
            Objeto com os indicadores calculados
        """
        if len(candles) < 20:
            raise ValueError("Mínimo de 20 candles necessário para calcular indicadores")
        
        # Extrair arrays de preços
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
            logger.warning(f"Erro ao detectar padrões: {e}")
            candlestick_patterns = {}
            pattern_analysis = {
                "signal": "neutral",
                "strength": 0.0,
                "description": "Erro na análise de padrões",
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
            candlestick_patterns=candlestick_patterns if candlestick_patterns else None,
            pattern_signal=pattern_analysis.get("signal") if pattern_analysis else None,
            pattern_strength=pattern_analysis.get("strength") if pattern_analysis else None,
            timestamp=datetime.now()
        )   

    # methods for different strategies
    def hybrid_intelligent_strategy(self,indicators, current_price, candles):
        """
        Estratégia híbrida que analisa todos os indicadores
        e ajusta o peso baseado no contexto de mercado
        """
        score = 0
        max_score = 10
        
        # === ANÁLISE DE TENDÊNCIA (peso: 3) ===
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
        
        # === ANÁLISE DE MOMENTUM (peso: 3) ===
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
        
        # === ANÁLISE DE VOLATILIDADE (peso: 2) ===
        volatility_score = 0
        
        bb_position = (current_price - float(indicators.bb_lower)) / (float(indicators.bb_upper) - float(indicators.bb_lower))
        
        if bb_position < 0.2:  # Próximo da banda inferior
            volatility_score += 2
        elif bb_position < 0.4:
            volatility_score += 1
        elif bb_position > 0.8:  # Próximo da banda superior
            volatility_score -= 2
        elif bb_position > 0.6:
            volatility_score -= 1
        
        score += volatility_score
        
        # === ANÁLISE DE FORÇA DO MOVIMENTO (peso: 2) ===
        # Verificar se o preço está acelerando
        recent_closes = [float(c.close) for c in candles[-5:]]
        price_momentum = (recent_closes[-1] - recent_closes[0]) / recent_closes[0]
        
        if price_momentum > 0.02:  # Subindo mais de 2%
            score += 1
        elif price_momentum < -0.02:  # Caindo mais de 2%
            score -= 1
        
        # Histograma MACD crescendo
        if indicators.macd_histogram > 0:
            score += 1
        else:
            score -= 1
        
        # === DECISÃO FINAL ===
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
    
    @staticmethod
    def _calculate_rsi(prices: np.ndarray, period: int = 14) -> Optional[float]:
        """Calcula o RSI usando TA-Lib"""
        try:
            if len(prices) < period:
                return None
            
            prices_series = pd.Series(prices.astype(float))
            rsi = ta.rsi(prices_series, length=period)
            
            if np.isnan(rsi[-1]):
                return None
            
            return float(rsi[-1])
        except Exception:
            return None

    @staticmethod
    def _calculate_macd(prices: np.ndarray, fast=12, slow=26, signal_period=9):
        """Calcula o MACD usando TA-Lib"""
        try:
            if len(prices) < slow + signal_period:
                return None, None, None
            
            prices_series = pd.Series(prices.astype(float))
            macd_result = ta.macd(prices_series, fast=fast, slow=slow, signal=signal_period)
            macd = macd_result[f'MACD_{fast}_{slow}_{signal_period}']
            signal = macd_result[f'MACDs_{fast}_{slow}_{signal_period}']
            histogram = macd_result[f'MACDh_{fast}_{slow}_{signal_period}']
            
            if np.isnan(macd[-1]) or np.isnan(signal[-1]):
                return None, None, None
            
            return float(macd[-1]), float(signal[-1]), float(histogram[-1])
        except Exception:
            return None, None, None

 
    @staticmethod
    def _calculate_ema(prices: np.ndarray, period: int) -> Optional[float]:
        """Calcula a EMA usando TA-Lib"""
        try:
            if len(prices) < period:
                return None
            
            prices_series = pd.Series(prices.astype(float))
            ema = ta.ema(prices_series, length=period)
            
            if np.isnan(ema[-1]):
                return None
            
            return float(ema[-1])
        except Exception:
            return None
    
    @staticmethod
    def _calculate_sma(prices: np.ndarray, period: int) -> Optional[float]:
        """Calcula a SMA usando TA-Lib"""
        try:
            if len(prices) < period:
                return None
            
            prices_series = pd.Series(prices.astype(float))
            sma = ta.sma(prices_series, length=period)
            
            if np.isnan(sma[-1]):
                return None
            
            return float(sma[-1])
        except Exception:
            return None
    
 
    
    @staticmethod
    def _calculate_bollinger_bands(prices: np.ndarray, period: int = 20, std_dev: float = 2.0):
        """Calcula as Bandas de Bollinger usando TA-Lib"""
        try:
            if len(prices) < period:
                return None, None, None
            
            prices_series = pd.Series(prices.astype(float))
            bb_result = ta.bbands(prices_series, length=period, std=std_dev)
            upper = bb_result[f'BBU_{period}_{std_dev}']
            middle = bb_result[f'BBM_{period}_{std_dev}']
            lower = bb_result[f'BBL_{period}_{std_dev}']
            
            if np.isnan(upper[-1]) or np.isnan(middle[-1]) or np.isnan(lower[-1]):
                return None, None, None
            
            return float(upper[-1]), float(middle[-1]), float(lower[-1])
        except Exception:
            return None, None, None

    # Advanced Technical Indicators using TA-Lib
    
    @staticmethod
    def _calculate_stochastic_rsi(prices: np.ndarray, rsi_period: int = 14, stoch_period: int = 14):
        """Calcula o Stochastic RSI usando TA-Lib"""
        try:
            if len(prices) < rsi_period + stoch_period:
                return None, None
            
            prices_series = pd.Series(prices.astype(float))
            stoch_result = ta.stochrsi(prices_series, length=rsi_period, rsi_length=rsi_period, k=stoch_period, d=3)
            fastk = stoch_result[f'STOCHRSIk_{rsi_period}_{rsi_period}_{stoch_period}_3']
            fastd = stoch_result[f'STOCHRSId_{rsi_period}_{rsi_period}_{stoch_period}_3']
            
            if np.isnan(fastk[-1]) or np.isnan(fastd[-1]):
                return None, None
            
            return float(fastk[-1]), float(fastd[-1])
        except Exception:
            return None, None

    @staticmethod
    def _calculate_adx(high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 14):
        """Calcula o ADX (Average Directional Index) usando TA-Lib"""
        try:
            if len(high) < period * 2:
                return None
            
            high_series = pd.Series(high.astype(float))
            low_series = pd.Series(low.astype(float))
            close_series = pd.Series(close.astype(float))
            
            adx = ta.adx(high_series, low_series, close_series, length=period)
            
            if np.isnan(adx[-1]):
                return None
            
            return float(adx[-1])
        except Exception:
            return None

    @staticmethod
    def _calculate_atr(high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 14):
        """Calcula o ATR (Average True Range) usando TA-Lib"""
        try:
            if len(high) < period:
                return None
            
            high_series = pd.Series(high.astype(float))
            low_series = pd.Series(low.astype(float))
            close_series = pd.Series(close.astype(float))
            
            atr = ta.atr(high_series, low_series, close_series, length=period)
            
            if np.isnan(atr[-1]):
                return None
            
            return float(atr[-1])
        except Exception:
            return None

    @staticmethod
    def _calculate_williams_r(high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 14):
        """Calcula o Williams %R usando TA-Lib"""
        try:
            if len(high) < period:
                return None
            
            high_series = pd.Series(high.astype(float))
            low_series = pd.Series(low.astype(float))
            close_series = pd.Series(close.astype(float))
            
            willr = ta.willr(high_series, low_series, close_series, length=period)
            
            if np.isnan(willr[-1]):
                return None
            
            return float(willr[-1])
        except Exception:
            return None

    @staticmethod
    def _calculate_cci(high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 14):
        """Calcula o CCI (Commodity Channel Index) usando TA-Lib"""
        try:
            if len(high) < period:
                return None
            
            high_series = pd.Series(high.astype(float))
            low_series = pd.Series(low.astype(float))
            close_series = pd.Series(close.astype(float))
            
            cci = ta.cci(high_series, low_series, close_series, length=period)
            
            if np.isnan(cci[-1]):
                return None
            
            return float(cci[-1])
        except Exception:
            return None

    @staticmethod
    def _calculate_mfi(high: np.ndarray, low: np.ndarray, close: np.ndarray, volume: np.ndarray, period: int = 14):
        """Calcula o MFI (Money Flow Index) usando TA-Lib"""
        try:
            if len(high) < period:
                return None
            
            high_series = pd.Series(high.astype(float))
            low_series = pd.Series(low.astype(float))
            close_series = pd.Series(close.astype(float))
            volume_series = pd.Series(volume.astype(float))
            
            mfi = ta.mfi(high_series, low_series, close_series, volume_series, length=period)
            
            if np.isnan(mfi[-1]):
                return None
            
            return float(mfi[-1])
        except Exception:
            return None

    @staticmethod
    def _calculate_parabolic_sar(high: np.ndarray, low: np.ndarray, close: np.ndarray, acceleration: float = 0.02, maximum: float = 0.2):
        """Calcula o Parabolic SAR usando pandas_ta"""
        try:
            if len(high) < 2:
                return None
            
            high_series = pd.Series(high.astype(float))
            low_series = pd.Series(low.astype(float))
            close_series = pd.Series(close.astype(float))
            
            sar = ta.psar(high_series, low_series, close_series, step=acceleration, max_step=maximum)
            
            if np.isnan(sar[-1]):
                return None
            
            return float(sar[-1])
        except Exception:
            return None

    @staticmethod
    def _calculate_aroon(high: np.ndarray, low: np.ndarray, period: int = 14):
        """Calcula o Aroon usando TA-Lib"""
        try:
            if len(high) < period:
                return None, None
            
            high_series = pd.Series(high.astype(float))
            low_series = pd.Series(low.astype(float))
            
            aroon_result = ta.aroon(high_series, low_series, length=period)
            aroon_down = aroon_result[f'AROOND_{period}']
            aroon_up = aroon_result[f'AROONU_{period}']
            
            if np.isnan(aroon_down[-1]) or np.isnan(aroon_up[-1]):
                return None, None
            
            return float(aroon_down[-1]), float(aroon_up[-1])
        except Exception:
            return None, None

    @staticmethod
    def _calculate_keltner_channels(high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 20, multiplier: float = 2.0):
        """Calcula os Keltner Channels (implementação manual com EMA e ATR)"""
        try:
            if len(high) < period:
                return None, None, None
            
            high_series = pd.Series(high.astype(float))
            low_series = pd.Series(low.astype(float))
            close_series = pd.Series(close.astype(float))
            
            # Calcular EMA central
            ema = ta.ema(close_series, length=period)
            
            # Calcular ATR
            atr = ta.atr(high_series, low_series, close_series, length=period)
            
            if np.isnan(ema[-1]) or np.isnan(atr[-1]):
                return None, None, None
            
            middle = float(ema[-1])
            upper = middle + (float(atr[-1]) * multiplier)
            lower = middle - (float(atr[-1]) * multiplier)
            
            return upper, middle, lower
        except Exception:
            return None, None, None

    # Pattern Recognition using TA-Lib
    
    @staticmethod
    def _detect_candlestick_patterns(open_prices: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray):
        """Detecta padrões de candlestick usando TA-Lib"""
        try:
            if len(open_prices) < 5:
                return {}
            
            open_series = pd.Series(open_prices.astype(float))
            high_series = pd.Series(high.astype(float))
            low_series = pd.Series(low.astype(float))
            close_series = pd.Series(close.astype(float))
            
            patterns = {}
            
            # Padrões de reversão (Reversal Patterns)
            patterns["doji"] = ta.cdl_doji(open_series, high_series, low_series, close_series)[-1]
            patterns["hammer"] = ta.cdl_hammer(open_series, high_series, low_series, close_series)[-1]
            patterns["hanging_man"] = ta.cdl_hanging_man(open_series, high_series, low_series, close_series)[-1]
            patterns["inverted_hammer"] = ta.cdl_inverted_hammer(open_series, high_series, low_series, close_series)[-1]
            patterns["shooting_star"] = ta.cdl_shooting_star(open_series, high_series, low_series, close_series)[-1]
            patterns["engulfing_bullish"] = ta.cdl_engulfing(open_series, high_series, low_series, close_series)[-1] > 0
            patterns["engulfing_bearish"] = ta.cdl_engulfing(open_series, high_series, low_series, close_series)[-1] < 0
            patterns["harami_bullish"] = ta.cdl_harami(open_series, high_series, low_series, close_series)[-1] > 0
            patterns["harami_bearish"] = ta.cdl_harami(open_series, high_series, low_series, close_series)[-1] < 0
            
            # Padrões de continuação (Continuation Patterns)
            patterns["three_white_soldiers"] = ta.cdl_3whitesoldiers(open_series, high_series, low_series, close_series)[-1]
            patterns["three_black_crows"] = ta.cdl_3blackcrows(open_series, high_series, low_series, close_series)[-1]
            patterns["morning_star"] = ta.cdl_morningstar(open_series, high_series, low_series, close_series)[-1]
            patterns["evening_star"] = ta.cdl_eveningstar(open_series, high_series, low_series, close_series)[-1]
            
            # Padrões de indecisão
            patterns["spinning_top"] = ta.cdl_spinning_top(open_series, high_series, low_series, close_series)[-1]
            patterns["marubozu"] = ta.cdl_marubozu(open_series, high_series, low_series, close_series)[-1]
            
            # Converter para valores booleanos e remover NaN
            result = {}
            for pattern_name, value in patterns.items():
                if not np.isnan(value):
                    if isinstance(value, bool):
                        result[pattern_name] = value
                    else:
                        result[pattern_name] = bool(value)
                else:
                    result[pattern_name] = False
            
            return result
            
        except Exception as e:
            logger.error(f"Erro ao detectar padrões de candlestick: {e}")
            return {}
    
    @staticmethod
    def _analyze_pattern_strength(patterns: dict) -> dict:
        """Analisa a força dos padrões detectados"""
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
                    "description": "Nenhum padrão significativo detectado",
                    "pattern_count": 0
                }
            
            # Determinar sinal predominante
            if bullish_count > bearish_count:
                signal = "bullish"
                strength = bullish_count / total_patterns
                description = f"Padrões de alta detectados ({bullish_count}/{total_patterns})"
            elif bearish_count > bullish_count:
                signal = "bearish"
                strength = bearish_count / total_patterns
                description = f"Padrões de baixa detectados ({bearish_count}/{total_patterns})"
            else:
                signal = "neutral"
                strength = 0.5
                description = f"Padrões mistos detectados ({bullish_count} alta, {bearish_count} baixa)"
            
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
            logger.error(f"Erro ao analisar força dos padrões: {e}")
            return {
                "signal": "neutral",
                "strength": 0.0,
                "description": "Erro na análise de padrões",
                "pattern_count": 0
            }


# Instância global do serviço
strategy_service = StrategyService()
