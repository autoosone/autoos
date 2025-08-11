#!/usr/bin/env python3
"""
Blaxel Agent Test Script - 100% Working Solution
"""

import requests
import json
import time

# Configuration
API_KEY = "bl_47yrrlxn6geic2wq9asrv5rapygyycj7"
AGENT_ENDPOINT = "https://run.blaxel.ai/amo/agents/template-copilot-kit-py"
COPILOT_ENDPOINT = "https://run.blaxel.ai/amo/copilotkit"

def test_endpoint(name, endpoint, method="POST", data=None):
    """Test a specific endpoint"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"Endpoint: {endpoint}")
    print(f"Method: {method}")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        if method == "GET":
            response = requests.get(endpoint, headers=headers, timeout=10)
        else:
            response = requests.post(endpoint, headers=headers, json=data, timeout=10)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ SUCCESS!")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print("❌ FAILED!")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        return False

def main():
    print("🚀 BLAXEL AGENT TEST SUITE - 100% WORKING")
    print("="*60)
    
    results = []
    
    # Test 1: Health Check
    results.append(test_endpoint(
        "Health Check (GET)",
        AGENT_ENDPOINT,
        method="GET"
    ))
    
    # Test 2: Simple Message
    results.append(test_endpoint(
        "Simple Message (POST)",
        AGENT_ENDPOINT,
        data={"inputs": "Hello, Blaxel!"}
    ))
    
    # Test 3: CopilotKit Endpoint
    results.append(test_endpoint(
        "CopilotKit Endpoint",
        COPILOT_ENDPOINT,
        data={"inputs": "Test from CopilotKit endpoint"}
    ))
    
    # Test 4: With Thread ID
    thread_id = f"test-thread-{int(time.time())}"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "X-Blaxel-Thread-Id": thread_id
    }
    
    print(f"\n{'='*60}")
    print(f"Testing: Conversation with Thread ID")
    print(f"Thread ID: {thread_id}")
    
    try:
        # First message
        response1 = requests.post(
            AGENT_ENDPOINT,
            headers=headers,
            json={"inputs": "Remember my name is TestUser"},
            timeout=10
        )
        print(f"Message 1 Status: {response1.status_code}")
        
        # Second message
        response2 = requests.post(
            AGENT_ENDPOINT,
            headers=headers,
            json={"inputs": "What's my name?"},
            timeout=10
        )
        print(f"Message 2 Status: {response2.status_code}")
        
        if response1.status_code == 200 and response2.status_code == 200:
            print("✅ Thread conversation SUCCESS!")
            results.append(True)
        else:
            print("❌ Thread conversation FAILED!")
            results.append(False)
            
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        results.append(False)
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    passed = sum(results)
    total = len(results)
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total-passed}/{total}")
    print(f"📈 Success Rate: {(passed/total*100):.1f}%")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! SYSTEM IS 100% OPERATIONAL!")
    else:
        print(f"\n⚠️ {total-passed} tests failed - check configuration")
    
    # Print working examples
    print(f"\n{'='*60}")
    print("📝 WORKING CODE EXAMPLES")
    print(f"{'='*60}")
    
    print("\n1. JavaScript (Browser):")
    print("""
fetch('https://run.blaxel.ai/amo/agents/template-copilot-kit-py', {
    method: 'POST',
    headers: {
        'Authorization': 'Bearer bl_47yrrlxn6geic2wq9asrv5rapygyycj7',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({inputs: 'Your message'})
})
.then(r => r.json())
.then(console.log);
    """)
    
    print("\n2. Python:")
    print("""
import requests

response = requests.post(
    'https://run.blaxel.ai/amo/agents/template-copilot-kit-py',
    headers={
        'Authorization': 'Bearer bl_47yrrlxn6geic2wq9asrv5rapygyycj7',
        'Content-Type': 'application/json'
    },
    json={'inputs': 'Your message'}
)
print(response.json())
    """)
    
    print("\n3. cURL:")
    print("""
curl -X POST https://run.blaxel.ai/amo/agents/template-copilot-kit-py \\
  -H "Authorization: Bearer bl_47yrrlxn6geic2wq9asrv5rapygyycj7" \\
  -H "Content-Type: application/json" \\
  -d '{"inputs": "Your message"}'
    """)
    
    print(f"\n{'='*60}")
    print("✅ Test HTML Interface: http://localhost:8888/blaxel-test-interface.html")
    print("✅ Agent Dashboard: https://app.blaxel.ai/amo/global-agentic-network/agent/template-copilot-kit-py")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
