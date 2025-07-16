from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os
import requests
import json
import time
import traceback
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configuration
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
HUGGING_FACE_API_KEY = os.environ.get('HUGGING_FACE') or os.environ.get('HUGGINGFACE_API_KEY')

# HTML Template for the frontend
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mythiq Gateway</title>
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
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            color: #00ffff;
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 30px;
            text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
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
            margin-bottom: 20px;
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
    </style>
</head>
<body>
    <div class="status-indicator" id="statusIndicator">
        🟢 System Online
    </div>
    
    <div class="container">
        <h1>🧠 Mythiq Gateway</h1>
        
        <textarea id="userInput" placeholder="Ask Mythiq anything..."></textarea>
        
        <button onclick="sendToBrain()">Send to Brain</button>
        <button onclick="testHealth()" style="margin-left: 10px;">Test Health</button>
        <button onclick="clearResponse()" style="margin-left: 10px;">Clear</button>
        
        <div class="response-container" id="responseArea">
            <div style="color: #a0a0a0; text-align: center;">
                Welcome to Mythiq Gateway! Ask me anything to get started.
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
            
            responseArea.innerHTML = '<div class="loading">🧠 Thinking...</div>';
            
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
                            Provider: ${data.provider || 'AI'} | Status: ${data.status} | Time: ${new Date().toLocaleTimeString()}
                        </div>
                    `;
                } else {
                    responseArea.innerHTML = `<div class="error">Error: ${data.error || 'Unknown error occurred'}</div>`;
                }
            } catch (error) {
                responseArea.innerHTML = `<div class="error">Network error: ${error.message}</div>`;
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
                            Timestamp: ${data.timestamp}<br>
                            Available Providers: ${data.available_providers || 0}
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
                '<div style="color: #a0a0a0; text-align: center;">Ready for new questions!</div>';
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
                        indicator.innerHTML = '🟢 System Online';
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
        };
    </script>
</body>
</html>
'''

# AI Provider Functions
def make_groq_request(message):
    """Make request to Groq API"""
    if not GROQ_API_KEY:
        return None
    
    try:
        headers = {
            'Authorization': f'Bearer {GROQ_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'mixtral-8x7b-32768',
            'messages': [{'role': 'user', 'content': message}],
            'max_tokens': 1000,
            'temperature': 0.7
        }
        
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            print(f"Groq API error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Groq request error: {e}")
        return None

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
    """Generate fallback response when APIs are unavailable"""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['hello', 'hi', 'hey']):
        return "Hello! I'm Mythiq Gateway, your AI assistant. How can I help you today?"
    
    elif any(word in message_lower for word in ['test', 'working', 'functionality']):
        return "Yes, I'm working properly! My AI capabilities are active and I'm ready to assist you with questions, explanations, and various tasks."
    
    elif any(word in message_lower for word in ['artificial intelligence', 'ai', 'machine learning']):
        return """Artificial Intelligence (AI) is a branch of computer science that aims to create intelligent machines capable of performing tasks that typically require human intelligence. This includes:

• Machine Learning: Systems that improve through experience
• Natural Language Processing: Understanding and generating human language
• Computer Vision: Interpreting visual information
• Robotics: Physical AI applications
• Expert Systems: AI that mimics human expertise in specific domains

AI is transforming industries from healthcare to finance, enabling automation, better decision-making, and new capabilities we never thought possible."""
    
    elif any(word in message_lower for word in ['help', 'what can you do']):
        return """I can help you with:

• Answering questions on various topics
• Explaining complex concepts
• Providing information and research
• Creative writing and brainstorming
• Problem-solving assistance
• Technical discussions
• General conversation

Feel free to ask me anything you'd like to know about!"""
    
    else:
        return f"I understand you're asking about: {message}. While my AI providers are currently unavailable, I'm designed to help with questions, explanations, and various tasks. Please try again in a moment, or rephrase your question for a more specific response."

# Routes
@app.route('/')
def index():
    """Main route - serves the frontend interface"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/health')
def health_check():
    """Health check route - returns JSON status"""
    try:
        available_providers = 0
        if GROQ_API_KEY:
            available_providers += 1
        if HUGGING_FACE_API_KEY:
            available_providers += 1
        
        return jsonify({
            'status': 'healthy',
            'api_key_configured': bool(GROQ_API_KEY),
            'available_providers': available_providers,
            'timestamp': datetime.now().isoformat(),
            'version': '2.0.0',
            'features': ['groq_api', 'huggingface_api', 'fallback_responses']
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/status')
def api_status():
    """API status route - alternative health check"""
    return jsonify({
        'status': 'online',
        'message': 'Mythiq Gateway API is operational',
        'timestamp': time.time(),
        'endpoints': ['/api/brain', '/health', '/api/status']
    }), 200

@app.route('/api/brain', methods=['POST'])
def brain_api():
    """Main AI processing route - returns JSON responses"""
    try:
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Invalid JSON in request body',
                'status': 'error',
                'timestamp': datetime.now().isoformat()
            }), 400
        
        # Extract message
        message = data.get('message', '').strip()
        if not message:
            return jsonify({
                'error': 'No message provided',
                'status': 'error',
                'timestamp': datetime.now().isoformat()
            }), 400
        
        # Try AI providers in order
        ai_response = None
        provider_used = None
        
        # Try Groq first
        if GROQ_API_KEY:
            ai_response = make_groq_request(message)
            if ai_response:
                provider_used = 'groq'
        
        # Try Hugging Face if Groq failed
        if not ai_response and HUGGING_FACE_API_KEY:
            ai_response = make_huggingface_request(message)
            if ai_response:
                provider_used = 'huggingface'
        
        # Use fallback if all APIs failed
        if not ai_response:
            ai_response = get_fallback_response(message)
            provider_used = 'fallback'
        
        # Return JSON response
        return jsonify({
            'response': ai_response,
            'provider': provider_used,
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'input_length': len(message),
            'response_length': len(ai_response)
        }), 200
        
    except Exception as e:
        # Always return JSON, never HTML
        return jsonify({
            'error': f'Internal server error: {str(e)}',
            'status': 'error',
            'timestamp': datetime.now().isoformat(),
            'traceback': traceback.format_exc() if app.debug else None
        }), 500

# Error handlers to ensure JSON responses
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'status': 'error',
        'available_endpoints': ['/', '/health', '/api/brain', '/api/status'],
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
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Starting Mythiq Gateway on port {port}")
    print(f"🔑 Groq API Key: {'✅ Configured' if GROQ_API_KEY else '❌ Missing'}")
    print(f"🔑 Hugging Face API Key: {'✅ Configured' if HUGGING_FACE_API_KEY else '❌ Missing'}")
    app.run(host='0.0.0.0', port=port, debug=False)
