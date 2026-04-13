# 🚀 DEPLOY NOW - 3 Simple Steps

## ✅ Step 1: Git Ready (DONE!)
```bash
✅ Repository initialized
✅ All files committed and ready
✅ Ready for GitHub push
```

---

## 📋 Step 2: Create GitHub Repo & Push (5 minutes)

### Part A: Create Empty Repo on GitHub

1. Go to **https://github.com/new**
2. Fill in:
   ```
   Repository name:  swing-trading-bot
   Description:      Automated Swing Trading Alert System
   Visibility:       Public
   DO NOT initialize anything else
   ```
3. Click **"Create repository"**
4. Copy the URL (looks like): `https://github.com/YOUR_USERNAME/swing-trading-bot.git`

### Part B: Push Your Code

Replace `YOUR_USERNAME` with your actual GitHub username in this command:

```bash
cd /home/artham/projects/py01
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/swing-trading-bot.git
git push -u origin main
```

✅ Your code is now on GitHub!

---

## 🎯 Step 3: Get Telegram Credentials (3 minutes)

### Get TELEGRAM_TOKEN

1. Open **Telegram app**
2. Search for: **@BotFather**
3. Click **"Start"**
4. Send: `/newbot`
5. Answer questions:
   - **Name:** `Swing Trading Bot`
   - **Username:** `swing_trading_bot_YOUR_NAME` (must end with `_bot`)
6. **Copy the token** that looks like:
   ```
   123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh
   ```
   ✅ Save this as `TELEGRAM_TOKEN`

### Get TELEGRAM_CHAT_ID

1. Go to your bot in Telegram
2. Click **"Start"**
3. Send any message (e.g., "hi")
4. Visit this URL (replace TOKEN):
   ```
   https://api.telegram.org/botINSERT_TOKEN_HERE/getUpdates
   ```
5. In the response, find:
   ```json
   "chat": {
     "id": 123456789
   }
   ```
6. **Copy the number** as `TELEGRAM_CHAT_ID`
   ✅ Save this

---

## 🌐 Step 4: Deploy on Render (5 minutes)

### Part A: Create Render Account

1. Go to **https://render.com**
2. Click **"Sign up"**
3. Choose **"GitHub"** option
4. Authorize to access your GitHub repos
5. ✅ Done!

### Part B: Create Web Service

1. Click **"New +"** → **"Web Service"**
2. Click **"Build and deploy from Git repository"**
3. Click **"Connect account"** → Authorize GitHub
4. Find **"swing-trading-bot"** repo
5. Click **"Connect"**

### Part C: Configure Service

Fill in these exact values:

**Basic Configuration:**
```
Name:              swing-trading-bot
Environment:       Python 3
Region:            Select closest to you (e.g., US East)
Branch:            main
Build Command:     pip install -r requirements.txt
Start Command:     uvicorn main:app --host 0.0.0.0 --port $PORT
Plan:              Free
```

**Environment Variables** (Click "Add Environment Variable" for each):

1. First variable:
   ```
   Key:    TELEGRAM_TOKEN
   Value:  (Paste your token from Step 3)
   ```

2. Second variable:
   ```
   Key:    TELEGRAM_CHAT_ID
   Value:  (Paste your chat ID from Step 3)
   ```

3. Third variable:
   ```
   Key:    WATCHLIST
   Value:  RELIANCE.NS,TCS.NS,INFY.NS
   ```

### Part D: Deploy!

1. Scroll to bottom
2. Click **"Create Web Service"**
3. 🎬 Deployment starts (takes 2-3 minutes)
4. Watch logs for: `✅ Uvicorn running`
5. Look for **green checkmark** and **"Live"** status

---

## ✅ Step 5: Test Deployment (2 minutes)

Once it says "Live", you'll see your URL at the top:
```
https://swing-trading-bot.onrender.com
```

### Test 1: Health Check
```bash
curl https://swing-trading-bot.onrender.com/health
```

Should return:
```json
{"status": "healthy", ...}
```

### Test 2: Alert (Most Important!)
```bash
curl -X POST https://swing-trading-bot.onrender.com/test-market-open-alert
```

✅ **Check your Telegram** - you should get an alert message!

---

## ⚠️ Step 6: Keep Service Alive 24/7 (3 minutes) - CRITICAL!

Without this, service sleeps after 15 minutes!

### Use UptimeRobot (FREE)

1. Go to **https://uptimerobot.com**
2. Click **"Sign Up"** → Create free account
3. Verify email
4. Click **"Add New Monitor"**
5. Fill in:
   ```
   Monitor Type:        HTTP(s)
   Friendly Name:       Swing Trading Bot
   URL:                 https://swing-trading-bot.onrender.com/health
   Monitoring Interval: 5 minutes
   ```
6. Click **"Create"**

✅ **Your service now runs 24/7 for FREE!**

---

## 📊 Final Checklist

- [ ] GitHub repository created
- [ ] Code pushed to GitHub (✅ Done locally)
- [ ] Telegram token obtained
- [ ] Telegram chat ID obtained
- [ ] Render account created
- [ ] Service deployed on Render
- [ ] All environment variables set
- [ ] Service shows "Live" (green)
- [ ] Health endpoint responds
- [ ] Alert test received in Telegram ✅
- [ ] UptimeRobot monitor created

---

## 🎉 You're Live!

Your bot is now deployed and will automatically send alerts:

```
⏰ SCHEDULE
09:15 AM IST → 🌅 Market Opening Alert
10:15+ AM   → 📊 Hourly Analysis
03:30 PM    → 🌆 Market Closing Summary
```

---

## 📞 Quick Help

**Can't find your URL?**
- Render Dashboard → Your service → Top of page

**Telegram token wrong?**
- @BotFather → /mybots → Select bot → API Token

**Service not deploying?**
- Render Dashboard → Logs tab → Look for errors
- Common: Wrong env var, GitHub not connected

**Service sleeping?**
- Set up UptimeRobot to keep alive
- Or upgrade to Starter plan ($7/month)

---

## 🚀 What Next?

1. ✅ Deploy using steps above
2. ✅ Get alerts at market open/close
3. ✅ Review trading signals
4. ✅ Execute trades based on recommendations
5. ✅ Backtest strategy
6. ✅ Add more stocks to watchlist

**You're all set for automated swing trading!** 📈

---

**Need help?** See:
- [RENDER_STEP_BY_STEP.md](RENDER_STEP_BY_STEP.md) - Visual guide
- [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) - Full documentation
- [API_REFERENCE.md](API_REFERENCE.md) - All endpoints
