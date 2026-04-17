# GenOpsLab Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     User Browser                             │
│              (http://localhost:3000)                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ HTTP/HTTPS
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Frontend (Next.js 16.2.4)                       │
│  - SaaS Landing Page with dark theme                        │
│  - React Components with Tailwind CSS                       │
│  - Terraform Generator Modal                                │
│  - API Route Proxies (/api/generate, /api/download)         │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ HTTP/JSON
                       ▼
┌─────────────────────────────────────────────────────────────┐
│           Backend (Python Flask)                             │
│            (http://localhost:5000)                           │
│  - REST API endpoints                                        │
│  - Terraform code generation logic                           │
│  - Google Gemini AI integration                              │
│  - ZIP file generation                                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ API Call
                       ▼
┌─────────────────────────────────────────────────────────────┐
│         Google Gemini AI (Cloud)                             │
│  - Code generation models                                    │
│  - Natural language processing                               │
│  - Infrastructure understanding                              │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### Frontend Layer (Next.js)

**Location:** `/frontend`

**Key Files:**
- `app/page.tsx` - Main landing page composition
- `app/components/Hero.tsx` - Hero section
- `app/components/Features.tsx` - Feature cards with modal trigger
- `app/components/TerraformGenerator.tsx` - Modal component (NEW!)
- `app/api/generate/route.ts` - API proxy for generation
- `app/api/download/route.ts` - API proxy for ZIP download
- `app/globals.css` - Dark theme + custom animations
- `tailwind.config.ts` - Tailwind configuration

**Technology Stack:**
- React 19.2.4
- Next.js 16.2.4
- Tailwind CSS 4
- TypeScript 5
- Axios/Fetch for HTTP requests

**Features:**
- Component-based architecture
- API routes for proxying backend calls
- Modal dialogs for user interaction
- Responsive design (mobile-first)
- Dark theme with gradients
- Smooth animations

### Backend Layer (Python Flask)

**Location:** `/backend`

**Key Files:**
- `index.py` - Flask app with REST API endpoints
- `antigravity_terraform_generator.py` - Core Terraform generation logic
- `requirements.txt` - Python dependencies

**Technology Stack:**
- Flask 2.3+
- Google Generative AI SDK
- Python 3.8+
- Standard library modules (json, io, zipfile)

**Endpoints:**
```
POST /generate
  - Generate Terraform code
  - Input: api_key, cloud_provider, services, requirements
  - Output: JSON with generated code files

POST /download
  - Package code as ZIP
  - Input: code dict, cloud_provider
  - Output: Binary ZIP file

GET /
  - Web UI (legacy)
```

### Data Flow

```
1. User opens landing page
   ↓
2. Clicks "Generate Infrastructure" feature card
   ↓
3. Modal appears with form
   ↓
4. User fills: API key, cloud provider, services, requirements
   ↓
5. User clicks "Generate Terraform Code"
   ↓
6. Frontend sends POST to /api/generate
   ↓
7. Next.js API route proxies to backend /generate
   ↓
8. Flask receives request, validates inputs
   ↓
9. Calls Google Gemini API with detailed prompt
   ↓
10. Gemini generates Terraform code
    ↓
11. Flask returns generated files as JSON
    ↓
12. Frontend displays code in modal
    ↓
13. User can:
    - Copy code to clipboard
    - Download individual files
    - Download all as ZIP
```

## API Contract

### Generate Endpoint

**Request:**
```json
POST /api/generate
Content-Type: application/json

{
  "api_key": "your-gemini-api-key",
  "cloud_provider": "aws|azure|gcp",
  "services": "ec2, rds, s3",
  "requirements": "use t3.micro, enable encryption, us-east-1"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "provider.tf": "terraform { required_version = ... }",
    "main.tf": "resource \"aws_instance\" \"web\" { ... }",
    "variables.tf": "variable \"instance_type\" { ... }",
    "outputs.tf": "output \"instance_id\" { ... }",
    "terraform.tfvars.example": "instance_type = \"t3.micro\" ...",
    "README.md": "# AWS Infrastructure\n..."
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Error message describing what went wrong"
}
```

### Download Endpoint

**Request:**
```json
POST /api/download
Content-Type: application/json

{
  "code": {
    "provider.tf": "...",
    "main.tf": "..."
  },
  "cloud_provider": "aws"
}
```

**Response:**
- Binary ZIP file

## Security Considerations

### API Key Handling
✅ **GOOD:** Only transmitted to backend, not exposed in frontend
✅ **GOOD:** User enters key in browser (not captured)
✅ **GOOD:** Backend forwards to Gemini securely

⚠️ **NOTE:** For production, consider:
- User authentication system
- API key encryption in database
- Rate limiting per user
- Audit logging

### Input Validation
- Backend validates all inputs
- Services list validated against cloud provider
- Requirements checked for dangerous patterns
- Terraform code generated in isolated environment

### Network Security
✅ HTTPS in production
✅ CORS configured
✅ No sensitive data in logs
✅ Request validation on all endpoints

## Scalability

### Current (Development)
- Single Flask process
- Next.js development server
- In-memory request handling
- No database

### Production (Recommended)
```
┌─────────────────────────────────────────────┐
│         Frontend (Vercel)                    │
│  - Global CDN                                │
│  - Automatic scaling                         │
│  - Edge functions                            │
└────────────┬────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────┐
│      Backend (Kubernetes/Docker)             │
│  - Multiple Flask instances                  │
│  - Load balancer                             │
│  - Redis cache for code generation           │
│  - Database for user code history            │
│  - Async job queue (Celery)                  │
└────────────┬────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────┐
│  External Services                           │
│  - Google Gemini API (cloud)                 │
│  - PostgreSQL (database)                     │
│  - S3/GCS (file storage)                     │
└─────────────────────────────────────────────┘
```

### Performance Optimization

1. **Caching**
   - Cache generated code for same inputs
   - Cache popular service combinations

2. **Async Processing**
   - Long-running generations in background
   - Webhook callbacks when ready

3. **CDN**
   - Vercel global edge network for frontend
   - Cloudflare for API endpoints

4. **Database**
   - Store user code history
   - Track API usage
   - User preferences

## Deployment Topology

### Development
```
Local Machine
├── Frontend (npm run dev)
└── Backend (python backend/index.py)
```

### Staging
```
Vercel (Frontend)
│
Railway/Heroku (Backend)
│
Google Gemini API (Cloud)
```

### Production
```
Vercel (Frontend - Global CDN)
│
AWS/GCP/Azure (Backend - Region specific)
│
├─ Kubernetes cluster
├─ PostgreSQL database
├─ Redis cache
└─ S3 file storage
│
Google Gemini API (Cloud)
```

## Monitoring & Observability

### Key Metrics to Track
- API response time
- Gemini API quota usage
- Error rates by cloud provider
- User generation success rate
- Code generation time

### Logging
- All API requests
- Terraform generation steps
- Errors and exceptions
- User actions

### Alerts
- High API latency
- API quota exceeded
- Generation failures
- Service downtime

## File Organization

```
genopslab/
├── frontend/              # Next.js SaaS application
│   ├── app/
│   │   ├── api/          # API route handlers
│   │   ├── components/   # React components
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── public/
│   ├── package.json
│   ├── next.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   └── ...docs
│
├── backend/               # Python Flask API
│   ├── index.py          # Main Flask app
│   ├── antigravity_terraform_generator.py
│   ├── requirements.txt
│   └── README.md
│
├── docs/                 # Documentation
│   ├── ARCHITECTURE.md   # This file
│   ├── DEPLOYMENT.md
│   └── API.md
│
└── _archive/            # Legacy files
    └── legacy/
```

## Technology Decisions

### Why Next.js?
- ✅ React ecosystem with server capabilities
- ✅ Built-in API routes (perfect for proxying)
- ✅ SSR/SSG options
- ✅ Vercel integration
- ✅ TypeScript support

### Why Flask?
- ✅ Lightweight and simple
- ✅ Perfect for REST APIs
- ✅ Easy integration with Python AI libraries
- ✅ Flexible deployment options
- ✅ Active community

### Why Google Gemini?
- ✅ Free tier available
- ✅ Excellent code generation capabilities
- ✅ Multi-modal support
- ✅ Fast response times
- ✅ Good for structured output (Terraform)

### Why Tailwind CSS?
- ✅ Utility-first approach
- ✅ Small bundle size
- ✅ Easy dark mode
- ✅ Great animations
- ✅ Complete component library

---

**Next:** [DEPLOYMENT.md](./DEPLOYMENT.md) - Production deployment guide
