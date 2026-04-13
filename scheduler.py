"""
Scheduler module.
Runs periodic stock analysis and market alerts using APScheduler.
"""

from typing import Optional, Dict
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from logger_config import app_logger
from config import settings
from data import StockDataFetcher
from strategy import TradingStrategy, Signal
from market_hours import MarketHours
from notifier import notifier
import pytz


class StockAnalysisScheduler:
    """Manages scheduled stock analysis and market alerts."""

    def __init__(self):
        """Initialize the scheduler."""
        self.scheduler = BackgroundScheduler()
        self.fetcher = StockDataFetcher()

    def start(self):
        """Start the scheduler with multiple jobs."""
        try:
            if not self.scheduler.running:
                # Market opening alert - 9:15 AM IST (Monday-Friday)
                self.scheduler.add_job(
                    func=self._market_opening_alert,
                    trigger=CronTrigger(
                        hour=9,
                        minute=15,
                        day_of_week='mon-fri',
                        timezone=pytz.timezone('Asia/Kolkata')
                    ),
                    id="market_open_alert",
                    name="Market Opening Alert",
                    replace_existing=True
                )
                
                # Market closing alert - 3:30 PM IST (Monday-Friday)
                self.scheduler.add_job(
                    func=self._market_closing_alert,
                    trigger=CronTrigger(
                        hour=15,
                        minute=30,
                        day_of_week='mon-fri',
                        timezone=pytz.timezone('Asia/Kolkata')
                    ),
                    id="market_close_alert",
                    name="Market Closing Alert",
                    replace_existing=True
                )
                
                # Periodic analysis during market hours
                self.scheduler.add_job(
                    func=self._periodic_analysis,
                    trigger=IntervalTrigger(hours=settings.analyzer_interval_hours),
                    id="periodic_analysis",
                    name="Periodic Analysis",
                    replace_existing=True
                )
                
                self.scheduler.start()
                app_logger.info(
                    f"Scheduler started with market alerts and "
                    f"periodic analysis every {settings.analyzer_interval_hours} hour(s)"
                )
        except Exception as e:
            app_logger.error(f"Failed to start scheduler: {str(e)}")

    def stop(self):
        """Stop the scheduler."""
        try:
            if self.scheduler.running:
                self.scheduler.shutdown()
                app_logger.info("Scheduler stopped")
        except Exception as e:
            app_logger.error(f"Error stopping scheduler: {str(e)}")

    def _analyze_all_stocks(self) -> Dict[str, any]:
        """
        Analyze all stocks in watchlist.
        
        Returns:
            Dictionary of symbol -> AnalysisResult
        """
        results = {}
        
        for symbol in settings.watchlist:
            try:
                data = self.fetcher.fetch_stock_data(symbol)
                if data is None:
                    app_logger.warning(f"Could not fetch data for {symbol}")
                    continue
                
                current_price = self.fetcher.get_latest_price(symbol)
                if current_price is None:
                    app_logger.warning(f"Could not fetch price for {symbol}")
                    continue
                
                analysis = TradingStrategy.analyze_stock(data, symbol, current_price)
                results[symbol] = analysis
                
            except Exception as e:
                app_logger.error(f"Error analyzing {symbol}: {str(e)}")
                continue
        
        return results

    def _market_opening_alert(self):
        """Send detailed alert when market opens at 9:15 AM IST."""
        try:
            app_logger.info("Market opening alert triggered")
            
            analyses = self._analyze_all_stocks()
            if not analyses:
                app_logger.warning("Could not analyze stocks for market open alert")
                return
            
            # Send market open alert via Telegram
            notifier.send_market_open_alert_sync(analyses)
            
            # Also send individual BUY/SELL signals
            for symbol, analysis in analyses.items():
                if analysis.signal in [Signal.BUY, Signal.SELL]:
                    app_logger.info(f"Market open signal for {symbol}: {analysis.signal.value}")
                    notifier.send_signal_notification_sync(analysis)
            
            app_logger.info("Market opening alert completed")
            
        except Exception as e:
            app_logger.error(f"Error in market opening alert: {str(e)}")

    def _market_closing_alert(self):
        """Send alert when market closes at 3:30 PM IST."""
        try:
            app_logger.info("Market closing alert triggered")
            
            analyses = self._analyze_all_stocks()
            if not analyses:
                app_logger.warning("Could not analyze stocks for market close alert")
                return
            
            # Send market close alert via Telegram
            notifier.send_market_close_alert_sync(analyses)
            
            app_logger.info("Market closing alert completed")
            
        except Exception as e:
            app_logger.error(f"Error in market closing alert: {str(e)}")

    def _periodic_analysis(self):
        """Run periodic analysis during market hours."""
        try:
            # Only run if market is open
            if not MarketHours.is_market_open():
                app_logger.debug("Market is closed, skipping periodic analysis")
                return
            
            app_logger.info("Periodic analysis started")
            
            for symbol in settings.watchlist:
                try:
                    data = self.fetcher.fetch_stock_data(symbol)
                    if data is None:
                        app_logger.warning(f"Could not fetch data for {symbol}")
                        continue
                    
                    current_price = self.fetcher.get_latest_price(symbol)
                    if current_price is None:
                        app_logger.warning(f"Could not fetch price for {symbol}")
                        continue
                    
                    analysis = TradingStrategy.analyze_stock(data, symbol, current_price)
                    
                    # Send notification if strong signal
                    if analysis.signal in [Signal.BUY, Signal.SELL]:
                        app_logger.info(f"Signal during periodic analysis for {symbol}: {analysis.signal.value}")
                        notifier.send_signal_notification_sync(analysis)
                    
                except Exception as e:
                    app_logger.error(f"Error in periodic analysis for {symbol}: {str(e)}")
                    continue
            
            app_logger.info("Periodic analysis completed")
            
        except Exception as e:
            app_logger.error(f"Error in periodic analysis: {str(e)}")

    def _analyze_stock(self, symbol: str) -> Optional[dict]:
        """
        Analyze a single stock and send notification if signal generated.
        
        Args:
            symbol: Stock symbol to analyze
            
        Returns:
            Analysis result as dictionary
        """
        try:
            app_logger.info(f"Scheduled analysis started for {symbol}")

            # Fetch data
            data = self.fetcher.fetch_stock_data(symbol)
            if data is None:
                app_logger.warning(f"Could not fetch data for {symbol}")
                return None

            # Get current price
            current_price = self.fetcher.get_latest_price(symbol)
            if current_price is None:
                app_logger.warning(f"Could not fetch price for {symbol}")
                return None

            # Analyze
            analysis = TradingStrategy.analyze_stock(data, symbol, current_price)

            # Send notification if BUY or SELL
            if analysis.signal in [Signal.BUY, Signal.SELL]:
                app_logger.info(f"Signal generated for {symbol}: {analysis.signal.value}")
                notifier.send_signal_notification_sync(analysis)

            return {
                "symbol": analysis.symbol,
                "signal": analysis.signal.value,
                "price": analysis.current_price,
                "rsi": analysis.rsi,
                "reason": analysis.reason
            }

        except Exception as e:
            app_logger.error(f"Error in scheduled analysis for {symbol}: {str(e)}")
            return None


# Global scheduler instance
scheduler = StockAnalysisScheduler()
