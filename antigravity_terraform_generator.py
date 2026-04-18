#!/usr/bin/env python3
"""
Cloud Terraform Generator - Python Version
AI-Powered Infrastructure as Code Generator using Google Gemini API
"""

import os
import json
import sys
from typing import Dict, List, Optional
import argparse
from datetime import datetime

try:
    import google.generativeai as genai
except ImportError:
    print("Error: google-generativeai package not installed.")
    print("Install it with: pip install google-generativeai")
    sys.exit(1)


class TerraformGenerator:
    """Generate Terraform code using Google Gemini API"""
    
    MODEL_NAMES = [
        "gemini-2.0-flash",
        "gemini-2.0-flash-exp",
        "gemini-2.5-flash",
        "gemini-flash-latest",
        "gemini-1.5-flash",
        "gemini-1.5-pro"
    ]
    
    CLOUD_PROVIDERS = ["aws", "azure", "gcp"]
    
    def __init__(self, api_key: str):
        """Initialize with Gemini API key"""
        if not api_key:
            raise ValueError("API key is required")
        genai.configure(api_key=api_key)
        self.api_key = api_key
    
    def generate_terraform(
        self,
        cloud_provider: str,
        services: List[str],
        requirements: Optional[str] = None
    ) -> Optional[Dict[str, str]]:
        """
        Generate Terraform code for specified cloud infrastructure
        
        Args:
            cloud_provider: Cloud provider (aws, azure, gcp)
            services: List of services/resources to create
            requirements: Additional requirements and specifications
            
        Returns:
            Dictionary with filenames as keys and code as values, or None if failed
        """
        if cloud_provider.lower() not in self.CLOUD_PROVIDERS:
            raise ValueError(f"Cloud provider must be one of: {', '.join(self.CLOUD_PROVIDERS)}")
        
        services_str = ", ".join(services)
        requirements_str = requirements or "Use best practices and sensible defaults"
        
        prompt = f"""You are an expert DevOps engineer and Terraform specialist.

Task: Generate production-ready Terraform code for the following cloud infrastructure.

Inputs:
- Cloud Provider: {cloud_provider.upper()}
- Services/Resources: {services_str}
- Additional Requirements: {requirements_str}

Requirements:
1. Generate complete, working Terraform code with proper structure
2. Include:
   - provider.tf (provider configuration)
   - variables.tf (input variables with descriptions)
   - main.tf (main resource definitions)
   - outputs.tf (useful outputs)
   - terraform.tfvars.example (example variable values)
3. Follow Terraform best practices:
   - Use variables for configurable values
   - Add meaningful descriptions
   - Include tags/labels for resources
   - Use proper naming conventions
   - Add comments for clarity
4. Make it production-ready with security considerations
5. Include a README.md with:
   - Prerequisites
   - Usage instructions
   - Variable descriptions
   - Deployment steps

Output JSON Format ONLY:
{{
    "provider.tf": "terraform code here",
    "variables.tf": "terraform code here",
    "main.tf": "terraform code here",
    "outputs.tf": "terraform code here",
    "terraform.tfvars.example": "example values here",
    "README.md": "markdown documentation here"
}}

IMPORTANT: Return ONLY valid JSON. Do not include any markdown formatting or explanations outside the JSON."""
        
        errors = []
        import traceback
        for model_name in self.MODEL_NAMES:
            try:
                print(f"Attempting model: {model_name}...", file=sys.stderr)
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                
                # Extract JSON from response
                text = response.text
                json_str = text.replace("```json", "").replace("```", "").strip()
                
                # Find JSON boundaries
                first_open = json_str.find('{')
                last_close = json_str.rfind('}')
                
                if first_open != -1 and last_close != -1:
                    json_str = json_str[first_open:last_close + 1]
                
                data = json.loads(json_str)
                print(f"✓ Successfully generated with {model_name}", file=sys.stderr)
                return data
                
            except Exception as e:
                error_msg = f"{model_name}: {str(e)}"
                errors.append(error_msg)
                print(f"✗ {error_msg}", file=sys.stderr)
                traceback.print_exc(file=sys.stderr)
                continue
        
        print(f"\n❌ All models failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return None
    
    def save_to_files(self, terraform_code: Dict[str, str], output_dir: str) -> None:
        """
        Save generated Terraform code to individual files
        
        Args:
            terraform_code: Dictionary with filenames and code
            output_dir: Directory to save files to
        """
        os.makedirs(output_dir, exist_ok=True)
        
        for filename, code in terraform_code.items():
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(code)
            print(f"✓ Created: {filepath}", file=sys.stderr)
    
    def create_bundle(self, terraform_code: Dict[str, str], cloud_provider: str) -> str:
        """
        Create a text bundle of all Terraform files
        
        Args:
            terraform_code: Dictionary with filenames and code
            cloud_provider: Cloud provider name
            
        Returns:
            Formatted text bundle
        """
        lines = []
        lines.append(f"TERRAFORM CODE BUNDLE - {cloud_provider.upper()}")
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 60)
        lines.append("")
        
        file_order = [
            'README.md',
            'provider.tf',
            'variables.tf',
            'main.tf',
            'outputs.tf',
            'terraform.tfvars.example'
        ]
        
        for filename in file_order:
            if filename in terraform_code:
                lines.append("")
                lines.append("=" * 60)
                lines.append(f"FILE: {filename}")
                lines.append("=" * 60)
                lines.append("")
                lines.append(terraform_code[filename])
                lines.append("")
        
        return "\n".join(lines)


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="Generate Terraform infrastructure code using Google Gemini AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate AWS infrastructure
  python terraform_generator.py -k YOUR_API_KEY -p aws -s "ec2,rds,s3,vpc"
  
  # Generate with requirements and save to directory
  python terraform_generator.py -k YOUR_API_KEY -p azure -s "vm,sql-database,storage-account" \\
    -r "Use Standard tier, enable encryption, add production tags" -o ./azure-infra
  
  # Generate GCP infrastructure with bundle output
  python terraform_generator.py -k YOUR_API_KEY -p gcp -s "compute-instance,cloud-sql" \\
    -b terraform-bundle.txt
  
  # Use API key from environment variable
  export GEMINI_API_KEY="your-api-key"
  python terraform_generator.py -p aws -s "lambda,api-gateway,dynamodb"
        """
    )
    
    parser.add_argument(
        '-k', '--api-key',
        help='Google Gemini API key (or set GEMINI_API_KEY env var)',
        default=os.environ.get('GEMINI_API_KEY')
    )
    
    parser.add_argument(
        '-p', '--provider',
        required=True,
        choices=['aws', 'azure', 'gcp'],
        help='Cloud provider'
    )
    
    parser.add_argument(
        '-s', '--services',
        required=True,
        help='Comma-separated list of services/resources'
    )
    
    parser.add_argument(
        '-r', '--requirements',
        help='Additional requirements and specifications'
    )
    
    parser.add_argument(
        '-o', '--output-dir',
        help='Output directory to save Terraform files'
    )
    
    parser.add_argument(
        '-b', '--bundle',
        help='Save as a single bundle file instead of separate files'
    )
    
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output raw JSON instead of formatted files'
    )
    
    args = parser.parse_args()
    
    # Validate API key
    if not args.api_key:
        print("Error: API key required. Use -k flag or set GEMINI_API_KEY environment variable.", file=sys.stderr)
        print("\nGet your free API key from: https://aistudio.google.com/app/apikey", file=sys.stderr)
        sys.exit(1)
    
    # Parse services
    services = [s.strip() for s in args.services.split(',') if s.strip()]
    if not services:
        print("Error: No services provided", file=sys.stderr)
        sys.exit(1)
    
    print(f"☁️  Generating Terraform code for {args.provider.upper()}...", file=sys.stderr)
    print(f"🛠️  Services: {', '.join(services)}", file=sys.stderr)
    if args.requirements:
        print(f"📋 Requirements: {args.requirements}", file=sys.stderr)
    print("", file=sys.stderr)
    
    # Generate Terraform code
    generator = TerraformGenerator(args.api_key)
    terraform_code = generator.generate_terraform(
        args.provider,
        services,
        args.requirements
    )
    
    if not terraform_code:
        print("\n❌ Failed to generate Terraform code", file=sys.stderr)
        sys.exit(1)
    
    # Output handling
    if args.json:
        # Output raw JSON
        print(json.dumps(terraform_code, indent=2))
    elif args.bundle:
        # Save as bundle
        bundle_content = generator.create_bundle(terraform_code, args.provider)
        with open(args.bundle, 'w', encoding='utf-8') as f:
            f.write(bundle_content)
        print(f"\n✅ Terraform bundle saved to: {args.bundle}", file=sys.stderr)
    elif args.output_dir:
        # Save to directory
        generator.save_to_files(terraform_code, args.output_dir)
        print(f"\n✅ Terraform files saved to: {args.output_dir}", file=sys.stderr)
    else:
        # Print to stdout
        bundle_content = generator.create_bundle(terraform_code, args.provider)
        print(bundle_content)


if __name__ == '__main__':
    main()
