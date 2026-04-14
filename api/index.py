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
    <title>Cloud Terraform Generator - Python Edition</title>
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

        .copy-btn:hover {
            background: rgba(255, 255, 255, 0.2);
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
            <h1>☁️ Cloud Terraform Generator <span class="badge">Python Edition</span></h1>
            <p>AI-Powered Infrastructure as Code Generator</p>
        </div>

        <div class="input-section" id="inputForm">
            <div class="input-group">
                <label for="apiKey">🔑 Gemini API Key</label>
                <input type="password" id="apiKey" placeholder="Enter your Gemini API Key">
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

            if (!apiKey || !selectedCloud || !services) {
                errorMsg.textContent = "Please fill in API Key, select a cloud provider, and enter services!";
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
                            <button class="copy-btn" onclick="copyCode('${filename}')">📋 Copy</button>
                            <pre id="code-${filename}">${escapeHtml(data[filename])}</pre>
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
</body>
</html>
"""


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


if __name__ == '__main__':
    print("=" * 70)
    print("☁️  Cloud Terraform Generator - Python Web Edition")
    print("=" * 70)
    print("\n🚀 Starting server...")
    print("📍 Open your browser and go to: http://localhost:5000")
    print("\n💡 Press Ctrl+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)