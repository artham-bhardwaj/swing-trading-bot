"""
Market hours management.
Handles market opening/closing times and scheduling for different exchanges.
"""

from datetime import datetime
from typing import Tuple
import pytz
from logger_config import app_logger


class MarketHours:
    """Manages market hours for different exchanges."""
    
    # Market timings (IST/UTC)
    MARKET_OPEN = (9, 15)  # 9:15 AM IST
    MARKET_CLOSE = (15, 30)  # 3:30 PM IST
    PRE_CLOSE = (15, 0)  # Pre-close alert at 3:00 PM
    
    # Timezones
    IST = pytz.timezone('Asia/Kolkata')
    
    @staticmethod
    def is_market_open() -> bool:
        """
        Check if market is currently open.
        
        Returns:
            True if market is open, False otherwise
        """
        now = datetime.now(MarketHours.IST)
        
        # Market closed on weekends
        if now.weekday() >= 5:  # Saturday=5, Sunday=6
            return False
        
        # Market open time: 9:15 AM to 3:30 PM IST
        market_open_time = now.replace(hour=9, minute=15, second=0, microsecond=0)
        market_close_time = now.replace(hour=15, minute=30, second=0, microsecond=0)
        
        return market_open_time <= now <= market_close_time
    
    @staticmethod
    def get_market_status() -> dict:
        """
        Get current market status.
        
        Returns:
            Dictionary with market info
        """
        now = datetime.now(MarketHours.IST)
        is_open = MarketHours.is_market_open()
        
        # Next open/close time
        if now.weekday() >= 5:  # Weekend
            # Next Monday 9:15 AM
            days_until_monday = (7 - now.weekday()) % 7
            if days_until_monday == 0:
                days_until_monday = 0
            next_open = now.replace(hour=9, minute=15, second=0, microsecond=0)
            if now.weekday() < 5:
                next_open = next_open + __import__('datetime').timedelta(days=days_until_monday)
        elif now.hour < 9 or (now.hour == 9 and now.minute < 15):
            next_open = now.replace(hour=9, minute=15, second=0, microsecond=0)
        else:
            next_open = now.replace(hour=9, minute=15, second=0, microsecond=0) + __import__('datetime').timedelta(days=1)
        
        if is_open:
            close_time = now.replace(hour=15, minute=30, second=0, microsecond=0)
            time_until_close = (close_time - now).total_seconds() / 60
        else:
            close_time = None
            time_until_close = None
        
        return {
            "is_market_open": is_open,
            "current_time_ist": now.strftime("%Y-%m-%d %H:%M:%S IST"),
            "market_open_time": "09:15 AM IST",
            "market_close_time": "03:30 PM IST",
            "next_open": next_open.strftime("%Y-%m-%d %H:%M:%S IST"),
            "minutes_until_close": round(time_until_close) if time_until_close else None
        }
    
    @staticmethod
    def is_opening_time() -> bool:
        """Check if it's market opening time (9:15 AM ± 5 minutes)."""
        now = datetime.now(MarketHours.IST)
        
        if now.weekday() >= 5:
            return False
        
        # Check if between 9:10 AM and 9:20 AM
        return (now.hour == 9 and 10 <= now.minute <= 20) or \
               (now.hour == 9 and now.minute == 15)
    
    @staticmethod
    def is_closing_time() -> bool:
        """Check if it's market closing time (3:30 PM ± 5 minutes)."""
        now = datetime.now(MarketHours.IST)
        
        if now.weekday() >= 5:
            return False
        
        # Check if between 3:25 PM and 3:35 PM
        return (now.hour == 15 and 25 <= now.minute <= 35) or \
               (now.hour == 15 and now.minute == 30)
    
    @staticmethod
    def get_next_market_event() -> Tuple[str, datetime]:
        """
        Get next market event (open or close).
        
        Returns:
            Tuple of (event_type, datetime)
        """
        now = datetime.now(MarketHours.IST)
        
        if now.weekday() >= 5:  # Weekend
            next_open = now.replace(hour=9, minute=15, second=0, microsecond=0)
            days_until_monday = (7 - now.weekday()) % 7
            if days_until_monday == 0:
                days_until_monday = 7
            next_open = next_open + __import__('datetime').timedelta(days=days_until_monday)
            return "market_open", next_open
        
        market_open = now.replace(hour=9, minute=15, second=0, microsecond=0)
        market_close = now.replace(hour=15, minute=30, second=0, microsecond=0)
        
        if now < market_open:
            return "market_open", market_open
        elif now < market_close:
            return "market_close", market_close
        else:
            # Next day opening
            market_open = market_open + __import__('datetime').timedelta(days=1)
            return "market_open", market_open
