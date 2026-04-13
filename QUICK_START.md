# 🚀 Quick Deployment & Usage Guide

## Deploy to Production

### Option 1: Docker (Recommended)
```bash
docker-compose up --build
```

### Option 2: Local Python
```bash
bash start.sh
```

---

## Verify Installation

### Health Check
```bash
curl http://localhost:10000/health
```

### Market Status
```bash
curl http://localhost:10000/market-status
```

---

## Send Test Alerts

### Morning Alert (Market Opens)
```bash
curl -X POST http://localhost:10000/test-market-open-alert
```

### Evening Alert (Market Closes)
```bash
curl -X POST http://localhost:10000/test-market-close-alert
```

### Test Individual Stock
```bash
curl -X POST "http://localhost:10000/test-trading-alert/RELIANCE.NS?signal=BUY"
```

---

## Automatic Alert Schedule

✅ **9:15 AM IST** - Market Opening Alert  
✅ **Every Hour** - Real-time Trading Signals  
✅ **3:30 PM IST** - Market Closing Alert  

**Auto-runs on:** Monday-Friday only

---

## View Logs

### Docker Logs
```bash
docker-compose logs -f
```

### Local Logs
```bash
tail -f logs/trading.log
```

---

## Configuration

Edit `.env` for:
- `TELEGRAM_TOKEN` - Your bot token
- `TELEGRAM_CHAT_ID` - Your chat ID
- `WATCHLIST` - Stocks to monitor

---

## Alert Format Includes

✅ Entry/Exit Prices  
✅ Stop Loss Levels (-3% / +3%)  
✅ Profit Targets (+3% / +5%)  
✅ Technical Indicators (RSI, MACD, EMA)  
✅ Recommended Action (BUY/SELL/HOLD)  
✅ Time & Date  

---

## See Full Documentation

📖 Read [ALERTS_GUIDE.md](ALERTS_GUIDE.md) for complete details

---

**Ready to trade? Let the alerts guide you!** 🎯
