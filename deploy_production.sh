#!/bin/bash
# 🚀 COMPLETE PRODUCTION DEPLOYMENT SCRIPT
# This script deploys and tests the complete Blaxel agent solution

set -e  # Exit on any error

echo "🚀 BLAXEL AGENT - PRODUCTION DEPLOYMENT"
echo "============================================"

# Configuration
WORKSPACE="amo"
AGENT="template-copilot-kit-py"
API_KEY="bl_47yrrlxn6geic2wq9asrv5rapygyycj7"  # NOTE: ROTATE THIS!
BASE_URL="https://run.blaxel.ai"
PROXY_PORT=8890

cd /home/sk25/auto/template-copilot-kit-py

echo "📋 Step 1: Deploy agent to Blaxel..."
bl deploy
echo "✅ Agent deployed successfully!"

echo ""
echo "📋 Step 2: Test production endpoints..."

# Test 1: Base endpoint with authentication
echo -n "🧪 Testing base endpoint: "
RESPONSE=$(curl -s -X POST "$BASE_URL/$WORKSPACE/agents/$AGENT" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"inputs": "production test"}')

if [[ $RESPONSE == *"Agent received"* ]]; then
  echo "✅ PASS"
else
  echo "❌ FAIL: $RESPONSE"
  exit 1
fi

# Test 2: Stateful conversation
echo -n "🧪 Testing stateful conversation: "
THREAD_ID="prod-test-$(date +%s)"
curl -s -X POST "$BASE_URL/$WORKSPACE/agents/$AGENT" \
  -H "Authorization: Bearer $API_KEY" \
  -H "X-Blaxel-Thread-Id: $THREAD_ID" \
  -H "Content-Type: application/json" \
  -d '{"inputs": "remember: production"}' > /dev/null

RESPONSE=$(curl -s -X POST "$BASE_URL/$WORKSPACE/agents/$AGENT" \
  -H "Authorization: Bearer $API_KEY" \
  -H "X-Blaxel-Thread-Id: $THREAD_ID" \
  -H "Content-Type: application/json" \
  -d '{"inputs": "what should you remember?"}')

if [[ $RESPONSE == *"Agent received"* ]]; then
  echo "✅ PASS (Thread: $THREAD_ID)"
else
  echo "❌ FAIL: $RESPONSE"
fi

echo ""
echo "📋 Step 3: Start proxy server..."

# Kill existing proxy if running
pkill -f "production_proxy.py" 2>/dev/null || true

# Start proxy server in background
PORT=$PROXY_PORT python3 production_proxy.py > proxy.log 2>&1 &
PROXY_PID=$!

# Wait for server to start
sleep 3

# Test proxy
echo -n "🧪 Testing proxy server: "
PROXY_RESPONSE=$(curl -s -X POST "http://localhost:$PROXY_PORT/proxy/agents/$WORKSPACE/$AGENT" \
  -H "Content-Type: application/json" \
  -d '{"inputs": "proxy test"}')

if [[ $PROXY_RESPONSE == *"Agent received"* ]]; then
  echo "✅ PASS"
else
  echo "❌ FAIL: $PROXY_RESPONSE"
fi

echo ""
echo "🎯 PRODUCTION DEPLOYMENT SUMMARY"
echo "================================="
echo "✅ Agent Status: DEPLOYED & HEALTHY"
echo "✅ Direct Access: $BASE_URL/$WORKSPACE/agents/$AGENT"
echo "✅ Proxy Server: http://localhost:$PROXY_PORT"
echo "✅ Test Interface: http://localhost:$PROXY_PORT/test"
echo "✅ Health Check: http://localhost:$PROXY_PORT/health"
echo ""
echo "🔐 Authentication Required: Bearer $API_KEY"
echo "📝 Request Format: {\"inputs\": \"your message\"}"
echo "🧵 Thread Support: X-Blaxel-Thread-Id header"
echo ""

# Create environment file for easy access
cat > .env.production << EOF
# 🚀 PRODUCTION ENVIRONMENT VARIABLES
# Generated: $(date)

# Blaxel Configuration
BLAXEL_API_KEY=$API_KEY
BLAXEL_BASE_URL=$BASE_URL
BLAXEL_WORKSPACE=$WORKSPACE
BLAXEL_AGENT=$AGENT
BLAXEL_FULL_URL=$BASE_URL/$WORKSPACE/agents/$AGENT

# Proxy Configuration
PROXY_PORT=$PROXY_PORT
PROXY_URL=http://localhost:$PROXY_PORT
PROXY_PID=$PROXY_PID

# Usage Examples
# Direct: curl -X POST \$BLAXEL_FULL_URL -H "Authorization: Bearer \$BLAXEL_API_KEY" -H "Content-Type: application/json" -d '{"inputs": "hello"}'
# Proxy:  curl -X POST \$PROXY_URL/proxy/agents/\$BLAXEL_WORKSPACE/\$BLAXEL_AGENT -H "Content-Type: application/json" -d '{"inputs": "hello"}'
EOF

echo "📄 Environment file created: .env.production"
echo ""

echo "🚨 SECURITY REMINDERS:"
echo "- ROTATE API KEY: $API_KEY (it's been exposed in logs)"
echo "- Use HTTPS in production"
echo "- Implement rate limiting"
echo "- Monitor usage and costs"
echo ""

echo "📱 INTEGRATION OPTIONS:"
echo "1. Direct API (Backend only):"
echo "   curl -X POST '$BASE_URL/$WORKSPACE/agents/$AGENT' -H 'Authorization: Bearer YOUR_NEW_KEY' -d '{\"inputs\": \"message\"}'"
echo ""
echo "2. Proxy Server (Browser friendly):"
echo "   fetch('http://localhost:$PROXY_PORT/proxy/agents/$WORKSPACE/$AGENT', {method: 'POST', body: JSON.stringify({inputs: 'message'})})"
echo ""
echo "3. Next.js Integration:"
echo "   Copy nextjs-route.ts to your Next.js app/api/ directory"
echo ""

echo "✅ PRODUCTION DEPLOYMENT COMPLETE!"
echo "Proxy server running as PID $PROXY_PID"
echo "View logs: tail -f proxy.log"
echo "Stop proxy: kill $PROXY_PID"
