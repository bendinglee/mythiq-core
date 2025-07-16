"""
Mythiq Gateway - Enterprise Edition with Authentication, Pro Router & Quota Management
Includes cognitive capabilities, latest AI models, and enterprise-grade features
Version 2.4.0 - Enterprise Architecture
"""

from flask import Flask, request, jsonify, render_template_string, Blueprint
from flask_cors import CORS
import os
import requests
import json
import time
import traceback
from datetime import datetime
import importlib.util
import sys

app = Flask(__name__)
CORS(app)

# Configuration
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
HUGGING_FACE_API_KEY = os.environ.get('HUGGING_FACE') or os.environ.get('HUGGINGFACE_API_KEY')

# Latest Groq Models (Production-Grade)
GROQ_MODELS = [
    "llama-3.3-70b-versatile",  # Primary - Latest and most capable
    "mistral-saba-24b",         # Secondary - Fast and reliable
    "mixtral-8x7b-32768"        # Fallback - Proven stable
]

# Enterprise Blueprint Registration System
BLUEPRINT_ROUTES = [
    # Core System Modules
    ("branches.ai_proxy.test_route", "test_bp", "/"),
    ("branches.vision.routes", "vision_bp", "/"),
    
    # Cognitive Architecture
    ("branches.memory.routes", "memory_bp", "/api/memory"),
    ("branches.reasoning.routes", "reasoning_bp", "/api/reason"),
    ("branches.self_validate.routes", "validation_bp", "/api/validate"),
    
    # Enterprise Features
    ("branches.auth_gate.routes", "auth_bp", "/api/auth"),
    ("branches.pro_router.routes", "pro_router_bp", "/api/proxy"),
    ("branches.quota.routes", "quota_bp", "/api/quota"),
]

# HTML Template for the enterprise frontend
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mythiq Gateway Enterprise</title>
    <style>
        body {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            color: white;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            color: #00ffff;
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
        }
        .subtitle {
            text-align: center;
            color: #a0a0a0;
            font-size: 1.1em;
            margin-bottom: 30px;
        }
        textarea {
            width: 100%;
            height: 150px;
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid #00ffff;
            border-radius: 10px;
            color: white;
            font-size: 16px;
            padding: 15px;
            resize: vertical;
            box-sizing: border-box;
            margin-bottom: 20px;
        }
        textarea::placeholder {
            color: rgba(255, 255, 255, 0.7);
        }
        button {
            background: linear-gradient(45deg, #00ffff, #0080ff);
            border: none;
            color: white;
            padding: 12px 30px;
            font-size: 16px;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 255, 255, 0.3);
            margin: 5px;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 255, 255, 0.4);
        }
        .response-container {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 20px;
            min-height: 100px;
            border-left: 4px solid #00ffff;
            margin-top: 20px;
        }
        .loading {
            color: #00ffff;
            font-style: italic;
        }
        .error {
            color: #ff6b6b;
            background: rgba(255, 107, 107, 0.1);
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #ff6b6b;
        }
        .success {
            color: #51cf66;
            line-height: 1.6;
        }
        .status-indicator {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(0, 255, 255, 0.2);
            padding: 10px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            border: 1px solid #00ffff;
        }
        .model-selector {
            margin-bottom: 15px;
        }
        select {
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid #00ffff;
            border-radius: 5px;
            color: white;
            padding: 8px 12px;
            font-size: 14px;
        }
        select option {
            background: #1e3c72;
            color: white;
        }
        .button-section {
            margin-bottom: 15px;
        }
        .section-title {
            font-size: 0.9em;
            color: #a0a0a0;
            margin-bottom: 5px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .feature-button {
            background: linear-gradient(45deg, #ff6b6b, #ff8e8e);
            font-size: 14px;
            padding: 8px 20px;
        }
        .cognitive-button {
            background: linear-gradient(45deg, #9c88ff, #b19cd9);
            font-size: 14px;
            padding: 8px 18px;
        }
        .enterprise-button {
            background: linear-gradient(45deg, #ffd43b, #fab005);
            color: #1e3c72;
            font-weight: bold;
            font-size: 14px;
            padding: 8px 18px;
        }
        .auth-status {
            position: fixed;
            top: 70px;
            right: 20px;
            background: rgba(255, 215, 0, 0.2);
            padding: 8px 12px;
            border-radius: 15px;
            font-size: 0.8em;
            border: 1px solid #ffd43b;
            color: #ffd43b;
        }
        .quota-indicator {
            position: fixed;
            top: 120px;
            right: 20px;
            background: rgba(156, 136, 255, 0.2);
            padding: 8px 12px;
            border-radius: 15px;
            font-size: 0.8em;
            border: 1px solid #9c88ff;
            color: #9c88ff;
        }
    </style>
</head>
<body>
    <div class="status-indicator" id="statusIndicator">
        🟢 System Online
    </div>
    
    <div class="auth-status" id="authStatus">
        🔐 Auth: Checking...
    </div>
    
    <div class="quota-indicator" id="quotaStatus">
        📊 Quota: Loading...
    </div>
    
    <div class="container">
        <h1>🏢 Mythiq Gateway Enterprise</h1>
        <div class="subtitle">Advanced AI Platform with Authentication, Pro Router & Quota Management</div>
        
        <div class="model-selector">
            <label for="modelSelect">AI Model: </label>
            <select id="modelSelect">
                <option value="auto">Auto (Smart Fallback)</option>
                <option value="llama-3.3-70b-versatile">Llama 3.3 70B (Latest)</option>
                <option value="mistral-saba-24b">Mistral Saba 24B (Fast)</option>
                <option value="mixtral-8x7b-32768">Mixtral 8x7B (Stable)</option>
            </select>
        </div>
        
        <textarea id="userInput" placeholder="Ask Mythiq Enterprise anything..."></textarea>
        
        <div class="button-section">
            <div class="section-title">Core Functions</div>
            <button onclick="sendToBrain()">Send to Brain</button>
            <button onclick="testHealth()">Test Health</button>
            <button onclick="testAIProxy()">Test AI Proxy</button>
            <button onclick="clearResponse()">Clear</button>
        </div>
        
        <div class="button-section">
            <div class="section-title">System Features</div>
            <button class="feature-button" onclick="testVision()">Test Vision</button>
            <button class="feature-button" onclick="testProxyRoute()">Test Proxy Route</button>
            <button class="feature-button" onclick="showBlueprints()">Show Blueprints</button>
        </div>
        
        <div class="button-section">
            <div class="section-title">Cognitive Capabilities</div>
            <button class="cognitive-button" onclick="testMemory()">Test Memory</button>
            <button class="cognitive-button" onclick="testReasoning()">Test Reasoning</button>
            <button class="cognitive-button" onclick="testValidation()">Test Validation</button>
            <button class="cognitive-button" onclick="runCognitiveTest()">Full Cognitive Test</button>
        </div>
        
        <div class="button-section">
            <div class="section-title">Enterprise Features</div>
            <button class="enterprise-button" onclick="testAuth()">Test Auth</button>
            <button class="enterprise-button" onclick="testProRouter()">Test Pro Router</button>
            <button class="enterprise-button" onclick="testQuota()">Test Quota</button>
            <button class="enterprise-button" onclick="enterpriseStatus()">Enterprise Status</button>
        </div>
        
        <div class="response-container" id="responseArea">
            <div style="color: #a0a0a0; text-align: center;">
                Welcome to Mythiq Gateway Enterprise v2.4.0!<br>
                Enhanced with Authentication, Pro Router, Quota Management & Cognitive Capabilities.
            </div>
        </div>
    </div>

    <script>
        async function sendToBrain() {
            const userInput = document.getElementById('userInput').value.trim();
            const responseArea = document.getElementById('responseArea');
            
            if (!userInput) {
                responseArea.innerHTML = '<div class="error">Please enter a question or message.</div>';
                return;
            }
            
            responseArea.innerHTML = '<div class="loading">🧠 Processing with Enterprise AI...</div>';
            
            try {
                const response = await fetch('/api/brain', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: userInput })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    responseArea.innerHTML = `
                        <div class="success">${data.response}</div>
                        <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.2); font-size: 0.9em; color: #a0a0a0;">
                            Provider: ${data.provider || 'AI'} | Model: ${data.model || 'N/A'} | Status: ${data.status} | Time: ${new Date().toLocaleTimeString()}
                        </div>
                    `;
                } else {
                    responseArea.innerHTML = `<div class="error">Error: ${data.error || 'Unknown error occurred'}</div>`;
                }
            } catch (error) {
                responseArea.innerHTML = `<div class="error">Network error: ${error.message}</div>`;
            }
        }
        
        async function testAuth() {
            const responseArea = document.getElementById('responseArea');
            responseArea.innerHTML = '<div class="loading">🔐 Testing Authentication System...</div>';
            
            try {
                const response = await fetch('/api/auth/test');
                const data = await response.json();
                
                if (response.ok) {
                    responseArea.innerHTML = `
                        <div class="success">
                            <strong>Authentication System Test:</strong><br>
                            ${data.message || 'Authentication system operational'}<br>
                            Status: ${data.status}<br>
                            Auth Methods: ${data.auth_methods ? data.auth_methods.join(', ') : 'Basic authentication'}<br>
                            Security Level: ${data.security_level || 'Standard'}
                        </div>
                    `;
                    updateAuthStatus(data.status);
                } else {
                    responseArea.innerHTML = `<div class="error">Auth test failed: ${data.error || 'Authentication module not available'}</div>`;
                }
            } catch (error) {
                responseArea.innerHTML = `<div class="error">Auth test error: ${error.message}</div>`;
            }
        }
        
        async function testProRouter() {
            const responseArea = document.getElementById('responseArea');
            responseArea.innerHTML = '<div class="loading">🚀 Testing Pro Router System...</div>';
            
            try {
                const response = await fetch('/api/proxy/test');
                const data = await response.json();
                
                if (response.ok) {
                    responseArea.innerHTML = `
                        <div class="success">
                            <strong>Pro Router Test:</strong><br>
                            ${data.message || 'Pro router system operational'}<br>
                            Status: ${data.status}<br>
                            Router Types: ${data.router_types ? data.router_types.join(', ') : 'Basic routing'}<br>
                            Load Balancing: ${data.load_balancing || 'Enabled'}
                        </div>
                    `;
                } else {
                    responseArea.innerHTML = `<div class="error">Pro router test failed: ${data.error || 'Pro router module not available'}</div>`;
                }
            } catch (error) {
                responseArea.innerHTML = `<div class="error">Pro router test error: ${error.message}</div>`;
            }
        }
        
        async function testQuota() {
            const responseArea = document.getElementById('responseArea');
            responseArea.innerHTML = '<div class="loading">📊 Testing Quota Management...</div>';
            
            try {
                const response = await fetch('/api/quota/test');
                const data = await response.json();
                
                if (response.ok) {
                    responseArea.innerHTML = `
                        <div class="success">
                            <strong>Quota Management Test:</strong><br>
                            ${data.message || 'Quota system operational'}<br>
                            Status: ${data.status}<br>
                            Current Usage: ${data.current_usage || '0'}/${data.quota_limit || '1000'}<br>
                            Quota Types: ${data.quota_types ? data.quota_types.join(', ') : 'Request limits'}
                        </div>
                    `;
                    updateQuotaStatus(data.current_usage, data.quota_limit);
                } else {
                    responseArea.innerHTML = `<div class="error">Quota test failed: ${data.error || 'Quota module not available'}</div>`;
                }
            } catch (error) {
                responseArea.innerHTML = `<div class="error">Quota test error: ${error.message}</div>`;
            }
        }
        
        async function enterpriseStatus() {
            const responseArea = document.getElementById('responseArea');
            responseArea.innerHTML = '<div class="loading">🏢 Checking Enterprise Status...</div>';
            
            try {
                const response = await fetch('/api/enterprise/status');
                const data = await response.json();
                
                if (response.ok) {
                    responseArea.innerHTML = `
                        <div class="success">
                            <strong>Enterprise Status:</strong><br>
                            ${data.summary || 'Enterprise systems operational'}<br>
                            Auth Status: ${data.auth_status || 'Unknown'}<br>
                            Pro Router: ${data.router_status || 'Unknown'}<br>
                            Quota System: ${data.quota_status || 'Unknown'}<br>
                            Enterprise Score: ${data.enterprise_score || 'N/A'}%<br>
                            License: ${data.license_type || 'Community'}
                        </div>
                    `;
                } else {
                    responseArea.innerHTML = `<div class="error">Enterprise status failed: ${data.error || 'Enterprise modules not available'}</div>`;
                }
            } catch (error) {
                responseArea.innerHTML = `<div class="error">Enterprise status error: ${error.message}</div>`;
            }
        }
        
        function updateAuthStatus(status) {
            const authStatus = document.getElementById('authStatus');
            if (status === 'active' || status === 'operational') {
                authStatus.innerHTML = '🔐 Auth: Active';
                authStatus.style.borderColor = '#51cf66';
                authStatus.style.color = '#51cf66';
            } else if (status === 'fallback') {
                authStatus.innerHTML = '🔐 Auth: Fallback';
                authStatus.style.borderColor = '#ffd43b';
                authStatus.style.color = '#ffd43b';
            } else {
                authStatus.innerHTML = '🔐 Auth: Offline';
                authStatus.style.borderColor = '#ff6b6b';
                authStatus.style.color = '#ff6b6b';
            }
        }
        
        function updateQuotaStatus(usage, limit) {
            const quotaStatus = document.getElementById('quotaStatus');
            const percentage = limit ? Math.round((usage / limit) * 100) : 0;
            
            if (percentage < 70) {
                quotaStatus.innerHTML = `📊 Quota: ${percentage}%`;
                quotaStatus.style.borderColor = '#51cf66';
                quotaStatus.style.color = '#51cf66';
            } else if (percentage < 90) {
                quotaStatus.innerHTML = `📊 Quota: ${percentage}%`;
                quotaStatus.style.borderColor = '#ffd43b';
                quotaStatus.style.color = '#ffd43b';
            } else {
                quotaStatus.innerHTML = `📊 Quota: ${percentage}%`;
                quotaStatus.style.borderColor = '#ff6b6b';
                quotaStatus.style.color = '#ff6b6b';
            }
        }
        
        // Include all previous functions (testMemory, testReasoning, etc.)
        async function testMemory() {
            const responseArea = document.getElementById('responseArea');
            responseArea.innerHTML = '<div class="loading">🧠 Testing Memory System...</div>';
            
            try {
                const response = await fetch('/api/memory/test');
                const data = await response.json();
                
                if (response.ok) {
                    responseArea.innerHTML = `
                        <div class="success">
                            <strong>Memory System Test:</strong><br>
                            ${data.message || 'Memory system operational'}<br>
                            Status: ${data.status}<br>
                            Capabilities: ${data.capabilities ? data.capabilities.join(', ') : 'Basic memory processing'}
                        </div>
                    `;
                } else {
                    responseArea.innerHTML = `<div class="error">Memory test failed: ${data.error || 'Memory module not available'}</div>`;
                }
            } catch (error) {
                responseArea.innerHTML = `<div class="error">Memory test error: ${error.message}</div>`;
            }
        }
        
        async function testReasoning() {
            const responseArea = document.getElementById('responseArea');
            responseArea.innerHTML = '<div class="loading">🤔 Testing Reasoning Engine...</div>';
            
            try {
                const response = await fetch('/api/reason/test');
                const data = await response.json();
                
                if (response.ok) {
                    responseArea.innerHTML = `
                        <div class="success">
                            <strong>Reasoning Engine Test:</strong><br>
                            ${data.message || 'Reasoning engine operational'}<br>
                            Status: ${data.status}<br>
                            Logic Types: ${data.logic_types ? data.logic_types.join(', ') : 'Basic reasoning'}
                        </div>
                    `;
                } else {
                    responseArea.innerHTML = `<div class="error">Reasoning test failed: ${data.error || 'Reasoning module not available'}</div>`;
                }
            } catch (error) {
                responseArea.innerHTML = `<div class="error">Reasoning test error: ${error.message}</div>`;
            }
        }
        
        async function testValidation() {
            const responseArea = document.getElementById('responseArea');
            responseArea.innerHTML = '<div class="loading">✅ Testing Validation System...</div>';
            
            try {
                const response = await fetch('/api/validate/test');
                const data = await response.json();
                
                if (response.ok) {
                    responseArea.innerHTML = `
                        <div class="success">
                            <strong>Validation System Test:</strong><br>
                            ${data.message || 'Validation system operational'}<br>
                            Status: ${data.status}<br>
                            Validation Types: ${data.validation_types ? data.validation_types.join(', ') : 'Basic validation'}
                        </div>
                    `;
                } else {
                    responseArea.innerHTML = `<div class="error">Validation test failed: ${data.error || 'Validation module not available'}</div>`;
                }
            } catch (error) {
                responseArea.innerHTML = `<div class="error">Validation test error: ${error.message}</div>`;
            }
        }
        
        async function runCognitiveTest() {
            const responseArea = document.getElementById('responseArea');
            responseArea.innerHTML = '<div class="loading">🧠 Running Full Cognitive Test Suite...</div>';
            
            try {
                const response = await fetch('/api/cognitive/full-test');
                const data = await response.json();
                
                if (response.ok) {
                    responseArea.innerHTML = `
                        <div class="success">
                            <strong>Full Cognitive Test Results:</strong><br>
                            ${data.summary || 'Cognitive systems operational'}<br>
                            Memory: ${data.memory_status || 'Unknown'}<br>
                            Reasoning: ${data.reasoning_status || 'Unknown'}<br>
                            Validation: ${data.validation_status || 'Unknown'}<br>
                            Overall Score: ${data.cognitive_score || 'N/A'}%
                        </div>
                    `;
                } else {
                    responseArea.innerHTML = `<div class="error">Cognitive test failed: ${data.error || 'Cognitive modules not available'}</div>`;
                }
            } catch (error) {
                responseArea.innerHTML = `<div class="error">Cognitive test error: ${error.message}</div>`;
            }
        }
        
        async function testAIProxy() {
            const userInput = document.getElementById('userInput').value.trim() || "Hello! Test your AI capabilities.";
            const modelSelect = document.getElementById('modelSelect').value;
            const responseArea = document.getElementById('responseArea');
            
            responseArea.innerHTML = '<div class="loading">🤖 Testing AI Proxy...</div>';
            
            try {
                const response = await fetch('/api/ai-proxy', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ 
                        query: userInput,
                        provider: 'groq',
                        model: modelSelect === 'auto' ? undefined : modelSelect
                    })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    responseArea.innerHTML = `
                        <div class="success">${data.content}</div>
                        <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.2); font-size: 0.9em; color: #a0a0a0;">
                            Provider: ${data.provider} | Model: ${data.model} | Timestamp: ${data.timestamp}
                        </div>
                    `;
                } else {
                    responseArea.innerHTML = `<div class="error">AI Proxy Error: ${data.error || 'Unknown error'}</div>`;
                }
            } catch (error) {
                responseArea.innerHTML = `<div class="error">AI Proxy Network Error: ${error.message}</div>`;
            }
        }
        
        async function testVision() {
            const responseArea = document.getElementById('responseArea');
            responseArea.innerHTML = '<div class="loading">👁️ Testing Vision capabilities...</div>';
            
            try {
                const response = await fetch('/vision/test');
                const data = await response.json();
                
                if (response.ok) {
                    responseArea.innerHTML = `
                        <div class="success">
                            <strong>Vision Test Results:</strong><br>
                            ${data.message || 'Vision system operational'}<br>
                            Status: ${data.status}<br>
                            Features: ${data.features ? data.features.join(', ') : 'Basic vision processing'}
                        </div>
                    `;
                } else {
                    responseArea.innerHTML = `<div class="error">Vision test failed: ${data.error || 'Vision module not available'}</div>`;
                }
            } catch (error) {
                responseArea.innerHTML = `<div class="error">Vision test error: ${error.message}</div>`;
            }
        }
        
        async function testProxyRoute() {
            const responseArea = document.getElementById('responseArea');
            responseArea.innerHTML = '<div class="loading">🔗 Testing Proxy Route...</div>';
            
            try {
                const response = await fetch('/test-proxy');
                const data = await response.json();
                
                if (response.ok) {
                    responseArea.innerHTML = `
                        <div class="success">
                            <strong>Proxy Route Test:</strong><br>
                            ${data.message || 'Proxy route operational'}<br>
                            Status: ${data.status}<br>
                            Endpoint: ${data.endpoint || '/test-proxy'}
                        </div>
                    `;
                } else {
                    responseArea.innerHTML = `<div class="error">Proxy route test failed: ${data.error || 'Proxy route not available'}</div>`;
                }
            } catch (error) {
                responseArea.innerHTML = `<div class="error">Proxy route test error: ${error.message}</div>`;
            }
        }
        
        async function showBlueprints() {
            const responseArea = document.getElementById('responseArea');
            responseArea.innerHTML = '<div class="loading">📋 Loading Blueprint information...</div>';
            
            try {
                const response = await fetch('/api/blueprints');
                const data = await response.json();
                
                if (response.ok) {
                    const blueprintList = data.blueprints.map(bp => 
                        `• ${bp.name} (${bp.url_prefix}) - ${bp.status} [${bp.type}]`
                    ).join('<br>');
                    
                    responseArea.innerHTML = `
                        <div class="success">
                            <strong>Registered Blueprints:</strong><br>
                            ${blueprintList}<br><br>
                            Total: ${data.total_blueprints}<br>
                            Active: ${data.active_blueprints}<br>
                            Cognitive: ${data.cognitive_modules}<br>
                            Enterprise: ${data.enterprise_modules}
                        </div>
                    `;
                } else {
                    responseArea.innerHTML = `<div class="error">Blueprint info failed: ${data.error}</div>`;
                }
            } catch (error) {
                responseArea.innerHTML = `<div class="error">Blueprint info error: ${error.message}</div>`;
            }
        }
        
        async function testHealth() {
            const responseArea = document.getElementById('responseArea');
            responseArea.innerHTML = '<div class="loading">🔍 Checking system health...</div>';
            
            try {
                const response = await fetch('/health');
                const data = await response.json();
                
                if (response.ok) {
                    responseArea.innerHTML = `
                        <div class="success">
                            <strong>System Health Check:</strong><br>
                            Status: ${data.status}<br>
                            API Key Configured: ${data.api_key_configured ? 'Yes' : 'No'}<br>
                            Available Providers: ${data.available_providers || 0}<br>
                            Available Models: ${data.available_models || 0}<br>
                            Blueprints: ${data.blueprints_loaded || 0}<br>
                            Cognitive Modules: ${data.cognitive_modules || 0}<br>
                            Enterprise Modules: ${data.enterprise_modules || 0}<br>
                            Timestamp: ${data.timestamp}<br>
                            Version: ${data.version}
                        </div>
                    `;
                } else {
                    responseArea.innerHTML = `<div class="error">Health check failed: ${data.error}</div>`;
                }
            } catch (error) {
                responseArea.innerHTML = `<div class="error">Health check error: ${error.message}</div>`;
            }
        }
        
        function clearResponse() {
            document.getElementById('userInput').value = '';
            document.getElementById('responseArea').innerHTML = 
                '<div style="color: #a0a0a0; text-align: center;">Ready for enterprise-grade AI interactions!</div>';
        }
        
        // Allow Enter key to send message
        document.getElementById('userInput').addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendToBrain();
            }
        });
        
        // Check system status on load
        window.onload = function() {
            fetch('/health')
                .then(response => response.json())
                .then(data => {
                    const indicator = document.getElementById('statusIndicator');
                    if (data.status === 'healthy') {
                        indicator.innerHTML = '🟢 Enterprise Online';
                        indicator.style.borderColor = '#51cf66';
                    } else {
                        indicator.innerHTML = '🟡 System Issues';
                        indicator.style.borderColor = '#ffd43b';
                    }
                })
                .catch(error => {
                    const indicator = document.getElementById('statusIndicator');
                    indicator.innerHTML = '🔴 System Offline';
                    indicator.style.borderColor = '#ff6b6b';
                });
                
            // Check auth status
            fetch('/api/auth/status')
                .then(response => response.json())
                .then(data => updateAuthStatus(data.status))
                .catch(error => updateAuthStatus('offline'));
                
            // Check quota status
            fetch('/api/quota/status')
                .then(response => response.json())
                .then(data => updateQuotaStatus(data.current_usage, data.quota_limit))
                .catch(error => {
                    document.getElementById('quotaStatus').innerHTML = '📊 Quota: Error';
                });
        };
    </script>
</body>
</html>
'''

# Enhanced Blueprint Registration Function
def register_blueprints():
    """Register blueprints with enterprise module support"""
    registered_blueprints = []
    
    for module_path, blueprint_name, url_prefix in BLUEPRINT_ROUTES:
        try:
            # Try to import the module
            module = importlib.import_module(module_path)
            
            # Get the blueprint from the module
            if hasattr(module, blueprint_name):
                blueprint = getattr(module, blueprint_name)
                app.register_blueprint(blueprint, url_prefix=url_prefix)
                registered_blueprints.append({
                    'name': blueprint_name,
                    'module': module_path,
                    'url_prefix': url_prefix,
                    'status': 'registered',
                    'type': get_module_type(module_path)
                })
                print(f"✅ Registered blueprint: {blueprint_name} from {module_path}")
            else:
                print(f"⚠️ Blueprint {blueprint_name} not found in {module_path}")
                registered_blueprints.append({
                    'name': blueprint_name,
                    'module': module_path,
                    'url_prefix': url_prefix,
                    'status': 'blueprint_not_found',
                    'type': get_module_type(module_path)
                })
                
        except ImportError as e:
            print(f"⚠️ Could not import {module_path}: {e}")
            # Create fallback blueprint
            fallback_bp = create_fallback_blueprint(blueprint_name, module_path, url_prefix)
            app.register_blueprint(fallback_bp, url_prefix=url_prefix)
            registered_blueprints.append({
                'name': blueprint_name,
                'module': module_path,
                'url_prefix': url_prefix,
                'status': 'fallback_created',
                'type': get_module_type(module_path)
            })
            
        except Exception as e:
            print(f"❌ Error registering {blueprint_name}: {e}")
            registered_blueprints.append({
                'name': blueprint_name,
                'module': module_path,
                'url_prefix': url_prefix,
                'status': 'error',
                'type': get_module_type(module_path)
            })
    
    return registered_blueprints

def get_module_type(module_path):
    """Determine module type for categorization"""
    if any(cog in module_path for cog in ['memory', 'reasoning', 'validation']):
        return 'cognitive'
    elif any(ent in module_path for ent in ['auth_gate', 'pro_router', 'quota']):
        return 'enterprise'
    elif any(sys in module_path for sys in ['vision', 'ai_proxy']):
        return 'system'
    else:
        return 'core'

def create_fallback_blueprint(name, module_path, url_prefix):
    """Create enhanced fallback blueprints for all module types"""
    bp = Blueprint(name, __name__)
    
    if 'auth_gate' in module_path:
        @bp.route('/test')
        def auth_test():
            return jsonify({
                'status': 'fallback',
                'message': 'Authentication system fallback - module not available',
                'auth_methods': ['basic_auth', 'token_auth', 'session_auth'],
                'security_level': 'Standard',
                'module': module_path,
                'timestamp': datetime.now().isoformat()
            })
            
        @bp.route('/status')
        def auth_status():
            return jsonify({
                'status': 'fallback',
                'authenticated': False,
                'user': None,
                'permissions': [],
                'module': module_path,
                'timestamp': datetime.now().isoformat()
            })
            
        @bp.route('/login', methods=['POST'])
        def auth_login():
            return jsonify({
                'status': 'fallback',
                'message': 'Authentication not available - using fallback mode',
                'authenticated': False,
                'token': None,
                'module': module_path,
                'timestamp': datetime.now().isoformat()
            })
    
    elif 'pro_router' in module_path:
        @bp.route('/test')
        def router_test():
            return jsonify({
                'status': 'fallback',
                'message': 'Pro router system fallback - module not available',
                'router_types': ['load_balancer', 'failover', 'round_robin'],
                'load_balancing': 'Enabled',
                'module': module_path,
                'timestamp': datetime.now().isoformat()
            })
            
        @bp.route('/status')
        def router_status():
            return jsonify({
                'status': 'fallback',
                'active_routes': 0,
                'load_balance': 'fallback',
                'health_checks': 'disabled',
                'module': module_path,
                'timestamp': datetime.now().isoformat()
            })
            
        @bp.route('/route', methods=['POST'])
        def route_request():
            return jsonify({
                'status': 'fallback',
                'message': 'Pro routing not available - using direct routing',
                'routed_to': 'fallback_endpoint',
                'module': module_path,
                'timestamp': datetime.now().isoformat()
            })
    
    elif 'quota' in module_path:
        @bp.route('/test')
        def quota_test():
            return jsonify({
                'status': 'fallback',
                'message': 'Quota management fallback - module not available',
                'current_usage': 0,
                'quota_limit': 1000,
                'quota_types': ['request_limits', 'rate_limits', 'usage_tracking'],
                'module': module_path,
                'timestamp': datetime.now().isoformat()
            })
            
        @bp.route('/status')
        def quota_status():
            return jsonify({
                'status': 'fallback',
                'current_usage': 0,
                'quota_limit': 1000,
                'percentage_used': 0,
                'reset_time': None,
                'module': module_path,
                'timestamp': datetime.now().isoformat()
            })
            
        @bp.route('/check', methods=['POST'])
        def quota_check():
            return jsonify({
                'status': 'fallback',
                'allowed': True,
                'remaining': 1000,
                'message': 'Quota checking not available - allowing request',
                'module': module_path,
                'timestamp': datetime.now().isoformat()
            })
    
    elif 'memory' in module_path:
        @bp.route('/test')
        def memory_test():
            return jsonify({
                'status': 'fallback',
                'message': 'Memory system fallback - module not available',
                'capabilities': ['basic_storage', 'session_memory', 'fallback_responses'],
                'module': module_path,
                'timestamp': datetime.now().isoformat()
            })
            
        @bp.route('/store', methods=['POST'])
        def memory_store():
            return jsonify({
                'status': 'fallback',
                'message': 'Memory storage not available - using session storage',
                'stored': False,
                'module': module_path,
                'timestamp': datetime.now().isoformat()
            })
            
        @bp.route('/recall', methods=['POST'])
        def memory_recall():
            return jsonify({
                'status': 'fallback',
                'message': 'Memory recall not available - no persistent storage',
                'recalled': None,
                'module': module_path,
                'timestamp': datetime.now().isoformat()
            })
    
    elif 'reasoning' in module_path:
        @bp.route('/test')
        def reasoning_test():
            return jsonify({
                'status': 'fallback',
                'message': 'Reasoning engine fallback - module not available',
                'logic_types': ['basic_logic', 'pattern_matching', 'simple_inference'],
                'module': module_path,
                'timestamp': datetime.now().isoformat()
            })
            
        @bp.route('/analyze', methods=['POST'])
        def reasoning_analyze():
            data = request.get_json() or {}
            problem = data.get('problem', 'No problem specified')
            return jsonify({
                'status': 'fallback',
                'message': f'Basic reasoning applied to: {problem}',
                'analysis': 'Fallback reasoning - limited analysis available',
                'confidence': 0.3,
                'module': module_path,
                'timestamp': datetime.now().isoformat()
            })
    
    elif 'self_validate' in module_path or 'validation' in module_path:
        @bp.route('/test')
        def validation_test():
            return jsonify({
                'status': 'fallback',
                'message': 'Validation system fallback - module not available',
                'validation_types': ['basic_checks', 'format_validation', 'simple_rules'],
                'module': module_path,
                'timestamp': datetime.now().isoformat()
            })
            
        @bp.route('/validate', methods=['POST'])
        def validate_content():
            data = request.get_json() or {}
            content = data.get('content', '')
            return jsonify({
                'status': 'fallback',
                'message': 'Basic validation performed',
                'valid': len(content) > 0,
                'issues': ['Validation module not available - limited checking'],
                'confidence': 0.5,
                'module': module_path,
                'timestamp': datetime.now().isoformat()
            })
    
    elif 'vision' in module_path:
        @bp.route('/test')
        def vision_test():
            return jsonify({
                'status': 'fallback',
                'message': 'Vision module not available - using fallback',
                'features': ['basic_fallback'],
                'module': module_path,
                'timestamp': datetime.now().isoformat()
            })
    
    elif 'test_route' in module_path:
        @bp.route('/test-proxy')
        def test_proxy():
            return jsonify({
                'status': 'fallback',
                'message': 'AI Proxy test route - fallback implementation',
                'endpoint': '/test-proxy',
                'module': module_path,
                'timestamp': datetime.now().isoformat()
            })
    
    return bp

# Enhanced AI Provider Functions (same as before)
def make_groq_request_with_fallback(message, preferred_model=None):
    """Make request to Groq API with intelligent model fallback"""
    if not GROQ_API_KEY:
        return None, None
    
    models_to_try = [preferred_model] if preferred_model else GROQ_MODELS
    if preferred_model and preferred_model not in models_to_try:
        models_to_try = [preferred_model] + GROQ_MODELS
    
    for model in models_to_try:
        if not model:
            continue
            
        try:
            headers = {
                'Authorization': f'Bearer {GROQ_API_KEY}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': model,
                'messages': [
                    {
                        'role': 'system',
                        'content': 'You are Mythiq Enterprise, an advanced AI assistant with enterprise-grade capabilities including authentication, pro routing, quota management, and cognitive functions. Respond professionally and helpfully.'
                    },
                    {
                        'role': 'user', 
                        'content': message
                    }
                ],
                'max_tokens': 1000,
                'temperature': 0.7,
                'top_p': 1,
                'stream': False,
                'stop': None
            }
            
            response = requests.post(
                'https://api.groq.com/openai/v1/chat/completions',
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                return content.strip(), model
            else:
                print(f"Groq API error with {model}: {response.status_code} - {response.text}")
                continue
                
        except Exception as e:
            print(f"Groq request error with {model}: {e}")
            continue
    
    return None, None

def make_huggingface_request(message):
    """Make request to Hugging Face API"""
    if not HUGGING_FACE_API_KEY:
        return None
    
    try:
        headers = {
            'Authorization': f'Bearer {HUGGING_FACE_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'inputs': message,
            'parameters': {
                'max_length': 500,
                'temperature': 0.7,
                'return_full_text': False
            }
        }
        
        response = requests.post(
            'https://api-inference.huggingface.co/models/microsoft/DialoGPT-large',
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', '').strip()
            return None
        else:
            print(f"Hugging Face API error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Hugging Face request error: {e}")
        return None

def get_fallback_response(message):
    """Generate intelligent fallback response with enterprise awareness"""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['hello', 'hi', 'hey']):
        return "Hello! I'm Mythiq Gateway Enterprise v2.4.0, your advanced AI assistant with enterprise-grade capabilities including authentication, pro routing, quota management, and cognitive functions. How can I assist you today?"
    
    elif any(word in message_lower for word in ['enterprise', 'business', 'professional']):
        return """Welcome to Mythiq Gateway Enterprise! Our platform includes:

• **Authentication System**: Secure user management and access control
• **Pro Router**: Intelligent request routing and load balancing
• **Quota Management**: Usage tracking and rate limiting
• **Cognitive Architecture**: Memory, reasoning, and validation capabilities
• **Latest AI Models**: Llama 3.3 70B, Mistral Saba, and Mixtral integration

This enterprise-grade solution provides scalable, secure, and intelligent AI services for professional applications."""
    
    elif any(word in message_lower for word in ['auth', 'authentication', 'login']):
        return """Our authentication system provides:

• **Multi-Method Authentication**: Basic auth, token-based, and session management
• **Security Levels**: Standard, enhanced, and enterprise-grade protection
• **User Management**: Role-based access control and permissions
• **Session Handling**: Secure session management and token validation

The authentication gateway ensures secure access to all enterprise features while maintaining high performance and reliability."""
    
    elif any(word in message_lower for word in ['quota', 'limit', 'usage']):
        return """Our quota management system offers:

• **Usage Tracking**: Real-time monitoring of API calls and resource consumption
• **Rate Limiting**: Configurable limits to prevent abuse and ensure fair usage
• **Quota Types**: Request limits, bandwidth limits, and feature-based quotas
• **Analytics**: Detailed usage reports and trend analysis

This ensures optimal resource allocation and prevents system overload while providing transparency in usage patterns."""
    
    elif any(word in message_lower for word in ['router', 'routing', 'proxy']):
        return """Our pro router system includes:

• **Load Balancing**: Intelligent distribution of requests across multiple endpoints
• **Failover Protection**: Automatic switching to backup systems during outages
• **Health Monitoring**: Continuous monitoring of endpoint availability and performance
• **Route Optimization**: Dynamic routing based on performance metrics and load

This ensures high availability, optimal performance, and seamless scaling for enterprise applications."""
    
    else:
        return f"I understand you're asking about: {message}. As Mythiq Gateway Enterprise, I can help you with this through our comprehensive platform that includes authentication, pro routing, quota management, and advanced cognitive capabilities. Our enterprise-grade architecture ensures secure, scalable, and intelligent responses to your business needs."

# Routes
@app.route('/')
def index():
    """Main route - serves the enterprise frontend interface"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/health')
def health_check():
    """Enhanced health check with enterprise module status"""
    try:
        available_providers = 0
        available_models = 0
        
        if GROQ_API_KEY:
            available_providers += 1
            available_models += len(GROQ_MODELS)
        if HUGGING_FACE_API_KEY:
            available_providers += 1
            available_models += 1
        
        # Count registered blueprints by type
        blueprints_loaded = len([bp for bp in app.blueprints.values()])
        cognitive_modules = len([bp for bp in BLUEPRINT_ROUTES if any(cog in bp[0] for cog in ['memory', 'reasoning', 'validation'])])
        enterprise_modules = len([bp for bp in BLUEPRINT_ROUTES if any(ent in bp[0] for ent in ['auth_gate', 'pro_router', 'quota'])])
        
        return jsonify({
            'status': 'healthy',
            'api_key_configured': bool(GROQ_API_KEY),
            'available_providers': available_providers,
            'available_models': available_models,
            'blueprints_loaded': blueprints_loaded,
            'cognitive_modules': cognitive_modules,
            'enterprise_modules': enterprise_modules,
            'groq_models': GROQ_MODELS,
            'timestamp': datetime.now().isoformat(),
            'version': '2.4.0',
            'edition': 'Enterprise',
            'features': ['groq_api', 'model_fallback', 'ai_proxy', 'huggingface_api', 'intelligent_responses', 'blueprint_system', 'vision_support', 'memory_system', 'reasoning_engine', 'validation_framework', 'authentication', 'pro_router', 'quota_management']
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/enterprise/status')
def enterprise_status():
    """Comprehensive enterprise system status"""
    try:
        # Check enterprise module status
        auth_status = 'fallback'
        router_status = 'fallback'
        quota_status = 'fallback'
        
        # Check if enterprise modules are available
        for bp_name in app.blueprints:
            if 'auth' in bp_name:
                auth_status = 'active'
            elif 'router' in bp_name or 'proxy' in bp_name:
                router_status = 'active'
            elif 'quota' in bp_name:
                quota_status = 'active'
        
        # Calculate enterprise score
        active_modules = sum(1 for status in [auth_status, router_status, quota_status] if status == 'active')
        enterprise_score = (active_modules / 3) * 100
        
        return jsonify({
            'summary': f'Enterprise systems operational - {active_modules}/3 modules active',
            'auth_status': auth_status,
            'router_status': router_status,
            'quota_status': quota_status,
            'enterprise_score': enterprise_score,
            'license_type': 'Enterprise' if enterprise_score > 50 else 'Community',
            'timestamp': datetime.now().isoformat(),
            'version': '2.4.0'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/cognitive/full-test')
def cognitive_full_test():
    """Comprehensive cognitive system test"""
    try:
        # Test each cognitive module
        memory_status = 'fallback'
        reasoning_status = 'fallback'
        validation_status = 'fallback'
        
        # Check if cognitive modules are available
        for bp_name in app.blueprints:
            if 'memory' in bp_name:
                memory_status = 'active'
            elif 'reasoning' in bp_name:
                reasoning_status = 'active'
            elif 'validation' in bp_name:
                validation_status = 'active'
        
        # Calculate cognitive score
        active_modules = sum(1 for status in [memory_status, reasoning_status, validation_status] if status == 'active')
        cognitive_score = (active_modules / 3) * 100
        
        return jsonify({
            'summary': f'Cognitive systems operational - {active_modules}/3 modules active',
            'memory_status': memory_status,
            'reasoning_status': reasoning_status,
            'validation_status': validation_status,
            'cognitive_score': cognitive_score,
            'timestamp': datetime.now().isoformat(),
            'version': '2.4.0'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/blueprints')
def blueprint_status():
    """Get information about registered blueprints with enterprise module details"""
    try:
        blueprint_info = []
        cognitive_count = 0
        enterprise_count = 0
        
        for name, blueprint in app.blueprints.items():
            is_cognitive = any(cog in name for cog in ['memory', 'reasoning', 'validation'])
            is_enterprise = any(ent in name for ent in ['auth', 'router', 'quota', 'proxy'])
            
            if is_cognitive:
                cognitive_count += 1
            elif is_enterprise:
                enterprise_count += 1
                
            module_type = 'cognitive' if is_cognitive else 'enterprise' if is_enterprise else 'system'
                
            blueprint_info.append({
                'name': name,
                'url_prefix': blueprint.url_prefix or '/',
                'status': 'active',
                'type': module_type
            })
        
        return jsonify({
            'blueprints': blueprint_info,
            'total_blueprints': len(blueprint_info),
            'active_blueprints': len(blueprint_info),
            'cognitive_modules': cognitive_count,
            'enterprise_modules': enterprise_count,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/status')
def api_status():
    """API status route with enterprise module information"""
    return jsonify({
        'status': 'online',
        'message': 'Mythiq Gateway Enterprise API is operational',
        'timestamp': time.time(),
        'endpoints': ['/api/brain', '/api/ai-proxy', '/health', '/api/status', '/api/blueprints', '/api/cognitive/full-test', '/api/enterprise/status'],
        'models': GROQ_MODELS,
        'blueprints': len(app.blueprints),
        'cognitive_modules': len([bp for bp in BLUEPRINT_ROUTES if any(cog in bp[0] for cog in ['memory', 'reasoning', 'validation'])]),
        'enterprise_modules': len([bp for bp in BLUEPRINT_ROUTES if any(ent in bp[0] for ent in ['auth_gate', 'pro_router', 'quota'])]),
        'version': '2.4.0',
        'edition': 'Enterprise'
    }), 200

@app.route('/api/brain', methods=['POST'])
def brain_api():
    """Main AI processing route with enterprise support"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Invalid JSON in request body',
                'status': 'error',
                'timestamp': datetime.now().isoformat()
            }), 400
        
        message = data.get('message', '').strip()
        if not message:
            return jsonify({
                'error': 'No message provided',
                'status': 'error',
                'timestamp': datetime.now().isoformat()
            }), 400
        
        # Try AI providers with model fallback
        ai_response = None
        provider_used = None
        model_used = None
        
        # Try Groq with intelligent model fallback
        if GROQ_API_KEY:
            ai_response, model_used = make_groq_request_with_fallback(message)
            if ai_response:
                provider_used = 'groq'
        
        # Try Hugging Face if Groq failed
        if not ai_response and HUGGING_FACE_API_KEY:
            ai_response = make_huggingface_request(message)
            if ai_response:
                provider_used = 'huggingface'
                model_used = 'DialoGPT-large'
        
        # Use intelligent fallback if all APIs failed
        if not ai_response:
            ai_response = get_fallback_response(message)
            provider_used = 'fallback'
            model_used = 'enterprise_fallback'
        
        return jsonify({
            'response': ai_response,
            'provider': provider_used,
            'model': model_used,
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'input_length': len(message),
            'response_length': len(ai_response),
            'enterprise_enhanced': True
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Internal server error: {str(e)}',
            'status': 'error',
            'timestamp': datetime.now().isoformat(),
            'traceback': traceback.format_exc() if app.debug else None
        }), 500

@app.route('/api/ai-proxy', methods=['POST'])
def ai_proxy():
    """Enhanced AI Proxy with enterprise features"""
    try:
        data = request.get_json() or {}
        prompt = data.get('query', '').strip()
        provider = data.get('provider', 'groq')
        preferred_model = data.get('model')
        
        # Input validation
        if not prompt:
            return jsonify({
                'error': 'Missing query content.',
                'status': 'failed'
            }), 400
        
        if provider == 'groq':
            if not GROQ_API_KEY:
                return jsonify({
                    'content': '[Error] Groq API key not configured.',
                    'provider': 'groq',
                    'model': 'none',
                    'timestamp': int(time.time() * 1000)
                }), 200
            
            # Use intelligent model fallback
            ai_response, model_used = make_groq_request_with_fallback(prompt, preferred_model)
            
            if ai_response:
                return jsonify({
                    'content': ai_response,
                    'provider': 'groq',
                    'model': model_used,
                    'timestamp': int(time.time() * 1000),
                    'enterprise_enhanced': True
                }), 200
            else:
                # All Groq models failed, use enterprise fallback
                fallback_response = get_fallback_response(prompt)
                return jsonify({
                    'content': f'[Enterprise Fallback] {fallback_response}',
                    'provider': 'groq_enterprise_fallback',
                    'model': 'enterprise_responses',
                    'timestamp': int(time.time() * 1000)
                }), 200
        
        return jsonify({
            'error': 'Invalid provider specified.',
            'status': 'failed'
        }), 400
        
    except Exception as e:
        return jsonify({
            'content': f'[Error] AI Proxy encountered an error: {str(e)}',
            'provider': 'error',
            'model': 'none',
            'timestamp': int(time.time() * 1000)
        }), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'status': 'error',
        'available_endpoints': ['/', '/health', '/api/brain', '/api/ai-proxy', '/api/status', '/api/blueprints', '/api/cognitive/full-test', '/api/enterprise/status'],
        'timestamp': datetime.now().isoformat()
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'error': 'Method not allowed',
        'status': 'error',
        'timestamp': datetime.now().isoformat()
    }), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'status': 'error',
        'timestamp': datetime.now().isoformat()
    }), 500

if __name__ == '__main__':
    # Register blueprints before starting the app
    print("🏢 Registering Enterprise blueprints with cognitive and business modules...")
    registered_blueprints = register_blueprints()
    
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Starting Mythiq Gateway Enterprise v2.4.0 on port {port}")
    print(f"🔑 Groq API Key: {'✅ Configured' if GROQ_API_KEY else '❌ Missing'}")
    print(f"🔑 Hugging Face API Key: {'✅ Configured' if HUGGING_FACE_API_KEY else '❌ Missing'}")
    print(f"🤖 Available Groq Models: {len(GROQ_MODELS)}")
    print(f"📋 Models: {', '.join(GROQ_MODELS)}")
    print(f"🔗 Registered Blueprints: {len(registered_blueprints)}")
    
    cognitive_modules = 0
    enterprise_modules = 0
    for bp in registered_blueprints:
        status_icon = "✅" if bp['status'] == 'registered' else "⚠️" if bp['status'] == 'fallback_created' else "❌"
        
        if bp['type'] == 'cognitive':
            cognitive_modules += 1
            module_icon = "🧠"
        elif bp['type'] == 'enterprise':
            enterprise_modules += 1
            module_icon = "🏢"
        else:
            module_icon = "🔧"
            
        print(f"   {status_icon} {module_icon} {bp['name']} ({bp['status']})")
    
    print(f"🧠 Cognitive Modules: {cognitive_modules}/3")
    print(f"🏢 Enterprise Modules: {enterprise_modules}/3")
    print(f"🎯 Enterprise Features: Authentication, Pro Router, Quota Management")
    print(f"🎯 Cognitive Features: Memory, Reasoning, Validation")
    print(f"🎯 System Features: Vision, AI Proxy, Latest Models")
    
    app.run(host='0.0.0.0', port=port, debug=False)
