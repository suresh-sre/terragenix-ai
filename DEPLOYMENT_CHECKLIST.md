# 🎯 GenOpsLab Production Deployment Checklist

## ✅ Step-by-Step Deployment

### PHASE 1: Prepare (5 mins)

**Pre-Deployment:**
- [ ] Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
- [ ] Create free Heroku account: https://www.heroku.com
- [ ] Have GitHub access (for frontend redeployment)
- [ ] Have Vercel access for your GenOpsLab project

**Verify Code:**
- [ ] Run `frontend npm run build` - builds successfully
- [ ] Review `Procfile` exists in root
- [ ] Review `requirements.txt` has gunicorn

---

### PHASE 2: Deploy Backend to Heroku (5-10 mins)

#### Terminal Steps:

```bash
# 1. Install Heroku CLI (if not done)
# From: https://devcenter.heroku.com/articles/heroku-cli

# 2. Login
heroku login
# Opens browser - authenticate with your account

# 3. Navigate to project root
cd e:\AWS-Interview\terragenix-ai-

# 4. Create Heroku app (PICK UNIQUE NAME!)
heroku create your-genopslab-api
# Example: heroku create genopslab-api-kavin-2024
# Copy the app name - you'll need it

# 5. Deploy from Git
git push heroku main
# Wait 2-3 minutes... you should see:
# "https://your-genopslab-api.herokuapp.com deployed to Heroku"

# 6. Get your backend URL
heroku info your-genopslab-api
# Look for "Web URL:" - COPY THIS
# Example: https://your-genopslab-api.herokuapp.com
```

**Verification:**
```bash
# Test your backend is running
curl https://your-genopslab-api.herokuapp.com/

# Should return HTML (web UI)
```

#### ✅ Checklist:
- [ ] `heroku login` successful
- [ ] `heroku create your-app-name` worked
- [ ] `git push heroku main` completed without errors
- [ ] Got backend URL from `heroku info`
- [ ] Tested backend URL with curl - returns 200

---

### PHASE 3: Update Vercel Frontend (3-5 mins)

#### Web Dashboard Steps:

1. **Go to Vercel Dashboard**
   - https://vercel.com
   - Select your GenOpsLab project

2. **Navigate to Environment Variables**
   - Click **Settings** (top menu)
   - Click **Environment Variables** (left sidebar)

3. **Add Backend URL**
   - Click **Add New**
   - Fill in:
     ```
     Name:  NEXT_PUBLIC_API_URL
     Value: https://your-genopslab-api.herokuapp.com
     ```
   - Value should be EXACTLY your backend URL from Step 2
   - Click **Save**

4. **Trigger Redeployment**
   - Option A: Push to GitHub (auto-deploys)
     ```bash
     git push origin main
     ```
   - Option B: Manual redeploy
     ```bash
     cd frontend
     vercel --prod
     ```

**Wait for deployment:**
- Check Vercel dashboard for "Deployment Complete"
- Should show green checkmark
- Takes 2-3 minutes

#### ✅ Checklist:
- [ ] Vercel environment variable set
- [ ] `NEXT_PUBLIC_API_URL` value is correct
- [ ] Frontend redeployed
- [ ] Vercel shows "Deployment Complete"

---

### PHASE 4: Test Everything (5 mins)

#### Test Frontend:

```bash
# Visit your Vercel URL
# Should see GenOpsLab landing page ✓
# Should see "Generate Infrastructure" card ✓
```

#### Test Generator Modal:

1. Visit your Vercel frontend URL
2. Scroll down to **"Generate Infrastructure"** feature card
3. Click on the card
4. Modal should open without error ✓

#### Test Full Integration:

1. **Get Gemini API Key** (free):
   - Visit: https://aistudio.google.com/app/apikey
   - Click "Create API Key"
   - Copy the key

2. **Fill Generator Form:**
   - Paste your Gemini API key
   - Select cloud provider: AWS
   - Services: `ec2, rds, s3`
   - Requirements: (leave blank)

3. **Click "Generate Terraform Code"**
   - Should see loading spinner
   - After ~10 seconds, code should appear
   - Shows README.md, provider.tf, main.tf, etc.

4. **Test Download:**
   - Click "Copy" on any file - should work
   - Click "Download ZIP" - should download

#### ✅ Checklist:
- [ ] Frontend loads without 500 errors
- [ ] Modal opens successfully
- [ ] Generated code appears (not errors)
- [ ] Can copy code to clipboard
- [ ] Can download individual files
- [ ] Can download as ZIP

---

### PHASE 5: Verify Production (2 mins)

#### Check Services Are Healthy:

```bash
# Frontend health check
curl -I https://your-vercel-url.vercel.app
# Should show: HTTP/2 200

# Backend health check
curl -I https://your-genopslab-api.herokuapp.com
# Should show: HTTP/1.1 200 OK

# API endpoint check
curl -X POST https://your-genopslab-api.herokuapp.com/generate \
  -H "Content-Type: application/json" \
  -d '{"api_key":"test","cloud_provider":"aws","services":"ec2"}'
# Should return JSON response (with Gemini error about API key, but proves connectivity)
```

#### ✅ Checklist:
- [ ] Frontend returns 200
- [ ] Backend returns 200
- [ ] API endpoint responds
- [ ] No connection errors

---

## 📊 Summary

| Component | Location | Status |
|-----------|----------|--------|
| **Frontend** | Vercel | ✅ Deployed |
| **Backend** | Heroku | ✅ Deployed |
| **API Route** | Vercel Function | ✅ Configured |
| **Environment Variable** | Vercel | ✅ Set |
| **Integration** | Frontend → Backend | ✅ Connected |

---

## 🎉 You're Live!

Your GenOpsLab SaaS platform is now live in production! 🚀

### Share Your Links:
- **Landing Page:** https://your-vercel-url.vercel.app
- **API Backend:** https://your-genopslab-api.herokuapp.com

### Next Steps:
1. **Monitor**: Check Vercel Analytics & Heroku Dashboard
2. **Customize**: Update landing page content
3. **Add Domain**: Set up custom domain on Vercel
4. **Marketing**: Share your app with users!

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Modal shows "Backend API URL not configured"** | Check `NEXT_PUBLIC_API_URL` is set in Vercel → Re-redeploy |
| **500 Internal Server Error** | Check backend deployment with `curl` - might not be running |
| **Slow code generation** | Normal - Gemini API takes 10-30 seconds |
| **API key rejected** | Get free key from https://aistudio.google.com/app/apikey |
| **Heroku deployment fails** | Check git history - might be pushing wrong branch |

For more help, see:
- `DEPLOYMENT_QUICK_START.md` - Detailed steps
- `docs/DEPLOYMENT.md` - Multiple deployment options
- `docs/ARCHITECTURE.md` - System design

---

**Questions? You're all set up for production!** ✨

