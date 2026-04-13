# 🚀 Deploy on Render (Free Tier)

## Overview

Deploy your swing trading assistant on **Render's free tier** for free hosting!

**Free Tier Limits:**
- ✅ Always running
- ✅ 0.5GB RAM
- ✅ Shared CPU
- ⚠️ Puts to sleep after 15 min inactivity (we'll fix this)

---

## Step 1: Prepare GitHub Repository

### Option A: If You Already Have Git Repo

```bash
cd /home/artham/projects/py01
git add .
git commit -m "Deploy to Render"
git push origin main
```

### Option B: Create New GitHub Repo

1. Go to https://github.com/new
2. Create repo: `swing-trading-bot`
3. In your project folder:

```bash
cd /home/artham/projects/py01
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/swing-trading-bot.git
git push -u origin main
```

---

## Step 2: Set Up Render Account

1. Go to https://render.com
2. Sign up (free account)
3. Click **"New +"** → **"Web Service"**

---

## Step 3: Connect GitHub

1. Select **"Build and deploy from a Git repository"**
2. Click **"Connect account"** (GitHub)
3. Authorize Render to access your repos
4. Select your `swing-trading-bot` repository
5. Click **"Connect"**

---

## Step 4: Configure Service

Fill in the following:

### Basic Settings
```
Service Name:     swing-trading-bot
Environment:      Python 3
Plan:             Free (stays running!)
Region:           Choose closest to you
Build Command:    pip install -r requirements.txt
Start Command:    uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Environment Variables
Click **"Add Environment Variable"** for each:

```
TELEGRAM_TOKEN       → (Get from @BotFather on Telegram)
TELEGRAM_CHAT_ID     → (Get from getUpdates API)
WATCHLIST            → RELIANCE.NS,TCS.NS,INFY.NS
```

**How to get these:**

#### Get TELEGRAM_TOKEN:
1. Chat with [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot`
3. Follow prompts
4. Copy the token (looks like: `123456:ABCDEFghijklmnop`)

#### Get TELEGRAM_CHAT_ID:
1. Send any message to your bot
2. Visit: `https://api.telegram.org/botTOKEN/getUpdates` (replace TOKEN)
3. Find `chat.id` in response
4. Copy that number

---

## Step 5: Deploy

1. Click **"Create Web Service"**
2. Wait for deployment (2-3 minutes)
3. View logs - should see: `✅ Uvicorn running`

---

## Step 6: Test on Render

Once deployed, you'll get a URL like:
```
https://swing-trading-bot.onrender.com
```

### Test Health
```bash
curl https://swing-trading-bot.onrender.com/health
```

### Test Market Status
```bash
curl https://swing-trading-bot.onrender.com/market-status
```

### Test Alert (Most Important!)
```bash
curl -X POST https://swing-trading-bot.onrender.com/test-market-open-alert
```

✅ Check Telegram - you should receive an alert!

---

## ⚠️ Important: Keep Service Awake

Render's free tier spins down after 15 minutes of inactivity. To keep it running:

### Solution 1: Use UptimeRobot (Recommended)

1. Go to https://uptimerobot.com
2. Sign up (free)
3. Click **"Add New Monitor"**
4. Select **"HTTP(s)"**
5. Fill in:
```
Friendly Name:  Swing Trading Bot
URL:            https://swing-trading-bot.onrender.com/health
Monitoring Interval: 5 minutes (keep alive)
```
6. Click **"Create Monitor"**

✅ Now your service stays awake 24/7!

---

### Solution 2: Manual Curl (Alternative)

Run this periodically from your local machine:
```bash
#!/bin/bash
while true; do
  curl https://swing-trading-bot.onrender.com/health
  sleep 300  # Every 5 minutes
done
```

---

## 📊 Important Limitations on Free Tier

| Feature | Free Tier | Notes |
|---------|-----------|-------|
| API Requests | Unlimited | You can make many requests ✅ |
| Background Jobs | ❌ Limited | Scheduler works but may delay |
| Database | ❌ Not included | Not needed for this app |
| Bandwidth | Unlimited | ✅ Good for alerts |
| Uptime SLA | No guarantee | May go down occasionally |
| Restart | Automatic | Happens regularly |

**Critical:** The scheduled tasks (9:15 AM, 3:30 PM alerts) may NOT run reliably on free tier due to restarts.

---

## ✅ Better Alternative: Production-Ready Setup

For reliable scheduled alerts, upgrade to Render **Starter ($7/month)**:

1. On Render Dashboard
2. Select your service
3. Click **"Settings"**
4. Click **"Change Plan"**
5. Select **"Starter"** ($7/month)

✅ Guaranteed uptime  
✅ Reliable scheduling  
✅ Better performance

---

## 📱 Alternative: Deploy on Railway or Replit

### Railway
1. Go to https://railway.app
2. Sign up with GitHub
3. Connect your repo
4. Let it auto-detect (Python)
5. Add environment variables
✅ Free tier: $5 credit/month

### Replit
1. Go to https://replit.com
2. Import from GitHub
3. Set environment variables
4. Click **"Run"**
✅ Free tier available

---

## 🔧 Environment Variables Checklist

Before deploying, get these ready:

- [ ] **TELEGRAM_TOKEN** - From @BotFather
- [ ] **TELEGRAM_CHAT_ID** - From getUpdates API
- [ ] **WATCHLIST** - Comma-separated stocks
- [ ] **README**:
  - Default watchlist: RELIANCE.NS,TCS.NS,INFY.NS
  - Market hours: 9:15 AM - 3:30 PM IST
  - Timezone: Asia/Kolkata

---

## 📋 Deployment Checklist

**Before Deploying:**
- [ ] GitHub repo created and pushed
- [ ] Render account created
- [ ] TELEGRAM_TOKEN ready
- [ ] TELEGRAM_CHAT_ID ready
- [ ] render.yaml file ready

**During Deployment:**
- [ ] Service name: `swing-trading-bot`
- [ ] Environment set to Python 3
- [ ] All env vars added
- [ ] Start command correct

**After Deployment:**
- [ ] ✅ Health endpoint works
- [ ] ✅ Market status works
- [ ] ✅ Test alert sends to Telegram
- [ ] ✅ UptimeRobot configured (keep awake)

---

## 🎯 Using Your Deployed App

### API URL
```
https://swing-trading-bot.onrender.com
```

### Test Endpoints
```bash
# Health
curl https://swing-trading-bot.onrender.com/health

# Market Status
curl https://swing-trading-bot.onrender.com/market-status

# Analyze Stock
curl https://swing-trading-bot.onrender.com/analyze/RELIANCE.NS

# Test Alert
curl -X POST https://swing-trading-bot.onrender.com/test-market-open-alert
```

### From Local Code
```python
import requests

API_URL = "https://swing-trading-bot.onrender.com"

# Get market status
status = requests.get(f"{API_URL}/market-status").json()
print(status)

# Send test alert
response = requests.post(f"{API_URL}/test-market-open-alert").json()
print(response)
```

---

## 📞 Troubleshooting

### Service Won't Start
1. Check logs: **Logs** tab in Render
2. Look for error messages
3. Common issues:
   - Missing TELEGRAM_TOKEN env var
   - Python version mismatch
   - Missing dependencies

### Logs Show "ModuleNotFoundError"
- Solution: Add missing module to requirements.txt
- Push to GitHub
- Render auto-redeploys

### Alerts Not Sending
1. Test locally first: `curl -X POST http://localhost:10000/test-market-open-alert`
2. Verify TELEGRAM_TOKEN is correct
3. Verify TELEGRAM_CHAT_ID is correct
4. Check Render logs for errors

### Service Sleeping / Not Responding
1. Set up UptimeRobot to keep it alive
2. Or upgrade to Starter plan ($7/month)

---

## 💰 Cost Analysis

| Plan | Price | Limits |
|------|-------|--------|
| Free | $0 | May sleep if inactive |
| Starter | $7/month | Always running ✅ |
| Standard | $12/month | Better performance |

**Recommendation:** Start free, upgrade to Starter if you need reliability.

---

## 🚀 Quick Deploy Command (If Already on Render)

After first deployment, redeploy with:
```bash
git push origin main  # Render auto-deploys on push
```

---

## 📈 Monitor Your Deployment

1. Go to Render Dashboard
2. Click your service
3. View:
   - **Logs** - Real-time events
   - **Metrics** - CPU, RAM usage
   - **Events** - Deployment history
   - **Settings** - Configuration

---

## ✅ Success Checklist

- [ ] Repository pushed to GitHub
- [ ] Service deployed on Render
- [ ] All environment variables set
- [ ] Health endpoint responds ✅
- [ ] Test alert receives in Telegram ✅
- [ ] UptimeRobot keeping service awake ✅

**Congratulations! You're deployed on the cloud!** 🎉

---

## 📚 Next Steps

1. **Set up notification service:**
   - Use UptimeRobot to keep alive
   - Or upgrade to Starter plan

2. **Monitor alerts:**
   - Check Telegram daily
   - Review trading signals

3. **Optimize:**
   - Add more stocks to watchlist
   - Adjust trading parameters
   - Upgrade to paid plan if needed

---

## 🎨 Render Dashboard Tips

- **View logs in real-time** - Click "Logs" tab
- **Check resource usage** - CPU, RAM, disk
- **Redeploy** - Click "Manual Deploy"
- **Update env vars** - Click "Environment"
- **Change plan** - Click "Settings" → "Plan"

---

Made with ❤️ for free hosting | Questions? See troubleshooting above! 🚀
