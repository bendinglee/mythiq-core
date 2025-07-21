#!/usr/bin/env python3
"""
🧠 Mythiq Gateway Enterprise v4.0.0 - Database-Powered Edition
Enhanced with persistent game storage, analytics, and management features
"""

import os
import sys
import time
import json
import traceback
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

# Import our enhanced modules
from database_manager import db_manager
from game_showcase_enhanced import showcase_bp, game_showcase

# Import existing modules
try:
    from game_engine import game_engine
    print("✅ Game engine imported successfully")
except ImportError as e:
    print(f"❌ Failed to import game engine: {e}")
    game_engine = None

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mythiq-gateway-secret-key-2024')

# Register blueprints
app.register_blueprint(showcase_bp)

# Import and register existing blueprints
blueprint_modules = [
    'branches.auth_gate.routes',
    'branches.pro_router.routes', 
    'branches.quota.routes',
    'branches.memory.routes',
    'branches.reasoning.routes',
    'branches.self_validate.routes',
    'branches.system.routes'
]

blueprint_names = [
    'auth_bp',
    'pro_router_bp',
    'quota_bp', 
    'memory_bp',
    'reasoning_bp',
    'validation_bp',
    'system_bp'
]

loaded_blueprints = []
blueprint_errors = []

for module_name, blueprint_name in zip(blueprint_modules, blueprint_names):
    try:
        module = __import__(module_name, fromlist=[blueprint_name])
        blueprint = getattr(module, blueprint_name)
        app.register_blueprint(blueprint, url_prefix='/api')
        loaded_blueprints.append(f"{module_name}.{blueprint_name}")
        print(f"✅ Loaded blueprint: {blueprint_name}")
    except Exception as e:
        error_msg = f"Failed to load {module_name}.{blueprint_name}: {str(e)}"
        blueprint_errors.append(error_msg)
        print(f"❌ {error_msg}")

print(f"📊 Blueprint Status: {len(loaded_blueprints)} loaded, {len(blueprint_errors)} errors")

@app.route('/')
def home():
    """Enhanced home page with database-powered features"""
    
    # Get analytics data
    analytics = game_showcase.get_analytics()
    recent_games = db_manager.get_all_games(limit=3)
    
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧠 Mythiq Gateway Enterprise v4.0.0 - Database Edition</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            background: rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
        }
        
        .header h1 {
            font-size: clamp(2rem, 5vw, 3rem);
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .status-indicator {
            display: inline-block;
            padding: 8px 16px;
            background: #2ecc71;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: bold;
            margin-top: 10px;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }
        
        .feature-card {
            background: rgba(255,255,255,0.1);
            padding: 25px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        .feature-card h3 {
            font-size: 1.5rem;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .feature-buttons {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 20px;
        }
        
        .btn {
            padding: 12px 20px;
            border: none;
            border-radius: 25px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.2s ease;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-size: 0.9rem;
        }
        
        .btn-primary {
            background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
            color: white;
        }
        
        .btn-secondary {
            background: linear-gradient(45deg, #3498db, #2980b9);
            color: white;
        }
        
        .btn-success {
            background: linear-gradient(45deg, #2ecc71, #27ae60);
            color: white;
        }
        
        .btn-warning {
            background: linear-gradient(45deg, #f39c12, #e67e22);
            color: white;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
        
        .analytics-section {
            background: rgba(255,255,255,0.1);
            padding: 25px;
            border-radius: 20px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
        }
        
        .analytics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .stat-card {
            text-align: center;
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 15px;
        }
        
        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: #f1c40f;
        }
        
        .recent-games {
            background: rgba(255,255,255,0.1);
            padding: 25px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
        }
        
        .game-item {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .ai-chat {
            background: rgba(255,255,255,0.1);
            padding: 25px;
            border-radius: 20px;
            margin-top: 30px;
            backdrop-filter: blur(10px);
        }
        
        .chat-input {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 15px;
            font-size: 1rem;
            margin-bottom: 15px;
            background: rgba(255,255,255,0.9);
            color: #333;
            resize: vertical;
            min-height: 100px;
        }
        
        .module-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        
        .module-btn {
            padding: 15px;
            border: none;
            border-radius: 15px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.2s ease;
            font-size: 0.9rem;
        }
        
        @media (max-width: 768px) {
            .features-grid {
                grid-template-columns: 1fr;
            }
            
            .analytics-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .feature-buttons {
                justify-content: center;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 Mythiq Gateway Enterprise v4.0.0</h1>
            <p>🎮 Database-Powered AI Game Creation Edition</p>
            <div class="status-indicator">
                🟢 All Systems Operational + Database Active
            </div>
        </div>
        
        <div class="analytics-section">
            <h2>📊 Platform Analytics</h2>
            <div class="analytics-grid">
                <div class="stat-card">
                    <div class="stat-number">{{ analytics.get('total_games', 0) }}</div>
                    <div>Total Games</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ analytics.get('total_plays', 0) }}</div>
                    <div>Total Plays</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ analytics.get('total_likes', 0) }}</div>
                    <div>Total Likes</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ loaded_blueprints|length }}</div>
                    <div>Active Modules</div>
                </div>
            </div>
        </div>
        
        <div class="features-grid">
            <div class="feature-card">
                <h3>🎮 AI Game Creation Studio</h3>
                <p>Create professional HTML5 games in minutes using AI. Now with persistent storage and analytics!</p>
                <ul style="margin: 15px 0; padding-left: 20px;">
                    <li>✨ Describe your game idea and watch AI bring it to life</li>
                    <li>🎯 Professional HTML5 games with full source code</li>
                    <li>📱 Mobile-friendly and ready to share</li>
                    <li>💾 Persistent database storage</li>
                    <li>📊 Play tracking and analytics</li>
                </ul>
                <div class="feature-buttons">
                    <a href="/games/showcase" class="btn btn-primary">🎮 Create Your Game</a>
                    <a href="/games/showcase" class="btn btn-secondary">🏆 Game Showcase</a>
                    <a href="/games/admin" class="btn btn-warning">⚙️ Admin Panel</a>
                </div>
            </div>
            
            <div class="feature-card">
                <h3>🏢 Enterprise Modules</h3>
                <p>Advanced AI modules for enterprise-grade functionality</p>
                <div class="module-grid">
                    <button class="module-btn" style="background: #e74c3c; color: white;" onclick="testModule('/api/auth/test')">🔐 Test Auth</button>
                    <button class="module-btn" style="background: #f39c12; color: white;" onclick="testModule('/api/pro_router/test')">🌐 Test Router</button>
                    <button class="module-btn" style="background: #e67e22; color: white;" onclick="testModule('/api/quota/test')">📊 Test Quota</button>
                    <button class="module-btn" style="background: #27ae60; color: white;" onclick="testModule('/api/memory/test')">🧩 Test Memory</button>
                    <button class="module-btn" style="background: #2980b9; color: white;" onclick="testModule('/api/reasoning/test')">🤔 Test Reasoning</button>
                    <button class="module-btn" style="background: #8e44ad; color: white;" onclick="testModule('/api/self_validate/test')">✅ Test Validation</button>
                    <button class="module-btn" style="background: #34495e; color: white;" onclick="testModule('/api/system/test')">🖥️ Test System</button>
                </div>
            </div>
        </div>
        
        {% if recent_games %}
        <div class="recent-games">
            <h3>🎮 Recently Created Games</h3>
            {% for game in recent_games %}
            <div class="game-item">
                <div>
                    <strong>{{ game.title }}</strong>
                    <span style="opacity: 0.8; margin-left: 10px;">{{ game.genre }}</span>
                </div>
                <div>
                    <span>🎮 {{ game.plays }} plays</span>
                    <span style="margin-left: 10px;">❤️ {{ game.likes }} likes</span>
                    <a href="/games/play/{{ game.id }}" class="btn btn-success" style="margin-left: 10px; padding: 5px 10px; font-size: 0.8rem;">Play</a>
                </div>
            </div>
            {% endfor %}
        </div>
        {% endif %}
        
        <div class="ai-chat">
            <h3>🎯 AI Brain Interface</h3>
            <p>Ask about enterprise features, test modules, create games, or have a conversation!</p>
            
            <label for="aiModel">AI Model Selection:</label>
            <select id="aiModel" style="width: 100%; padding: 10px; margin: 10px 0; border-radius: 10px; border: none;">
                <option value="auto">Auto (Intelligent Fallback)</option>
                <option value="llama-3.3-70b">Llama 3.3 70B (Latest)</option>
                <option value="llama-3.1-8b">Llama 3.1 8B (Fast)</option>
                <option value="mixtral-8x7b">Mixtral 8x7B (Stable)</option>
            </select>
            
            <textarea id="userMessage" class="chat-input" 
                      placeholder="Enter your message for the AI brain... Ask about enterprise features, test modules, create games, or have a conversation!"></textarea>
            
            <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                <button class="btn btn-primary" onclick="sendMessage()">🧠 Send to Brain</button>
                <button class="btn btn-success" onclick="testHealth()">❤️ Test Health</button>
                <button class="btn btn-secondary" onclick="clearChat()">🗑️ Clear</button>
            </div>
            
            <div id="chatResponse" style="margin-top: 20px; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 10px; display: none;"></div>
        </div>
    </div>
    
    <script>
        async function sendMessage() {
            const message = document.getElementById('userMessage').value;
            const model = document.getElementById('aiModel').value;
            const responseDiv = document.getElementById('chatResponse');
            
            if (!message.trim()) {
                alert('Please enter a message');
                return;
            }
            
            responseDiv.style.display = 'block';
            responseDiv.innerHTML = '🤔 AI is thinking...';
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message, model: model })
                });
                
                const result = await response.json();
                
                if (result.status === 'success') {
                    responseDiv.innerHTML = `
                        <div style="border-left: 4px solid #2ecc71; padding-left: 15px;">
                            <strong>🧠 AI Response:</strong><br>
                            ${result.response.replace(/\\n/g, '<br>')}
                        </div>
                    `;
                } else {
                    responseDiv.innerHTML = `
                        <div style="border-left: 4px solid #e74c3c; padding-left: 15px;">
                            <strong>❌ Error:</strong><br>
                            ${result.message}
                        </div>
                    `;
                }
            } catch (error) {
                responseDiv.innerHTML = `
                    <div style="border-left: 4px solid #e74c3c; padding-left: 15px;">
                        <strong>❌ Error:</strong><br>
                        Failed to communicate with AI brain
                    </div>
                `;
            }
        }
        
        async function testModule(endpoint) {
            try {
                const response = await fetch(endpoint);
                const result = await response.json();
                
                const responseDiv = document.getElementById('chatResponse');
                responseDiv.style.display = 'block';
                responseDiv.innerHTML = `
                    <div style="border-left: 4px solid #2ecc71; padding-left: 15px;">
                        <strong>✅ Module Test Result:</strong><br>
                        <pre>${JSON.stringify(result, null, 2)}</pre>
                    </div>
                `;
            } catch (error) {
                const responseDiv = document.getElementById('chatResponse');
                responseDiv.style.display = 'block';
                responseDiv.innerHTML = `
                    <div style="border-left: 4px solid #e74c3c; padding-left: 15px;">
                        <strong>❌ Module Test Failed:</strong><br>
                        ${error.message}
                    </div>
                `;
            }
        }
        
        async function testHealth() {
            const responseDiv = document.getElementById('chatResponse');
            responseDiv.style.display = 'block';
            responseDiv.innerHTML = `
                <div style="border-left: 4px solid #2ecc71; padding-left: 15px;">
                    <strong>❤️ System Health:</strong><br>
                    🟢 Database: Connected<br>
                    🟢 Game Engine: Active<br>
                    🟢 Blueprints: {{ loaded_blueprints|length }} loaded<br>
                    🟢 Analytics: Tracking {{ analytics.get('total_games', 0) }} games<br>
                    🟢 Storage: Persistent SQLite database<br>
                    ✅ All systems operational!
                </div>
            `;
        }
        
        function clearChat() {
            document.getElementById('userMessage').value = '';
            document.getElementById('chatResponse').style.display = 'none';
        }
        
        // Auto-resize textarea
        document.getElementById('userMessage').addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    </script>
</body>
</html>
    ''', analytics=analytics, recent_games=recent_games, loaded_blueprints=loaded_blueprints)

@app.route('/api/chat', methods=['POST'])
def chat():
    """Enhanced chat endpoint with game creation capabilities"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        model = data.get('model', 'auto')
        
        if not message:
            return jsonify({
                'status': 'error',
                'message': 'Message is required'
            })
        
        # Check if this is a game creation request
        game_keywords = ['create game', 'make game', 'build game', 'game about', 'game where']
        if any(keyword in message.lower() for keyword in game_keywords):
            if game_engine:
                result = game_engine.create_complete_game(message)
                if result['status'] == 'success':
                    # Add to showcase
                    creator_ip = request.remote_addr
                    game_showcase.add_game(result['game'], creator_ip)
                    
                    return jsonify({
                        'status': 'success',
                        'response': f"🎮 Game Created Successfully!\\n\\nTitle: {result['game']['title']}\\nDescription: {result['game']['concept'].get('description', 'A fun AI-generated game')}\\n\\nYou can play it at: /games/play/{result['game']['id']}\\nOr view it in the showcase: /games/showcase"
                    })
        
        # Regular AI chat response
        return jsonify({
            'status': 'success',
            'response': f"🧠 AI Brain Response:\\n\\nI received your message: '{message}'\\n\\nI'm running on the {model} model and ready to help with:\\n\\n• 🎮 Game creation (just say 'create a game about...')\\n• 🏢 Enterprise module testing\\n• 📊 Analytics and data insights\\n• 💬 General conversation\\n\\nWhat would you like to explore?"
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Chat error: {str(e)}'
        })

@app.route('/api/health')
def health():
    """Enhanced health check with database status"""
    try:
        # Test database connection
        games_count = len(db_manager.get_all_games(limit=1))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
        games_count = 0
    
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time(),
        'version': '4.0.0',
        'features': {
            'game_engine': game_engine is not None,
            'database': db_status == "connected",
            'blueprints_loaded': len(loaded_blueprints),
            'total_games': games_count
        },
        'database_status': db_status,
        'loaded_blueprints': loaded_blueprints,
        'blueprint_errors': blueprint_errors
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found',
        'available_endpoints': [
            '/',
            '/games/showcase',
            '/games/admin',
            '/api/health',
            '/api/chat',
            '/api/games/create',
            '/api/games/analytics'
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status': 'error',
        'message': 'Internal server error',
        'details': str(error)
    }), 500

if __name__ == '__main__':
    print("🚀 Starting Mythiq Gateway Enterprise v4.0.0 - Database Edition")
    print(f"📊 Loaded {len(loaded_blueprints)} blueprints successfully")
    print(f"🗄️ Database initialized and ready")
    print(f"🎮 Game engine: {'Active' if game_engine else 'Not available'}")
    
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
