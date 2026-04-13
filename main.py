"""
Main FastAPI application.
Provides REST API endpoints for swing trading analysis.
"""

from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from logger_config import app_logger
from config import settings
from data import StockDataFetcher
from strategy import TradingStrategy, Signal
from scheduler import scheduler
from backtest import Backtester
from market_hours import MarketHours
from notifier import notifier


# Pydantic models
class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    message: str


class AnalysisResponse(BaseModel):
    """Stock analysis response."""
    symbol: str
    signal: str
    current_price: float
    rsi: Optional[float]
    macd: Optional[float]
    macd_signal: Optional[float]
    ema_50: Optional[float]
    reason: str


# Initialize FastAPI app
app = FastAPI(
    title=settings.app_title,
    version=settings.app_version,
    description="REST API for swing trading assistant with technical analysis"
)

# Global instances
fetcher = StockDataFetcher()


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    app_logger.info("Starting Swing Trading Assistant")
    scheduler.start()
    app_logger.info("Application startup complete")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    app_logger.info("Shutting down Swing Trading Assistant")
    scheduler.stop()
    app_logger.info("Application shutdown complete")


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.
    
    Returns:
        Health status
    """
    return HealthResponse(
        status="OK",
        message="Swing Trading Assistant is running"
    )


@app.get("/analyze/{symbol}", response_model=AnalysisResponse)
async def analyze_stock(symbol: str) -> AnalysisResponse:
    """
    Analyze a stock and return trading signal.
    
    Args:
        symbol: Stock symbol (e.g., 'RELIANCE.NS', 'AAPL')
        
    Returns:
        Analysis result with signal and indicators
        
    Raises:
        HTTPException: If analysis fails
    """
    try:
        app_logger.info(f"Received analysis request for {symbol}")

        # Validate symbol format
        if not symbol or len(symbol) < 1:
            raise HTTPException(
                status_code=400,
                detail="Invalid symbol format"
            )

        # Fetch data
        data = fetcher.fetch_stock_data(symbol)
        if data is None:
            raise HTTPException(
                status_code=404,
                detail=f"Could not fetch data for symbol: {symbol}"
            )

        # Get current price
        current_price = fetcher.get_latest_price(symbol)
        if current_price is None:
            raise HTTPException(
                status_code=404,
                detail=f"Could not fetch current price for symbol: {symbol}"
            )

        # Perform analysis
        analysis = TradingStrategy.analyze_stock(data, symbol, current_price)

        app_logger.info(
            f"Analysis complete for {symbol}: Signal={analysis.signal.value}"
        )

        return AnalysisResponse(
            symbol=analysis.symbol,
            signal=analysis.signal.value,
            current_price=analysis.current_price,
            rsi=analysis.rsi,
            macd=analysis.macd,
            macd_signal=analysis.macd_signal,
            ema_50=analysis.ema_50,
            reason=analysis.reason
        )

    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error analyzing {symbol}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/watchlist")
async def get_watchlist():
    """
    Get the current watchlist of stocks.
    
    Returns:
        List of symbols being monitored
    """
    return {
        "watchlist": settings.watchlist,
        "analysis_interval_hours": settings.analyzer_interval_hours
    }


@app.get("/config")
async def get_config():
    """
    Get trading strategy configuration.
    
    Returns:
        Configuration parameters
    """
    return {
        "rsi_period": settings.rsi_period,
        "rsi_buy_threshold": settings.rsi_buy_threshold,
        "rsi_sell_threshold": settings.rsi_sell_threshold,
        "ema_period": settings.ema_period,
        "stock_history_days": settings.stock_history_days
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    app_logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


@app.get("/backtest/{symbol}")
async def backtest_stock(symbol: str, days: Optional[int] = 180):
    """
    Backtest trading strategy on a stock.
    
    Args:
        symbol: Stock symbol
        days: Number of historical days to backtest
        
    Returns:
        Backtest results with trades and metrics
    """
    try:
        app_logger.info(f"Backtest requested for {symbol}")
        
        result = Backtester.backtest_symbol(symbol, days=days)
        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"Could not run backtest for {symbol}"
            )
        
        return result.to_dict()
        
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Backtest error for {symbol}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Backtest error: {str(e)}"
        )


@app.get("/backtest-portfolio")
async def backtest_portfolio(days: Optional[int] = 180):
    """
    Backtest strategy on entire watchlist.
    
    Args:
        days: Number of historical days to backtest
        
    Returns:
        Dictionary with results for each symbol
    """
    try:
        app_logger.info("Portfolio backtest requested")
        
        results = Backtester.backtest_portfolio(
            settings.watchlist,
            days=days
        )
        
        if not results:
            raise HTTPException(
                status_code=500,
                detail="Backtest failed for all symbols"
            )
        
        return {
            "backtest_date": datetime.now().isoformat(),
            "watchlist": settings.watchlist,
            "days": days,
            "results": results
        }
        
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Portfolio backtest error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Portfolio backtest error: {str(e)}"
        )


@app.get("/demo")
async def demo_analysis():
    """
    Get analysis using demo data (for testing when API is down).
    
    Returns:
        Analysis results using synthetic data
    """
    try:
        from demo_data import DemoDataGenerator
        
        app_logger.info("Demo analysis requested")
        
        results = {}
        for symbol in settings.watchlist:
            data = DemoDataGenerator.generate_stock_data(symbol)
            
            if data is not None:
                current_price = data["Close"].iloc[-1]
                analysis = TradingStrategy.analyze_stock(data, symbol, current_price)
                
                results[symbol] = {
                    "symbol": analysis.symbol,
                    "signal": analysis.signal.value,
                    "current_price": analysis.current_price,
                    "rsi": analysis.rsi,
                    "macd": analysis.macd,
                    "ema_50": analysis.ema_50,
                    "reason": analysis.reason,
                    "note": "DEMO DATA - For testing only"
                }
        
        return {
            "timestamp": datetime.now().isoformat(),
            "mode": "DEMO",
            "results": results
        }
        
    except Exception as e:
        app_logger.error(f"Demo analysis error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Demo analysis error: {str(e)}"
        )


@app.get("/market-status")
async def get_market_status():
    """
    Get current market status and timings.
    
    Returns:
        Market information
    """
    try:
        status = MarketHours.get_market_status()
        event, next_time = MarketHours.get_next_market_event()
        
        return {
            **status,
            "next_event": event,
            "next_event_time": next_time.isoformat()
        }
    except Exception as e:
        app_logger.error(f"Error getting market status: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Could not get market status"
        )


@app.post("/test-market-open-alert")
async def test_market_open_alert():
    """
    Test market opening alert (sends Telegram message).
    
    Returns:
        Alert status
    """
    try:
        app_logger.info("Testing market opening alert")
        
        # Analyze all stocks
        fetcher = StockDataFetcher()
        analyses = {}
        
        for symbol in settings.watchlist:
            data = fetcher.fetch_stock_data(symbol)
            if data is not None:
                # Use current price from data if API fails
                current_price = fetcher.get_latest_price(symbol)
                if current_price is None:
                    # Fallback to latest close price from data
                    current_price = data["Close"].iloc[-1]
                
                if current_price is not None:
                    analysis = TradingStrategy.analyze_stock(data, symbol, current_price)
                    analyses[symbol] = analysis
        
        if not analyses:
            raise HTTPException(
                status_code=404,
                detail="Could not analyze stocks"
            )
        
        # Send alert
        result = notifier.send_market_open_alert_sync(analyses)
        
        return {
            "status": "sent" if result else "failed",
            "alert_type": "market_open",
            "stocks_analyzed": len(analyses),
            "message": "Market opening alert sent to Telegram" if result else "Failed to send alert"
        }
        
    except Exception as e:
        app_logger.error(f"Error testing market open alert: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Test failed: {str(e)}"
        )


@app.post("/test-market-close-alert")
async def test_market_close_alert():
    """
    Test market closing alert (sends Telegram message).
    
    Returns:
        Alert status
    """
    try:
        app_logger.info("Testing market closing alert")
        
        # Analyze all stocks
        fetcher = StockDataFetcher()
        analyses = {}
        
        for symbol in settings.watchlist:
            data = fetcher.fetch_stock_data(symbol)
            if data is not None:
                # Use current price from data if API fails
                current_price = fetcher.get_latest_price(symbol)
                if current_price is None:
                    # Fallback to latest close price from data
                    current_price = data["Close"].iloc[-1]
                
                if current_price is not None:
                    analysis = TradingStrategy.analyze_stock(data, symbol, current_price)
                    analyses[symbol] = analysis
        
        if not analyses:
            raise HTTPException(
                status_code=404,
                detail="Could not analyze stocks"
            )
        
        # Send alert
        result = notifier.send_market_close_alert_sync(analyses)
        
        return {
            "status": "sent" if result else "failed",
            "alert_type": "market_close",
            "stocks_analyzed": len(analyses),
            "message": "Market closing alert sent to Telegram" if result else "Failed to send alert"
        }
        
    except Exception as e:
        app_logger.error(f"Error testing market close alert: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Test failed: {str(e)}"
        )


@app.post("/test-trading-alert/{symbol}")
async def test_trading_alert(symbol: str, signal: str = "BUY"):
    """
    Test a trading alert for a specific stock.
    
    Args:
        symbol: Stock symbol
        signal: BUY, SELL, or HOLD
        
    Returns:
        Alert status
    """
    try:
        app_logger.info(f"Testing trading alert for {symbol}")
        
        fetcher = StockDataFetcher()
        data = fetcher.fetch_stock_data(symbol)
        
        if data is None:
            raise HTTPException(
                status_code=404,
                detail=f"Could not fetch data for {symbol}"
            )
        
        # Use current price from data if API fails
        current_price = fetcher.get_latest_price(symbol)
        if current_price is None:
            # Fallback to latest close price from data
            current_price = data["Close"].iloc[-1]
        
        if current_price is None:
            raise HTTPException(
                status_code=404,
                detail=f"Could not fetch price for {symbol}"
            )
        
        analysis = TradingStrategy.analyze_stock(data, symbol, current_price)
        
        # Override signal for testing
        if signal.upper() in ["BUY", "SELL", "HOLD"]:
            from strategy import Signal as SignalEnum
            analysis.signal = SignalEnum[signal.upper()]
        
        # Send alert
        result = notifier.send_signal_notification_sync(analysis)
        
        return {
            "status": "sent" if result else "failed",
            "symbol": symbol,
            "signal": analysis.signal.value,
            "price": analysis.current_price,
            "message": "Trading alert sent to Telegram" if result else "Failed to send alert"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error testing trading alert: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Test failed: {str(e)}"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    app_logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    
    app_logger.info(f"Starting FastAPI server on {settings.host}:{settings.port}")
    
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level.lower()
    )
