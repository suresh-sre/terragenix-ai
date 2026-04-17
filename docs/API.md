# API Reference - GenOpsLab

Complete API documentation for frontend and backend endpoints.

## Overview

GenOpsLab provides two layers of API:

1. **Frontend API Routes** (Next.js) - `/api/*`
   - Proxy requests to backend
   - Handle authentication, validation
   - Format responses for frontend

2. **Backend API Endpoints** (Flask) - Root service
   - Generate Terraform code
   - Download files
   - Legacy web UI

## Frontend API Routes

### POST /api/generate

Generate Terraform infrastructure code using AI.

**Endpoint:** `POST /api/generate`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "api_key": "string (required)",
  "cloud_provider": "aws|azure|gcp (required)",
  "services": "string (required)",
  "requirements": "string (optional)"
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| api_key | string | Yes | Google Gemini API key |
| cloud_provider | enum | Yes | Target cloud: `aws`, `azure`, or `gcp` |
| services | string | Yes | Comma-separated services (e.g., "ec2, rds, s3") |
| requirements | string | No | Additional requirements (e.g., "use t3.micro, enable encryption") |

**Response (Success):**
```json
{
  "data": {
    "README.md": "# AWS Infrastructure\n...",
    "provider.tf": "terraform { required_providers { ... } }",
    "main.tf": "resource \"aws_instance\" \"web\" { ... }",
    "variables.tf": "variable \"instance_type\" { ... }",
    "outputs.tf": "output \"instance_id\" { ... }",
    "terraform.tfvars.example": "instance_type = \"t3.micro\"\n..."
  }
}
```

**Response (Error):**
```json
{
  "error": "Error description"
}
```

**HTTP Status Codes:**
- `200` - Successfully generated code
- `400` - Invalid parameters
- `500` - Server error

**Example (cURL):**
```bash
curl -X POST http://localhost:3000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "AIzaSy...",
    "cloud_provider": "aws",
    "services": "ec2, rds, s3",
    "requirements": "us-east-1, t3.micro"
  }'
```

**Example (JavaScript):**
```javascript
const response = await fetch('/api/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    api_key: 'AIzaSy...',
    cloud_provider: 'aws',
    services: 'ec2, rds, s3',
    requirements: 'us-east-1, t3.micro'
  })
});

const data = await response.json();
console.log(data.data); // Generated code files
```

**Example (Python):**
```python
import requests

response = requests.post('http://localhost:3000/api/generate', json={
    'api_key': 'AIzaSy...',
    'cloud_provider': 'aws',
    'services': 'ec2, rds, s3',
    'requirements': 'us-east-1, t3.micro'
})

code_files = response.json()['data']
```

---

### POST /api/download

Download generated Terraform code as ZIP file.

**Endpoint:** `POST /api/download`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "code": {
    "README.md": "string",
    "provider.tf": "string",
    "main.tf": "string",
    "variables.tf": "string",
    "outputs.tf": "string",
    "terraform.tfvars.example": "string"
  },
  "cloud_provider": "aws|azure|gcp (optional)"
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| code | object | Yes | Generated code files (key: filename, value: content) |
| cloud_provider | enum | No | For naming: `aws`, `azure`, or `gcp` |

**Response (Success):**
- Binary ZIP file

**Response Headers:**
```
Content-Type: application/zip
Content-Disposition: attachment; filename="terraform-aws-1234567890.zip"
```

**HTTP Status Codes:**
- `200` - Successfully created ZIP
- `400` - Invalid parameters
- `500` - Server error

**Example (cURL):**
```bash
curl -X POST http://localhost:3000/api/download \
  -H "Content-Type: application/json" \
  -d '{
    "code": {
      "README.md": "# Infrastructure",
      "provider.tf": "..."
    },
    "cloud_provider": "aws"
  }' \
  --output infrastructure.zip
```

**Example (JavaScript):**
```javascript
const response = await fetch('/api/download', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    code: codeFiles,
    cloud_provider: 'aws'
  })
});

const blob = await response.blob();
const url = window.URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url;
a.download = 'terraform-aws.zip';
a.click();
```

---

## Backend API Endpoints

### Backend Base URL
- Development: `http://localhost:5000`
- Production: `https://api.genopslab.com` (or your domain)

### POST /generate

Backend endpoint for code generation (used by frontend proxy).

**Endpoint:** `POST /generate`

**Request:**
```json
{
  "api_key": "string",
  "cloud_provider": "aws|azure|gcp",
  "services": "string",
  "requirements": "string"
}
```

**Response:**
```json
{
  "success": true,
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

---

### POST /download

Backend endpoint for ZIP creation (used by frontend proxy).

**Endpoint:** `POST /download`

**Request:**
```json
{
  "code": { ... },
  "cloud_provider": "aws"
}
```

**Response:**
- Binary ZIP file

---

### GET /

Legacy web UI (for backwards compatibility).

**Endpoint:** `GET /`

**Response:**
- HTML web interface

---

## Error Handling

### Error Response Format

All errors return JSON:
```json
{
  "success": false,
  "error": "Descriptive error message"
}
```

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| Missing API key | api_key not provided | Provide valid Gemini API key |
| Invalid cloud provider | Unsupported provider | Use aws, azure, or gcp |
| Missing services | services empty | Specify at least one service |
| API rate limited | Too many requests | Wait before retrying |
| Invalid API key | Gemini key incorrect | Get new key from aistudio.google.com |
| Network error | Backend unreachable | Check backend is running |

---

## Rate Limiting

Current: No limit (development)

Recommended for production:
```
- 60 requests per minute per IP
- 1000 requests per hour per user
- Burst limit: 10 concurrent requests
```

---

## Authentication

Current: No authentication (API key is per-request)

Recommended for production:
```
POST /auth/login
- Accept email/password or OAuth
- Return JWT token

POST /api/generate
- Require Authorization header with JWT
- Track usage per user
```

---

## Pagination

Not applicable (single generation endpoint).

---

## Versioning

Current: v1 (implicit)

Recommended versioning:
```
/api/v1/generate
/api/v2/generate (future versions)
```

---

## Example Workflows

### Workflow 1: Generate and Download

```javascript
// Step 1: Generate code
const generateRes = await fetch('/api/generate', {
  method: 'POST',
  body: JSON.stringify({
    api_key: apiKey,
    cloud_provider: 'aws',
    services: 'ec2, rds, s3'
  })
});

const generated = await generateRes.json();
const codeFiles = generated.data;

// Step 2: Download as ZIP
const downloadRes = await fetch('/api/download', {
  method: 'POST',
  body: JSON.stringify({
    code: codeFiles,
    cloud_provider: 'aws'
  })
});

const blob = await downloadRes.blob();
// ... save blob as file
```

### Workflow 2: Generate and Display

```javascript
// Generate code
const res = await fetch('/api/generate', {
  method: 'POST',
  body: JSON.stringify({
    api_key: apiKey,
    cloud_provider: 'aws',
    services: 'lambda, apigateway'
  })
});

const { data } = await res.json();

// Display in code editor
Object.entries(data).forEach(([filename, content]) => {
  console.log(`File: ${filename}`);
  console.log(content);
});
```

### Workflow 3: Integration with Terraform Cloud

```javascript
// Generate code
const res = await fetch('/api/generate', { ... });
const { data } = await res.json();

// Upload to Terraform Cloud
const tfContent = data['main.tf'];
const res2 = await fetch('https://app.terraform.io/api/v2/workspaces/.../uploads', {
  method: 'POST',
  headers: { Authorization: 'Bearer YOUR_TF_TOKEN' },
  body: tfContent
});
```

---

## Limits & Constraints

| Item | Limit | Notes |
|------|-------|-------|
| Max services per request | 50 | Comma-separated list |
| Max requirements length | 2000 chars | Input validation |
| Max response size | 10 MB | ZIP file limit |
| Timeout | 30 seconds | API call duration |
| Concurrent requests | 10 | Per IP address |

---

## Testing

### Using Postman

1. Import collection:
```json
{
  "info": {
    "name": "GenOpsLab API"
  },
  "item": [
    {
      "name": "Generate Code",
      "request": {
        "method": "POST",
        "url": "{{baseUrl}}/api/generate",
        "body": {
          "mode": "raw",
          "raw": "{\"api_key\": \"...\", \"cloud_provider\": \"aws\", \"services\": \"ec2, rds\"}"
        }
      }
    }
  ]
}
```

2. Set variables:
```
baseUrl = http://localhost:3000
```

3. Test endpoints

### Using Thunder Client
- Import the same Postman collection

### Using REST Client (VS Code)
```http
### Generate Terraform
POST http://localhost:3000/api/generate
Content-Type: application/json

{
  "api_key": "AIzaSy...",
  "cloud_provider": "aws",
  "services": "ec2, rds, s3"
}

### Download ZIP
POST http://localhost:3000/api/download
Content-Type: application/json

{
  "code": {
    "main.tf": "resource..."
  },
  "cloud_provider": "aws"
}
```

---

## Support

For API issues:
1. Check response error message
2. Review documentation above
3. Check backend logs
4. Verify API key validity
5. Test with Postman/cURL

---

**Last Updated:** April 2024
**API Version:** v1
**Stability:** Production Ready
