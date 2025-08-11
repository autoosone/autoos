import requests
import json

# SERVICE ACCOUNT KEY - This is the correct one!
SERVICE_ACCOUNT_KEY = "bl_ogpdihxp6c503zffr81jyftlwc35ibdi"

print("=" * 60)
print("Testing with SERVICE ACCOUNT API Key")
print("=" * 60)

# Test 1: Direct agent endpoint
print("\n1. Testing Direct Agent Endpoint...")
print("-" * 40)

response = requests.post(
    "https://run.blaxel.ai/amo/agents/template-copilot-kit-py",
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {SERVICE_ACCOUNT_KEY}",
        "X-Blaxel-Thread-Id": "test-thread-001"
    },
    json={
        "inputs": "Hello, find hotels in Paris"
    }
)

print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    print("✅ SUCCESS! Agent is responding!")
    print(f"Response: {response.text[:500]}")
else:
    print(f"❌ Error: {response.text[:200]}")

# Test 2: CopilotKit endpoint
print("\n" + "=" * 60)
print("2. Testing CopilotKit Endpoint...")
print("-" * 40)

response2 = requests.post(
    "https://run.blaxel.ai/amo/agents/template-copilot-kit-py/copilotkit",
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {SERVICE_ACCOUNT_KEY}",
        "X-Blaxel-Thread-Id": "test-thread-002"
    },
    json={
        "message": "Hello, I need help finding hotels",
        "actions": []
    }
)

print(f"Status Code: {response2.status_code}")
if response2.status_code == 200:
    print("✅ SUCCESS! CopilotKit endpoint working!")
    try:
        data = response2.json()
        print(f"Response: {json.dumps(data, indent=2)[:500]}")
    except:
        print(f"Response: {response2.text[:500]}")
else:
    print(f"❌ Error: {response2.text[:200]}")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
if response.status_code == 200 or response2.status_code == 200:
    print("🎉 SERVICE ACCOUNT KEY IS WORKING!")
    print(f"Key: {SERVICE_ACCOUNT_KEY}")
    print("You can now use this key in your frontend!")
else:
    print("⚠️ Both endpoints failed. Checking deployment status...")
