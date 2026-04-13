"""
Trading strategy module.
Implements technical analysis and trading logic.
"""

from enum import Enum
from typing import Dict, Optional
from dataclasses import dataclass
import pandas as pd
import ta
from logger_config import app_logger
from config import settings


class Signal(str, Enum):
    """Trading signal types."""
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


@dataclass
class AnalysisResult:
    """Result of stock analysis."""
    symbol: str
    signal: Signal
    rsi: Optional[float]
    macd: Optional[float]
    macd_signal: Optional[float]
    ema_50: Optional[float]
    current_price: Optional[float]
    reason: str


class TradingStrategy:
    """Implements swing trading strategy with technical indicators."""

    @staticmethod
    def calculate_indicators(data: pd.DataFrame) -> Dict[str, pd.Series]:
        """
        Calculate technical indicators.
        
        Args:
            data: DataFrame with OHLCV data
            
        Returns:
            Dictionary with calculated indicators
        """
        try:
            indicators = {}

            # RSI
            indicators["rsi"] = ta.momentum.rsi(data["Close"], length=settings.rsi_period)

            # MACD
            macd = ta.trend.macd(data["Close"])
            indicators["macd"] = macd.iloc[:, 0]  # MACD line
            indicators["macd_signal"] = macd.iloc[:, 1]  # Signal line
            indicators["macd_hist"] = macd.iloc[:, 2]  # Histogram

            # 50 EMA
            indicators["ema_50"] = ta.trend.ema_indicator(data["Close"], window=settings.ema_period)

            return indicators

        except Exception as e:
            app_logger.error(f"Error calculating indicators: {str(e)}")
            return {}

    @staticmethod
    def analyze_stock(data: pd.DataFrame, symbol: str, current_price: float) -> AnalysisResult:
        """
        Analyze stock and generate trading signal.
        
        Args:
            data: Historical OHLCV data
            symbol: Stock symbol
            current_price: Current price
            
        Returns:
            AnalysisResult with signal and reasoning
        """
        try:
            if data.empty or len(data) < settings.rsi_period:
                app_logger.warning(f"Insufficient data for {symbol}")
                return AnalysisResult(
                    symbol=symbol,
                    signal=Signal.HOLD,
                    rsi=None,
                    macd=None,
                    macd_signal=None,
                    ema_50=None,
                    current_price=current_price,
                    reason="Insufficient data"
                )

            # Calculate indicators
            indicators = TradingStrategy.calculate_indicators(data)

            if not indicators:
                return AnalysisResult(
                    symbol=symbol,
                    signal=Signal.HOLD,
                    rsi=None,
                    macd=None,
                    macd_signal=None,
                    ema_50=None,
                    current_price=current_price,
                    reason="Failed to calculate indicators"
                )

            # Get latest values
            rsi = indicators["rsi"].iloc[-1]
            macd = indicators["macd"].iloc[-1]
            macd_signal = indicators["macd_signal"].iloc[-1]
            ema_50 = indicators["ema_50"].iloc[-1]

            # Check for bullish MACD crossover (within last 2 candles)
            macd_bullish = False
            if len(indicators["macd"]) >= 2:
                prev_macd = indicators["macd"].iloc[-2]
                prev_signal = indicators["macd_signal"].iloc[-2]
                # Bullish crossover: MACD crosses above signal line
                macd_bullish = (prev_macd <= prev_signal) and (macd > macd_signal)

            # Check for bearish MACD crossover (within last 2 candles)
            macd_bearish = False
            if len(indicators["macd"]) >= 2:
                prev_macd = indicators["macd"].iloc[-2]
                prev_signal = indicators["macd_signal"].iloc[-2]
                # Bearish crossover: MACD crosses below signal line
                macd_bearish = (prev_macd >= prev_signal) and (macd < macd_signal)

            # Trading logic
            signal = Signal.HOLD
            reason = "No conditions met"

            # BUY conditions
            if (rsi < settings.rsi_buy_threshold and
                current_price > ema_50 and
                macd_bullish):
                signal = Signal.BUY
                reason = (
                    f"RSI ({rsi:.2f}) < {settings.rsi_buy_threshold}, "
                    f"Price ({current_price:.2f}) > EMA50 ({ema_50:.2f}), "
                    f"Bullish MACD crossover"
                )

            # SELL conditions
            elif (rsi > settings.rsi_sell_threshold and macd_bearish):
                signal = Signal.SELL
                reason = (
                    f"RSI ({rsi:.2f}) > {settings.rsi_sell_threshold}, "
                    f"Bearish MACD crossover"
                )

            app_logger.info(
                f"Analysis for {symbol}: Signal={signal}, RSI={rsi:.2f}, "
                f"MACD={macd:.4f}, EMA50={ema_50:.2f}, Price={current_price:.2f}"
            )

            return AnalysisResult(
                symbol=symbol,
                signal=signal,
                rsi=float(rsi),
                macd=float(macd),
                macd_signal=float(macd_signal),
                ema_50=float(ema_50),
                current_price=current_price,
                reason=reason
            )

        except Exception as e:
            app_logger.error(f"Error analyzing {symbol}: {str(e)}")
            return AnalysisResult(
                symbol=symbol,
                signal=Signal.HOLD,
                rsi=None,
                macd=None,
                macd_signal=None,
                ema_50=None,
                current_price=current_price,
                reason=f"Analysis error: {str(e)}"
            )
