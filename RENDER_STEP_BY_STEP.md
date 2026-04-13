# 🎯 Render Deployment - Step-by-Step Visual Guide

## What You'll Need

- GitHub account (create at https://github.com if you don't have one)
- Telegram account
- Render account (free)
- Your Telegram bot token and chat ID

---

## 📋 Complete Step-by-Step Instructions

### PART 1: GitHub Setup (5 minutes)

#### Step 1.1: Create GitHub Repository

1. Go to https://github.com/new
2. Fill in:
   ```
   Repository name:    swing-trading-bot
   Description:        Automated swing trading alert system
   Public/Private:     Public (unless you prefer private)
   Initialize readme:  ✓ (check)
   ```
3. Click **"Create repository"**

#### Step 1.2: Push Your Code to GitHub

In your terminal:

```bash
# Go to project folder
cd /home/artham/projects/py01

# If not already a git repo
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - swing trading bot"

# Rename main branch
git branch -M main

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/swing-trading-bot.git

# Push code
git push -u origin main
```

✅ Your code is now on GitHub!

---

### PART 2: Prepare Telegram Credentials (5 minutes)

#### Step 2.1: Create Telegram Bot

1. Open Telegram app
2. Search for: `@BotFather`
3. Click to start conversation
4. Send message: `/newbot`
5. Follow the prompts:
   ```
   BotFather asks: "What's the name of your new bot?"
   You answer: swing-trading-bot (or any name)
   
   BotFather asks: "Give your bot a username"
   You answer: swing_trading_bot_USERNAME (must end with _bot)
   ```
6. **Copy the token** that looks like:
   ```
   123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh
   ```
   ✅ Save this as `TELEGRAM_TOKEN`

#### Step 2.2: Get Your Chat ID

1. Go to your new bot (search for it in Telegram)
2. Click **"Start"** button
3. Send any message (e.g., "hi")
4. In your browser, visit:
   ```
   https://api.telegram.org/botINSERT_TOKEN_HERE/getUpdates
   ```
   Replace `INSERT_TOKEN_HERE` with your token
5. Look for this in the response:
   ```json
   "chat": {
     "id": 123456789
   }
   ```
   ✅ Copy the number in `"id"` as `TELEGRAM_CHAT_ID`

---

### PART 3: Deploy on Render (10 minutes)

#### Step 3.1: Create Render Account

1. Go to https://render.com
2. Click **"Sign up"**
3. Choose **"Sign up with GitHub"**
4. Authorize Render to access your GitHub
5. ✅ Account created!

#### Step 3.2: Create New Web Service

1. On Render dashboard, click **"New +"**
2. Select **"Web Service"**
3. Select **"Build and deploy from a Git repository"**
4. Click **"Connect account"** (GitHub)
5. Find and select `swing-trading-bot` repository
6. Click **"Connect"**

#### Step 3.3: Configure Service

Fill in these fields:

**Section 1: Basic Details**
```
Name:              swing-trading-bot
Environment:       Python 3
Region:            Select closest to you
Branch:            main
Build Command:     pip install -r requirements.txt
Start Command:     uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Section 2: Plan**
```
Plan:              Free
```

#### Step 3.4: Add Environment Variables

Click **"Add Environment Variable"** and add each:

**Variable 1:**
```
Key:    TELEGRAM_TOKEN
Value:  (paste your token from Step 2.1)
```

**Variable 2:**
```
Key:    TELEGRAM_CHAT_ID
Value:  (paste your chat ID from Step 2.2)
```

**Variable 3:**
```
Key:    WATCHLIST
Value:  RELIANCE.NS,TCS.NS,INFY.NS
```

#### Step 3.5: Deploy!

1. Scroll down
2. Click **"Create Web Service"**
3. **Wait 2-3 minutes** for deployment
4. Look for green checkmark ✅ and "Live" status

---

### PART 4: Test Your Deployment (2 minutes)

#### Step 4.1: Find Your URL

On Render, you'll see your service URL at the top. It looks like:
```
https://swing-trading-bot.onrender.com
```

#### Step 4.2: Test Health Endpoint

In terminal (or browser):
```bash
curl https://swing-trading-bot.onrender.com/health
```

Should respond:
```json
{"status": "healthy", "timestamp": "..."}
```

#### Step 4.3: Test Alert (Most Important!)

```bash
curl -X POST https://swing-trading-bot.onrender.com/test-market-open-alert
```

✅ **Check your Telegram** - you should get an alert message!

---

### PART 5: Keep Service Alive 24/7 (3 minutes)

⚠️ **Critical:** Without this step, your service sleeps after inactivity!

#### Step 5.1: Sign Up for UptimeRobot

1. Go to https://uptimerobot.com
2. Click **"Sign Up"**
3. Create free account
4. Verify email

#### Step 5.2: Create Monitor

1. Log into UptimeRobot
2. Click **"Add New Monitor"**
3. Fill in:
   ```
   Monitor Type:        HTTP(s)
   Friendly Name:       Swing Trading Bot
   URL:                 https://swing-trading-bot.onrender.com/health
   Monitoring Interval: 5 minutes
   Notification:        Email (optional)
   ```
4. Click **"Create"**

✅ **Your service now stays alive 24/7!**

---

## 🎉 Success Checklist

- [ ] GitHub account created
- [ ] Code pushed to GitHub
- [ ] Telegram bot created
- [ ] Token saved
- [ ] Chat ID saved
- [ ] Render service deployed
- [ ] All environment variables set
- [ ] `/health` endpoint responds
- [ ] Test alert received in Telegram
- [ ] UptimeRobot monitor created

---

## 📊 What Happens Now

### Automatic Daily Alerts

The bot will automatically send:

**9:15 AM IST (Every Trading Day)**
```
🌅 MARKET OPENING ALERT
🟢 BUY: RELIANCE.NS at ₹2850
🔴 SELL: INFY.NS at ₹1800
(and more...)
```

**Every Hour During Market**
```
🟢 SWING TRADE ALERT: BUY
Symbol: RELIANCE.NS
Entry: ₹2850.50
Target: ₹2997.03
Stop Loss: ₹2764.98
```

**3:30 PM IST (Every Trading Day)**
```
🌆 MARKET CLOSING ALERT
Buy Signals: 3
Sell Signals: 2
See you tomorrow!
```

---

## 🔧 Manual API Calls

After deployment, you can test any endpoint:

```bash
# Check market status
curl https://swing-trading-bot.onrender.com/market-status

# Analyze a stock
curl https://swing-trading-bot.onrender.com/analyze/RELIANCE.NS

# Get watchlist
curl https://swing-trading-bot.onrender.com/watchlist

# Backtest
curl https://swing-trading-bot.onrender.com/backtest/RELIANCE.NS

# Test individual stock alert
curl -X POST "https://swing-trading-bot.onrender.com/test-trading-alert/TCS.NS?signal=BUY"
```

---

## 📞 Troubleshooting

### Deployment Failed

**Check Logs:**
1. Render Dashboard
2. Your service
3. Click **"Logs"** tab
4. Look for error messages

**Common Issues:**
- Missing Python dependencies → Add to `requirements.txt`
- Wrong start command → Check spelling
- GitHub not connected → Reconnect in settings

### Test Alert Shows Error

**Solution:**
1. Verify TELEGRAM_TOKEN is 100% correct
2. Verify TELEGRAM_CHAT_ID is numeric only
3. Send message to bot first
4. Try again

### Service Keeps Showing as "Not Running"

1. Check Render logs for errors
2. Try manual deploy: Render Dashboard → Manual Deploy
3. Check environment variables are set
4. Verify GitHub repo is accessible

### Can't Connect to GitHub

1. Go to Render Settings
2. Click "Connected Services"
3. Reconnect GitHub
4. Authorize again

---

## 💡 Pro Tips

1. **Monitor your service:** Check Render logs daily
2. **Test regularly:** Use health endpoint
3. **Keep UptimeRobot running:** It's free and critical
4. **Update code:** Push to GitHub → Render auto-redeploys
5. **Review alerts:** Check Telegram daily for signals

---

## 📈 Next Steps After Deployment

1. ✅ Verify alerts arrive at 9:15 AM
2. ✅ Review trading signals throughout the day
3. ✅ Execute trades based on alerts
4. ✅ Check closing alert at 3:30 PM
5. ✅ Backtest strategy
6. ✅ Add more stocks to watchlist
7. ✅ Optimize parameters

---

## 🎓 Video Guides (Alternative)

If you prefer videos:
- Render deployment: Search "Deploy Python to Render"
- GitHub setup: Search "GitHub first time setup"
- Telegram bot: Search "Create Telegram bot BotFather"

---

## 📚 Documentation

See these files for more info:
- [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) - Complete guide
- [RENDER_QUICK_START.md](RENDER_QUICK_START.md) - Quick reference
- [API_REFERENCE.md](API_REFERENCE.md) - All endpoints
- [ALERTS_GUIDE.md](ALERTS_GUIDE.md) - Alert details

---

## ✅ You're Ready!

Your swing trading bot is now deployed for FREE on Render!

**Next:** Monitor your alerts and trade with confidence! 🚀

---

Questions? Stuck somewhere? Refer back to the relevant troubleshooting section!
