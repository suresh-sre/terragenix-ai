# Terraform Generator Integration Guide

## Overview

The GenOpsLab landing page is now integrated with your Python Flask backend Terraform generator. Users can generate production-ready Terraform code directly from the landing page.

## Architecture

```
Frontend (Next.js)
  ↓
TerraformGenerator Modal Component
  ↓
Next.js API Routes (/api/generate, /api/download)
  ↓
Python Flask Backend (e:\AWS-Interview\terragenix-ai-\api\index.py)
  ↓
TerraformGenerator + Gemini AI
```

## Setup Instructions

### 1. Configure the Backend URL

Create a `.env.local` file in the `genopslab/` directory:

```bash
cp .env.local.example .env.local
```

Edit `.env.local` and update the API URL:

```env
# For local development
NEXT_PUBLIC_API_URL=http://localhost:5000

# For production (example with ngrok or deployed server)
NEXT_PUBLIC_API_URL=https://your-api-domain.com
```

### 2. Start the Python Backend

In a separate terminal, start your Flask API:

```bash
cd e:\AWS-Interview\terragenix-ai-
python api/index.py
```

The Flask server runs on `http://localhost:5000`

### 3. Start the Next.js Frontend

In another terminal:

```bash
cd genopslab
npm install
npm run dev
```

The frontend runs on `http://localhost:3000`

### 4. Test the Integration

1. Open http://localhost:3000 in your browser
2. Scroll to the "Generate Infrastructure" feature card
3. Click on the card or "Try it now" button
4. A modal will open with the Terraform generator form
5. Enter your Gemini API key (from https://aistudio.google.com/app/apikey)
6. Select a cloud provider (AWS, Azure, or GCP)
7. Enter services/resources you want to generate
8. Click "Generate Terraform Code"
9. View and download the generated code!

## Files Added/Modified

### New Files

```
genopslab/
├── app/api/
│   ├── generate/route.ts          # API route to proxy generate requests
│   └── download/route.ts          # API route to proxy download requests
├── app/components/
│   └── TerraformGenerator.tsx      # Modal component for Terraform generator
├── .env.local.example             # Example environment file
└── TERRAFORM_INTEGRATION.md       # This file
```

### Modified Files

```
genopslab/
├── app/components/
│   └── Features.tsx               # Updated to open generator modal
```

## Component Details

### TerraformGenerator Modal (`app/components/TerraformGenerator.tsx`)

A React component that provides:

- **Form Inputs:**
  - Gemini API Key (password field)
  - Cloud Provider Selection (AWS, Azure, GCP)
  - Services/Resources (textarea with examples)
  - Additional Requirements (textarea, optional)

- **States:**
  - Form input
  - Loading state with spinner
  - Generated code display
  - Error handling

- **Actions:**
  - Generate Terraform code
  - Copy code to clipboard
  - Download individual files
  - Download all as ZIP
  - Generate new code

### API Routes

#### `/api/generate` (POST)

Proxies requests to the Python backend's `/generate` endpoint.

**Request:**
```json
{
  "api_key": "your-gemini-api-key",
  "cloud_provider": "aws|azure|gcp",
  "services": "ec2, rds, s3",
  "requirements": "optional: use t3.micro, enable encryption"
}
```

**Response:**
```json
{
  "data": {
    "README.md": "...",
    "provider.tf": "...",
    "main.tf": "...",
    "variables.tf": "...",
    "outputs.tf": "...",
    "terraform.tfvars.example": "..."
  }
}
```

#### `/api/download` (POST)

Proxies requests to the Python backend's `/download` endpoint.

**Request:**
```json
{
  "code": {
    "README.md": "...",
    "provider.tf": "..."
  },
  "cloud_provider": "aws"
}
```

**Response:**
- Binary ZIP file with all Terraform files

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend Flask server URL | `http://localhost:5000` |

**Important:** The `NEXT_PUBLIC_` prefix means this variable is exposed to the browser. Keep your API key request secure on the backend.

## Deployment

### Local Development
```bash
# Terminal 1: Start Flask backend
python api/index.py

# Terminal 2: Start Next.js frontend
cd genopslab && npm run dev
```

### Production Deployment

**For Vercel (Recommended):**

1. Deploy Flask backend separately (Heroku, Railway, AWS, etc.)
2. Update `NEXT_PUBLIC_API_URL` in Vercel environment variables
3. Deploy Next.js to Vercel as usual

**Example Vercel Environment Variable:**
```
NEXT_PUBLIC_API_URL=https://your-api.herokuapp.com
```

### CORS Considerations

If your frontend and backend are on different domains, ensure your Flask backend has CORS enabled. You may need to add this to `api/index.py`:

```python
from flask_cors import CORS
CORS(app)
```

## Error Handling

The integration includes error handling for:

- Missing API key
- Missing services/resources
- Backend connection failures
- Generation failures
- Network timeouts

All errors are displayed in the modal with user-friendly messages.

## User Flow

```
1. User lands on homepage
2. Sees "Generate Infrastructure" feature card
3. Clicks card → TerraformGenerator modal opens
4. Fills in form:
   - Gemini API Key
   - Cloud Provider
   - Services
   - Requirements (optional)
5. Clicks "Generate Terraform Code"
6. Modal shows loading spinner
7. Backend generates code using Gemini AI
8. Code displayed in modal
9. User can:
   - Copy individual files
   - Download individual files
   - Download all as ZIP
   - Generate new code
10. Close modal and continue browsing
```

## Future Enhancements

Potential features to add:

- [ ] Save generated code to user account
- [ ] Template library with pre-built configurations
- [ ] Cost estimation before generation
- [ ] GitHub integration to create repos
- [ ] Version control for generated code
- [ ] Deployment preview/simulation
- [ ] Code review suggestions
- [ ] Integration with Terraform Cloud

## Troubleshooting

### "Cannot connect to backend"

- Ensure Flask server is running on port 5000
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Verify no firewall is blocking connections

### "API key error"

- Generate a free API key from https://aistudio.google.com/app/apikey
- Ensure key is valid and not expired

### "Generation failed"

- Check Flask server logs for detailed error
- Verify services are valid for selected cloud provider
- Try simpler services first

### CORS errors

- Add CORS support to Flask backend
- Verify frontend and backend URLs are correct

## Support

For issues:

1. Check the Python backend logs
2. Verify environment configuration
3. Review error messages in browser console
4. Check Network tab in browser DevTools

## Files Reference

- **Frontend:** `genopslab/app/components/TerraformGenerator.tsx`
- **API Routes:** `genopslab/app/api/generate/route.ts`, `genopslab/app/api/download/route.ts`
- **Python Backend:** `e:\AWS-Interview\terragenix-ai-\api\index.py`
- **Environment:** `genopslab\.env.local`

---

**Integration Status:** ✅ Complete and functional!
