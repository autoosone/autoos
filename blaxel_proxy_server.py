#!/usr/bin/env python3
"""
Blaxel Agent Proxy Server - Solves CORS issues
This server acts as a proxy to forward requests to Blaxel API
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
API_KEY = "bl_47yrrlxn6geic2wq9asrv5rapygyycj7"
BASE_URL = "https://run.blaxel.ai/amo"

@app.route('/')
def index():
    """Serve the HTML interface"""
    return send_file('blaxel-test-interface.html')

@app.route('/api/agent', methods=['GET', 'POST'])
def agent_proxy():
    """Proxy requests to the Blaxel agent endpoint"""
    endpoint = f"{BASE_URL}/agents/template-copilot-kit-py"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Add thread ID if provided
    thread_id = request.headers.get('X-Thread-Id')
    if thread_id:
        headers["X-Blaxel-Thread-Id"] = thread_id
    
    try:
        if request.method == 'GET':
            response = requests.get(endpoint, headers=headers)
        else:
            response = requests.post(
                endpoint, 
                headers=headers, 
                json=request.get_json()
            )
        
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/copilotkit', methods=['POST'])
def copilotkit_proxy():
    """Proxy requests to the CopilotKit endpoint"""
    endpoint = f"{BASE_URL}/copilotkit"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Add thread ID if provided
    thread_id = request.headers.get('X-Thread-Id')
    if thread_id:
        headers["X-Blaxel-Thread-Id"] = thread_id
    
    try:
        response = requests.post(
            endpoint, 
            headers=headers, 
            json=request.get_json()
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/test')
def test():
    """Test endpoint to verify server is running"""
    return jsonify({
        "status": "running",
        "message": "Blaxel proxy server is operational",
        "endpoints": [
            "/api/agent (GET/POST)",
            "/api/copilotkit (POST)"
        ]
    })

if __name__ == '__main__':
    print("🚀 Starting Blaxel Proxy Server...")
    print("📡 API Key:", API_KEY[:20] + "...")
    print("🌐 Access the interface at: http://localhost:5000")
    print("✅ Proxy endpoints:")
    print("   - http://localhost:5000/api/agent")
    print("   - http://localhost:5000/api/copilotkit")
    print("\n⚡ Server running with CORS enabled - no more CORS errors!")
    app.run(debug=True, port=5000)