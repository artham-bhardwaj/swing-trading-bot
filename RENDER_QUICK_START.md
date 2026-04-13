# 📊 Deploy to Render - Quick Reference

## ⚡ 10-Minute Deploy Checklist

### Step 1: GitHub (2 min)
```bash
cd /home/artham/projects/py01
git init
git add .
git commit -m "Deploy to Render"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/swing-trading-bot.git
git push -u origin main
```
**Replace** `YOUR_USERNAME` with your GitHub username

---

### Step 2: Get Credentials (3 min)

#### Telegram Token
1. Open Telegram
2. Chat: [@BotFather](https://t.me/botfather)
3. Send: `/newbot`
4. Follow prompts
5. **Copy token** (e.g., `123456:ABC...`)

#### Telegram Chat ID
1. Send ANY message to your new bot
2. Visit: `https://api.telegram.org/botTOKEN/getUpdates`
3. Replace `TOKEN` with your token
4. Find `chat.id` value
5. **Copy chat ID** (e.g., `9876543210`)

---

### Step 3: Render Deployment (5 min)

1. Go to https://render.com
2. Sign up (free)
3. Click **"New +"** → **"Web Service"**
4. Select **"Build and deploy from Git repository"**
5. Authorize GitHub
6. Select `swing-trading-bot` repo
7. Configure:
   ```
   Name:            swing-trading-bot
   Environment:     Python 3
   Build Command:   pip install -r requirements.txt
   Start Command:   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
8. Add environment variables:
   - `TELEGRAM_TOKEN` = (your token)
   - `TELEGRAM_CHAT_ID` = (your chat ID)
   - `WATCHLIST` = RELIANCE.NS,TCS.NS,INFY.NS
9. Click **"Create Web Service"**
10. **Wait 2-3 minutes for deployment**

---

### Step 4: Test (as soon as deployment finishes)

You'll get a URL: `https://swing-trading-bot.onrender.com`

```bash
# Test it
curl https://swing-trading-bot.onrender.com/health

# Test alert (should send to Telegram)
curl -X POST https://swing-trading-bot.onrender.com/test-market-open-alert
```

✅ **Check Telegram** - you should receive an alert!

---

## ⚠️ CRITICAL: Keep Service Alive

Without this, your service will sleep after 15 minutes!

### Use UptimeRobot (FREE)

1. Go to https://uptimerobot.com
2. Sign up
3. **Add Monitor**:
   - Type: HTTP(s)
   - URL: `https://swing-trading-bot.onrender.com/health`
   - Interval: 5 minutes
4. Done! ✅

**This keeps your service running 24/7 for FREE**

---

## ✅ Success Indicators

- [ ] Render shows "Live" (green dot)
- [ ] `/health` endpoint responds with 200
- [ ] `/test-market-open-alert` sends alert to Telegram
- [ ] UptimeRobot shows service as "Up"

---

## 🎯 Your Deployed App

```
API URL:  https://swing-trading-bot.onrender.com
Logs:     Render Dashboard → Logs tab
Monitor:  UptimeRobot dashboard
```

### Test Endpoints
```bash
# Health Check
curl https://swing-trading-bot.onrender.com/health

# Market Status
curl https://swing-trading-bot.onrender.com/market-status

# Analyze Stock
curl https://swing-trading-bot.onrender.com/analyze/RELIANCE.NS

# Test Market Open Alert
curl -X POST https://swing-trading-bot.onrender.com/test-market-open-alert

# Test Trading Alert
curl -X POST "https://swing-trading-bot.onrender.com/test-trading-alert/RELIANCE.NS?signal=BUY"
```

---

## 🚨 Common Issues

### Service Won't Deploy
- Check GitHub is connected
- Check all files pushed to GitHub
- View Render logs for errors

### Alerts Not Sending
- Verify TELEGRAM_TOKEN is correct
- Verify TELEGRAM_CHAT_ID is correct (numeric only)
- Test locally first

### Service Keeps Going Down
- Deploy UptimeRobot (prevents sleeping)
- Or upgrade to Starter ($7/month)

---

## 💰 Free Tier Limitations

✅ **Always On** (if using UptimeRobot)  
✅ **Unlimited Requests**  
✅ **Unlimited Bandwidth**  
❌ **May restart without notice**  
❌ **Limited RAM (0.5GB)**  
❌ **Shared CPU**  

**Upgrade to Starter ($7/month) for:**
- Guaranteed uptime
- Dedicated CPU
- Reliable scheduling

---

## 📚 Full Guides

- [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) - Complete guide
- [API_REFERENCE.md](API_REFERENCE.md) - All endpoints
- [ALERTS_GUIDE.md](ALERTS_GUIDE.md) - Alert details

---

## 🎉 You're Done!

Your swing trading bot is now deployed on **Render for FREE**! 

Next steps:
1. ✅ Deploy
2. ✅ Test alerts  
3. ✅ Set up UptimeRobot
4. ✅ Enjoy automated trading alerts

---

**Questions?** See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for full details
