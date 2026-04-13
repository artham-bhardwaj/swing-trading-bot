# Quick Start Guide

## 1. Get Telegram Credentials (2 minutes)

### Create Telegram Bot
1. Open Telegram and search for **@BotFather**
2. Send `/newbot`
3. Follow the prompts to create your bot
4. **Copy the token** (save it)

### Get Your Chat ID
1. Start a conversation with your bot
2. Send any message to your bot
3. Visit this URL in your browser:
   ```
   https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
   ```
   Replace `<YOUR_TOKEN>` with your bot token
4. Look for `"chat":{"id":<NUMBER>}` - **Copy this number**

## 2. Configure Environment (1 minute)

### Method A: Using .env file

```bash
cp .env.example .env
```

Edit `.env` and add your Telegram credentials:
```env
TELEGRAM_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

### Method B: Using Docker environment

When running Docker, pass environment variables:
```bash
docker run -e TELEGRAM_TOKEN=xxx -e TELEGRAM_CHAT_ID=yyy ...
```

## 3. Run Locally (Linux/Mac)

### One-command startup:
```bash
bash start.sh
```

This will:
- ✅ Create virtual environment
- ✅ Install dependencies
- ✅ Start the server

Server will be available at: `http://localhost:10000`

## 3. Run Locally (Windows)

### One-command startup:
```bash
start.bat
```

## 4. Run with Docker

### Quick start:
```bash
docker-compose up --build
```

### View logs:
```bash
docker-compose logs -f
```

### Stop:
```bash
docker-compose down
```

## 5. Test the API

### Health check:
```bash
curl http://localhost:10000/health
```

### Analyze a stock:
```bash
curl http://localhost:10000/analyze/RELIANCE.NS
```

### View API documentation (Interactive):
Open in browser: `http://localhost:10000/docs`

## 6. Customize Watchlist

Edit `.env`:
```env
WATCHLIST=RELIANCE.NS,TCS.NS,INFY.NS,WIPRO.NS,SBIN.NS
```

The scheduler will analyze these stocks every hour.

## 7. Customize Trading Parameters

Edit `.env` to fine-tune the strategy:

```env
# When to BUY (RSI must be BELOW this)
RSI_BUY_THRESHOLD=35

# When to SELL (RSI must be ABOVE this)
RSI_SELL_THRESHOLD=65

# Moving average period
EMA_PERIOD=50
RSI_PERIOD=14

# How much historical data to fetch
STOCK_HISTORY_DAYS=180
```

## Typical Workflow

```
1. Start application
   ↓
2. API runs on http://localhost:10000
   ↓
3. Scheduler starts in background
   ↓
4. Every 1 hour: Analyzes RELIANCE.NS, TCS.NS, INFY.NS
   ↓
5. If BUY or SELL signal: Sends Telegram message
   ↓
6. You get notified with detailed analysis
```

## Example Telegram Message

When a BUY signal is generated:

```
📈 BUY Signal for RELIANCE.NS

Current Price: ₹2850.50
RSI (14): 32.45
MACD: 0.0234
Signal Line: 0.0190
EMA (50): ₹2800.00

Reason:
RSI (32.45) < 35, Price (2850.50) > EMA50 (2800.00), Bullish MACD crossover
```

## Troubleshooting

### "No data retrieved for symbol"
- Symbol might be invalid
- Try: RELIANCE.NS, TCS.NS, INFY.NS (Indian stocks)
- Or: AAPL, GOOGL, MSFT (US stocks)

### "Telegram messages not being sent"
- Check: TELEGRAM_TOKEN is correct
- Check: TELEGRAM_CHAT_ID is correct
- Verify bot is not blocked

### "API not responding"
```bash
# Check if service is running
curl http://localhost:10000/health

# View logs
docker-compose logs trading-assistant
```

### "TA library not found"
```bash
pip install ta
```

## Next Steps

1. ✅ Start trading with automated signals
2. 📊 Monitor analysis results via API
3. 🔔 Receive Telegram notifications
4. 📈 Backtest different parameters
5. 🚀 Deploy to cloud (Railway, AWS, etc.)

## Getting Help

- 📖 Full docs: See README.md
- 🐳 Docker issues: Check docker-compose.yml
- 📊 API docs: Visit http://localhost:10000/docs
- 🔍 Logs: Check console output or logs/trading.log

## Production Checklist

- [ ] Change RSI_BUY_THRESHOLD and RSI_SELL_THRESHOLD based on backtesting
- [ ] Add more symbols to WATCHLIST
- [ ] Enable LOG_FILE for persistent logging
- [ ] Set LOG_LEVEL=WARNING in production
- [ ] Use reverse proxy (Nginx) for HTTPS
- [ ] Monitor health check: /health endpoint
- [ ] Set up error alerts

Happy trading! 📈
