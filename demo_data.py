"""
Demo data generation for testing and development.
Generates realistic mock stock data when API is unavailable.
"""

from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from logger_config import app_logger


class DemoDataGenerator:
    """Generates realistic demo stock data."""
    
    @staticmethod
    def generate_stock_data(
        symbol: str = "DEMO",
        days: int = 180,
        starting_price: float = 100.0,
        volatility: float = 0.02
    ) -> pd.DataFrame:
        """
        Generate realistic mock stock data.
        
        Args:
            symbol: Stock symbol
            days: Number of days to generate
            starting_price: Initial price
            volatility: Daily volatility (std dev)
            
        Returns:
            DataFrame with OHLCV data
        """
        try:
            dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
            
            # Generate realistic price movements with trend and volatility
            returns = np.random.normal(0.0005, volatility, days)  # Daily return distribution
            close_prices = starting_price * np.exp(np.cumsum(returns))
            
            # Generate OHLC from close prices
            data = []
            for i, (date, close) in enumerate(zip(dates, close_prices)):
                # Realistic intraday movement
                open_price = close_prices[i-1] if i > 0 else starting_price
                high_price = max(open_price, close) * (1 + abs(np.random.normal(0.002, 0.001)))
                low_price = min(open_price, close) * (1 - abs(np.random.normal(0.002, 0.001)))
                volume = np.random.randint(1000000, 10000000)
                
                data.append({
                    "Date": date,
                    "Open": open_price,
                    "High": high_price,
                    "Low": low_price,
                    "Close": close,
                    "Adj Close": close,
                    "Volume": volume
                })
            
            df = pd.DataFrame(data)
            df.set_index("Date", inplace=True)
            
            app_logger.info(f"Generated demo data for {symbol}: {days} days, price range ${df['Close'].min():.2f}-${df['Close'].max():.2f}")
            
            return df
            
        except Exception as e:
            app_logger.error(f"Error generating demo data: {str(e)}")
            return None
    
    @staticmethod
    def get_realistic_data() -> dict:
        """
        Get pre-configured realistic demo datasets.
        
        Returns:
            Dictionary with symbol -> DataFrame mapping
        """
        demo_configs = {
            "RELIANCE.NS": {"starting_price": 2800, "volatility": 0.018},
            "TCS.NS": {"starting_price": 3500, "volatility": 0.015},
            "INFY.NS": {"starting_price": 1800, "volatility": 0.020},
            "AAPL": {"starting_price": 180, "volatility": 0.016},
            "GOOGL": {"starting_price": 140, "volatility": 0.018},
            "MSFT": {"starting_price": 380, "volatility": 0.014},
        }
        
        data = {}
        for symbol, config in demo_configs.items():
            data[symbol] = DemoDataGenerator.generate_stock_data(
                symbol=symbol,
                days=180,
                starting_price=config["starting_price"],
                volatility=config["volatility"]
            )
        
        return data
