# Swing Trading Assistant

A production-ready Python application for automated stock analysis and trading signal generation using FastAPI, technical indicators, and Telegram notifications.

## Features

✅ **FastAPI REST API** - High-performance web framework with automatic documentation  
✅ **Technical Analysis** - RSI, MACD, and EMA indicators using `ta` library  
✅ **Swing Trading Strategy** - Automated BUY/SELL/HOLD signal generation  
✅ **Telegram Notifications** - Real-time trading alerts  
✅ **Scheduled Analysis** - Hourly stock analysis using APScheduler  
✅ **Docker Support** - Containerized deployment with health checks  
✅ **Comprehensive Logging** - Production-grade logging with file rotation  
✅ **Error Handling** - Graceful API failure handling and recovery  
✅ **Configuration Management** - Environment variable-based configuration  

## Architecture

```
swing-trading-assistant/
├── main.py              # FastAPI application & endpoints
├── strategy.py          # Trading logic & technical analysis
├── data.py              # Stock data fetching (yfinance)
├── notifier.py          # Telegram notifications
├── scheduler.py         # APScheduler background jobs
├── config.py            # Configuration management
├── logger_config.py     # Logging setup
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker image definition
├── docker-compose.yml   # Docker Compose configuration
└── .env.example        # Environment variables template
```

## Installation

### Prerequisites

- Python 3.10+
- Docker & Docker Compose (optional)
- Telegram Bot Token (for notifications)

### Local Setup

1. **Clone and navigate to project**
   ```bash
   cd py01
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your Telegram credentials and settings
   ```

5. **Run application**
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:10000`

### Docker Setup

1. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

2. **Build and run**
   ```bash
   docker-compose up --build
   ```

3. **Access API**
   ```
   http://localhost:10000
   ```

## API Endpoints

### Health Check
```http
GET /health
```
Response:
```json
{
  "status": "OK",
  "message": "Swing Trading Assistant is running"
}
```

### Analyze Stock
```http
GET /analyze/{symbol}
```

Example: `GET /analyze/RELIANCE.NS`

Response:
```json
{
  "symbol": "RELIANCE.NS",
  "signal": "BUY",
  "current_price": 2850.50,
  "rsi": 32.45,
  "macd": 0.0234,
  "macd_signal": 0.0190,
  "ema_50": 2800.00,
  "reason": "RSI (32.45) < 35, Price (2850.50) > EMA50 (2800.00), Bullish MACD crossover"
}
```

### Get Watchlist
```http
GET /watchlist
```

### Get Configuration
```http
GET /config
```

## Trading Strategy

### Buy Conditions
- RSI < 35 (Oversold)
- Current Price > 50-day EMA (Uptrend)
- MACD bullish crossover (Momentum shift)

### Sell Conditions
- RSI > 65 (Overbought)
- MACD bearish crossover (Momentum shift)

### Otherwise
- Hold

## Technical Indicators

| Indicator | Period | Purpose |
|-----------|--------|---------|
| RSI (Relative Strength Index) | 14 | Measures momentum and overbought/oversold conditions |
| MACD (Moving Average Convergence Divergence) | 12,26,9 | Identifies trend direction and momentum |
| EMA (Exponential Moving Average) | 50 | Determines primary trend direction |

## Configuration

Edit `.env` file to customize:

```env
# Trading Parameters
RSI_BUY_THRESHOLD=35          # RSI threshold for buy signal
RSI_SELL_THRESHOLD=65         # RSI threshold for sell signal
EMA_PERIOD=50                 # EMA period in days
RSI_PERIOD=14                 # RSI period in days
STOCK_HISTORY_DAYS=180        # Historical data for analysis

# Scheduler
ANALYZER_INTERVAL_HOURS=1     # Analysis frequency
WATCHLIST=RELIANCE.NS,TCS.NS,INFY.NS

# Telegram
TELEGRAM_TOKEN=your_token     # Telegram bot token
TELEGRAM_CHAT_ID=your_chat_id # Your Telegram chat ID

# Logging
LOG_LEVEL=INFO                # Log level (DEBUG, INFO, WARNING, ERROR)
LOG_FILE=/app/logs/trading.log # Optional log file path
```

## Telegram Setup

1. **Create Bot**
   - Chat with [@BotFather](https://t.me/botfather) on Telegram
   - Use `/newbot` command
   - Get your bot token

2. **Get Chat ID**
   - Start a conversation with your bot
   - Visit: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
   - Find your chat ID from the response

3. **Configure**
   - Add `TELEGRAM_TOKEN` and `TELEGRAM_CHAT_ID` to `.env`

## Logging

Logs are output to console and optionally to a file:

```
2024-04-13 10:30:15 - SwingTrading - INFO - Starting Swing Trading Assistant
2024-04-13 10:30:16 - SwingTrading - INFO - Scheduler started
2024-04-13 10:30:20 - SwingTrading - INFO - Received analysis request for RELIANCE.NS
2024-04-13 10:30:25 - SwingTrading - INFO - Analysis complete for RELIANCE.NS: Signal=BUY
```

## Error Handling

The application handles common failures gracefully:

- **No Data Available**: Returns HOLD signal with explanation
- **API Rate Limits**: Retries with backoff
- **Telegram Unavailable**: Logs error, continues analysis
- **Invalid Symbol**: Returns 400 Bad Request
- **Network Issues**: Graceful degradation with logging

## Performance Considerations

- **Caching**: Stock prices are fetched fresh for each analysis
- **Background Jobs**: Scheduled analysis runs in separate thread
- **Async Operations**: API endpoints are async-ready
- **Resource Usage**: Minimal - runs efficiently in 512MB RAM containers

## Monitoring

### Docker Health Check
```bash
docker-compose ps
```

### View Logs
```bash
# Docker logs
docker-compose logs -f trading-assistant

# Local logs
tail -f logs/trading.log
```

### Check Running Jobs
Access `/docs` endpoint for interactive API documentation:
```
http://localhost:10000/docs
```

## Production Deployment

### Railway, Railway, or Similar

1. Push code to GitHub
2. Connect repository to deployment platform
3. Set environment variables in platform dashboard
4. Deploy using Dockerfile

### AWS, Azure, GCP

```bash
# Build image
docker build -t swing-trading:latest .

# Push to registry
docker tag swing-trading:latest <registry>/swing-trading:latest
docker push <registry>/swing-trading:latest

# Deploy
# Use your platform's container deployment service
```

### Self-Hosted

```bash
# Run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## Troubleshooting

### Telegram Notifications Not Working

```python
# Check logs for Telegram errors
# Verify TELEGRAM_TOKEN and TELEGRAM_CHAT_ID in .env
# Test bot connectivity: curl https://api.telegram.org/bot<TOKEN>/getMe
```

### API Not Responding

```bash
# Check if service is running
curl http://localhost:10000/health

# View logs
docker-compose logs trading-assistant

# Restart service
docker-compose restart
```

### Scheduler Not Running

```python
# Verify in logs: "Scheduler started"
# Check APScheduler jobs: Monitor /analyze/{symbol} calls
```

### High CPU Usage

- Reduce `ANALYZER_INTERVAL_HOURS`
- Reduce number of symbols in `WATCHLIST`
- Increase `STOCK_HISTORY_DAYS` to reduce API calls

## Development

### Adding Custom Indicators

Edit `strategy.py`:

```python
def calculate_indicators(data):
    indicators["your_indicator"] = ta.your_library.your_indicator(...)
    return indicators
```

### Adding New Watchlist Symbols

Edit `.env`:
```env
WATCHLIST=RELIANCE.NS,TCS.NS,INFY.NS,WIPRO.NS
```

### Custom Notification Logic

Edit `notifier.py` to add webhooks, email, SMS, etc.

## Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/

# Test specific endpoint
curl http://localhost:10000/analyze/RELIANCE.NS
```

## Security Considerations

✅ Non-root Docker user  
✅ Environment variables for secrets  
✅ Input validation on API endpoints  
✅ Error messages don't leak sensitive data  
✅ HTTPS ready (use reverse proxy like Nginx)  

## License

MIT License - Feel free to use and modify

## Contributing

Contributions welcome! Areas for improvement:

- [ ] Add RSI divergence detection
- [ ] Implement support levels/resistance
- [ ] Add volume analysis
- [ ] Machine learning signal validation
- [ ] WebSocket support for real-time updates
- [ ] Database for historical signals

## Support

For issues or questions:
1. Check logs: `docker-compose logs -f`
2. Verify `.env` configuration
3. Review API documentation: `http://localhost:10000/docs`

## Disclaimer

This is an educational tool. **Always do your own research** before making investment decisions. Past performance does not guarantee future results. Use at your own risk.

---

Made with ❤️ for traders and developers
