#!/usr/bin/env python3
"""
Diagnose and fix Blaxel authentication issue
"""

import requests
import json

print("🔍 BLAXEL AUTHENTICATION DIAGNOSTIC")
print("="*60)
print()

# Test different endpoint formats
endpoints = [
    "https://run.blaxel.ai/amo/agents/template-copilot-kit-py",
    "https://run.blaxel.ai/amo/template-copilot-kit-py",
    "https://api.blaxel.ai/amo/agents/template-copilot-kit-py",
]

# Test all available API keys
api_keys = {
    "Workspace Key 1": "bl_0u6521qylyby1e948qghtgp5msl3rl8q",
    "Workspace Key 2": "bl_ypbq1x2cdwy272rekcj6017jpvn8o161",
    "Service Key 1": "bl_47yrrlxn6geic2wq9asrv5rapygyycj7",
    "Service Key 2": "bl_ogpdihxp6c503zffr81jyftlwc35ibdi",
}

working_combinations = []

for endpoint in endpoints:
    print(f"Testing endpoint: {endpoint}")
    print("-" * 40)
    
    for key_name, api_key in api_keys.items():
        # Test without Bearer prefix
        print(f"  {key_name} (no Bearer)... ", end="")
        try:
            resp = requests.post(
                endpoint,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": api_key  # Without Bearer
                },
                json={"inputs": "test"},
                timeout=3
            )
            if resp.status_code == 200:
                print("✅ WORKS!")
                working_combinations.append((endpoint, key_name, api_key, "no Bearer"))
            else:
                print(f"❌ {resp.status_code}")
        except Exception as e:
            print(f"❌ Error")
        
        # Test with Bearer prefix
        print(f"  {key_name} (with Bearer)... ", end="")
        try:
            resp = requests.post(
                endpoint,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}"
                },
                json={"inputs": "test"},
                timeout=3
            )
            if resp.status_code == 200:
                print("✅ WORKS!")
                working_combinations.append((endpoint, key_name, api_key, "Bearer"))
            else:
                print(f"❌ {resp.status_code}")
        except Exception as e:
            print(f"❌ Error")
    
    print()

print("="*60)
print("📊 RESULTS")
print("="*60)

if working_combinations:
    print("✅ WORKING COMBINATIONS FOUND:")
    print()
    for endpoint, key_name, api_key, auth_type in working_combinations:
        print(f"Endpoint: {endpoint}")
        print(f"Key: {key_name} ({api_key})")
        print(f"Auth Format: {'Bearer ' + api_key if auth_type == 'Bearer' else api_key}")
        print()
        print("Python code:")
        print("```python")
        auth_header = f"Bearer {api_key}" if auth_type == "Bearer" else api_key
        print(f'''response = requests.post(
    "{endpoint}",
    headers={{
        "Content-Type": "application/json",
        "Authorization": "{auth_header}"
    }},
    json={{"inputs": "your message"}}
)''')
        print("```")
        print("-" * 40)
else:
    print("❌ No working combinations found")
    print()
    print("Possible issues:")
    print("1. Agent may not be deployed yet")
    print("2. API keys may need regeneration")
    print("3. Workspace 'amo' might be incorrect")
    print()
    print("Try:")
    print("1. Check https://blaxel.ai dashboard")
    print("2. Verify agent deployment status")
    print("3. Regenerate API keys if needed")