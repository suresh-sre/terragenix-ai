# 🚀 Production Deployment Guide

Get your GenOpsLab application live in minutes!

## Quick Overview

**Frontend** (Next.js) → Vercel
**Backend** (Python Flask) → Heroku / Railway / AWS

---

## 🎯 Fastest Path: Heroku + Vercel

**Time: 5-10 minutes**

### Backend: Deploy to Heroku

#### 1️⃣ Install Heroku CLI

**Windows:**
```bash
# Download: https://devcenter.heroku.com/articles/heroku-cli
# Or use Chocolatey:
choco install heroku-cli
```

**macOS:**
```bash
brew tap heroku/brew && brew install heroku
```

**Linux:**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

#### 2️⃣ Login to Heroku

```bash
heroku login
# Opens browser to authenticate
# Create free account if needed
```

#### 3️⃣ Create & Deploy App

```bash
cd e:\AWS-Interview\terragenix-ai-

# Create Heroku app (unique name required)
heroku create your-genopslab-api
# Example: heroku create genopslab-api-2024

# Deploy from Git
git push heroku main

# Wait 2-3 minutes for deployment...
# You'll see: "https://your-genopslab-api.herokuapp.com deployed to Heroku"
```

#### 4️⃣ Get Your Backend URL

```bash
heroku info your-genopslab-api
# Look for "Web URL"
# Copy: https://your-genopslab-api.herokuapp.com
```

---

### Frontend: Update & Redeploy on Vercel

#### 1️⃣ Set Environment Variable

1. **Go to:** https://vercel.com
2. **Select** your GenOpsLab project
3. **Settings** → **Environment Variables**
4. **Add New:**
   ```
   Name:  NEXT_PUBLIC_API_URL
   Value: https://your-genopslab-api.herokuapp.com
   ```
5. **Save**

#### 2️⃣ Redeploy

```bash
# Option A: Auto-deploy via Git push
git push origin main

# Option B: Manual redeploy
cd frontend
vercel --prod
```

#### 3️⃣ Wait & Test

- Wait 2-3 minutes
- Visit your Vercel URL
- Click "Generate Infrastructure"
- Test with Gemini API key

---

## 🚁 Alternative: Railway (Easiest)

**Time: 2-3 minutes (auto-deploys)**

### 1️⃣ Connect GitHub

1. Go to https://railway.app
2. Click **"New Project"**
3. Select **"Deploy from GitHub"**
4. Select your **genopslab** repository
5. Railway auto-detects Flask and deploys

### 2️⃣ Get URL

1. Go to **Railway Dashboard**
2. Select your deployment
3. Copy the **service URL**
4. Add to Vercel as `NEXT_PUBLIC_API_URL`

### 3️⃣ Redeploy Frontend

```bash
# Git push triggers auto-deploy
git push origin main
```

---

## ☁️ Alternative: AWS Lambda (Serverless)

See `docs/DEPLOYMENT.md` for detailed instructions.

---

## 📋 Complete Deployment Checklist

- [ ] Backend deployed (Heroku/Railway/AWS)
- [ ] Backend URL copied
- [ ] Vercel environment variable set
- [ ] Frontend redeployed on Vercel
- [ ] Tested with Gemini API key
- [ ] Both services responding (200)

---

## 🔧 Troubleshooting

### Vercel showing 500 error

**Problem:** Backend URL not configured
**Solution:**
1. Check `NEXT_PUBLIC_API_URL` is set in Vercel
2. Verify backend is deployed and running
3. Test: `curl https://your-backend-url/`

### Heroku deployment fails

**Problem:** Missing dependencies
**Solution:**
```bash
pip install -r requirements.txt
# Commit and push again
git push heroku main
```

### Local testing not working

**Problem:** Backend not running
**Solution:**
```bash
python backend/index.py
# Keep running while testing
cd frontend && npm run dev
```

---

## 🌍 Verifying Your Deployment

### Check Frontend

```bash
# Visit your Vercel URL
curl https://your-vercel-url.vercel.app

# Should show GenOpsLab landing page HTML
```

### Check Backend

```bash
# Visit your backend URL
curl https://your-backend-url.herokuapp.com/

# Should return HTML (web UI)
```

### Check API Endpoint

```bash
curl -X POST https://your-backend-url.herokuapp.com/generate \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "YOUR_GEMINI_KEY",
    "cloud_provider": "aws",
    "services": "ec2, rds"
  }'

# Should return generated Terraform code
```

---

## 📊 Free Tier Limits

| Service | Limit | Cost Beyond |
|---------|-------|-------------|
| **Vercel** | 100 GB bandwidth | $0.50/GB |
| **Heroku** | 550 free dyno hours | $7/month dyno |
| **Railway** | $5 free monthly | $0.26/hour after |

**For hobby projects:** All services above work fine free!

---

## 🔐 Setting API Keys Securely

### For Backend (Heroku Example)

```bash
# Set Gemini API key on Heroku
heroku config:set YOUTUBE_API_KEY=your_key --app your-genopslab-api

# Verify it's set (won't show value)
heroku config --app your-genopslab-api
```

**In Flask code:** `api_key = os.getenv('YOUTUBE_API_KEY')`

### For Frontend

✅ `NEXT_PUBLIC_API_URL` - Safe to expose (server URL only)
✗ Never put API keys in frontend environment variables!

---

## 📚 Additional Resources

- **Heroku Docs:** https://devcenter.heroku.com
- **Vercel Docs:** https://vercel.com/docs
- **Railway Docs:** https://docs.railway.app
- **AWS Lambda:** https://aws.amazon.com/lambda/

---

## ✅ Next Steps After Deployment

1. **Monitor Performance**
   - Check Vercel Analytics
   - Monitor Heroku Dyno
   - Review error logs

2. **Add Custom Domain**
   - Vercel: Settings → Domains
   - Heroku: `heroku domains:add`

3. **Enable HTTPS**
   - Both auto-enable for free

4. **Set Up Monitoring**
   - Vercel integrations
   - Heroku logging
   - Sentry error tracking

---

## 🎉 You're Live!

Your GenOpsLab SaaS platform is now live on the internet! 🚀

**Share your deployment:**
- Frontend: `https://your-vercel-url.vercel.app`
- Backend API: `https://your-heroku-app.herokuapp.com`

---

**Questions?** Check `docs/ARCHITECTURE.md` or `QUICK_START.md`
