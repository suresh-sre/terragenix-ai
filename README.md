# GenOpsLab - Cloud & DevOps AI Platform

## Deployment Note

This repo contains two deployable apps:

- `frontend/` is the main Next.js site that should be deployed to Vercel
- `backend/` is the Flask API that should be deployed separately

If Vercel is connected to the repository root, it may serve the legacy Python entrypoint instead of the main landing page. See [DEPLOY_ON_VERCEL.md](./DEPLOY_ON_VERCEL.md) for the safest setup.

> Generate Terraform code for AWS, Azure & GCP in seconds with AI ⚡

A full-stack AI-powered platform for generating production-ready infrastructure as code with a modern SaaS landing page.

## 📦 Project Structure

```
genopslab/
├── frontend/                    # Next.js SaaS Landing Page & App
│   ├── app/                     # Next.js app directory
│   │   ├── api/                 # API routes (proxying backend)
│   │   ├── components/          # React components
│   │   ├── globals.css          # Global styles
│   │   ├── layout.tsx           # Root layout
│   │   └── page.tsx             # Home page
│   ├── public/                  # Static assets
│   ├── package.json             # Frontend dependencies
│   ├── next.config.ts           # Next.js config
│   ├── tailwind.config.ts       # Tailwind CSS config
│   ├── tsconfig.json            # TypeScript config
│   ├── LANDING_PAGE.md          # Landing page documentation
│   ├── TERRAFORM_INTEGRATION.md # Integration guide
│   └── SETUP_GUIDE.md           # Setup instructions
│
├── backend/                     # Python Flask API Server
│   ├── index.py                 # Main Flask app
│   ├── antigravity_terraform_generator.py  # Core generator logic
│   ├── requirements.txt         # Python dependencies
│   └── README.md               # Backend documentation
│
├── docs/                        # Documentation
│   ├── ARCHITECTURE.md          # Architecture overview
│   ├── DEPLOYMENT.md            # Deployment guide
│   └── API.md                   # API documentation
│
├── _archive/                    # Legacy files (archived)
│   └── legacy/
│       ├── antigravity_terraform_generator.py
│       └── my-rds-infra/
│
├── .gitignore
├── README.md                    # This file
├── QUICK_START.md               # Quick start guide
└── package.json                 # Root workspace config
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ (for frontend)
- Python 3.8+ (for backend)
- Google Gemini API key (free from [aistudio.google.com](https://aistudio.google.com/app/apikey))

### 1️⃣ Start Python Backend

```bash
# Install Python dependencies
pip install -r backend/requirements.txt

# Start Flask server (runs on http://localhost:5000)
python backend/index.py
```

### 2️⃣ Start Next.js Frontend

```bash
# Install frontend dependencies
cd frontend
npm install

# Configure API URL
cp .env.local.example .env.local
# Edit .env.local: NEXT_PUBLIC_API_URL=http://localhost:5000

# Start development server (runs on http://localhost:3000)
npm run dev
```

### 3️⃣ Test Integration

1. Open http://localhost:3000 in browser
2. Scroll to "Generate Infrastructure" feature card
3. Click the card to open Terraform generator modal
4. Enter your Gemini API key
5. Select cloud provider and services
6. Click "Generate Terraform Code"
7. View, copy, or download generated code

✅ **That's it!** Your full-stack application is running!

## 📋 Features

### Frontend (Next.js)
- ✨ Modern SaaS landing page with dark theme
- 🎨 Beautiful gradient UI with Tailwind CSS
- 📱 Fully responsive mobile-first design
- ⚡ Smooth animations and transitions
- 🤖 Integrated Terraform generator modal
- 📥 Copy & download functionality
- 🔍 SEO optimized

### Backend (Python Flask)
- 🚀 AI-powered code generation with Google Gemini
- ☁️ Multi-cloud support (AWS, Azure, GCP)
- 📊 Intelligent infrastructure analysis
- 💾 Generate provider.tf, main.tf, variables.tf, outputs.tf, README.md
- 📦 ZIP file export
- 🔒 Secure API endpoints

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 16.2.4
- **UI Library**: React 19.2.4
- **Styling**: Tailwind CSS 4
- **Language**: TypeScript 5
- **Runtime**: Node.js

### Backend
- **Framework**: Flask
- **AI**: Google Gemini API
- **Language**: Python 3.8+
- **Runtime**: Python

## 📖 Documentation

- **[QUICK_START.md](./QUICK_START.md)** - 5-minute setup guide
- **[frontend/SETUP_GUIDE.md](./frontend/SETUP_GUIDE.md)** - Frontend detailed setup
- **[frontend/TERRAFORM_INTEGRATION.md](./frontend/TERRAFORM_INTEGRATION.md)** - API integration guide
- **[docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md)** - System architecture
- **[docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md)** - Production deployment
- **[docs/API.md](./docs/API.md)** - API reference

## 🌐 Deployment

### Frontend (Vercel)
```bash
cd frontend
vercel
```

Preferred Vercel settings:

- Root Directory: `frontend`
- Framework Preset: `Next.js`
- Environment Variable: `NEXT_PUBLIC_API_URL=https://your-backend-api.com`

### Backend (Heroku/Railway/AWS)
```bash
# Option 1: Heroku
heroku create your-app-name
git push heroku main

# Option 2: Railway
railway up

# Option 3: AWS Lambda
# Use serverless framework or Zappa
```

### Environment Variables

**Frontend (.env.local)**
```
NEXT_PUBLIC_API_URL=https://your-backend-api.com
```

**Backend (.env)**
```
YOUTUBE_API_KEY=your_gemini_api_key
FLASK_ENV=production
```

## 🎨 Customization

### Change Branding
1. Edit text in `frontend/app/components/Hero.tsx`
2. Update colors in `frontend/app/globals.css`
3. Replace logo in `frontend/app/components/Header.tsx`

### Change API Endpoints
1. Update `NEXT_PUBLIC_API_URL` in `frontend/.env.local`
2. Modify API routes in `frontend/app/api/`

### Customize Generator
1. Edit core logic in `backend/antigravity_terraform_generator.py`
2. Modify Flask routes in `backend/index.py`

## 📊 API Endpoints

### Frontend API Routes (Next.js)
- `POST /api/generate` - Generate Terraform code
- `POST /api/download` - Download as ZIP

### Backend API Routes (Flask)
- `POST /generate` - Generate Terraform code
- `POST /download` - Download ZIP
- `GET /` - HTML web UI

## 🔐 Security

- API key stored securely on backend
- Frontend proxies requests through API routes
- No sensitive data exposed to client
- CORS configured for production

## 🐛 Troubleshooting

### Backend not responding
- Ensure Flask is running: `python backend/index.py`
- Check `NEXT_PUBLIC_API_URL` in frontend `.env.local`
- Verify port 5000 is available

### Can't generate code
- Validate Gemini API key
- Check backend logs for errors
- Ensure services are valid for selected cloud provider

### Build errors
```bash
# Clear Next.js cache
cd frontend && rm -rf .next && npm run build
```

## 📞 Support

- 📖 Check documentation in `docs/`
- 🔍 Review API integration guide
- 💬 Check backend logs for errors
- 🐛 Submit issues on GitHub

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Credits

- Built with Next.js, React, Tailwind CSS, Flask, and Google Gemini AI
- Modern SaaS design inspired by contemporary tech products
- Infrastructure generation powered by AI

---

**Ready to generate cloud infrastructure with AI?** Start with [QUICK_START.md](./QUICK_START.md)!
