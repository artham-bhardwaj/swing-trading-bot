# Automated Trading Alerts & Market Notifications

## 🚨 Overview

The swing trading assistant now sends **detailed automated Telegram alerts** every trading day:

✅ **Market Opening Alert** (9:15 AM IST)  
✅ **Market Closing Alert** (3:30 PM IST)  
✅ **Real-time Trading Signals** (Every hour during market)  
✅ **Specific Price Targets** (For each BUY/SELL signal)  

---

## 📍 Trading Hours (IST - Indian Standard Time)

| Event | Time | Days |
|-------|------|------|
| 🌅 Market Opens | 09:15 AM IST | Monday-Friday |
| 📊 Periodic Analysis | Every 1 hour | During market hours |
| 🌆 Market Closes | 03:30 PM IST | Monday-Friday |

**Note:** The system is automatically aware of weekends and doesn't send alerts on Saturdays/Sundays.

---

## 📨 Alert Types

### 1️⃣ **Market Opening Alert** (Every Day at 9:15 AM)

Sent as the market opens with all recommended trades for the day.

**Content:**
```
🌅 MARKET OPENING ALERT
Time: 09:15 AM IST
Date: Monday, April 14, 2026

🟢 BUY RECOMMENDATIONS
  • RELIANCE.NS
    Entry: ₹2850.50 | Target: ₹2997.03 | Stop: ₹2764.98

  • TCS.NS
    Entry: ₹3500.00 | Target: ₹3675.00 | Stop: ₹3395.00

🔴 SELL RECOMMENDATIONS
  • INFY.NS
    Exit: ₹1800.00 | Target: ₹1710.00 | Stop: ₹1854.00

⏸️ HOLD/MONITOR
  • Other stocks...

⏰ MARKET HOURS
Open: 09:15 AM | Close: 03:30 PM IST

💡 TIP: Follow the signals closely. Set alerts for target and stop-loss prices.
🚀 Good luck with your swing trades today!
```

---

### 2️⃣ **Real-time Trading Signals** (Every Hour During Market)

Sent whenever a strong BUY or SELL signal is generated.

**Content:**
```
🟢 SWING TRADE ALERT: BUY
Symbol: RELIANCE.NS
Time: 13:45:32

📊 CURRENT PRICE
Price: ₹2850.50

📈 TECHNICAL INDICATORS
RSI (14): 32.45
MACD: 0.0234
EMA (50): ₹2800.00
Signal Line: 0.0190

🎯 BUY STRATEGY
Entry Price: ₹2850.50
Stop Loss: ₹2764.98 (-3% = ₹85.52)
Target 1: ₹2997.03 (+5.14%)
Target 2: ₹2997.03 (+5.14%)

📋 ANALYSIS
RSI (32.45) < 35, Price (2850.50) > EMA50 (2800.00), Bullish MACD crossover

⏰ SWING TRADE TIP
Hold position until target or stop loss hit
```

**For SELL signals:**
```
🔴 SWING TRADE ALERT: SELL
Symbol: TCS.NS
Time: 14:30:15

Exit Price: ₹3500.00
Stop Loss: ₹3605.00
Target 1: ₹3395.00 (-2.86%)
Target 2: ₹3325.00 (-5.00%)

📋 ANALYSIS
RSI (68.50) > 65, Bearish MACD crossover

⏰ SWING TRADE TIP
Exit position or reduce holdings
```

---

### 3️⃣ **Market Closing Alert** (Every Day at 3:30 PM)

Summary of the day's trading activity and tomorrow's plan.

**Content:**
```
🌆 MARKET CLOSING ALERT
Time: 03:30 PM IST
Date: Monday, April 14, 2026

📊 TODAY'S SIGNALS SUMMARY
Buy Signals: 3 | Sell Signals: 2 | Hold: 1

🟢 STOCKS TO BUY
  RELIANCE.NS: ₹2850.50
  TCS.NS: ₹3500.00
  WIPRO.NS: ₹650.75

🔴 STOCKS TO SELL
  INFY.NS: ₹1800.00
  SBIN.NS: ₹520.25

📋 TOMORROW'S PLAN
• Review today's trades
• Check positions
• Market opens at 09:15 AM tomorrow

🌙 Good evening! See you tomorrow at market open!
```

---

## 🎯 Price Targets Explained

### For BUY Signals:
```
Entry Price: ₹100.00

Target 1: ₹103.00 (+3%)    - Quick profit booking
Target 2: ₹105.00 (+5%)    - Extended target
Stop Loss: ₹97.00  (-3%)   - Risk management
```

### For SELL Signals:
```
Exit Price: ₹100.00

Target 1: ₹97.00 (-3%)     - Quick exit profit
Target 2: ₹95.00 (-5%)     - Extended exit
Stop Loss: ₹103.00 (+3%)   - Risk management
```

---

## 🧪 Testing the Alerts

### Test Market Opening Alert
```bash
curl -X POST http://localhost:10000/test-market-open-alert
```

Response:
```json
{
  "status": "sent",
  "alert_type": "market_open",
  "stocks_analyzed": 3,
  "message": "Market opening alert sent to Telegram"
}
```

### Test Market Closing Alert
```bash
curl -X POST http://localhost:10000/test-market-close-alert
```

### Test Individual Stock Alert
```bash
# BUY Signal
curl -X POST "http://localhost:10000/test-trading-alert/RELIANCE.NS?signal=BUY"

# SELL Signal
curl -X POST "http://localhost:10000/test-trading-alert/TCS.NS?signal=SELL"

# HOLD
curl -X POST "http://localhost:10000/test-trading-alert/INFY.NS?signal=HOLD"
```

---

## 📅 Sample Daily Schedule

```
09:15 AM IST  → 🌅 Market Opens
              → 🟢 Detailed opening analysis
              → 📊 BUY/SELL recommendations for the day

10:15 AM IST  → 📈 Periodic analysis (every hour)
11:15 AM IST  → 📈 If signal found, immediate alert sent
12:15 PM IST  → 📈 Continuous monitoring
01:15 PM IST  → 📈 More opportunities analyzed
02:15 PM IST  → 📈 Keep watching

03:30 PM IST  → 🌆 Market Closes
              → 🔴 Final analysis summary
              → 📋 Tomorrow's plan
```

---

## 🎨 Alert Features

### ✅ What You Get in Each Alert:

1. **Signal Type:** 🟢 BUY, 🔴 SELL, or ⏸️ HOLD
2. **Current Price:** Real market price
3. **Entry/Exit Price:** Where to execute
4. **Stop Loss:** Risk management price
5. **Target Prices:** Where to take profit
6. **Technical Indicators:**
   - RSI (14) - Momentum
   - MACD - Trend confirmation
   - EMA (50) - Direction

7. **Detailed Reasoning:** Why this signal?
8. **Time & Date:** When was this analyzed?
9. **Trading Tips:** How to follow up

---

## 📱 Setting Up Telegram Alerts

### Step 1: Get Telegram Token
1. Chat with [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot`
3. Follow prompts to create a bot
4. Copy the token

### Step 2: Get Your Chat ID
1. Start conversation with your bot
2. Send any message to your bot
3. Visit: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
4. Find your `chat_id`

### Step 3: Configure
Edit `.env`:
```env
TELEGRAM_TOKEN=123456:ABCDEFghijklmnop
TELEGRAM_CHAT_ID=9876543210
```

### Step 4: Restart
```bash
python main.py
```

---

## 📊 Understanding the Alerts

### RSI Levels
- **RSI < 35:** Oversold → Possible BUY signal
- **RSI 35-65:** Neutral → Possible entry/exit
- **RSI > 65:** Overbought → Possible SELL signal

### MACD Signals
- **Bullish Crossover:** MACD crosses above signal line → BUY
- **Bearish Crossover:** MACD crosses below signal line → SELL

### EMA Confirmation
- **Price > 50 EMA:** Uptrend (favor buys)
- **Price < 50 EMA:** Downtrend (favor sells)

---

## 🚀 Automatic Scheduling

The system automatically:

1. ✅ Checks the time (IST)
2. ✅ Verifies it's a market day (Mon-Fri)
3. ✅ Sends 9:15 AM opening alert with all signals
4. ✅ Analyzes every hour for new signals
5. ✅ Sends real-time alerts on BUY/SELL
6. ✅ Sends 3:30 PM closing summary
7. ✅ Skips weekends automatically

---

## 📋 All Available Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/market-status` | GET | Current market status & timings |
| `/test-market-open-alert` | POST | Test morning alert |
| `/test-market-close-alert` | POST | Test evening alert |
| `/test-trading-alert/{symbol}` | POST | Test individual stock alert |
| `/health` | GET | Server status |
| `/demo` | GET | Demo analysis |
| `/analyze/{symbol}` | GET | Real-time analysis |

---

## 💡 Tips for Best Results

1. **Set Telegram Notifications:** Don't miss morning/evening alerts
2. **Review Entry Prices:** Execute at recommended entry, not market price
3. **Use Stop Loss:** Always protect with stop loss
4. **Take Partial Profits:** Sell half at target 1, rest at target 2
5. **Check Market Hours:** Trading only 9:15 AM - 3:30 PM IST
6. **Monitor Continuously:** Check alerts throughout the day

---

## 🛑 Stop Loss & Target Examples

### Example 1: RELIANCE.NS
```
Entry:       ₹2850.00
Stop Loss:   ₹2764.50 (-3% = ₹85.50)
Target 1:    ₹2997.00 (+5.14%)
Target 2:    ₹2997.00 (+5.14%)
```

### Example 2: TCS.NS
```
Entry:       ₹3500.00
Stop Loss:   ₹3395.00 (-3%)
Target 1:    ₹3605.00 (+3%)
Target 2:    ₹3675.00 (+5%)
```

---

## 📞 Troubleshooting

### Alerts Not Received?
- Check TELEGRAM_TOKEN is correct
- Verify TELEGRAM_CHAT_ID
- Ensure bot is not blocked
- Test: `curl -X POST http://localhost:10000/test-market-open-alert`

### Wrong Time Alerts?
- System uses **IST (India Standard Time)**
- Adjust your system time zone
- Check market status: `curl http://localhost:10000/market-status`

### Missing Signals?
- Check your watchlist: `curl http://localhost:10000/watchlist`
- Test analysis: `curl http://localhost:10000/demo`
- Review logs: `docker-compose logs -f`

---

## 🎯 Quick Start

### 1. Verify System Running
```bash
curl http://localhost:10000/health
```

### 2. Test Alerts
```bash
curl -X POST http://localhost:10000/test-market-open-alert
```

### 3. Check Market Status
```bash
curl http://localhost:10000/market-status
```

### 4. Monitor Logs
```bash
docker-compose logs -f
# or
tail -f logs/trading.log
```

---

## 🌟 Success Indicators

✅ Alerts sent at 9:15 AM every trading day  
✅ Real-time signals during market hours  
✅ Closing alert at 3:30 PM every day  
✅ Price targets and stop losses included  
✅ No alerts on weekends  
✅ Detailed reasoning for each signal  

---

## 📈 Swing Trading Tips

- **Small Position Size:** Risk 1-2% per trade
- **Use Limit Orders:** Don't chase prices
- **Follow Targets:** Avoid emotional trades
- **Honor Stop Loss:** Protect capital
- **Track Records:** Log all trades
- **Review Daily:** Learn from results

---

Made with ❤️ for swing traders who want precise alerts and execution strategies
