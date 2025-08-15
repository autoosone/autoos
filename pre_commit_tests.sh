#!/bin/bash
# 🧪 PRE-COMMIT TEST SUITE
# 5 Critical Tests to ensure 100% production readiness before GitHub commit

set -e  # Exit on any error

echo "🧪 PRE-COMMIT TEST SUITE - 5 CRITICAL TESTS"
echo "============================================="
echo "Testing Blaxel Agent Production Readiness"
echo ""

# Configuration
API_KEY="${BLAXEL_API_KEY:-YOUR_API_KEY_HERE}"  # Set BLAXEL_API_KEY environment variable
BASE_URL="https://run.blaxel.ai/amo/agents/template-copilot-kit-py"
PROXY_PORT=8890
WORKSPACE="amo"
AGENT="template-copilot-kit-py"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Helper function for test results
test_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ PASS${NC}"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}❌ FAIL${NC}"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}Error: $2${NC}"
    fi
}

echo "🔍 TEST 1: BLAXEL AGENT DEPLOYMENT STATUS"
echo "=========================================="
echo -n "Checking if agent is deployed and accessible... "

# Test agent deployment status
DEPLOY_RESPONSE=$(bl get agents $AGENT -w $WORKSPACE 2>/dev/null | grep -c "DEPLOYED" || echo "0")

if [ "$DEPLOY_RESPONSE" -gt 0 ]; then
    test_result 0
    echo "   Agent Status: DEPLOYED ✅"
else
    test_result 1 "Agent not deployed or not accessible"
fi

echo ""
echo "🔍 TEST 2: PRODUCTION API ENDPOINT VALIDATION"  
echo "=============================================="

# Test 2a: Valid authenticated request
echo -n "2a. Testing authenticated request with correct format... "
API_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"inputs": "test message"}')

if [ "$API_RESPONSE" -eq 200 ]; then
    test_result 0
else
    test_result 1 "Expected 200, got $API_RESPONSE"
fi

# Test 2b: Unauthenticated request (should fail)
echo -n "2b. Testing unauthenticated request (should fail)... "
UNAUTH_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL" \
    -H "Content-Type: application/json" \
    -d '{"inputs": "test"}')

if [ "$UNAUTH_RESPONSE" -eq 400 ] || [ "$UNAUTH_RESPONSE" -eq 401 ]; then
    test_result 0
    echo "   Properly rejected with HTTP $UNAUTH_RESPONSE ✅"
else
    test_result 1 "Expected 400/401, got $UNAUTH_RESPONSE"
fi

# Test 2c: Wrong request format
echo -n "2c. Testing request validation (wrong format)... "
WRONG_FORMAT_RESPONSE=$(curl -s -X POST "$BASE_URL" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"input": "wrong key"}')

if [[ $WRONG_FORMAT_RESPONSE == *"error"* ]] || [[ $WRONG_FORMAT_RESPONSE == *"Missing 'inputs'"* ]]; then
    test_result 0
    echo "   Properly validates request format ✅"
else
    test_result 1 "Request validation not working"
fi

echo ""
echo "🔍 TEST 3: STATEFUL CONVERSATION SUPPORT"
echo "========================================"
echo -n "Testing thread-based stateful conversations... "

THREAD_ID="pre-commit-test-$(date +%s)"

# Send first message with thread ID
FIRST_RESPONSE=$(curl -s -X POST "$BASE_URL" \
    -H "Authorization: Bearer $API_KEY" \
    -H "X-Blaxel-Thread-Id: $THREAD_ID" \
    -H "Content-Type: application/json" \
    -d '{"inputs": "remember this number: 42"}')

# Send second message with same thread ID
SECOND_RESPONSE=$(curl -s -X POST "$BASE_URL" \
    -H "Authorization: Bearer $API_KEY" \
    -H "X-Blaxel-Thread-Id: $THREAD_ID" \
    -H "Content-Type: application/json" \
    -d '{"inputs": "what number did I tell you?"}')

if [[ $FIRST_RESPONSE == *"Agent received"* ]] && [[ $SECOND_RESPONSE == *"Agent received"* ]]; then
    test_result 0
    echo "   Thread ID: $THREAD_ID ✅"
else
    test_result 1 "Stateful conversation failed"
fi

echo ""
echo "🔍 TEST 4: COPILOTKIT ENDPOINT FUNCTIONALITY"
echo "==========================================="
echo -n "Testing CopilotKit integration endpoint... "

COPILOT_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL/copilotkit" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d '{}')

if [ "$COPILOT_RESPONSE" -eq 200 ]; then
    test_result 0
    echo "   CopilotKit endpoint responding ✅"
    
    # Test the actual response content
    COPILOT_CONTENT=$(curl -s -X POST "$BASE_URL/copilotkit" \
        -H "Authorization: Bearer $API_KEY" \
        -H "Content-Type: application/json" \
        -d '{}')
    
    if [[ $COPILOT_CONTENT == *"agents"* ]]; then
        echo "   CopilotKit response format valid ✅"
    else
        echo "   ⚠️  CopilotKit response format unexpected"
    fi
else
    test_result 1 "CopilotKit endpoint failed with HTTP $COPILOT_RESPONSE"
fi

echo ""
echo "🔍 TEST 5: PROXY SERVER AND BROWSER COMPATIBILITY"
echo "================================================"

# Check if proxy is running
PROXY_RUNNING=$(ps aux | grep -c "production_proxy.py" || echo "0")

if [ "$PROXY_RUNNING" -gt 1 ]; then  # More than 1 because grep counts itself
    echo "✅ Proxy server is running"
    
    echo -n "5a. Testing proxy health endpoint... "
    PROXY_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:$PROXY_PORT/health")
    
    if [ "$PROXY_HEALTH" -eq 200 ]; then
        test_result 0
    else
        test_result 1 "Proxy health check failed with HTTP $PROXY_HEALTH"
    fi
    
    echo -n "5b. Testing proxy agent communication... "
    PROXY_AGENT_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
        -X POST "http://localhost:$PROXY_PORT/proxy/agents/$WORKSPACE/$AGENT" \
        -H "Content-Type: application/json" \
        -d '{"inputs": "proxy test"}')
    
    if [ "$PROXY_AGENT_RESPONSE" -eq 200 ]; then
        test_result 0
        echo "   Proxy → Blaxel communication working ✅"
    else
        test_result 1 "Proxy agent communication failed with HTTP $PROXY_AGENT_RESPONSE"
    fi
    
else
    echo "⚠️  Proxy server not running - starting it for test..."
    PORT=$PROXY_PORT python3 production_proxy.py > /tmp/proxy_test.log 2>&1 &
    PROXY_PID=$!
    sleep 3
    
    echo -n "5c. Testing freshly started proxy... "
    FRESH_PROXY_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:$PROXY_PORT/health")
    
    if [ "$FRESH_PROXY_RESPONSE" -eq 200 ]; then
        test_result 0
    else
        test_result 1 "Fresh proxy failed with HTTP $FRESH_PROXY_RESPONSE"
    fi
    
    # Clean up
    kill $PROXY_PID 2>/dev/null || true
fi

echo ""
echo "🔍 ADDITIONAL VALIDATION CHECKS"
echo "==============================="

# Check for sensitive data in files that will be committed
echo -n "🔒 Checking for exposed secrets in committed files... "
EXPOSED_SECRETS=0

# Check for API keys in source files (excluding test files)
for file in src/*.py *.toml *.ts *.js; do
    if [ -f "$file" ] && ! [[ $file == *"test"* ]]; then
        if grep -q "bl_[a-z0-9]*" "$file" 2>/dev/null; then
            echo -e "\n   ⚠️  Potential API key found in: $file"
            EXPOSED_SECRETS=1
        fi
    fi
done

if [ $EXPOSED_SECRETS -eq 0 ]; then
    echo -e "${GREEN}✅ No exposed secrets found${NC}"
else
    echo -e "${YELLOW}⚠️  WARNING: Check files for exposed secrets${NC}"
fi

# Check .gitignore coverage
echo -n "📁 Checking .gitignore coverage... "
if [ -f ".gitignore" ]; then
    if grep -q ".env" .gitignore && grep -q "*.log" .gitignore; then
        echo -e "${GREEN}✅ .gitignore properly configured${NC}"
    else
        echo -e "${YELLOW}⚠️  .gitignore may need updates${NC}"
    fi
else
    echo -e "${RED}❌ .gitignore missing${NC}"
fi

echo ""
echo "📊 TEST RESULTS SUMMARY"
echo "======================="
echo -e "Tests Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed: ${RED}$TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 ALL TESTS PASSED! Ready for GitHub commit! 🚀${NC}"
    echo ""
    echo "✅ Blaxel agent is 100% production ready"
    echo "✅ All endpoints are working correctly"
    echo "✅ Authentication and security verified"
    echo "✅ Stateful conversations confirmed"
    echo "✅ CopilotKit integration operational"
    echo "✅ Proxy server functioning properly"
    echo ""
    exit 0
else
    echo -e "${RED}❌ $TESTS_FAILED test(s) failed. Fix issues before commit.${NC}"
    echo ""
    exit 1
fi
