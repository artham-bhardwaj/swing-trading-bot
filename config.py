"""
Configuration module for the swing trading assistant.
Loads settings from environment variables with defaults.
"""

import os
from typing import Optional, List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # FastAPI settings
    app_title: str = "Swing Trading Assistant"
    app_version: str = "1.0.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 10000

    # Telegram settings
    telegram_token: str = os.getenv("TELEGRAM_TOKEN", "")
    telegram_chat_id: str = os.getenv("TELEGRAM_CHAT_ID", "")

    # Stock analysis settings
    rsi_period: int = 14
    ema_period: int = 50
    rsi_buy_threshold: float = 35.0
    rsi_sell_threshold: float = 65.0
    stock_history_days: int = 180  # 6 months

    # Scheduler settings
    analyzer_interval_hours: int = 1
    watchlist: List[str] = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]

    # Logging settings
    log_level: str = "INFO"
    log_file: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
