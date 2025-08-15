#!/usr/bin/env python3
"""
🚀 PRODUCTION ENDPOINT TESTER
Tests all Blaxel endpoints with proper authentication
"""

import requests
import json
import os
import time
from datetime import datetime

# Get API key from environment
API_KEY = os.getenv("BLAXEL_API_KEY", "YOUR_API_KEY_HERE")  # Set this in your environment
BASE_URL = "https://run.blaxel.ai/amo/agents/template-copilot-kit-py"

def test_endpoint(url, method="POST", headers=None, data=None, expected_status=200):
    """Test an endpoint and return results"""
    print(f"\n🔍 Testing: {method} {url}")
    print(f"Headers: {headers}")
    print(f"Data: {data}")
    
    try:
        if method == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=30)
        else:
            response = requests.get(url, headers=headers, timeout=30)
            
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:500]}...")
        
        if response.status_code == expected_status:
            print("✅ PASS")
            return True
        else:
            print(f"❌ FAIL - Expected {expected_status}, got {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def main():
    print("🚀 PRODUCTION ENDPOINT TESTING")
    print("=" * 50)
    
    # Headers for authenticated requests
    auth_headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Test 1: Base endpoint with correct format
    print("\n1️⃣ Testing base endpoint with authentication")
    test_data = {"inputs": "healthcheck"}
    test_endpoint(BASE_URL, "POST", auth_headers, test_data)
    
    # Test 2: Test without authentication (should fail)
    print("\n2️⃣ Testing without authentication (should fail)")
    no_auth_headers = {"Content-Type": "application/json"}
    test_endpoint(BASE_URL, "POST", no_auth_headers, test_data, expected_status=401)
    
    # Test 3: Test with wrong body format
    print("\n3️⃣ Testing with wrong body format")
    wrong_data = {"input": "test"}  # Wrong key
    test_endpoint(BASE_URL, "POST", auth_headers, wrong_data)
    
    # Test 4: Test CopilotKit endpoint
    print("\n4️⃣ Testing CopilotKit endpoint")
    copilot_url = f"{BASE_URL}/copilotkit"
    test_endpoint(copilot_url, "POST", auth_headers, {})
    
    # Test 5: Test with thread ID (stateful)
    print("\n5️⃣ Testing stateful conversation with thread ID")
    thread_headers = auth_headers.copy()
    thread_headers["X-Blaxel-Thread-Id"] = f"test-{int(time.time())}"
    test_endpoint(BASE_URL, "POST", thread_headers, {"inputs": "remember this: Denver"})
    
    print("\n" + "=" * 50)
    print("🏁 Testing complete!")

if __name__ == "__main__":
    main()
