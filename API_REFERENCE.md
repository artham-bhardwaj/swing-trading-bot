# 📚 API Documentation - Swing Trading Assistant

## Base URL
```
http://localhost:10000
```

---

## 🏥 Health & Status Endpoints

### 1. Health Check
**Get server status**

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-04-14T09:15:30",
  "uptime": "2h 30m"
}
```

---

### 2. Market Status
**Get current market status with IST timezone**

```http
GET /market-status
```

**Response:**
```json
{
  "market_open": true,
  "current_time": "2024-04-14 09:45:30 IST",
  "market_hours": "09:15 AM - 03:30 PM IST",
  "day": "Monday",
  "next_event": "Market Close at 03:30 PM",
  "time_until_close": "5h 45m"
}
```

---

## 🟢 Trading Analysis Endpoints

### 3. Analyze Single Stock
**Get real-time trading signal for a stock**

```http
GET /analyze/{symbol}
```

**Parameters:**
- `symbol` - Stock ticker (e.g., `RELIANCE.NS`, `TCS.NS`)

**Example:**
```bash
curl http://localhost:10000/analyze/RELIANCE.NS
```

**Response:**
```json
{
  "symbol": "RELIANCE.NS",
  "signal": "BUY",
  "price": 2850.50,
  "rsi": 32.45,
  "macd": 0.0234,
  "ema_50": 2800.00,
  "entry_price": 2850.50,
  "stop_loss": 2764.98,
  "target_1": 2935.02,
  "target_2": 2997.03,
  "timestamp": "2024-04-14 09:45:30"
}
```

---

### 4. Get Watchlist
**Get signals for all watched stocks**

```http
GET /watchlist
```

**Response:**
```json
{
  "watchlist": [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS"
  ],
  "total_stocks": 3,
  "signals": {
    "RELIANCE.NS": {
      "signal": "BUY",
      "price": 2850.50
    },
    "TCS.NS": {
      "signal": "SELL",
      "price": 3500.00
    },
    "INFY.NS": {
      "signal": "HOLD",
      "price": 1800.00
    }
  }
}
```

---

## 🔔 Alert Endpoints

### 5. Test Market Opening Alert
**Send detailed morning alert (as if market opened)**

```http
POST /test-market-open-alert
```

**Response:**
```json
{
  "status": "sent",
  "alert_type": "market_open",
  "stocks_analyzed": 3,
  "buy_signals": 2,
  "sell_signals": 1,
  "message": "Market opening alert sent to Telegram"
}
```

**What it sends:**
- 🌅 Market opening announcement
- 🟢 All BUY recommendations with prices
- 🔴 All SELL recommendations with prices
- ⏸️ Stocks to HOLD/MONITOR

---

### 6. Test Market Closing Alert
**Send evening closing alert**

```http
POST /test-market-close-alert
```

**Response:**
```json
{
  "status": "sent",
  "alert_type": "market_close",
  "stocks_analyzed": 3,
  "signals_summary": {
    "buy": 2,
    "sell": 1,
    "hold": 0
  },
  "message": "Market closing alert sent to Telegram"
}
```

**What it sends:**
- 🌆 Market closing summary
- 📊 Today's signal count
- 📋 Tomorrow's plan

---

### 7. Test Individual Trading Alert
**Send alert for a specific stock**

```http
POST /test-trading-alert/{symbol}?signal={SIGNAL}
```

**Parameters:**
- `symbol` - Stock ticker (e.g., `RELIANCE.NS`)
- `signal` - Trading signal: `BUY`, `SELL`, or `HOLD` (optional)

**Examples:**
```bash
# BUY Signal
curl -X POST "http://localhost:10000/test-trading-alert/RELIANCE.NS?signal=BUY"

# SELL Signal
curl -X POST "http://localhost:10000/test-trading-alert/TCS.NS?signal=SELL"

# HOLD
curl -X POST "http://localhost:10000/test-trading-alert/INFY.NS"
```

**Response:**
```json
{
  "status": "sent",
  "symbol": "RELIANCE.NS",
  "signal": "BUY",
  "price": 2850.50,
  "target": 2997.03,
  "message": "Trading alert sent to Telegram"
}
```

**What it sends:**
- 🟢 Signal type (BUY/SELL/HOLD)
- 📊 Current price
- 🎯 Entry/Exit price
- 🛑 Stop loss level
- 🎯 Profit targets
- 📈 Technical indicators

---

## 📊 Backtesting Endpoints

### 8. Backtest Single Stock
**Test strategy on historical data**

```http
GET /backtest/{symbol}
```

**Parameters:**
- `symbol` - Stock ticker
- `period` - Optional: `1y` (default), `6mo`, `3mo`, `1mo`

**Example:**
```bash
curl "http://localhost:10000/backtest/RELIANCE.NS?period=6mo"
```

**Response:**
```json
{
  "symbol": "RELIANCE.NS",
  "period": "6mo",
  "total_signals": 45,
  "buy_signals": 23,
  "sell_signals": 22,
  "total_trades": 22,
  "winning_trades": 15,
  "losing_trades": 7,
  "win_rate": "68.18%",
  "avg_win": 2.34,
  "avg_loss": -1.89,
  "profit_factor": 1.24
}
```

---

### 9. Backtest Portfolio
**Test strategy on all watchlist stocks**

```http
GET /backtest-portfolio
```

**Parameters:**
- `period` - Optional: `1y` (default), `6mo`, `3mo`, `1mo`

**Response:**
```json
{
  "portfolio": {
    "RELIANCE.NS": {"win_rate": "68%", "profit_factor": 1.24},
    "TCS.NS": {"win_rate": "65%", "profit_factor": 1.18},
    "INFY.NS": {"win_rate": "72%", "profit_factor": 1.31}
  },
  "avg_win_rate": "68.33%",
  "avg_profit_factor": 1.24
}
```

---

## 🎮 Demo Endpoints

### 10. Demo Analysis
**Test with synthetic data (no API required)**

```http
GET /demo
```

**Response:**
```json
{
  "mode": "demo",
  "stocks": [
    {
      "symbol": "RELIANCE_DEMO",
      "signal": "BUY",
      "price": 2850.50,
      "rsi": 32.45,
      "target": 2997.03
    },
    {
      "symbol": "TCS_DEMO",
      "signal": "SELL",
      "price": 3500.00,
      "rsi": 68.50,
      "target": 3325.00
    }
  ]
}
```

---

## ⚙️ Configuration Endpoint

### 11. Get Configuration
**View current trading configuration**

```http
GET /config
```

**Response:**
```json
{
  "watchlist": ["RELIANCE.NS", "TCS.NS", "INFY.NS"],
  "market_hours": {
    "open": "09:15 AM IST",
    "close": "03:30 PM IST",
    "timezone": "Asia/Kolkata"
  },
  "trading_strategy": {
    "rsi_period": 14,
    "rsi_buy": 35,
    "rsi_sell": 65,
    "ema_period": 50
  },
  "targets": {
    "profit_target_1": "+3%",
    "profit_target_2": "+5%",
    "stop_loss": "-3%"
  }
}
```

---

## 🔄 Complete Request/Response Cycle

### Typical BUY Signal Workflow

**1. Analyze Stock**
```bash
curl http://localhost:10000/analyze/RELIANCE.NS
```

**2. Send Alert (if BUY is confirmed)**
```bash
curl -X POST "http://localhost:10000/test-trading-alert/RELIANCE.NS?signal=BUY"
```

**3. Check Alert Status**
- Alert sent to Telegram ✅
- Contains entry: ₹2850.50
- Contains stop loss: ₹2764.98
- Contains targets: ₹2935.02 and ₹2997.03

**4. Execute Trade (manually)**
- Place limit order at ₹2850.50
- Set stop loss at ₹2764.98
- Set profit targets at ₹2935.02 and ₹2997.03

---

## ⏰ Automatic Alert Schedule

The system automatically sends alerts on this schedule:

| Time | Event | Endpoint |
|------|-------|----------|
| 09:15 AM IST | Market Opens | `/test-market-open-alert` |
| 10:15 AM IST | Analysis | Real-time signals if BUY/SELL |
| 11:15 AM IST | Analysis | Real-time signals if BUY/SELL |
| 12:15 PM IST | Analysis | Real-time signals if BUY/SELL |
| 01:15 PM IST | Analysis | Real-time signals if BUY/SELL |
| 02:15 PM IST | Analysis | Real-time signals if BUY/SELL |
| 03:30 PM IST | Market Closes | `/test-market-close-alert` |

---

## 📈 Response Codes

| Code | Meaning |
|------|---------|
| 200 | ✅ Success |
| 400 | ❌ Bad request (invalid parameters) |
| 404 | ❌ Not found (stock doesn't exist) |
| 500 | ❌ Server error (check logs) |

---

## 🧪 Testing All Endpoints

Run this script to test everything:

```bash
#!/bin/bash

echo "🏥 Health Check"
curl http://localhost:10000/health | python3 -m json.tool

echo -e "\n📊 Market Status"
curl http://localhost:10000/market-status | python3 -m json.tool

echo -e "\n🟢 Analyze Stock"
curl http://localhost:10000/analyze/RELIANCE.NS | python3 -m json.tool

echo -e "\n📋 Watchlist"
curl http://localhost:10000/watchlist | python3 -m json.tool

echo -e "\n🔔 Test Market Open Alert"
curl -X POST http://localhost:10000/test-market-open-alert | python3 -m json.tool

echo -e "\n🔔 Test Market Close Alert"
curl -X POST http://localhost:10000/test-market-close-alert | python3 -m json.tool

echo -e "\n⚙️ Configuration"
curl http://localhost:10000/config | python3 -m json.tool
```

---

## 💡 Usage Tips

1. **Check market status first** before sending alerts
2. **Use `/analyze/{symbol}`** to test real-time analysis
3. **Test alerts** before trusting Telegram delivery
4. **Monitor logs** for any errors
5. **Review backtests** to validate strategy

---

## 🚀 Integration Example

```python
import requests
import json

BASE_URL = "http://localhost:10000"

# Check market status
status = requests.get(f"{BASE_URL}/market-status").json()
if status['market_open']:
    # Analyze a stock
    analysis = requests.get(f"{BASE_URL}/analyze/RELIANCE.NS").json()
    
    # If BUY signal
    if analysis['signal'] == 'BUY':
        # Send alert
        alert = requests.post(
            f"{BASE_URL}/test-trading-alert/RELIANCE.NS?signal=BUY"
        ).json()
        print(alert['message'])
```

---

## 📞 Troubleshooting

| Issue | Solution |
|-------|----------|
| 404 Stock Not Found | Add stock to watchlist in `.env` |
| Alerts Not Sending | Check TELEGRAM_TOKEN and TELEGRAM_CHAT_ID |
| Wrong Timezone | Verify IST timezone on system |
| No Signals | Check backtests - strategy may need tuning |

---

See [ALERTS_GUIDE.md](ALERTS_GUIDE.md) for detailed trading alerts documentation.
