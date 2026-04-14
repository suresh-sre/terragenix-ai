#!/usr/bin/env python3
"""
Cloud Terraform Generator - Flask Web Application
AI-Powered Infrastructure as Code Generator with Web Interface
"""

import os
import json
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify, send_file
from antigravity_terraform_generator import TerraformGenerator
import io
import zipfile

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TerraGenix AI - Cloud Terraform Generator</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --aws-orange: #FF9900;
            --azure-blue: #0078D4;
            --gcp-blue: #4285F4;
            --dark: #1a1a2e;
            --darker: #0f0f1e;
            --light: #f5f7fa;
            --accent: #6c5ce7;
            --success: #00b894;
            --border: #e1e8ed;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: var(--dark);
            min-height: 100vh;
            padding: 20px;
            line-height: 1.6;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
            animation: fadeInDown 0.6s ease-out;
        }

        .header h1 {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        }

        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }

        .badge {
            display: inline-block;
            background: var(--success);
            color: white;
            padding: 5px 12px;
            border-radius: 6px;
            font-size: 0.9rem;
            margin-left: 10px;
            font-weight: 600;
        }

        .input-section {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            margin-bottom: 30px;
            animation: fadeInUp 0.6s ease-out;
        }

        .input-group {
            margin-bottom: 25px;
        }

        label {
            display: block;
            font-weight: 600;
            margin-bottom: 8px;
            font-size: 1.1rem;
            color: var(--dark);
        }

        input, textarea, select {
            width: 100%;
            padding: 14px 18px;
            border: 2px solid var(--border);
            border-radius: 12px;
            font-family: 'Inter', sans-serif;
            font-size: 1rem;
            transition: all 0.3s ease;
            background: var(--light);
        }

        input:focus, textarea:focus, select:focus {
            outline: none;
            border-color: var(--accent);
            background: white;
            box-shadow: 0 0 0 3px rgba(108, 92, 231, 0.1);
        }

        textarea {
            resize: vertical;
            font-family: 'JetBrains Mono', monospace;
        }

        .cloud-selector {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 10px;
        }

        .cloud-option {
            padding: 20px;
            border: 3px solid var(--border);
            border-radius: 12px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            background: white;
            font-weight: 600;
        }

        .cloud-option:hover {
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }

        .cloud-option.selected {
            border-width: 3px;
        }

        .cloud-option.aws.selected {
            border-color: var(--aws-orange);
            background: rgba(255, 153, 0, 0.1);
            color: var(--aws-orange);
        }

        .cloud-option.azure.selected {
            border-color: var(--azure-blue);
            background: rgba(0, 120, 212, 0.1);
            color: var(--azure-blue);
        }

        .cloud-option.gcp.selected {
            border-color: var(--gcp-blue);
            background: rgba(66, 133, 244, 0.1);
            color: var(--gcp-blue);
        }

        button {
            background: linear-gradient(135deg, var(--accent) 0%, #5f3dc4 100%);
            color: white;
            border: none;
            padding: 18px 40px;
            font-size: 1.2rem;
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            cursor: pointer;
            border-radius: 12px;
            width: 100%;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(108, 92, 231, 0.4);
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(108, 92, 231, 0.6);
        }

        button:active {
            transform: translateY(0);
        }

        button:disabled {
            background: #ccc;
            cursor: not-allowed;
            box-shadow: none;
        }

        .output-section {
            display: none;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            animation: fadeInUp 0.6s ease-out;
        }

        .output-section.visible {
            display: block;
        }

        .output-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid var(--border);
        }

        .output-title {
            font-size: 2rem;
            font-weight: 700;
            color: var(--dark);
        }

        .action-buttons {
            display: flex;
            gap: 10px;
        }

        .btn-secondary {
            background: var(--success);
            padding: 12px 24px;
            font-size: 1rem;
            width: auto;
        }

        .btn-tertiary {
            background: #636e72;
            padding: 12px 24px;
            font-size: 1rem;
            width: auto;
        }

        .code-block {
            background: var(--darker);
            color: #f8f8f2;
            padding: 25px;
            border-radius: 12px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.95rem;
            overflow-x: auto;
            margin-bottom: 20px;
            position: relative;
            line-height: 1.6;
        }

        .code-block pre {
            margin: 0;
            white-space: pre-wrap;
            word-wrap: break-word;
        }

        .copy-btn {
            position: absolute;
            top: 15px;
            right: 15px;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: white;
            padding: 8px 16px;
            font-size: 0.85rem;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.3s ease;
            width: auto;
        }

        .code-actions {
            display: flex;
            gap: 10px;
            margin-bottom: 10px;
            justify-content: flex-end;
        }

        .download-btn {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: white;
            padding: 6px 12px;
            font-size: 0.8rem;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .download-btn:hover {
            background: rgba(255, 255, 255, 0.2);
        }

        .code-block pre {
            margin: 0;
            white-space: pre-wrap;
            word-wrap: break-word;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
            line-height: 1.5;
        }

        .code-block code {
            font-family: inherit;
        }

        .section-title {
            font-size: 1.5rem;
            font-weight: 600;
            margin: 30px 0 15px 0;
            color: var(--dark);
        }

        .loader {
            display: none;
            text-align: center;
            margin-top: 20px;
        }

        .loader.active {
            display: block;
        }

        .spinner {
            border: 4px solid rgba(108, 92, 231, 0.1);
            border-top: 4px solid var(--accent);
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }

        .error-msg {
            color: #d63031;
            text-align: center;
            margin-top: 15px;
            font-weight: 600;
            padding: 15px;
            background: rgba(214, 48, 49, 0.1);
            border-radius: 8px;
            display: none;
        }

        .error-msg.active {
            display: block;
        }

        .cta-line {
            text-align: center;
            margin-top: 20px;
            padding: 15px;
            background: rgba(108, 92, 231, 0.1);
            border-radius: 8px;
            border-left: 4px solid var(--accent);
        }

        .cta-line p {
            color: var(--accent);
            font-weight: 600;
            margin: 0;
            font-size: 1.1rem;
        }

        .footer {
            text-align: center;
            padding: 30px 20px;
            background: #000000;
            color: white;
            font-size: 1.1rem;
            margin-top: 40px;
            border-top: 2px solid var(--accent);
        }

        .footer p {
            margin: 0 0 10px 0;
            font-weight: 600;
        }

        .social-links {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 15px;
        }

        .social-link {
            color: #4a90e2;
            text-decoration: none;
            font-weight: 500;
            font-size: 0.95rem;
            transition: all 0.3s ease;
        }

        .social-link:hover {
            color: white;
            text-decoration: underline;
        }

        .cloud-icons {
            display: flex;
            justify-content: center;
            gap: 30px;
            opacity: 0.8;
        }

        .cloud-icons .cloud-icon {
            font-size: 2.5rem;
            transition: all 0.3s ease;
        }

        .cloud-icons .cloud-icon:hover {
            opacity: 1;
            transform: scale(1.1);
        }

        .cloud-icons .aws { color: var(--aws-orange); }
        .cloud-icons .azure { color: var(--azure-blue); }
        .cloud-icons .gcp { color: var(--gcp-blue); }

        .info-box {
            background: rgba(66, 133, 244, 0.1);
            border-left: 4px solid var(--gcp-blue);
            padding: 15px;
            border-radius: 8px;
            margin-top: 10px;
            font-size: 0.95rem;
        }

        .info-box a {
            color: var(--gcp-blue);
            font-weight: 600;
            text-decoration: none;
        }

        .info-box a:hover {
            text-decoration: underline;
        }

        .demo-notice {
            margin-top: 15px;
            text-align: center;
        }

        .demo-btn {
            background: linear-gradient(135deg, var(--success) 0%, #00a085 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 1rem;
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            cursor: pointer;
            border-radius: 8px;
            width: 100%;
            margin-bottom: 8px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 184, 148, 0.4);
        }

        .demo-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 184, 148, 0.6);
        }

        .demo-text {
            color: var(--accent);
            font-size: 0.9rem;
            margin: 0;
            font-weight: 500;
        }

        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        @media (max-width: 768px) {
            .header h1 {
                font-size: 2rem;
            }
            .input-section, .output-section {
                padding: 25px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>TerraGenix AI</h1>
            <p>Cloud Terraform Generator</p>
        </div>

        <div class="input-section" id="inputForm">
            <div class="input-group">
                <label for="apiKey">🔑 Gemini API Key</label>
                <input type="password" id="apiKey" placeholder="Enter your Gemini API Key">
                <div class="demo-notice">
                    <button class="demo-btn" onclick="enableDemoMode()">🚀 Try Demo Mode (No API Key Needed)</button>
                    <p class="demo-text">Generate sample Terraform code without an API key</p>
                </div>
                <div class="info-box">
                    Don't have an API key? Get it free from 
                    <a href="https://aistudio.google.com/app/apikey" target="_blank">Google AI Studio</a>
                </div>
            </div>

            <div class="input-group">
                <label>☁️ Select Cloud Provider</label>
                <div class="cloud-selector">
                    <div class="cloud-option aws" onclick="selectCloud('aws')">
                        <div style="font-size: 2rem;">☁️</div>
                        <div>AWS</div>
                    </div>
                    <div class="cloud-option azure" onclick="selectCloud('azure')">
                        <div style="font-size: 2rem;">☁️</div>
                        <div>Azure</div>
                    </div>
                    <div class="cloud-option gcp" onclick="selectCloud('gcp')">
                        <div style="font-size: 2rem;">☁️</div>
                        <div>GCP</div>
                    </div>
                </div>
                <input type="hidden" id="cloudProvider">
            </div>

            <div class="input-group">
                <label for="services">🛠️ Services/Resources (comma or line separated)</label>
                <textarea id="services" rows="5" placeholder="Examples:
AWS: ec2, rds, s3, vpc, lambda
Azure: vm, sql-database, storage-account, vnet
GCP: compute-instance, cloud-sql, storage-bucket, vpc"></textarea>
            </div>

            <div class="input-group">
                <label for="requirements">📋 Additional Requirements (Optional)</label>
                <textarea id="requirements" rows="4" placeholder="Example: Use t3.micro for EC2, enable encryption, add tags for production environment, use us-east-1 region"></textarea>
            </div>

            <button onclick="generateTerraform()">🚀 Generate Terraform Code</button>

            <div class="cta-line">
                <p>💡 Describe your infrastructure → Get Terraform instantly</p>
            </div>

            <div class="loader" id="loader">
                <div class="spinner"></div>
                <p>Generating your infrastructure code...</p>
            </div>
            <div class="error-msg" id="errorMsg"></div>
        </div>

        <div class="output-section" id="output">
            <div class="output-header">
                <div class="output-title">📄 Generated Terraform Code</div>
                <div class="action-buttons">
                    <button class="btn-secondary" onclick="downloadZip()">📦 Download ZIP</button>
                    <button class="btn-tertiary" onclick="resetForm()">🔄 New</button>
                </div>
            </div>

            <div id="outputContent"></div>
        </div>
    </div>

    <script>
        let selectedCloud = '';
        let generatedCode = {};
        let isDemoMode = false;

        function enableDemoMode() {
            isDemoMode = true;
            document.getElementById('apiKey').value = 'DEMO_MODE';
            document.getElementById('apiKey').disabled = true;
            document.querySelector('.demo-btn').textContent = '✅ Demo Mode Enabled';
            document.querySelector('.demo-btn').style.background = 'linear-gradient(135deg, #636e72 0%, #4a4a4a 100%)';
            alert('Demo Mode Enabled! You can now generate sample Terraform code without an API key.');
        }

        function generateDemoTerraform(cloud, services, requirements) {
            // Generate sample Terraform code for demo purposes
            const demoData = {};

            // Sample README
            demoData['README.md'] = `# Terraform Infrastructure for ${cloud.toUpperCase()}

This Terraform configuration creates a basic infrastructure setup on ${cloud.toUpperCase()}.

## Resources Created
${services.split(',').map(s => `- ${s.trim()}`).join('\n')}

## Requirements
- Terraform >= 1.0
- ${cloud.toUpperCase()} CLI configured

## Usage
\`\`\`bash
terraform init
terraform plan
terraform apply
\`\`\`

Generated by TerraGenix AI - Demo Mode
`;

            // Sample provider.tf
            if (cloud === 'aws') {
                demoData['provider.tf'] = `terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}`;
            } else if (cloud === 'azure') {
                demoData['provider.tf'] = `terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}`;
            } else if (cloud === 'gcp') {
                demoData['provider.tf'] = `terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = "your-project-id"
  region  = "us-central1"
}`;
            }

            // Sample variables.tf
            demoData['variables.tf'] = `# Input variables for ${cloud.toUpperCase()} infrastructure

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "demo"
}

variable "region" {
  description = "Cloud region"
  type        = string
  default     = "${cloud === 'aws' ? 'us-east-1' : cloud === 'azure' ? 'East US' : 'us-central1'}"
}`;

            // Sample main.tf with basic resources
            if (cloud === 'aws') {
                demoData['main.tf'] = `# Basic AWS infrastructure - DEMO MODE

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name        = "demo-vpc"
    Environment = var.environment
  }
}

resource "aws_subnet" "public" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"

  tags = {
    Name = "demo-public-subnet"
  }
}

# Add more resources based on selected services...
`;
            } else if (cloud === 'azure') {
                demoData['main.tf'] = `# Basic Azure infrastructure - DEMO MODE

resource "azurerm_resource_group" "demo" {
  name     = "demo-rg"
  location = var.region
}

resource "azurerm_virtual_network" "demo" {
  name                = "demo-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.demo.location
  resource_group_name = azurerm_resource_group.demo.name
}

# Add more resources based on selected services...
`;
            } else if (cloud === 'gcp') {
                demoData['main.tf'] = `# Basic GCP infrastructure - DEMO MODE

resource "google_compute_network" "demo" {
  name                    = "demo-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "demo" {
  name          = "demo-subnet"
  ip_cidr_range = "10.0.1.0/24"
  region        = var.region
  network       = google_compute_network.demo.id
}

# Add more resources based on selected services...
`;
            }

            // Sample outputs.tf
            demoData['outputs.tf'] = `# Infrastructure outputs

output "environment" {
  description = "Deployment environment"
  value       = var.environment
}

output "region" {
  description = "Cloud region"
  value       = var.region
}

# Add specific resource outputs here...
`;

            // Sample terraform.tfvars.example
            demoData['terraform.tfvars.example'] = `# Example variable values
# Copy this file to terraform.tfvars and customize

environment = "production"
region      = "${cloud === 'aws' ? 'us-east-1' : cloud === 'azure' ? 'East US' : 'us-central1'}"`;

            return demoData;
        }

        function selectCloud(cloud) {
            selectedCloud = cloud;
            document.getElementById('cloudProvider').value = cloud;

            document.querySelectorAll('.cloud-option').forEach(el => {
                el.classList.remove('selected');
            });

            document.querySelector(`.cloud-option.${cloud}`).classList.add('selected');
        }

        async function generateTerraform() {
            const apiKey = document.getElementById('apiKey').value.trim();
            const services = document.getElementById('services').value.trim();
            const requirements = document.getElementById('requirements').value.trim();
            const loader = document.getElementById('loader');
            const errorMsg = document.getElementById('errorMsg');
            const output = document.getElementById('output');
            const inputForm = document.getElementById('inputForm');

            if (!selectedCloud || !services) {
                errorMsg.textContent = "Please select a cloud provider and enter services!";
                errorMsg.classList.add('active');
                return;
            }

            if (!isDemoMode && !apiKey) {
                errorMsg.textContent = "Please enter an API key or try Demo Mode!";
                errorMsg.classList.add('active');
                return;
            }

            errorMsg.classList.remove('active');
            loader.classList.add('active');

            try {
                let result;

                if (isDemoMode) {
                    // Generate demo/sample Terraform code
                    result = generateDemoTerraform(selectedCloud, services, requirements);
                } else {
                    // Call actual API
                    const response = await fetch('/generate', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            api_key: apiKey,
                            cloud_provider: selectedCloud,
                            services: services,
                            requirements: requirements
                        })
                    });

                    result = await response.json();

                    if (!response.ok) {
                        throw new Error(result.error || 'Generation failed');
                    }
                    result = result.data;
                }

                generatedCode = result;
                renderOutput(result);

                loader.classList.remove('active');
                inputForm.style.display = 'none';
                output.classList.add('visible');

            } catch (error) {
                console.error(error);
                loader.classList.remove('active');
                errorMsg.innerHTML = `<strong>Generation Failed</strong><br>${error.message}`;
                errorMsg.classList.add('active');
            }
        }

        function renderOutput(data) {
            const outputContent = document.getElementById('outputContent');
            outputContent.innerHTML = '';

            const fileOrder = ['README.md', 'provider.tf', 'variables.tf', 'main.tf', 'outputs.tf', 'terraform.tfvars.example'];

            fileOrder.forEach(filename => {
                if (data[filename]) {
                    const section = document.createElement('div');
                    section.innerHTML = `
                        <div class="section-title">📄 ${filename}</div>
                        <div class="code-block">
                            <div class="code-actions">
                                <button class="copy-btn" onclick="copyCode('${filename}')">📋 Copy</button>
                                <button class="download-btn" onclick="downloadFile('${filename}')">📥 Download ${filename}</button>
                            </div>
                            <pre id="code-${filename}"><code>${escapeHtml(data[filename])}</code></pre>
                        </div>
                    `;
                    outputContent.appendChild(section);
                }
            });
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        function copyCode(filename) {
            const code = generatedCode[filename];
            navigator.clipboard.writeText(code).then(() => {
                const btn = event.target;
                const originalText = btn.textContent;
                btn.textContent = '✅ Copied!';
                setTimeout(() => {
                    btn.textContent = originalText;
                }, 2000);
            });
        }

        function downloadFile(filename) {
            const code = generatedCode[filename];
            const blob = new Blob([code], { type: 'text/plain' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        }

        async function downloadZip() {
            try {
                const response = await fetch('/download', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        code: generatedCode,
                        cloud_provider: selectedCloud
                    })
                });

                if (!response.ok) {
                    throw new Error('Download failed');
                }

                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `terraform-${selectedCloud}-${Date.now()}.zip`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
            } catch (error) {
                alert('Failed to download ZIP file: ' + error.message);
            }
        }

        function resetForm() {
            document.getElementById('inputForm').style.display = 'block';
            document.getElementById('output').classList.remove('visible');
            document.getElementById('apiKey').value = '';
            document.getElementById('apiKey').disabled = false;
            document.getElementById('services').value = '';
            document.getElementById('requirements').value = '';
            selectedCloud = '';
            isDemoMode = false;
            document.querySelectorAll('.cloud-option').forEach(el => {
                el.classList.remove('selected');
            });
            // Reset demo button
            document.querySelector('.demo-btn').textContent = '🚀 Try Demo Mode (No API Key Needed)';
            document.querySelector('.demo-btn').style.background = 'linear-gradient(135deg, var(--success) 0%, #00a085 100%)';
        }
    </script>

    <footer class="footer">
        <p>Built by Suresh Kumar | AWS DevOps Engineer</p>
        <div class="social-links">
            <a href="https://github.com/suresh-sre" target="_blank" class="social-link">🐙 GitHub</a>
            <a href="https://www.linkedin.com/in/suresh-cloud/" target="_blank" class="social-link">💼 LinkedIn</a>
        </div>
        <div class="cloud-icons">
            <span class="cloud-icon aws">☁️</span>
            <span class="cloud-icon azure">☁️</span>
            <span class="cloud-icon gcp">☁️</span>
        </div>
    </footer>
</body>
</html>"""


@app.route('/')
def index():
    """Render the main page"""
    return render_template_string(HTML_TEMPLATE)


@app.route('/generate', methods=['POST'])
def generate():
    """API endpoint to generate Terraform code"""
    try:
        data = request.get_json()
        
        api_key = data.get('api_key', '').strip()
        cloud_provider = data.get('cloud_provider', '').strip()
        services_input = data.get('services', '').strip()
        requirements = data.get('requirements', '').strip()
        
        if not api_key or not cloud_provider or not services_input:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Parse services
        services = [s.strip() for s in services_input.replace('\n', ',').split(',') if s.strip()]
        
        if not services:
            return jsonify({'error': 'No valid services provided'}), 400
        
        # Generate Terraform code
        generator = TerraformGenerator(api_key)
        result = generator.generate_terraform(
            cloud_provider,
            services,
            requirements if requirements else None
        )
        
        if not result:
            return jsonify({'error': 'Failed to generate Terraform code with all models'}), 500
        
        return jsonify({'data': result})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download', methods=['POST'])
def download():
    """API endpoint to download Terraform code as ZIP"""
    try:
        data = request.get_json()
        code = data.get('code', {})
        cloud_provider = data.get('cloud_provider', 'terraform')
        
        if not code:
            return jsonify({'error': 'No code to download'}), 400
        
        # Create ZIP file in memory
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for filename, content in code.items():
                zf.writestr(filename, content)
        
        memory_file.seek(0)
        
        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'terraform-{cloud_provider}-{datetime.now().strftime("%Y%m%d-%H%M%S")}.zip'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


