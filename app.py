from flask import Flask, request, jsonify, render_template_string
import requests
import os
import json
from datetime import datetime

app = Flask(__name__)

# Configuration
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# HTML Template (embedded for simplicity)
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
        .input-container {
            margin-bottom: 20px;
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
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 255, 255, 0.4);
        }
        .response-container {
            margin-top: 20px;
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
            padding: 10px;
            border-radius: 5px;
            border-left: 4px solid #ff6b6b;
        }
        .success {
            color: #51cf66;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Mythiq Gateway</h1>
        <div class="input-container">
            <textarea id="userInput" placeholder="Ask Mythiq anything..."></textarea>
        </div>
        <button onclick="sendToBrain()">Send to Brain</button>
        <div class="response-container" id="responseArea"></div>
    </div>

    <script>
        async function sendToBrain() {
            const userInput = document.getElementById('userInput').value.trim();
            const responseArea = document.getElementById('responseArea');
            
            if (!userInput) {
                responseArea.innerHTML = '<div class="error">Please enter a question or message.</div>';
                return;
            }
            
            // Show loading state
            responseArea.innerHTML = '<div class="loading">Thinking...</div>';
            
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
                    responseArea.innerHTML = `<div class="success">${data.response}</div>`;
                } else {
                    responseArea.innerHTML = `<div class="error">Error: ${data.error || 'Unknown error occurred'}</div>`;
                }
            } catch (error) {
                responseArea.innerHTML = `<div class="error">Network error: ${error.message}</div>`;
            }
        }
        
        // Allow Enter key to send message (with Shift+Enter for new line)
        document.getElementById('userInput').addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendToBrain();
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """Main route - serves the frontend interface"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/brain', methods=['POST'])
def brain_api():
    """
    CORRECTED API route - processes AI requests with proper Groq API formatting
    
    This route fixes the 400 error by implementing correct Groq API request structure
    """
    try:
        # Validate API key
        if not GROQ_API_KEY:
            return jsonify({
                'error': 'API key not configured',
                'details': 'GROQ_API_KEY environment variable is missing'
            }), 500
        
        # Get user message from request
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({
                'error': 'Invalid request format',
                'details': 'Request must include "message" field'
            }), 400
        
        user_message = data['message'].strip()
        if not user_message:
            return jsonify({
                'error': 'Empty message',
                'details': 'Message cannot be empty'
            }), 400
        
        # CORRECTED: Proper Groq API request format
        groq_request = {
            "model": "mixtral-8x7b-32768",  # Valid Groq model
            "messages": [
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            "max_tokens": 1000,
            "temperature": 0.7,
            "top_p": 1,
            "stream": False
        }
        
        # CORRECTED: Proper headers for Groq API
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Make request to Groq API
        response = requests.post(
            GROQ_API_URL,
            headers=headers,
            json=groq_request,
            timeout=30
        )
        
        # Handle Groq API response
        if response.status_code == 200:
            groq_data = response.json()
            
            # Extract AI response
            if 'choices' in groq_data and len(groq_data['choices']) > 0:
                ai_response = groq_data['choices'][0]['message']['content']
                
                return jsonify({
                    'response': ai_response,
                    'model': groq_request['model'],
                    'timestamp': datetime.now().isoformat(),
                    'status': 'success'
                })
            else:
                return jsonify({
                    'error': 'Invalid response from AI service',
                    'details': 'No choices returned from Groq API'
                }), 500
                
        else:
            # Handle Groq API errors
            try:
                error_data = response.json()
                error_message = error_data.get('error', {}).get('message', 'Unknown API error')
            except:
                error_message = f"HTTP {response.status_code} error"
            
            return jsonify({
                'error': f'AI service error: {error_message}',
                'details': f'Groq API returned status {response.status_code}'
            }), 500
            
    except requests.exceptions.Timeout:
        return jsonify({
            'error': 'Request timeout',
            'details': 'AI service took too long to respond'
        }), 504
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            'error': 'Network error',
            'details': f'Failed to connect to AI service: {str(e)}'
        }), 503
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'details': f'Unexpected error: {str(e)}'
        }), 500

@app.route('/health')
def health_check():
    """Health check route for monitoring"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'api_key_configured': bool(GROQ_API_KEY)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
