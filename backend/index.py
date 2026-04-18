#!/usr/bin/env python3
"""
Cloud Terraform Generator - Flask Web Application
AI-Powered Infrastructure as Code Generator with Web Interface
"""

import os
import json
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify, send_file
import io
import zipfile

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GenOps Lab - Cloud Terraform Generator</title>
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
            <h1>GenOps Lab</h1>
            <p>Cloud Terraform Generator</p>
        </div>

        <div class="input-section" id="inputForm">
            <div class="input-group">
                <label for="apiKey">🔑 Gemini API Key</label>
                <input type="password" id="apiKey" placeholder="Enter your Gemini API Key to generate Terraform code">
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

            if (!apiKey) {
                alert("Please enter your Gemini API key to generate Terraform code");
                return;
            }

            if (!selectedCloud || !services) {
                errorMsg.textContent = "Please select a cloud provider and enter services!";
                errorMsg.classList.add('active');
                return;
            }

            errorMsg.classList.remove('active');
            loader.classList.add('active');

            try {
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

                const result = await response.json();

                if (!response.ok) {
                    throw new Error(result.error || 'Generation failed');
                }

                generatedCode = result.data;
                renderOutput(result.data);

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
            document.getElementById('services').value = '';
            document.getElementById('requirements').value = '';
            selectedCloud = '';
            document.querySelectorAll('.cloud-option').forEach(el => {
                el.classList.remove('selected');
            });
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
        # ===== REQUEST PARSING =====
        data = request.get_json()
        if data is None:
            app.logger.error('[generate] Invalid JSON in request body')
            return jsonify({
                'error': 'Invalid request format',
                'code': 'INVALID_JSON',
                'message': 'Request body must be valid JSON'
            }), 400
        
        # ===== REQUEST VALIDATION =====
        api_key = data.get('api_key', '').strip()
        cloud_provider = data.get('cloud_provider', '').strip()
        services_input = data.get('services', '').strip()
        requirements = data.get('requirements', '').strip()
        
        # Check required fields
        if not api_key or not cloud_provider or not services_input:
            missing_fields = []
            if not api_key:
                missing_fields.append('api_key')
            if not cloud_provider:
                missing_fields.append('cloud_provider')
            if not services_input:
                missing_fields.append('services')
            
            app.logger.warning(f'[generate] Missing required fields: {missing_fields}')
            return jsonify({
                'error': 'Missing required fields',
                'code': 'REQUEST_VALIDATION_FAILED',
                'missing_fields': missing_fields,
                'message': f'Required fields are missing: {", ".join(missing_fields)}'
            }), 400
        
        # Validate cloud provider
        valid_providers = ['aws', 'azure', 'gcp']
        if cloud_provider.lower() not in valid_providers:
            app.logger.warning(f'[generate] Invalid cloud provider: {cloud_provider}')
            return jsonify({
                'error': 'Invalid cloud provider',
                'code': 'INVALID_CLOUD_PROVIDER',
                'message': f'Cloud provider must be one of: {", ".join(valid_providers)}',
                'provided': cloud_provider
            }), 400
        
        # ===== PARSE SERVICES =====
        services = [s.strip() for s in services_input.replace('\n', ',').split(',') if s.strip()]
        
        if not services:
            app.logger.warning('[generate] No valid services provided after parsing')
            return jsonify({
                'error': 'No valid services',
                'code': 'INVALID_SERVICES',
                'message': 'Please provide at least one service'
            }), 400
        
        # ===== LOGGING REQUEST DETAILS =====
        app.logger.info(f'[generate] Processing request')
        app.logger.info(f'[generate] Cloud provider: {cloud_provider}')
        app.logger.info(f'[generate] Services requested: {services}')
        app.logger.info(f'[generate] Requirements: {requirements if requirements else "None"}')
        
        # ===== GENERATION =====
        try:
            from antigravity_terraform_generator import TerraformGenerator

            generator = TerraformGenerator(api_key)
            result = generator.generate_terraform(
                cloud_provider,
                services,
                requirements if requirements else None
            )
        except ModuleNotFoundError as me:
            app.logger.error(f'[generate] Missing backend dependency: {str(me)}')
            return jsonify({
                'error': 'Backend generator module is missing',
                'code': 'BACKEND_MODULE_MISSING',
                'message': 'The Terraform generator backend is not fully deployed. Restore antigravity_terraform_generator.py and redeploy.',
                'details': str(me)
            }), 500
        except ValueError as ve:
            app.logger.error(f'[generate] Validation error during generation: {str(ve)}')
            return jsonify({
                'error': 'Invalid API key or parameters',
                'code': 'GENERATION_VALIDATION_FAILED',
                'message': str(ve)
            }), 400
        except Exception as ge:
            app.logger.error(f'[generate] Generation error: {str(ge)}')
            return jsonify({
                'error': 'Terraform generation failed',
                'code': 'GENERATION_FAILED',
                'message': 'Failed to generate Terraform code. Please check your API key and try again.',
                'details': str(ge)
            }), 500
        
        if not result:
            app.logger.error('[generate] Generator returned empty result')
            return jsonify({
                'error': 'Generation returned no content',
                'code': 'EMPTY_GENERATION',
                'message': 'Failed to generate Terraform code with available models'
            }), 500
        
        app.logger.info(f'[generate] Successfully generated Terraform code ({len(result)} files)')
        return jsonify({'data': result})
        
    except Exception as e:
        app.logger.error(f'[generate] Unexpected error: {str(e)}')
        return jsonify({
            'error': 'Internal server error',
            'code': 'INTERNAL_ERROR',
            'message': 'An unexpected error occurred. Please try again or contact support.'
        }), 500


@app.route('/download', methods=['POST'])
def download():
    """API endpoint to download Terraform code as ZIP"""
    try:
        # ===== REQUEST PARSING =====
        data = request.get_json()
        if data is None:
            app.logger.error('[download] Invalid JSON in request body')
            return jsonify({
                'error': 'Invalid request format',
                'code': 'INVALID_JSON',
                'message': 'Request body must be valid JSON'
            }), 400
        
        # ===== REQUEST VALIDATION =====
        code = data.get('code', {})
        cloud_provider = data.get('cloud_provider', 'terraform').strip()
        
        if not code or not isinstance(code, dict):
            app.logger.warning('[download] Missing or invalid code object')
            return jsonify({
                'error': 'No code to download',
                'code': 'INVALID_CODE',
                'message': 'Code object must be a non-empty dictionary with filenames as keys'
            }), 400
        
        if len(code) == 0:
            app.logger.warning('[download] Empty code object provided')
            return jsonify({
                'error': 'No files to download',
                'code': 'EMPTY_CODE',
                'message': 'Code object contains no files'
            }), 400
        
        app.logger.info(f'[download] Processing download request')
        app.logger.info(f'[download] Cloud provider: {cloud_provider}')
        app.logger.info(f'[download] Files to include: {list(code.keys())}')
        
        # ===== ZIP CREATION =====
        try:
            memory_file = io.BytesIO()
            with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
                for filename, content in code.items():
                    if not isinstance(filename, str) or not content:
                        app.logger.warning(f'[download] Skipping invalid file: {filename}')
                        continue
                    
                    try:
                        zf.writestr(filename, str(content))
                    except Exception as fe:
                        app.logger.error(f'[download] Failed to write file {filename}: {str(fe)}')
                        continue
            
            memory_file.seek(0)
            
            if memory_file.getbuffer().nbytes == 0:
                app.logger.error('[download] ZIP file is empty')
                return jsonify({
                    'error': 'Failed to create ZIP',
                    'code': 'ZIP_CREATION_FAILED',
                    'message': 'Could not create valid ZIP file'
                }), 500
            
            app.logger.info(f'[download] Successfully created ZIP file ({memory_file.getbuffer().nbytes} bytes)')
            
            return send_file(
                memory_file,
                mimetype='application/zip',
                as_attachment=True,
                download_name=f'terraform-{cloud_provider}-{datetime.now().strftime("%Y%m%d-%H%M%S")}.zip'
            )
        
        except Exception as ze:
            app.logger.error(f'[download] ZIP creation error: {str(ze)}')
            return jsonify({
                'error': 'ZIP creation failed',
                'code': 'ZIP_CREATION_ERROR',
                'message': 'Failed to create ZIP file. Please try again.'
            }), 500
        
    except Exception as e:
        app.logger.error(f'[download] Unexpected error: {str(e)}')
        return jsonify({
            'error': 'Internal server error',
            'code': 'INTERNAL_ERROR',
            'message': 'An unexpected error occurred. Please try again or contact support.'
        }), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', '').lower() in {'1', 'true', 'yes'}
    app.run(host='127.0.0.1', port=port, debug=debug)


