#!/bin/bash
# GenOpsLab Heroku Deployment Script
# Deploy backend to Heroku in one command

set -e

echo "🚀 GenOpsLab Heroku Deployment Script"
echo "======================================"
echo ""

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Install it from:"
    echo "   https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Check if user is logged in
if ! heroku auth:whoami &> /dev/null; then
    echo "🔑 Logging into Heroku..."
    heroku login
fi

echo ""
echo "📱 Enter your app name (must be unique):"
echo "   Example: genopslab-api-2024"
read -p "App name: " APP_NAME

if [ -z "$APP_NAME" ]; then
    echo "❌ App name cannot be empty"
    exit 1
fi

echo ""
echo "📦 Creating Heroku app: $APP_NAME..."
heroku create $APP_NAME

echo ""
echo "🚀 Deploying to Heroku..."
echo "   This may take 2-3 minutes..."
git push heroku main

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📋 Your Backend URL:"
BACKEND_URL=$(heroku apps:info $APP_NAME --json | grep '"web_url"' | cut -d'"' -f4)
echo "   $BACKEND_URL"
echo ""

echo "🔗 Next Steps:"
echo "1. Copy your backend URL: $BACKEND_URL"
echo "2. Go to Vercel Dashboard"
echo "3. Select GenOpsLab project → Settings → Environment Variables"
echo "4. Add:"
echo "   Name:  NEXT_PUBLIC_API_URL"
echo "   Value: $BACKEND_URL"
echo "5. Redeploy Vercel frontend"
echo ""
echo "✨ Your app will be live in a few minutes!"
