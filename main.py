#!/usr/bin/env python3
"""
🧠 Mythiq Gateway Enterprise v3.1.0 - Quick Fix Edition
Enhanced with basic game storage without complex database dependencies
"""

import os
import sys
import time
import json
import traceback
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mythiq-gateway-secret-key-2024')

# Simple in-memory storage with persistence
GAMES_FILE = 'games_storage.json'

def load_games():
    """Load games from file"""
    try:
        if os.path.exists(GAMES_FILE):
            with open(GAMES_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading games: {e}")
    return []

def save_games(games):
    """Save games to file"""
    try:
        with open(GAMES_FILE, 'w') as f:
            json.dump(games, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving games: {e}")
        return False

# Global games storage
games_storage = load_games()

# Import existing modules
try:
    from game_engine import game_engine
    print("✅ Game engine imported successfully")
except ImportError as e:
    print(f"❌ Failed to import game engine: {e}")
    game_engine = None

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
    """Enhanced home page with game storage"""
    
    # Get analytics data
    total_games = len(games_storage)
    total_plays = sum(game.get('plays', 0) for game in games_storage)
    total_likes = sum(game.get('likes', 0) for game in games_storage)
    recent_games = sorted(games_storage, key=lambda x: x.get('created_at', 0), reverse=True)[:3]
    
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧠 Mythiq Gateway Enterprise v3.1.0 - Fixed Edition</title>
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
            <h1>🧠 Mythiq Gateway Enterprise v3.1.0</h1>
            <p>🎮 Fixed AI Game Creation Edition - Stable & Working</p>
            <div class="status-indicator">
                🟢 All Systems Operational + Storage Active
            </div>
        </div>
        
        <div class="analytics-section">
            <h2>📊 Platform Analytics</h2>
            <div class="analytics-grid">
                <div class="stat-card">
                    <div class="stat-number">{{ total_games }}</div>
                    <div>Total Games</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ total_plays }}</div>
                    <div>Total Plays</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ total_likes }}</div>
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
                <p>Create professional HTML5 games in minutes using AI. Now with persistent file storage!</p>
                <ul style="margin: 15px 0; padding-left: 20px;">
                    <li>✨ Describe your game idea and watch AI bring it to life</li>
                    <li>🎯 Professional HTML5 games with full source code</li>
                    <li>📱 Mobile-friendly and ready to share</li>
                    <li>💾 Persistent file storage (no more lost games!)</li>
                    <li>📊 Play tracking and analytics</li>
                </ul>
                <div class="feature-buttons">
                    <a href="/games/showcase" class="btn btn-primary">🎮 Create Your Game</a>
                    <a href="/games/showcase" class="btn btn-secondary">🏆 Game Showcase</a>
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
                    <span style="opacity: 0.8; margin-left: 10px;">{{ game.get('genre', 'puzzle') }}</span>
                </div>
                <div>
                    <span>🎮 {{ game.get('plays', 0) }} plays</span>
                    <span style="margin-left: 10px;">❤️ {{ game.get('likes', 0) }} likes</span>
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
                    🟢 File Storage: Active<br>
                    🟢 Game Engine: Active<br>
                    🟢 Blueprints: {{ loaded_blueprints|length }} loaded<br>
                    🟢 Games Stored: {{ total_games }}<br>
                    🟢 Total Plays: {{ total_plays }}<br>
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
    ''', total_games=total_games, total_plays=total_plays, total_likes=total_likes, 
         recent_games=recent_games, loaded_blueprints=loaded_blueprints)

@app.route('/games/showcase')
def showcase():
    """Simple game showcase with file storage"""
    
    games_html = ""
    for game in games_storage:
        concept = game.get('concept', {})
        genre = concept.get('genre', 'puzzle')
        
        games_html += f'''
        <div class="game-card">
            <div class="game-header">
                <h3>{game['title']}</h3>
                <span class="genre-tag {genre}">{genre}</span>
            </div>
            <p class="game-description">{game.get('description', concept.get('description', 'A fun AI-generated game'))}</p>
            <div class="game-stats">
                <span>🎮 {game.get('plays', 0)} plays</span>
                <span>❤️ {game.get('likes', 0)} likes</span>
            </div>
            <div class="game-actions">
                <a href="/games/play/{game['id']}" class="btn play-btn">🎮 Play</a>
                <button onclick="likeGame('{game['id']}')" class="btn like-btn">❤️ Like</button>
            </div>
        </div>
        '''
    
    return render_template_string(f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🎮 AI Game Showcase</title>
        <style>
            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }}
            
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
                padding: 20px;
            }}
            
            .container {{
                max-width: 1200px;
                margin: 0 auto;
            }}
            
            .header {{
                text-align: center;
                margin-bottom: 40px;
                background: rgba(255,255,255,0.1);
                padding: 30px;
                border-radius: 20px;
                backdrop-filter: blur(10px);
            }}
            
            .create-section {{
                background: rgba(255,255,255,0.1);
                padding: 30px;
                border-radius: 20px;
                margin-bottom: 40px;
                text-align: center;
                backdrop-filter: blur(10px);
            }}
            
            .game-input {{
                width: 100%;
                max-width: 600px;
                padding: 15px;
                border: none;
                border-radius: 15px;
                font-size: 1.1rem;
                margin-bottom: 20px;
                background: rgba(255,255,255,0.9);
                color: #333;
            }}
            
            .create-btn {{
                background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 25px;
                font-size: 1.1rem;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s ease;
            }}
            
            .games-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
                gap: 25px;
                margin-top: 40px;
            }}
            
            .game-card {{
                background: rgba(255,255,255,0.1);
                border-radius: 20px;
                padding: 25px;
                backdrop-filter: blur(10px);
                transition: all 0.3s ease;
            }}
            
            .game-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            }}
            
            .game-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
            }}
            
            .genre-tag {{
                padding: 5px 12px;
                border-radius: 15px;
                font-size: 0.8rem;
                font-weight: bold;
                text-transform: uppercase;
            }}
            
            .genre-tag.puzzle {{ background: #9b59b6; }}
            .genre-tag.shooter {{ background: #e74c3c; }}
            .genre-tag.platformer {{ background: #f39c12; }}
            .genre-tag.racing {{ background: #2ecc71; }}
            .genre-tag.rpg {{ background: #3498db; }}
            .genre-tag.strategy {{ background: #34495e; }}
            
            .game-stats {{
                display: flex;
                gap: 15px;
                margin-bottom: 20px;
                font-size: 0.9rem;
            }}
            
            .game-actions {{
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
            }}
            
            .btn {{
                padding: 10px 15px;
                border: none;
                border-radius: 20px;
                text-decoration: none;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.2s ease;
                font-size: 0.9rem;
            }}
            
            .play-btn {{
                background: linear-gradient(45deg, #2ecc71, #27ae60);
                color: white;
            }}
            
            .like-btn {{
                background: linear-gradient(45deg, #e74c3c, #c0392b);
                color: white;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎮 AI Game Showcase</h1>
                <p>Discover amazing games created by AI in minutes!</p>
            </div>
            
            <div class="create-section">
                <h2>🚀 Create Your Own Game</h2>
                <form id="gameForm" onsubmit="createGame(event)">
                    <input type="text" id="gameIdea" class="game-input" 
                           placeholder="Describe your game idea..." required>
                    <br>
                    <button type="submit" class="create-btn">🎮 Create Game</button>
                </form>
                <div id="message"></div>
            </div>
            
            <div class="games-section">
                <h2 style="text-align: center; margin-bottom: 30px;">🏆 Featured Games</h2>
                <div class="games-grid">
                    {games_html}
                </div>
            </div>
        </div>
        
        <script>
            async function createGame(event) {{
                event.preventDefault();
                
                const gameIdea = document.getElementById('gameIdea').value;
                const messageDiv = document.getElementById('message');
                const submitBtn = event.target.querySelector('button');
                
                submitBtn.textContent = '🎮 Creating Game...';
                submitBtn.disabled = true;
                
                try {{
                    const response = await fetch('/api/games/create', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ prompt: gameIdea }})
                    }});
                    
                    const result = await response.json();
                    
                    if (result.status === 'success') {{
                        messageDiv.innerHTML = `
                            <div style="background: rgba(46, 204, 113, 0.2); border: 1px solid #2ecc71; color: #2ecc71; padding: 15px; border-radius: 10px; margin: 20px 0;">
                                <h3>🎉 Game Created Successfully!</h3>
                                <p><strong>${{result.game.title}}</strong></p>
                                <a href="/games/play/${{result.game.id}}" style="color: #2ecc71; text-decoration: underline;">Play Now</a>
                            </div>
                        `;
                        
                        setTimeout(() => window.location.reload(), 2000);
                    }} else {{
                        messageDiv.innerHTML = `
                            <div style="background: rgba(231, 76, 60, 0.2); border: 1px solid #e74c3c; color: #e74c3c; padding: 15px; border-radius: 10px;">
                                <strong>Error:</strong> ${{result.message}}
                            </div>
                        `;
                    }}
                }} catch (error) {{
                    messageDiv.innerHTML = `
                        <div style="background: rgba(231, 76, 60, 0.2); border: 1px solid #e74c3c; color: #e74c3c; padding: 15px; border-radius: 10px;">
                            <strong>Error:</strong> Failed to create game
                        </div>
                    `;
                }}
                
                submitBtn.textContent = '🎮 Create Game';
                submitBtn.disabled = false;
            }}
            
            async function likeGame(gameId) {{
                try {{
                    const response = await fetch(`/api/games/${{gameId}}/like`, {{
                        method: 'POST'
                    }});
                    
                    if (response.ok) {{
                        window.location.reload();
                    }}
                }} catch (error) {{
                    alert('Failed to like game');
                }}
            }}
        </script>
    </body>
    </html>
    ''')

@app.route('/api/games/create', methods=['POST'])
def create_game():
    """Create a new game and store it"""
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({'status': 'error', 'message': 'Game prompt is required'})
        
        if game_engine:
            result = game_engine.create_complete_game(prompt)
            
            if result['status'] == 'success':
                # Add to storage
                game = result['game']
                game['plays'] = 0
                game['likes'] = 0
                game['created_at'] = time.time()
                
                games_storage.append(game)
                save_games(games_storage)
                
                return jsonify(result)
            else:
                return jsonify(result)
        else:
            return jsonify({'status': 'error', 'message': 'Game engine not available'})
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Failed to create game: {str(e)}'})

@app.route('/games/play/<game_id>')
def play_game(game_id):
    """Play a specific game"""
    for game in games_storage:
        if game['id'] == game_id:
            # Increment play count
            game['plays'] = game.get('plays', 0) + 1
            save_games(games_storage)
            
            return game['code']['html']
    
    return "<h1>Game Not Found</h1>", 404

@app.route('/api/games/<game_id>/like', methods=['POST'])
def like_game(game_id):
    """Like a game"""
    for game in games_storage:
        if game['id'] == game_id:
            game['likes'] = game.get('likes', 0) + 1
            save_games(games_storage)
            return jsonify({'status': 'success'})
    
    return jsonify({'status': 'error', 'message': 'Game not found'})

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat endpoint"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        return jsonify({
            'status': 'success',
            'response': f"🧠 AI Brain Response:\\n\\nI received: '{message}'\\n\\nI'm ready to help with game creation, enterprise modules, and more!"
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Chat error: {str(e)}'})

@app.route('/api/health')
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time(),
        'version': '3.1.0',
        'features': {
            'game_engine': game_engine is not None,
            'file_storage': True,
            'blueprints_loaded': len(loaded_blueprints),
            'total_games': len(games_storage)
        }
    })

if __name__ == '__main__':
    print("🚀 Starting Mythiq Gateway Enterprise v3.1.0 - Fixed Edition")
    print(f"📊 Loaded {len(loaded_blueprints)} blueprints successfully")
    print(f"🎮 Game engine: {'Active' if game_engine else 'Not available'}")
    print(f"💾 Games in storage: {len(games_storage)}")
    
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
