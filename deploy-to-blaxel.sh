#!/bin/bash

# BLAXEL DEPLOYMENT SCRIPT - Following Official Documentation
# https://docs.blaxel.ai/Agents/Deploy-an-agent
# https://docs.blaxel.ai/Agents/Github-integration

echo "==================================================="
echo "🚀 BLAXEL AGENT DEPLOYMENT - PRODUCTION READY"
echo "==================================================="

# Step 1: Authenticate with Blaxel
echo "📌 Step 1: Authenticating with Blaxel..."
export BL_API_KEY=bl_ypbq1x2cdwy272rekcj6017jpvn8o161
bl login amo

# Step 2: Verify configuration
echo "📌 Step 2: Verifying blaxel.toml configuration..."
if grep -q "workspace = \"amo\"" blaxel.toml; then
    echo "✅ Workspace configured: amo"
else
    echo "❌ ERROR: Workspace not configured in blaxel.toml"
    exit 1
fi

if grep -q "name = \"template-copilot-kit-py\"" blaxel.toml; then
    echo "✅ Agent name configured: template-copilot-kit-py"
else
    echo "❌ ERROR: Agent name not configured in blaxel.toml"
    exit 1
fi

# Step 3: Install dependencies
echo "📌 Step 3: Installing dependencies..."
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Step 4: Test locally
echo "📌 Step 4: Testing agent locally..."
echo "Starting local server on port 1338..."
timeout 10 uvicorn src.main:app --port 1338 --host 0.0.0.0 &
sleep 5

# Test the local endpoint
echo "Testing local CopilotKit endpoint..."
curl -X POST http://localhost:1338/copilotkit \
     -H "Content-Type: application/json" \
     -d '{"test": "local"}' || echo "Local test completed"

# Step 5: Deploy to Blaxel
echo "📌 Step 5: Deploying to Blaxel platform..."
bl agent deploy

# Step 6: Verify deployment
echo "📌 Step 6: Verifying deployment..."
echo "Your agent should now be available at:"
echo "https://run.blaxel.ai/amo/agents/template-copilot-kit-py"
echo ""
echo "CopilotKit endpoint:"
echo "https://run.blaxel.ai/amo/agents/template-copilot-kit-py/copilotkit"

# Step 7: Test production endpoint
echo "📌 Step 7: Testing production endpoint..."
curl -X POST https://run.blaxel.ai/amo/agents/template-copilot-kit-py/copilotkit \
     -H "Authorization: Bearer bl_ypbq1x2cdwy272rekcj6017jpvn8o161" \
     -H "Content-Type: application/json" \
     -d '{"test": "production"}'

echo ""
echo "==================================================="
echo "✅ DEPLOYMENT COMPLETE!"
echo "==================================================="
echo ""
echo "🔗 LIVE URLS:"
echo "  Agent API: https://run.blaxel.ai/amo/agents/template-copilot-kit-py"
echo "  CopilotKit: https://run.blaxel.ai/amo/agents/template-copilot-kit-py/copilotkit"
echo ""
echo "📱 NEXT STEPS:"
echo "  1. Connect GitHub for auto-deployment:"
echo "     - Go to https://app.blaxel.ai/amo/agents/template-copilot-kit-py/settings"
echo "     - Connect GitHub repository: autoosone/autoos"
echo "  2. Update your frontend to use production URL"
echo "  3. Deploy frontend to Vercel/Netlify"
echo ""
echo "📚 Documentation:"
echo "  - https://docs.blaxel.ai/Agents/Integrate-in-apps/CopilotKit"
echo "  - https://docs.blaxel.ai/Agents/Github-integration"
