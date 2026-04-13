# Testing & Backtesting Guide

## 🚀 Now Available Features

After the latest update, the swing trading assistant now has:

✅ **Live Analysis** - Real stock data Analysis (when API available)  
✅ **Demo Mode** - Synthetic data for testing  
✅ **Backtesting** - Validate strategy on historical data  
✅ **Portfolio Testing** - Test entire watchlist at once  
✅ **Auto Fallback** - Demo data when API fails  

---

## 📊 New API Endpoints

### 1. **Demo Analysis** (Works Offline!)
Generate trading signals with synthetic data:

```bash
curl http://localhost:10000/demo | python3 -m json.tool
```

**Response:**
```json
{
  "timestamp": "2026-04-13T23:27:45.217981",
  "mode": "DEMO",
  "results": {
    "RELIANCE.NS": {
      "signal": "BUY/SELL/HOLD",
      "current_price": 2850.50,
      "rsi": 32.45,
      "note": "DEMO DATA - For testing only"
    }
  }
}
```

**Use Case:** Test the application without needing real market data

---

### 2. **Backtest Single Stock**
Validate strategy on historical data for one stock:

```bash
curl "http://localhost:10000/backtest/RELIANCE.NS?days=180" | python3 -m json.tool
```

**Parameters:**
- `symbol`: Stock symbol (RELIANCE.NS, AAPL, etc.)
- `days`: Historical days (default: 180)

**Response:**
```json
{
  "symbol": "RELIANCE.NS",
  "start_date": "2025-10-16T00:00:00",
  "end_date": "2026-04-13T00:00:00",
  "num_trades": 15,
  "winning_trades": 10,
  "losing_trades": 5,
  "win_rate": 66.67,
  "total_return_pct": 12.45,
  "max_drawdown_pct": -8.32,
  "trades": [
    {
      "entry_date": "2025-10-20",
      "entry_price": 2800.00,
      "exit_date": "2025-11-05",
      "exit_price": 2850.00,
      "return_pct": 1.79,
      "profit": 1785.71
    }
  ]
}
```

**Metrics Explained:**
- `num_trades`: Total number of trades executed
- `winning_trades`: Profitable trades
- `losing_trades`: Losing trades
- `win_rate`: Percentage of profitable trades
- `total_return_pct`: Total return on initial capital
- `max_drawdown_pct`: Largest peak-to-trough decline

---

### 3. **Backtest Portfolio**
Test strategy on all watchlist symbols:

```bash
curl "http://localhost:10000/backtest-portfolio?days=90" | python3 -m json.tool
```

**Parameters:**
- `days`: Historical days (default: 180)

**Response:**
```json
{
  "backtest_date": "2026-04-13T23:28:04.177321",
  "watchlist": ["RELIANCE.NS", "TCS.NS", "INFY.NS"],
  "days": 90,
  "results": {
    "RELIANCE.NS": { ... },
    "TCS.NS": { ... },
    "INFY.NS": { ... }
  }
}
```

---

## 🧪 Testing Scenarios

### Scenario 1: Test Without Internet
```bash
# API is down? No problem! Use demo mode
curl http://localhost:10000/demo

# Analysis automatically uses demo data
curl http://localhost:10000/analyze/AAPL
```

### Scenario 2: Validate Strategy on Past Data
```bash
# Test if strategy would have worked in the past 6 months
curl "http://localhost:10000/backtest/RELIANCE.NS?days=180"

# Check results - look for:
# - win_rate > 50%
# - total_return_pct > 0%
# - max_drawdown_pct not too large
```

### Scenario 3: Compare Strategies
Test different timeframes:

```bash
# Test 3 months
curl "http://localhost:10000/backtest/RELIANCE.NS?days=90"

# Test 6 months
curl "http://localhost:10000/backtest/RELIANCE.NS?days=180"

# Test 1 year
curl "http://localhost:10000/backtest/RELIANCE.NS?days=365"

# Compare results to see which period performed best
```

### Scenario 4: Full Portfolio Analysis
```bash
# Backtest all stocks at once
curl "http://localhost:10000/backtest-portfolio?days=180"

# Check which stocks performed best
# Review individual win rates
```

---

## 📈 Example: Complete Testing Workflow

```bash
# 1. Check if everything is running
curl http://localhost:10000/health

# 2. Get current configuration
curl http://localhost:10000/config

# 3. Test with demo data
curl http://localhost:10000/demo

# 4. Analyze a real stock (if API available, otherwise uses demo)
curl http://localhost:10000/analyze/RELIANCE.NS

# 5. Backtest the strategy
curl "http://localhost:10000/backtest/RELIANCE.NS?days=180"

# 6. Check portfolio performance
curl http://localhost:10000/backtest-portfolio?days=180

# 7. View docs in browser
http://localhost:10000/docs
```

---

## 🔄 Auto-Fallback Mechanism

The application now automatically falls back to demo data when:

1. **Yahoo Finance API fails** → Uses synthetic data
2. **Network timeout** → Generates local data
3. **Invalid symbol** → Creates demo data for that symbol

**No crashes, no errors** - always returns valid analysis!

---

## 📊 How to Interpret Backtest Results

| Metric | Good | Acceptable | Poor |
|--------|------|-----------|------|
| Win Rate | > 60% | 50-60% | < 50% |
| Total Return | > 15% | 0-15% | < 0% |
| Max Drawdown | < -5% | -5% to -15% | < -15% |
| Trades | 10-30 | 5-10 | < 5 |

---

## 🛠️ Customizing for Your Needs

### Make Strategy More Aggressive
Edit `.env`:
```env
RSI_BUY_THRESHOLD=40      # Higher = more buy signals
RSI_SELL_THRESHOLD=60     # Lower = more sell signals
```

Then backtest:
```bash
curl "http://localhost:10000/backtest/RELIANCE.NS?days=180"
```

### Test Different Signals
Edit `strategy.py` and modify the `BUY/SELL/HOLD` conditions, then:
```bash
# Restart app
python main.py

# Run backtest again
curl "http://localhost:10000/backtest/RELIANCE.NS?days=180"
```

---

## 🐳 Files Updated

- ✅ `backtest.py` - Backtesting engine
- ✅ `demo_data.py` - Synthetic data generator
- ✅ `data.py` - Added fallback to demo data
- ✅ `main.py` - Added 3 new endpoints
- ✅ `requirements.txt` - Added numpy

---

## 📋 All Available Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Server status |
| `/analyze/{symbol}` | GET | Analyze a stock |
| `/watchlist` | GET | Current watchlist |
| `/config` | GET | Strategy config |
| `/demo` | GET | Demo analysis |
| `/backtest/{symbol}` | GET | Single stock backtest |
| `/backtest-portfolio` | GET | Portfolio backtest |
| `/docs` | GET | Interactive API docs |

---

## 🧠 Key Improvements

| Feature | Before | After |
|---------|--------|-------|
| Works offline | ❌ | ✅ API fails → demo data |
| Can test strategy | ❌ | ✅ Full backtesting |
| Sees past performance | ❌ | ✅ Historical analysis |
| Handles failures | ✋ Crashes | ✅ Gracefully continues |

---

## 🚀 Next Steps

1. **Test Demo Mode:**
   ```bash
   curl http://localhost:10000/demo
   ```

2. **Backtest Your Strategy:**
   ```bash
   curl "http://localhost:10000/backtest-portfolio?days=180"
   ```

3. **Adjust Parameters:**
   Edit `.env` to fine-tune thresholds

4. **Run Live:**
   ```bash
   # Scheduler will run every hour
   # Check `/docs` for real-time updates
   ```

5. **Monitor Performance:**
   ```bash
   docker-compose logs -f
   # or
   tail -f logs/trading.log
   ```

---

## ⚡ Quick Command Reference

```bash
# Health check
curl http://localhost:10000/health

# Demo (works without API)
curl http://localhost:10000/demo

# Single backtest
curl "http://localhost:10000/backtest/AAPLRELIANCE.NS"

# Portfolio backtest (3 months)
curl "http://localhost:10000/backtest-portfolio?days=90"

# Portfolio backtest (6 months)
curl "http://localhost:10000/backtest-portfolio?days=180"

# Interactive docs
http://localhost:10000/docs
```

---

## 🎯 Success Indicators

✅ `/health` returns OK  
✅ `/demo` shows trading signals  
✅ `/backtest` shows trades completed  
✅ `/backtest-portfolio` shows all results  
✅ Scheduler logs show hourly analysis  
✅ Telegram receives signals (when available)  

Everything working! 🎉

---

Made with ❤️ for traders who want confidence in their strategies
