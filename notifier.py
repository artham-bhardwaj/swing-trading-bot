"""
Telegram notification module.
Sends detailed trading alerts and recommendations via Telegram bot.
"""

import asyncio
from typing import Optional
from telegram import Bot
from telegram.error import TelegramError
from logger_config import app_logger
from config import settings
from strategy import Signal, AnalysisResult


class TelegramNotifier:
    """Sends detailed trading notifications via Telegram."""

    def __init__(self):
        """Initialize Telegram bot."""
        self.bot = None
        self.enabled = False
        
        if settings.telegram_token and settings.telegram_chat_id:
            try:
                self.bot = Bot(token=settings.telegram_token)
                self.enabled = True
                app_logger.info("Telegram notifier initialized")
            except Exception as e:
                app_logger.warning(f"Failed to initialize Telegram bot: {str(e)}")
        else:
            app_logger.warning(
                "Telegram notifier disabled: Missing TELEGRAM_TOKEN or TELEGRAM_CHAT_ID"
            )

    async def send_signal_notification(
        self,
        analysis: AnalysisResult
    ) -> bool:
        """
        Send detailed trading signal notification.
        
        Args:
            analysis: AnalysisResult containing signal and details
            
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.enabled or not self.bot:
            return False

        try:
            message = self._format_trading_alert(analysis)
            await self.bot.send_message(
                chat_id=settings.telegram_chat_id,
                text=message,
                parse_mode="HTML"
            )
            app_logger.info(f"Trading alert sent for {analysis.symbol}: {analysis.signal.value}")
            return True

        except TelegramError as e:
            app_logger.error(f"Telegram error sending message: {str(e)}")
            return False
        except Exception as e:
            app_logger.error(f"Unexpected error sending notification: {str(e)}")
            return False

    async def send_market_open_alert(self, analyses: dict) -> bool:
        """
        Send market opening alert with day's recommendations.
        
        Args:
            analyses: Dictionary of symbol -> AnalysisResult
            
        Returns:
            True if sent successfully
        """
        if not self.enabled or not self.bot:
            return False

        try:
            message = self._format_market_open_alert(analyses)
            await self.bot.send_message(
                chat_id=settings.telegram_chat_id,
                text=message,
                parse_mode="HTML"
            )
            app_logger.info(f"Market open alert sent with {len(analyses)} stocks")
            return True

        except TelegramError as e:
            app_logger.error(f"Telegram error: {str(e)}")
            return False

    async def send_market_close_alert(self, analyses: dict) -> bool:
        """
        Send market closing alert with day's summary.
        
        Args:
            analyses: Dictionary of symbol -> AnalysisResult
            
        Returns:
            True if sent successfully
        """
        if not self.enabled or not self.bot:
            return False

        try:
            message = self._format_market_close_alert(analyses)
            await self.bot.send_message(
                chat_id=settings.telegram_chat_id,
                text=message,
                parse_mode="HTML"
            )
            app_logger.info(f"Market close alert sent")
            return True

        except TelegramError as e:
            app_logger.error(f"Telegram error: {str(e)}")
            return False

    async def send_status_notification(self, message: str) -> bool:
        """
        Send status update notification.
        
        Args:
            message: Message to send
            
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.enabled or not self.bot:
            return False

        try:
            await self.bot.send_message(
                chat_id=settings.telegram_chat_id,
                text=message,
                parse_mode="HTML"
            )
            app_logger.info("Status notification sent")
            return True

        except TelegramError as e:
            app_logger.error(f"Telegram error: {str(e)}")
            return False

    @staticmethod
    def _format_trading_alert(analysis: AnalysisResult) -> str:
        """Format trading signal as detailed alert."""
        emoji = "🟢" if analysis.signal == Signal.BUY else ("🔴" if analysis.signal == Signal.SELL else "⏸️")
        
        # Calculate price targets
        entry_price = analysis.current_price
        stop_loss = entry_price * 0.97 if analysis.signal == Signal.BUY else entry_price * 1.03
        target_1 = entry_price * 1.03 if analysis.signal == Signal.BUY else entry_price * 0.97
        target_2 = entry_price * 1.05 if analysis.signal == Signal.BUY else entry_price * 0.95
        
        action_text = "BUY" if analysis.signal == Signal.BUY else ("SELL" if analysis.signal == Signal.SELL else "HOLD")
        
        message = (
            f"{emoji} <b>SWING TRADE ALERT: {action_text}</b>\n"
            f"<b>Symbol:</b> {analysis.symbol}\n"
            f"<b>Time:</b> {__import__('datetime').datetime.now().strftime('%H:%M:%S')}\n\n"
            
            f"📊 <b>CURRENT PRICE</b>\n"
            f"Price: ₹{analysis.current_price:.2f}\n\n"
            
            f"📈 <b>TECHNICAL INDICATORS</b>\n"
            f"RSI (14): {analysis.rsi:.2f}\n"
            f"MACD: {analysis.macd:.4f}\n"
            f"EMA (50): ₹{analysis.ema_50:.2f}\n"
            f"Signal Line: {analysis.macd_signal:.4f}\n\n"
        )
        
        if analysis.signal == Signal.BUY:
            message += (
                f"🎯 <b>BUY STRATEGY</b>\n"
                f"Entry Price: ₹{entry_price:.2f}\n"
                f"Stop Loss: ₹{stop_loss:.2f}\n"
                f"Target 1: ₹{target_1:.2f} (+3%)\n"
                f"Target 2: ₹{target_2:.2f} (+5%)\n\n"
            )
        elif analysis.signal == Signal.SELL:
            message += (
                f"🎯 <b>SELL STRATEGY</b>\n"
                f"Exit Price: ₹{entry_price:.2f}\n"
                f"Stop Loss: ₹{stop_loss:.2f}\n"
                f"Target 1: ₹{target_1:.2f} (-3%)\n"
                f"Target 2: ₹{target_2:.2f} (-5%)\n\n"
            )
        
        message += (
            f"📋 <b>ANALYSIS</b>\n"
            f"{analysis.reason}\n\n"
            f"⏰ <b>SWING TRADE TIP</b>\n"
            f"{'Hold position until target or stop loss hit' if analysis.signal != Signal.HOLD else 'Wait for better setup'}\n"
        )
        
        return message

    @staticmethod
    def _format_market_open_alert(analyses: dict) -> str:
        """Format market opening alert with recommendations."""
        from datetime import datetime
        
        message = (
            "🌅 <b>MARKET OPENING ALERT</b>\n"
            f"<b>Time:</b> 09:15 AM IST\n"
            f"<b>Date:</b> {datetime.now().strftime('%A, %d %B %Y')}\n\n"
        )
        
        buy_signals = []
        sell_signals = []
        hold_signals = []
        
        for symbol, analysis in analyses.items():
            if analysis.signal == Signal.BUY:
                buy_signals.append(analysis)
            elif analysis.signal == Signal.SELL:
                sell_signals.append(analysis)
            else:
                hold_signals.append(analysis)
        
        if buy_signals:
            message += "🟢 <b>BUY RECOMMENDATIONS</b>\n"
            for analysis in buy_signals:
                entry = analysis.current_price
                target = entry * 1.05
                stopless = entry * 0.97
                message += (
                    f"  • {analysis.symbol}\n"
                    f"    Entry: ₹{entry:.2f} | Target: ₹{target:.2f} | Stop: ₹{stopless:.2f}\n"
                )
            message += "\n"
        
        if sell_signals:
            message += "🔴 <b>SELL RECOMMENDATIONS</b>\n"
            for analysis in sell_signals:
                entry = analysis.current_price
                target = entry * 0.95
                stopless = entry * 1.03
                message += (
                    f"  • {analysis.symbol}\n"
                    f"    Exit: ₹{entry:.2f} | Target: ₹{target:.2f} | Stop: ₹{stopless:.2f}\n"
                )
            message += "\n"
        
        if hold_signals:
            message += "⏸️ <b>HOLD/MONITOR</b>\n"
            for analysis in hold_signals:
                message += f"  • {analysis.symbol} (₹{analysis.current_price:.2f})\n"
            message += "\n"
        
        message += (
            "⏰ <b>MARKET HOURS</b>\n"
            "Open: 09:15 AM | Close: 03:30 PM IST\n\n"
            "💡 <b>TIP:</b> Follow the signals closely. Set alerts for target and stop-loss prices.\n"
            "🚀 Good luck with your swing trades today!"
        )
        
        return message

    @staticmethod
    def _format_market_close_alert(analyses: dict) -> str:
        """Format market closing alert with summary."""
        from datetime import datetime
        
        message = (
            "🌆 <b>MARKET CLOSING ALERT</b>\n"
            f"<b>Time:</b> 03:30 PM IST\n"
            f"<b>Date:</b> {datetime.now().strftime('%A, %d %B %Y')}\n\n"
        )
        
        buy_signals = []
        sell_signals = []
        hold_signals = []
        
        for symbol, analysis in analyses.items():
            if analysis.signal == Signal.BUY:
                buy_signals.append(analysis)
            elif analysis.signal == Signal.SELL:
                sell_signals.append(analysis)
            else:
                hold_signals.append(analysis)
        
        message += "📊 <b>TODAY'S SIGNALS SUMMARY</b>\n"
        message += f"Buy Signals: {len(buy_signals)} | Sell Signals: {len(sell_signals)} | Hold: {len(hold_signals)}\n\n"
        
        if buy_signals:
            message += "🟢 <b>STOCKS TO BUY</b>\n"
            for analysis in buy_signals:
                entry = analysis.current_price
                message += (
                    f"  {analysis.symbol}: ₹{entry:.2f}\n"
                )
            message += "\n"
        
        if sell_signals:
            message += "🔴 <b>STOCKS TO SELL</b>\n"
            for analysis in sell_signals:
                entry = analysis.current_price
                message += (
                    f"  {analysis.symbol}: ₹{entry:.2f}\n"
                )
            message += "\n"
        
        message += (
            "📋 <b>TOMORROW'S PLAN</b>\n"
            "• Review today's trades\n"
            "• Check positions\n"
            "• Market opens at 09:15 AM tomorrow\n\n"
            "🌙 Good evening! See you tomorrow at market open!"
        )
        
        return message

    def send_signal_notification_sync(self, analysis: AnalysisResult) -> bool:
        """
        Send notification synchronously (blocking).
        
        Args:
            analysis: AnalysisResult
            
        Returns:
            True if sent successfully
        """
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.create_task(self.send_signal_notification(analysis))
                return True
            else:
                return loop.run_until_complete(
                    self.send_signal_notification(analysis)
                )
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(
                    self.send_signal_notification(analysis)
                )
            finally:
                loop.close()

    def send_market_open_alert_sync(self, analyses: dict) -> bool:
        """Send market open alert synchronously."""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.create_task(self.send_market_open_alert(analyses))
                return True
            else:
                return loop.run_until_complete(
                    self.send_market_open_alert(analyses)
                )
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(
                    self.send_market_open_alert(analyses)
                )
            finally:
                loop.close()

    def send_market_close_alert_sync(self, analyses: dict) -> bool:
        """Send market close alert synchronously."""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.create_task(self.send_market_close_alert(analyses))
                return True
            else:
                return loop.run_until_complete(
                    self.send_market_close_alert(analyses)
                )
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(
                    self.send_market_close_alert(analyses)
                )
            finally:
                loop.close()


# Global notifier instance
notifier = TelegramNotifier()
