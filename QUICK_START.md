# 🚀 Quick Start Guide - GenOpsLab

Get your AI-powered cloud infrastructure generator running in 5 minutes!

## Step 1: Clone & Setup (1 min)

```bash
# Navigate to project root
cd genopslab

# Install dependencies
pip install -r backend/requirements.txt  # For backend
cd frontend && npm install                # For frontend
cd ..
```

## Step 2: Get API Key (1 min)

1. Visit https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy your free Gemini API key
4. Keep it safe (you'll need it when using the app)

## Step 3: Configure Frontend (1 min)

```bash
# From genopslab/frontend
cp .env.local.example .env.local

# Edit .env.local
# Set: NEXT_PUBLIC_API_URL=http://localhost:5000
```

## Step 4: Start Backend (1 min)

```bash
# Terminal 1: Start Flask API server
python backend/index.py

# You should see:
# * Running on http://localhost:5000
```

## Step 5: Start Frontend (1 min)

```bash
# Terminal 2: Start Next.js development server
cd frontend
npm run dev

# You should see:
# ✓ Ready in 700ms
# ▲ Next.js 16.2.4
# - Local: http://localhost:3000
```

## 🎯 Test It Out

1. **Open http://localhost:3000** in your browser
2. **Scroll down** to "Generate Infrastructure" feature card
3. **Click the card** - a modal opens
4. **Fill in the form:**
   - Paste your Gemini API key
   - Select "AWS" (or Azure/GCP)
   - Type some services: `ec2, rds, s3`
   - Leave requirements blank for now
5. **Click "Generate Terraform Code"**
6. **Watch the magic happen!** ✨

## 📁 Generated Output

The generator creates these Terraform files:
- `provider.tf` - Cloud provider configuration
- `main.tf` - Resource definitions
- `variables.tf` - Input variables
- `outputs.tf` - Output values
- `terraform.tfvars.example` - Example variables
- `README.md` - Documentation

You can:
- 📋 **Copy** code to clipboard
- 💾 **Download** individual files
- 📦 **Download ZIP** with all files

## 🛠️ Useful Commands

```bash
# Terminal 1: Backend
python backend/index.py          # Start Flask API

# Terminal 2: Frontend
cd frontend && npm run dev       # Start development
npm run build                    # Build for production
npm run lint                     # Check code quality

# View generated code in browser
open http://localhost:3000      # macOS
start http://localhost:3000     # Windows
xdg-open http://localhost:3000  # Linux
```

## 🔧 Troubleshooting

### "Cannot connect to backend"
```bash
# Check if Flask is running
curl http://localhost:5000

# If not, restart:
python backend/index.py
```

### "API key error"
- Get a free key from https://aistudio.google.com/app/apikey
- Make sure you copied the entire key
- No spaces before/after

### "Port 5000 already in use"
```bash
# Kill process on port 5000
# macOS/Linux:
lsof -i :5000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### "npm modules not found"
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## 📚 Next Steps

After the quick start, check out:
- **[docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md)** - How it all works
- **[frontend/TERRAFORM_INTEGRATION.md](../frontend/TERRAFORM_INTEGRATION.md)** - API integration details
- **[docs/DEPLOYMENT.md](../docs/DEPLOYMENT.md)** - Deploy to production

## 🌟 Features to Try

1. **Generate AWS Infrastructure** - EC2, RDS, S3, VPC
2. **Try Azure** - VMs, SQL Database, Storage
3. **Use GCP** - Compute Instances, Cloud SQL
4. **Add Requirements** - Specify instance types, regions, security
5. **Download as ZIP** - Get all files ready to deploy

## 🚀 You're All Set!

Your GenOpsLab platform is now running. Generate some awesome Terraform code! 🎉

---

**Questions?** Check the main [README.md](../README.md) or explore the `docs/` folder.
