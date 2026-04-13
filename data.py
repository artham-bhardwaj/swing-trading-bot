"""
Stock data fetching module.
Handles downloading historical stock data using yfinance.
Falls back to demo data when API is unavailable.
"""

from datetime import datetime, timedelta
from typing import Optional
import pandas as pd
import yfinance as yf
from logger_config import app_logger
from config import settings


# Flag to control demo mode
USE_DEMO_DATA = False  # Set to True to always use demo data


class StockDataFetcher:
    """Fetches historical stock data from Yahoo Finance."""

    @staticmethod
    def fetch_stock_data(
        symbol: str,
        days: Optional[int] = None
    ) -> Optional[pd.DataFrame]:
        """
        Fetch historical stock data.
        
        Args:
            symbol: Stock symbol (e.g., 'RELIANCE.NS')
            days: Number of days of historical data (default: 180 days)
            
        Returns:
            DataFrame with OHLCV data, or None if fetch fails
        """
        if days is None:
            days = settings.stock_history_days

        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            app_logger.info(f"Fetching data for {symbol} from {start_date.date()} to {end_date.date()}")
            
            data = yf.download(
                symbol,
                start=start_date,
                end=end_date,
                progress=False,
                interval="1d"
            )

            if data.empty:
                app_logger.warning(f"No data retrieved for symbol: {symbol}, trying demo data...")
                return StockDataFetcher._get_demo_data(symbol, days)

            # Ensure we have the required columns
            required_cols = ["Open", "High", "Low", "Close", "Volume"]
            if not all(col in data.columns for col in required_cols):
                app_logger.error(f"Missing required columns for {symbol}")
                return StockDataFetcher._get_demo_data(symbol, days)

            app_logger.info(f"Successfully fetched {len(data)} records for {symbol}")
            return data

        except Exception as e:
            app_logger.warning(f"Error fetching data for {symbol}: {str(e)}, using demo data...")
            return StockDataFetcher._get_demo_data(symbol, days)

    @staticmethod
    def _get_demo_data(symbol: str, days: int) -> Optional[pd.DataFrame]:
        """
        Get demo data as fallback when API fails.
        
        Args:
            symbol: Stock symbol
            days: Number of days
            
        Returns:
            Generated demo DataFrame
        """
        try:
            from demo_data import DemoDataGenerator
            app_logger.info(f"Generating demo data for {symbol}")
            return DemoDataGenerator.generate_stock_data(symbol, days=days)
        except Exception as e:
            app_logger.error(f"Failed to generate demo data: {str(e)}")
            return None

    @staticmethod
    def get_latest_price(symbol: str) -> Optional[float]:
        """
        Get the latest closing price for a symbol.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Latest closing price, or None if fetch fails
        """
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d")
            
            if data.empty:
                app_logger.warning(f"No price data for {symbol}")
                return None
                
            return float(data["Close"].iloc[-1])
            
        except Exception as e:
            app_logger.error(f"Error fetching price for {symbol}: {str(e)}")
            return None
