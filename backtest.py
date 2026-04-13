"""
Backtesting module for strategy validation.
Tests trading strategy against historical data.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
import pandas as pd
from data import StockDataFetcher
from strategy import TradingStrategy, Signal
from logger_config import app_logger


class BacktestResult:
    """Results from backtesting."""
    
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.trades = []
        self.total_return = 0.0
        self.win_rate = 0.0
        self.max_drawdown = 0.0
        self.num_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0
        self.start_date = None
        self.end_date = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "symbol": self.symbol,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "num_trades": self.num_trades,
            "winning_trades": self.winning_trades,
            "losing_trades": self.losing_trades,
            "win_rate": round(self.win_rate, 2),
            "total_return_pct": round(self.total_return, 2),
            "max_drawdown_pct": round(self.max_drawdown, 2),
            "trades": self.trades
        }


class Backtester:
    """Backtests trading strategy on historical data."""
    
    @staticmethod
    def backtest_symbol(
        symbol: str,
        days: int = 180,
        initial_capital: float = 100000.0
    ) -> Optional[BacktestResult]:
        """
        Backtest strategy on a single symbol.
        
        Args:
            symbol: Stock symbol
            days: Historical days to test
            initial_capital: Starting capital for simulation
            
        Returns:
            BacktestResult with test metrics
        """
        try:
            app_logger.info(f"Starting backtest for {symbol} ({days} days)")
            
            # Fetch data
            fetcher = StockDataFetcher()
            data = fetcher.fetch_stock_data(symbol, days=days)
            
            if data is None or len(data) < 30:
                app_logger.warning(f"Insufficient data for backtest: {symbol}")
                return None
            
            result = BacktestResult(symbol)
            result.start_date = data.index[0]
            result.end_date = data.index[-1]
            
            # Simulation variables
            position = None  # None, "LONG"
            entry_price = 0.0
            cash = initial_capital
            equity = initial_capital
            equity_curve = []
            
            # Walk through each day
            for i in range(20, len(data)):  # Start after 20 days for indicator stability
                current_date = data.index[i]
                current_price = data["Close"].iloc[i]
                
                # Get historical data up to current point
                historical_data = data.iloc[:i+1]
                
                # Analyze
                analysis = TradingStrategy.analyze_stock(
                    historical_data,
                    symbol,
                    current_price
                )
                
                # Trading logic
                if analysis.signal == Signal.BUY and position is None:
                    # Enter long
                    position = "LONG"
                    entry_price = current_price
                    app_logger.debug(f"BUY at {current_date}: ${current_price:.2f}")
                    
                elif analysis.signal == Signal.SELL and position == "LONG":
                    # Exit long
                    pnl = current_price - entry_price
                    pnl_pct = (pnl / entry_price) * 100
                    profit = (pnl / entry_price) * cash
                    equity += profit
                    
                    result.trades.append({
                        "entry_date": result.start_date.isoformat(),
                        "entry_price": round(entry_price, 2),
                        "exit_date": current_date.isoformat(),
                        "exit_price": round(current_price, 2),
                        "return_pct": round(pnl_pct, 2),
                        "profit": round(profit, 2)
                    })
                    
                    if pnl > 0:
                        result.winning_trades += 1
                    else:
                        result.losing_trades += 1
                    
                    position = None
                    result.num_trades += 1
                    app_logger.debug(f"SELL at {current_date}: ${current_price:.2f}, PnL: {pnl_pct:.2f}%")
                
                # Update equity
                if position == "LONG":
                    equity = cash + ((current_price - entry_price) / entry_price) * cash
                
                equity_curve.append(equity)
            
            # Close any open position at market close
            if position == "LONG":
                final_price = data["Close"].iloc[-1]
                pnl = final_price - entry_price
                pnl_pct = (pnl / entry_price) * 100
                profit = (pnl / entry_price) * cash
                equity += profit
                result.num_trades += 1
                
                if pnl > 0:
                    result.winning_trades += 1
                else:
                    result.losing_trades += 1
            
            # Calculate metrics
            result.total_return = ((equity - initial_capital) / initial_capital) * 100
            
            if result.num_trades > 0:
                result.win_rate = (result.winning_trades / result.num_trades) * 100
            
            # Calculate max drawdown
            if equity_curve:
                running_max = pd.Series(equity_curve).expanding().max()
                drawdown = (pd.Series(equity_curve) - running_max) / running_max
                result.max_drawdown = drawdown.min() * 100
            
            app_logger.info(
                f"Backtest complete for {symbol}: "
                f"{result.num_trades} trades, {result.win_rate:.1f}% win rate, "
                f"{result.total_return:.2f}% return"
            )
            
            return result
            
        except Exception as e:
            app_logger.error(f"Backtest error for {symbol}: {str(e)}")
            return None
    
    @staticmethod
    def backtest_portfolio(
        symbols: List[str],
        days: int = 180
    ) -> Dict[str, Dict]:
        """
        Backtest strategy on multiple symbols.
        
        Args:
            symbols: List of stock symbols
            days: Historical days to test
            
        Returns:
            Dictionary with results for each symbol
        """
        results = {}
        app_logger.info(f"Starting portfolio backtest for {len(symbols)} symbols")
        
        for symbol in symbols:
            result = Backtester.backtest_symbol(symbol, days=days)
            if result:
                results[symbol] = result.to_dict()
        
        return results
