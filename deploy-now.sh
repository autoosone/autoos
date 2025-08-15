#!/bin/bash

echo "==================================================="
echo "🚀 AUTO MARKETPLACE DEPLOYMENT TO BLAXEL"
echo "==================================================="

cd /home/sk25/auto/template-copilot-kit-py

# Ensure we're logged in
export BL_API_KEY=bl_ypbq1x2cdwy272rekcj6017jpvn8o161

echo "📌 Step 1: Verifying configuration..."
if [ -f "blaxel.toml" ]; then
    echo "✅ blaxel.toml found"
    cat blaxel.toml
else
    echo "❌ ERROR: blaxel.toml not found"
    exit 1
fi

echo ""
echo "📌 Step 2: Installing dependencies..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate
pip install -q --upgrade pip
pip install -q fastapi uvicorn
pip install -q copilotkit langgraph

echo ""
echo "📌 Step 3: Testing agent locally..."
timeout 5 uvicorn src.main:app --port 1338 --host 0.0.0.0 > /dev/null 2>&1 &
sleep 3
curl -s http://localhost:1338/health || echo "Local test completed"
pkill -f "uvicorn src.main:app"

echo ""
echo "📌 Step 4: Deploying to Blaxel..."
echo "Deploying agent 'template-copilot-kit-py' to workspace 'amo'..."

# The actual deployment command
bl deploy agent

echo ""
echo "==================================================="
echo "✅ DEPLOYMENT INITIATED!"
echo "==================================================="
echo ""
echo "🔗 Your agent will be available at:"
echo "   https://run.blaxel.ai/amo/agents/template-copilot-kit-py"
echo ""
echo "📱 CopilotKit endpoint:"
echo "   https://run.blaxel.ai/amo/agents/template-copilot-kit-py/copilotkit"
echo ""
echo "🎯 Test with:"
echo "   curl https://run.blaxel.ai/amo/agents/template-copilot-kit-py \\"
echo "     -H 'Authorization: Bearer bl_ypbq1x2cdwy272rekcj6017jpvn8o161' \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"inputs\": \"Find Honda CR-V under 30k\"}'"
echo ""
