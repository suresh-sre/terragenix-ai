# TerraGenix AI – Cloud Terraform Generator

> Generate Terraform code for AWS, Azure & GCP in seconds ⚡

## Table of Contents

- [🚀 Features](#-features)
- [📦 Installation](#-installation)
- [🔑 API Key Setup](#-api-key-setup)
- [💻 Usage](#-usage)
  - [Web Application](#1-web-application-recommended)
  - [Command Line Interface](#2-command-line-interface-cli)
- [🚀 Deployment to Vercel](#-deployment-to-vercel)
- [📂 Output Structure](#-output-structure)
- [🛠️ Troubleshooting](#️-troubleshooting)

## 🚀 Features

- **Multi-Cloud Support**: Generate infrastructure for AWS, Azure, and Google Cloud Platform (GCP)
- **AI-Powered**: Uses advanced Google Gemini models (`gemini-2.0-flash`, `gemini-1.5-pro`, etc.) for intelligent code generation
- **Dual Interface**:
  - **CLI Tool**: For automation, scripts, and quick generation
  - **Web Application**: A beautiful, interactive web UI for easy visual generation
- **Complete Output**: Generates `provider.tf`, `variables.tf`, `main.tf`, `outputs.tf`, `terraform.tfvars.example`, and `README.md`
- **Flexible Export**: Save as individual files, a single bundle text file, or download as a ZIP archive (Web)
- **Cloud Deployment**: Deploy to Vercel for free online hosting

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key (free from [Google AI Studio](https://aistudio.google.com/app/apikey))

### Install Dependencies
```bash
pip install -r requirements.txt
```

*Dependencies: `google-generativeai`, `flask`*

## 🔑 API Key Setup

Get your free Google Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

**Three ways to provide your API key:**

1. **Environment Variable**:
   ```bash
   # Linux/Mac
   export GEMINI_API_KEY="your_key_here"

   # Windows PowerShell
   $env:GEMINI_API_KEY="your_key_here"
   ```

2. **CLI Flag**: Pass via `-k "your_key_here"` argument

3. **Web UI**: Enter directly in the web interface

## 💻 Usage

### 1. Web Application (Recommended)

Start the interactive web server:

```bash
python antigravity_terraform_generator_web.py
```

Then open **http://localhost:5000** in your browser.

**How to use:**
- Enter your Gemini API Key
- Select your cloud provider (AWS/Azure/GCP)
- List the services/resources you need (e.g., `ec2, rds, vpc`)
- Add any specific requirements (optional)
- Click **🚀 Generate Terraform Code**
- Download the generated ZIP file with all Terraform files

### 2. Command Line Interface (CLI)

Generate Terraform code directly from your terminal.

**Basic Syntax:**
```bash
python antigravity_terraform_generator.py -k "YOUR_API_KEY" -p [aws|azure|gcp] -s "service1,service2" [options]
```

**Examples:**

**Generate AWS Infrastructure (Save to Directory):**
```bash
python antigravity_terraform_generator.py -k "AIzaSy..." -p aws -s "ec2,rds,vpc" -o ./my-aws-infra
```
*Creates a folder `my-aws-infra` with all Terraform files.*

**Generate Azure Infrastructure (Save as Bundle File):**
```bash
python antigravity_terraform_generator.py -k "AIzaSy..." -p azure -s "vm,sql-database" -b azure-bundle.txt
```

**Generate GCP Infrastructure (Print to Console):**
```bash
python antigravity_terraform_generator.py -k "AIzaSy..." -p gcp -s "compute-instance,cloud-sql"
```

## 🚀 Deployment to Vercel

Deploy your Terraform Generator web app to Vercel for free online hosting and sharing.

### Prerequisites
- GitHub account
- Vercel account ([vercel.com](https://vercel.com))

### Deployment Steps

1. **Push to GitHub**: Commit and push your code to a GitHub repository

2. **Connect to Vercel**:
   - Visit [vercel.com](https://vercel.com) and sign in
   - Click **"New Project"** and import your GitHub repository

3. **Auto-Configuration**:
   - Vercel automatically detects Python and uses `requirements.txt`
   - The `vercel.json` file routes all requests to your Flask app in `api/index.py`

4. **Deploy**: Click **"Deploy"** and wait for completion

5. **Access Your App**: Your web app will be live at `https://your-project-name.vercel.app`

### Benefits of Vercel Deployment
- **🌐 Online Access**: Share your Terraform Generator with anyone via the Vercel URL
- **🔄 Automatic Updates**: Push changes to GitHub, Vercel redeploys automatically
- **🆓 Free Tier**: Perfect for personal use with Vercel's generous free plan

## 📂 Output Structure

When you generate Terraform code (via CLI directory save or Web ZIP download), you get these files:

| File | Description |
|------|-------------|
| `provider.tf` | Cloud provider configuration and authentication |
| `variables.tf` | Input variables definitions |
| `main.tf` | Core infrastructure resources and configurations |
| `outputs.tf` | Output values (IPs, IDs, endpoints, etc.) |
| `terraform.tfvars.example` | Example variable values for customization |
| `README.md` | Documentation and usage instructions for the generated infrastructure |

## 🛠️ Troubleshooting

### Common Issues

**"Model not found" Error**
- The tool tries multiple Gemini models automatically (`gemini-2.0-flash`, `gemini-1.5-flash`, etc.)
- Ensure your API key has access to these models
- Check your API quota at [Google AI Studio](https://aistudio.google.com/app/apikey)

**"500 Internal Server Error"**
- Usually indicates invalid API key or network connectivity issues
- Check your terminal/console for detailed error logs
- Verify your API key is correct and has sufficient quota

**Web App Won't Start**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that port 5000 is available
- Try running with `python antigravity_terraform_generator_web.py`

**Vercel Deployment Issues**
- Ensure `vercel.json` and `api/index.py` are in the root directory
- Check Vercel build logs for Python dependency errors
- Verify your GitHub repository includes all necessary files

---

**Built with ❤️ using Google Gemini AI**  
*Generated by Antigravity Agent*
