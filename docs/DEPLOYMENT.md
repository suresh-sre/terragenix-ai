# Deployment Guide - GenOpsLab

Production deployment strategy for frontend and backend services.

## Overview

```
Frontend:  Vercel (Next.js)        | Backend:  Heroku/Railway (Flask)
Domain:    genopslab.com           | Domain:   api.genopslab.com
Hosting:   Global CDN              | Hosting:  Containerized Python
Deploy:    Git push (automatic)    | Deploy:   Docker or Procfile
```

## Frontend Deployment (Vercel)

### Prerequisites
- Vercel account (free tier)
- GitHub account with genopslab repository
- Domain (optional, get free one from Vercel)

### Step 1: Connect to Vercel

```bash
# Option 1: Use Vercel CLI
npm install -g vercel
cd frontend
vercel

# Option 2: Use Vercel Web Dashboard
# 1. Go to vercel.com
# 2. Click "New Project"
# 3. Import GitHub repository
# 4. Select "Next.js" framework
# 5. Click "Deploy"
```

### Step 2: Configure Environment Variables

In Vercel Dashboard:

```
Settings > Environment Variables

Add:
NEXT_PUBLIC_API_URL=https://your-backend-api.herokuapp.com
```

### Step 3: Deploy

```bash
# Automatic deployment on git push
git push origin main

# Or manual deployment
vercel --prod
```

### Verification

```bash
# Check deployment
curl https://your-app.vercel.app

# View logs
vercel logs

# Check health
vercel status
```

## Backend Deployment

### Option 1: Heroku (Recommended for quick start)

#### Prerequisites
- Heroku account
- Heroku CLI installed
- Git repository

#### Deploy Steps

```bash
# 1. Login to Heroku
heroku login

# 2. Create app
heroku create your-app-name

# 3. Set environment variables
heroku config:set YOUTUBE_API_KEY=your-gemini-api-key

# 4. Deploy
git push heroku main

# 5. Check logs
heroku logs --tail
```

#### Procfile

Create `backend/Procfile`:
```
web: gunicorn -w 4 -b 0.0.0.0:$PORT index:app
```

Install gunicorn:
```bash
pip install gunicorn
pip freeze > backend/requirements.txt
```

### Option 2: Railway

#### Prerequisites
- Railway account
- Railway CLI (optional)

#### Deploy Steps

```bash
# 1. Push to GitHub
git push origin main

# 2. Go to railway.app
# 3. New Project > Deploy from GitHub
# 4. Select genopslab repository
# 5. Railway auto-detects Flask app
# 6. Set environment variables
# 7. Deploy button

# View logs in Railway dashboard
```

### Option 3: AWS Lambda + API Gateway

#### Prerequisites
- AWS account
- SAM CLI or Serverless Framework
- Docker (for building Python packages)

#### Deploy with Serverless Framework

```bash
# Install serverless
npm install -g serverless

# Initialize serverless project
serverless config credentials --provider aws --key $AWS_KEY --secret $AWS_SECRET

# Deploy
serverless deploy

# Get endpoint URL
serverless info
```

#### Serverless YAML

```yaml
service: genopslab-backend

provider:
  name: aws
  runtime: python3.11
  region: us-east-1
  environment:
    YOUTUBE_API_KEY: ${env:YOUTUBE_API_KEY}

functions:
  api:
    handler: backend/index.handler
    events:
      - http:
          path: /{proxy+}
          method: ANY
          cors: true
      - http:
          path: /
          method: ANY
          cors: true

plugins:
  - serverless-wsgi
  - serverless-python-requirements

custom:
  wsgi:
    app: index.app
  pythonRequirements:
    dockerizePip: true
```

### Option 4: Docker + Google Cloud Run

#### Prerequisites
- Google Cloud account
- Docker installed
- `gcloud` CLI

#### Deploy Steps

```bash
# 1. Create Dockerfile
cat > backend/Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "index:app"]
EOF

# 2. Build image
docker build -t genopslab-backend ./backend

# 3. Tag for Google Cloud
docker tag genopslab-backend gcr.io/PROJECT_ID/genopslab-backend

# 4. Push to Container Registry
docker push gcr.io/PROJECT_ID/genopslab-backend

# 5. Deploy to Cloud Run
gcloud run deploy genopslab-backend \
  --image gcr.io/PROJECT_ID/genopslab-backend \
  --platform managed \
  --region us-central1 \
  --set-env-vars YOUTUBE_API_KEY=your-key \
  --allow-unauthenticated

# 6. Get service URL
gcloud run services describe genopslab-backend --platform managed --region us-central1
```

## Database Setup (Optional)

For user data storage, add PostgreSQL:

### Heroku PostgreSQL
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

### AWS RDS
```bash
aws rds create-db-instance \
  --db-instance-identifier genopslab-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username postgres \
  --master-user-password YOUR_PASSWORD
```

## Domain & DNS

### Connect Custom Domain

#### Vercel Frontend
```
1. Vercel Dashboard > Settings > Domains
2. Add Domain
3. Update DNS at domain registrar:
   - Add CNAME record pointing to Vercel
   - Or use Vercel nameservers
```

#### Backend API

```
1. Create subdomain: api.yourdomain.com
2. Point to backend service:
   - Heroku: DNS CNAME to *.herokuapp.com
   - AWS: CloudFront distribution
   - Cloud Run: Cloud Load Balancer
```

## SSL/TLS Certificates

- **Vercel:** Automatic (Let's Encrypt)
- **Heroku:** Automatic (Let's Encrypt)
- **AWS:** AWS Certificate Manager (free)
- **GCP:** Google-managed certificates

## CI/CD Pipeline

### GitHub Actions (Automatic)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Vercel
        run: |
          npm install -g vercel
          vercel --prod --token ${{ secrets.VERCEL_TOKEN }}

  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Heroku
        run: |
          git push https://heroku:${{ secrets.HEROKU_API_KEY }}@git.heroku.com/your-app.git main
```

## Environment Variables

### Frontend (Vercel)
```env
NEXT_PUBLIC_API_URL=https://api.genopslab.com
```

### Backend (All platforms)
```env
YOUTUBE_API_KEY=your-gemini-api-key
FLASK_ENV=production
DEBUG=False
```

## Monitoring & Logging

### Vercel
- Built-in analytics
- Speed insights
- Function logs

### Heroku
```bash
heroku logs --tail --app your-app-name
```

### AWS CloudWatch
```bash
aws logs tail /aws/lambda/genopslab-backend --follow
```

### GCP Cloud Logging
```bash
gcloud logging read resource.type=cloud_run_revision
```

## Scaling

### Frontend (Vercel)
- Automatic global CDN scaling
- No configuration needed
- Pay per request

### Backend Options

#### Heroku (Simple)
```bash
heroku ps:scale web=2  # Increase dynos
```

#### AWS Lambda (Automatic)
- Auto-scales based on requests
- Pay per execution

#### Kubernetes (Advanced)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: genopslab-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: genopslab
  template:
    metadata:
      labels:
        app: genopslab
    spec:
      containers:
      - name: api
        image: genopslab-backend:latest
        ports:
        - containerPort: 5000
        env:
        - name: YOUTUBE_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: gemini-key
```

## Cost Estimation

### Vercel Frontend
- Free tier: ✅ Sufficient for most projects
- Pro tier: $20/month (for advanced features)

### Backend Options

**Heroku**
- Free tier: ✅ (with limitations)
- Standard: $7-50/month

**AWS Lambda**
- Free tier: ✅ (1M requests/month)
- Pay as you go: $0.20 per 1M requests

**Cloud Run**
- Free tier: ✅ (2M requests/month)
- Pay as you go: $0.40 per 1M requests

**Total Estimated Cost:**
- **Free:** $0 (for hobby project)
- **Small:** $7-10/month (basic backend)
- **Medium:** $50-100/month (scaled backend)
- **Large:** $500+/month (enterprise)

## Rollback Strategy

### Revert Deployment
```bash
# Vercel
vercel rollback

# Heroku
heroku releases
heroku rollback v123

# GitHub (revert commit)
git revert HEAD
git push origin main
```

## Security Checklist

- [ ] API key stored as environment variable
- [ ] HTTPS enforced on all endpoints
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] Input validation on all endpoints
- [ ] Logging doesn't expose secrets
- [ ] Database encrypted at rest
- [ ] Regular security updates

## Troubleshooting

### Frontend not connecting to backend
```
1. Check NEXT_PUBLIC_API_URL in Vercel settings
2. Verify backend is running
3. Check CORS configuration
4. Review browser console for errors
```

### Backend crashes on deploy
```
1. Check deployment logs
2. Verify all environment variables set
3. Ensure dependencies in requirements.txt
4. Test locally first
```

### High latency
```
1. Enable caching
2. Use CDN
3. Optimize database queries
4. Consider async processing
```

---

**Next Steps:**
1. Choose backend platform (Heroku recommended)
2. Set up CI/CD pipeline
3. Configure monitoring
4. Test full deployment
5. Monitor costs and performance
