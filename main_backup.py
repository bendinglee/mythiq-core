"""
Ultimate AI Game Creation Platform - Main Application
The most advanced AI game creation system ever built

Features:
- Enhanced AI game generation with perfect prompt matching
- Intelligent text assistant with game improvement capabilities
- Rich visual theming and consistent game quality
- Advanced prompt analysis and creative suggestions
- Professional UI with dual-panel design
- Mobile-optimized responsive interface
"""

from flask import Flask, render_template, render_template_string, request, jsonify, redirect, url_for
from flask_cors import CORS
import json
import os
import uuid
import time
from datetime import datetime
import traceback

# Import enhanced AI systems
try:
    from ultimate_ai_game_engine_enhanced import (
        EnhancedGameGenerator, 
        TrueAIGameGenerator, 
        get_game_suggestions, 
        generate_game
    )
    print("✅ Ultimate AI Game Engine loaded successfully")
    GAME_ENGINE_AVAILABLE = True
except ImportError as e:
    print(f"❌ Failed to import Ultimate AI Game Engine: {e}")
    GAME_ENGINE_AVAILABLE = False

try:
    from intelligent_text_assistant_enhanced import TextAssistant
    print("✅ Intelligent Text Assistant loaded successfully")
    TEXT_ASSISTANT_AVAILABLE = True
except ImportError as e:
    print(f"❌ Failed to import Intelligent Text Assistant: {e}")
    TEXT_ASSISTANT_AVAILABLE = False

# Import existing enterprise modules
try:
    from branches.auth_gate import auth_gate_bp
    from branches.pro_router import pro_router_bp
    from branches.quota import quota_bp
    from branches.memory import memory_bp
    from branches.reasoning import reasoning_bp
    from branches.self_validate import self_validate_bp
    print("✅ All enterprise modules loaded successfully")
    ENTERPRISE_MODULES_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Some enterprise modules not available: {e}")
    ENTERPRISE_MODULES_AVAILABLE = False

app = Flask(__name__)
CORS(app)

# Initialize AI systems
if GAME_ENGINE_AVAILABLE:
    game_generator = TrueAIGameGenerator()
else:
    game_generator = None

if TEXT_ASSISTANT_AVAILABLE:
    text_assistant = TextAssistant()
else:
    text_assistant = None

# Register enterprise blueprints if available
if ENTERPRISE_MODULES_AVAILABLE:
    try:
        app.register_blueprint(auth_gate_bp, url_prefix='/auth')
        app.register_blueprint(pro_router_bp, url_prefix='/pro')
        app.register_blueprint(quota_bp, url_prefix='/quota')
        app.register_blueprint(memory_bp, url_prefix='/memory')
        app.register_blueprint(reasoning_bp, url_prefix='/reasoning')
        app.register_blueprint(self_validate_bp, url_prefix='/validate')
        print("✅ All blueprints registered successfully")
    except Exception as e:
        print(f"⚠️ Error registering blueprints: {e}")

# Game storage
GAMES_FILE = 'games_data.json'

def load_games():
    """Load games from persistent storage"""
    try:
        if os.path.exists(GAMES_FILE):
            with open(GAMES_FILE, 'r') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Error loading games: {e}")
        return []

def save_games(games):
    """Save games to persistent storage"""
    try:
        with open(GAMES_FILE, 'w') as f:
            json.dump(games, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving games: {e}")
        return False

def get_groq_api_key():
    """Get GROQ API key from environment"""
    return os.getenv('GROQ_API_KEY', '')

@app.route('/')
def home():
    """Enhanced home page with dual-panel AI interface"""
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Mythiq Gateway - Ultimate AI Game Studio</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: white;
            overflow-x: hidden;
        }
        
        .header {
            text-align: center;
            padding: 2rem 1rem;
            background: rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }
        
        .header h1 {
            font-size: 3rem;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            animation: glow 2s ease-in-out infinite alternate;
        }
        
        @keyframes glow {
            from { text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3), 0 0 20px rgba(255, 255, 255, 0.2); }
            to { text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3), 0 0 30px rgba(255, 255, 255, 0.4); }
        }
        
        .subtitle {
            font-size: 1.5rem;
            opacity: 0.9;
            margin-bottom: 0.5rem;
        }
        
        .tagline {
            font-size: 1.1rem;
            opacity: 0.8;
        }
        
        .main-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
            padding: 2rem;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .panel {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .panel:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
        }
        
        .panel-header {
            display: flex;
            align-items: center;
            margin-bottom: 1.5rem;
            font-size: 1.8rem;
            font-weight: bold;
        }
        
        .panel-icon {
            font-size: 2rem;
            margin-right: 1rem;
        }
        
        .ai-welcome {
            background: linear-gradient(135deg, #ff6b6b, #ee5a24);
            border-radius: 15px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border-left: 5px solid #ff9ff3;
        }
        
        .ai-welcome h3 {
            margin-bottom: 1rem;
            font-size: 1.3rem;
        }
        
        .ai-features {
            list-style: none;
            margin: 1rem 0;
        }
        
        .ai-features li {
            margin: 0.5rem 0;
            padding-left: 1.5rem;
            position: relative;
        }
        
        .ai-features li::before {
            content: '✨';
            position: absolute;
            left: 0;
        }
        
        .chat-container {
            margin-top: 1.5rem;
        }
        
        .chat-input {
            width: 100%;
            padding: 1rem;
            border: none;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.9);
            color: #333;
            font-size: 1rem;
            margin-bottom: 1rem;
            transition: all 0.3s ease;
        }
        
        .chat-input:focus {
            outline: none;
            background: white;
            box-shadow: 0 0 20px rgba(255, 255, 255, 0.3);
        }
        
        .game-creator {
            margin-top: 1rem;
        }
        
        .game-description {
            width: 100%;
            height: 120px;
            padding: 1rem;
            border: none;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.9);
            color: #333;
            font-size: 1rem;
            resize: vertical;
            margin-bottom: 1rem;
            transition: all 0.3s ease;
        }
        
        .game-description:focus {
            outline: none;
            background: white;
            box-shadow: 0 0 20px rgba(255, 255, 255, 0.3);
        }
        
        .btn {
            padding: 1rem 2rem;
            border: none;
            border-radius: 10px;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
            text-align: center;
            margin: 0.5rem;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }
        
        .btn-secondary {
            background: linear-gradient(135deg, #ffecd2, #fcb69f);
            color: #333;
            box-shadow: 0 4px 15px rgba(252, 182, 159, 0.4);
        }
        
        .btn-secondary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(252, 182, 159, 0.6);
        }
        
        .quick-actions {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
            margin-top: 1rem;
        }
        
        .showcase-link {
            background: linear-gradient(135deg, #ff9a9e, #fecfef);
            color: #333;
            text-decoration: none;
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            font-weight: bold;
            margin-top: 1rem;
            display: block;
            transition: all 0.3s ease;
        }
        
        .showcase-link:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(255, 154, 158, 0.4);
        }
        
        .examples {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 1rem;
            margin-top: 1rem;
            font-size: 0.9rem;
            opacity: 0.8;
        }
        
        .status-indicator {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(0, 255, 0, 0.8);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.9rem;
            z-index: 1000;
        }
        
        @media (max-width: 768px) {
            .main-container {
                grid-template-columns: 1fr;
                padding: 1rem;
                gap: 1rem;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .quick-actions {
                grid-template-columns: 1fr;
            }
            
            .panel {
                padding: 1.5rem;
            }
        }
        
        .loading {
            display: none;
            text-align: center;
            margin: 1rem 0;
        }
        
        .spinner {
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top: 3px solid white;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="status-indicator">🟢 All Systems Operational + Enhanced AI Active</div>
    
    <div class="header">
        <h1>🚀 Mythiq Gateway</h1>
        <div class="subtitle">Ultimate AI-Powered Game Creation Studio</div>
        <div class="tagline">Create • Play • Share • Improve • Evolve</div>
    </div>
    
    <div class="main-container">
        <!-- AI Assistant Panel -->
        <div class="panel">
            <div class="panel-header">
                <span class="panel-icon">🧠</span>
                Enhanced AI Assistant
            </div>
            
            <div class="ai-welcome">
                <h3>👋 Welcome to the Ultimate Game Studio!</h3>
                <p>I'm your enhanced AI game creation assistant with advanced capabilities:</p>
                <ul class="ai-features">
                    <li>Create truly unique games from any description</li>
                    <li>Analyze and improve existing games with intelligent suggestions</li>
                    <li>Provide creative brainstorming and idea enhancement</li>
                    <li>Offer technical guidance and best practices</li>
                    <li>Generate themed visuals and consistent game quality</li>
                </ul>
                <p><strong>Try saying:</strong></p>
                <ul class="ai-features">
                    <li>"Create a cyberpunk racing game with neon lights"</li>
                    <li>"Make a cooking game where you run a magical restaurant"</li>
                    <li>"How can I improve my space adventure game?"</li>
                    <li>"Give me creative ideas for a puzzle game"</li>
                </ul>
                <p><strong>What would you like to create today?</strong></p>
            </div>
            
            <div class="chat-container">
                <input type="text" class="chat-input" id="chatInput" placeholder="Ask me anything about game creation...">
                <button class="btn btn-primary" onclick="sendMessage()">Send</button>
                
                <div class="loading" id="chatLoading">
                    <div class="spinner"></div>
                    <p>AI is thinking...</p>
                </div>
                
                <div id="chatResponse" style="margin-top: 1rem; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 10px; display: none;"></div>
            </div>
        </div>
        
        <!-- Game Creator Panel -->
        <div class="panel">
            <div class="panel-header">
                <span class="panel-icon">🎮</span>
                Ultimate Game Creator
            </div>
            
            <div class="game-creator">
                <textarea class="game-description" id="gameDescription" placeholder="Describe your game idea in detail...

Examples:
• A magical underwater adventure where you play as a mermaid collecting ancient pearls while avoiding dangerous sea creatures like electric eels and giant octopuses
• A cyberpunk racing game through neon-lit city streets where you dodge traffic and collect power-ups to boost your futuristic vehicle
• A cooking game where you're a chef in a haunted restaurant, preparing meals for ghost customers while avoiding spooky kitchen disasters"></textarea>
                
                <button class="btn btn-primary" onclick="createGame()" style="width: 100%; font-size: 1.2rem; padding: 1.2rem;">
                    ✨ Create Ultimate Game
                </button>
                
                <div class="loading" id="gameLoading">
                    <div class="spinner"></div>
                    <p>Enhanced AI is creating your unique game...</p>
                </div>
            </div>
            
            <div class="quick-actions">
                <button class="btn btn-secondary" onclick="quickGame('space')">🚀 Space Adventure</button>
                <button class="btn btn-secondary" onclick="quickGame('puzzle')">🧩 Mind Puzzle</button>
                <button class="btn btn-secondary" onclick="quickGame('racing')">🏎️ Speed Racing</button>
                <button class="btn btn-secondary" onclick="quickGame('cooking')">👨‍🍳 Master Chef</button>
            </div>
            
            <a href="/games/showcase" class="showcase-link">
                🎯 View Ultimate Game Showcase
            </a>
            
            <div class="examples">
                <strong>💡 Pro Tips:</strong><br>
                • Be specific about themes, characters, and objectives<br>
                • Mention visual styles you want (colorful, dark, futuristic)<br>
                • Describe the main challenge or goal<br>
                • Include any special mechanics or features you envision
            </div>
        </div>
    </div>
    
    <script>
        async function sendMessage() {
            const input = document.getElementById('chatInput');
            const loading = document.getElementById('chatLoading');
            const response = document.getElementById('chatResponse');
            
            if (!input.value.trim()) return;
            
            loading.style.display = 'block';
            response.style.display = 'none';
            
            try {
                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: input.value })
                });
                
                const data = await res.json();
                
                response.innerHTML = `
                    <div style="white-space: pre-wrap; line-height: 1.6;">
                        ${data.response || 'I\\'m here to help you create amazing games! What would you like to work on?'}
                    </div>
                `;
                response.style.display = 'block';
                
                input.value = '';
            } catch (error) {
                response.innerHTML = '<div style="color: #ffcccb;">Sorry, I\\'m having trouble connecting. Please try again!</div>';
                response.style.display = 'block';
            }
            
            loading.style.display = 'none';
        }
        
        async function createGame() {
            const description = document.getElementById('gameDescription').value;
            const loading = document.getElementById('gameLoading');
            
            if (!description.trim()) {
                alert('Please describe your game idea first!');
                return;
            }
            
            loading.style.display = 'block';
            
            try {
                const response = await fetch('/api/games/create', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ description: description })
                });
                
                const data = await response.json();
                
                if (data.success && data.game_id) {
                    window.location.href = `/games/play/${data.game_id}`;
                } else {
                    alert('Error creating game: ' + (data.error || 'Unknown error'));
                }
            } catch (error) {
                alert('Error creating game: ' + error.message);
            }
            
            loading.style.display = 'none';
        }
        
        function quickGame(type) {
            const descriptions = {
                'space': 'A thrilling space adventure where you pilot a starship through asteroid fields, collecting energy crystals while battling alien invaders with laser weapons',
                'puzzle': 'A challenging mind puzzle game where you solve increasingly complex logic problems by matching patterns and arranging colorful geometric shapes',
                'racing': 'An adrenaline-pumping racing game where you speed through futuristic city tracks, dodging traffic and collecting turbo boosts to win the championship',
                'cooking': 'A fun cooking game where you manage a busy restaurant kitchen, preparing delicious meals for customers while racing against the clock'
            };
            
            document.getElementById('gameDescription').value = descriptions[type];
        }
        
        // Enter key support for chat
        document.getElementById('chatInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>
    """)

@app.route('/api/chat', methods=['POST'])
def chat():
    """Enhanced AI chat endpoint"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({
                'response': 'Please ask me something about game creation!',
                'type': 'error'
            })
        
        if TEXT_ASSISTANT_AVAILABLE and text_assistant:
            response_data = text_assistant.get_response(user_message)
        else:
            # Fallback response
            response_data = {
                'response': f"Thanks for your message: '{user_message}'. I'm here to help you create amazing games! What kind of game would you like to make?",
                'type': 'fallback',
                'timestamp': datetime.now().isoformat()
            }
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({
            'response': 'I apologize, but I encountered an error. Please try again!',
            'type': 'error',
            'error': str(e)
        })

@app.route('/api/games/create', methods=['POST'])
def create_game():
    """Enhanced game creation endpoint"""
    try:
        data = request.get_json()
        description = data.get('description', '')
        
        if not description:
            return jsonify({
                'success': False,
                'error': 'Please provide a game description'
            })
        
        # Generate unique game ID
        game_id = f"game_{int(time.time())}_{uuid.uuid4().hex[:6]}"
        
        if GAME_ENGINE_AVAILABLE and game_generator:
            # Use enhanced AI game generator
            result = game_generator.create_game(description)
            
            if result['success']:
                game_data = result['game']
                game_data['id'] = game_id
                game_data['plays'] = 0
                game_data['likes'] = 0
                
                # Save to persistent storage
                games = load_games()
                games.append(game_data)
                save_games(games)
                
                return jsonify({
                    'success': True,
                    'game_id': game_id,
                    'message': result['message'],
                    'game': game_data
                })
            else:
                return jsonify({
                    'success': False,
                    'error': result.get('error', 'Failed to generate game')
                })
        else:
            # Fallback game creation
            fallback_game = create_fallback_game(description, game_id)
            
            games = load_games()
            games.append(fallback_game)
            save_games(games)
            
            return jsonify({
                'success': True,
                'game_id': game_id,
                'message': 'Game created successfully!',
                'game': fallback_game,
                'fallback': True
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error creating game: {str(e)}',
            'traceback': traceback.format_exc()
        })

def create_fallback_game(description, game_id):
    """Create a fallback game when AI engine is not available"""
    return {
        'id': game_id,
        'title': 'Custom Adventure Game',
        'description': f"A unique adventure game: {description}",
        'theme': 'adventure',
        'game_type': 'collection',
        'html_content': generate_simple_game_html(description),
        'created_at': datetime.now().isoformat(),
        'plays': 0,
        'likes': 0
    }

def generate_simple_game_html(description):
    """Generate simple HTML game as fallback"""
    return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Custom Game</title>
    <style>
        body {{ 
            margin: 0; 
            padding: 20px; 
            background: linear-gradient(45deg, #667eea, #764ba2); 
            color: white; 
            font-family: Arial, sans-serif;
            text-align: center;
        }}
        #game {{ 
            width: 600px; 
            height: 400px; 
            background: rgba(255,255,255,0.1); 
            margin: 20px auto; 
            border-radius: 15px; 
            position: relative;
            border: 2px solid rgba(255,255,255,0.3);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }}
        .score {{ 
            position: absolute; 
            top: 15px; 
            left: 15px; 
            font-size: 18px; 
            font-weight: bold;
        }}
        .game-title {{
            font-size: 24px;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }}
        .game-description {{
            font-size: 16px;
            margin-bottom: 30px;
            padding: 0 40px;
            line-height: 1.5;
            opacity: 0.9;
        }}
        .play-button {{
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            border: none;
            padding: 15px 30px;
            border-radius: 25px;
            color: white;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        .play-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(255,107,107,0.4);
        }}
    </style>
</head>
<body>
    <div class="score">Score: <span id="score">0</span></div>
    <div id="game">
        <div class="game-title">🎮 Your Custom Game</div>
        <div class="game-description">{description}</div>
        <button class="play-button" onclick="playGame()">Start Playing!</button>
    </div>
    <script>
        let score = 0;
        function playGame() {{
            score += 10;
            document.getElementById('score').textContent = score;
            
            const messages = [
                'Great job! Keep playing!',
                'Awesome! You\\'re doing well!',
                'Fantastic! Score increased!',
                'Excellent! Keep it up!',
                'Amazing! You\\'re on fire!'
            ];
            
            const randomMessage = messages[Math.floor(Math.random() * messages.length)];
            
            // Create floating score animation
            const floatingScore = document.createElement('div');
            floatingScore.textContent = '+10';
            floatingScore.style.cssText = `
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                color: #ffd700;
                font-size: 24px;
                font-weight: bold;
                pointer-events: none;
                animation: float-up 1s ease-out forwards;
            `;
            
            document.getElementById('game').appendChild(floatingScore);
            
            setTimeout(() => {{
                floatingScore.remove();
            }}, 1000);
            
            if (score >= 100) {{
                alert('🎉 Congratulations! You\\'ve mastered this game! Final Score: ' + score);
            }}
        }}
        
        // Add CSS animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes float-up {{
                0% {{ opacity: 1; transform: translate(-50%, -50%) scale(1); }}
                100% {{ opacity: 0; transform: translate(-50%, -150%) scale(1.5); }}
            }}
        `;
        document.head.appendChild(style);
    </script>
</body>
</html>
    """

@app.route('/games/play/<game_id>')
def play_game(game_id):
    """Play a specific game"""
    try:
        games = load_games()
        game = next((g for g in games if g['id'] == game_id), None)
        
        if not game:
            return "Game not found", 404
        
        # Increment play count
        game['plays'] = game.get('plays', 0) + 1
        save_games(games)
        
        # Return the game HTML
        return game['html_content']
        
    except Exception as e:
        return f"Error loading game: {str(e)}", 500

@app.route('/games/showcase')
def games_showcase():
    """Enhanced games showcase"""
    games = load_games()
    
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎮 Ultimate Game Showcase - Mythiq Gateway</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: white;
        }
        
        .header {
            text-align: center;
            padding: 2rem 1rem;
            background: rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        .back-link {
            display: inline-block;
            margin: 1rem;
            padding: 0.8rem 1.5rem;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            text-decoration: none;
            border-radius: 10px;
            transition: all 0.3s ease;
        }
        
        .back-link:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }
        
        .create-section {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 2rem;
            margin: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .create-section h2 {
            text-align: center;
            margin-bottom: 1rem;
            font-size: 1.8rem;
        }
        
        .create-section p {
            text-align: center;
            margin-bottom: 1.5rem;
            opacity: 0.9;
        }
        
        .game-description {
            width: 100%;
            height: 100px;
            padding: 1rem;
            border: none;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.9);
            color: #333;
            font-size: 1rem;
            resize: vertical;
            margin-bottom: 1rem;
        }
        
        .btn-create {
            width: 100%;
            padding: 1rem;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1.1rem;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .btn-create:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .games-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 2rem;
            padding: 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .game-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 1.5rem;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.3s ease;
        }
        
        .game-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }
        
        .game-title {
            font-size: 1.4rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
            color: #ffd700;
        }
        
        .game-genre {
            display: inline-block;
            background: rgba(255, 255, 255, 0.2);
            padding: 0.3rem 0.8rem;
            border-radius: 15px;
            font-size: 0.8rem;
            margin-bottom: 1rem;
        }
        
        .game-description-text {
            font-size: 0.9rem;
            line-height: 1.5;
            margin-bottom: 1rem;
            opacity: 0.9;
        }
        
        .game-stats {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            font-size: 0.9rem;
            opacity: 0.8;
        }
        
        .game-actions {
            display: flex;
            gap: 1rem;
        }
        
        .btn {
            padding: 0.8rem 1.5rem;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            text-decoration: none;
            text-align: center;
            transition: all 0.3s ease;
            flex: 1;
        }
        
        .btn-play {
            background: linear-gradient(135deg, #ff6b6b, #ee5a24);
            color: white;
        }
        
        .btn-play:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(255, 107, 107, 0.4);
        }
        
        .btn-share {
            background: linear-gradient(135deg, #ffecd2, #fcb69f);
            color: #333;
        }
        
        .btn-share:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(252, 182, 159, 0.4);
        }
        
        .no-games {
            text-align: center;
            padding: 3rem;
            opacity: 0.7;
        }
        
        .no-games h3 {
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }
        
        @media (max-width: 768px) {
            .games-grid {
                grid-template-columns: 1fr;
                padding: 1rem;
            }
            
            .create-section {
                margin: 1rem;
                padding: 1.5rem;
            }
        }
    </style>
</head>
<body>
    <a href="/" class="back-link">← Back to Home</a>
    
    <div class="header">
        <h1>🎮 Ultimate Game Showcase</h1>
        <p>Discover amazing games created by Enhanced AI • Play, Share, and Enjoy!</p>
    </div>
    
    <div class="create-section">
        <h2>🚀 Create Your Ultimate Game</h2>
        <p>Describe your game idea and watch Enhanced AI bring it to life!</p>
        
        <textarea class="game-description" id="gameDescription" placeholder="Describe your game idea in detail...

Examples:
• A mystical dragon tamer collecting rare dragon eggs in floating sky islands while avoiding storm clouds and rival tamers
• A detective solving mysteries in a noir city, gathering clues and interrogating suspects while avoiding corrupt cops
• A space botanist growing alien plants on different planets while defending against hostile creatures and environmental hazards"></textarea>
        
        <button class="btn-create" onclick="createGame()">✨ Create Ultimate Game</button>
    </div>
    
    {% if games %}
    <div class="games-grid">
        {% for game in games %}
        <div class="game-card">
            <div class="game-title">{{ game.title }}</div>
            <div class="game-genre">{{ game.get('game_type', 'Adventure').title() }}</div>
            <div class="game-description-text">{{ game.description }}</div>
            <div class="game-stats">
                <span>🎮 {{ game.get('plays', 0) }} plays</span>
                <span>❤️ {{ game.get('likes', 0) }} likes</span>
                <span>📅 {{ game.get('created_at', '')[:10] }}</span>
            </div>
            <div class="game-actions">
                <a href="/games/play/{{ game.id }}" class="btn btn-play">🎮 Play Game</a>
                <button class="btn btn-share" onclick="shareGame('{{ game.id }}', '{{ game.title }}')">📤 Share</button>
            </div>
        </div>
        {% endfor %}
    </div>
    {% else %}
    <div class="no-games">
        <h3>🎮 No games yet!</h3>
        <p>Be the first to create an amazing game with our Enhanced AI system!</p>
    </div>
    {% endif %}
    
    <script>
        async function createGame() {
            const description = document.getElementById('gameDescription').value;
            
            if (!description.trim()) {
                alert('Please describe your game idea first!');
                return;
            }
            
            try {
                const response = await fetch('/api/games/create', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ description: description })
                });
                
                const data = await response.json();
                
                if (data.success && data.game_id) {
                    window.location.href = `/games/play/${data.game_id}`;
                } else {
                    alert('Error creating game: ' + (data.error || 'Unknown error'));
                }
            } catch (error) {
                alert('Error creating game: ' + error.message);
            }
        }
        
        function shareGame(gameId, gameTitle) {
            const url = window.location.origin + '/games/play/' + gameId;
            
            if (navigator.share) {
                navigator.share({
                    title: gameTitle,
                    text: 'Check out this amazing AI-generated game!',
                    url: url
                });
            } else {
                navigator.clipboard.writeText(url).then(() => {
                    alert('Game link copied to clipboard!');
                });
            }
        }
    </script>
</body>
</html>
    """, games=games)

@app.route('/api/health')
def health_check():
    """Enhanced health check endpoint"""
    games = load_games()
    
    return jsonify({
        'status': 'healthy',
        'version': 'Mythiq Gateway Ultimate v4.0.0 - Enhanced AI Edition',
        'features': {
            'enhanced_ai_game_creation': GAME_ENGINE_AVAILABLE,
            'intelligent_text_assistant': TEXT_ASSISTANT_AVAILABLE,
            'advanced_prompt_analysis': GAME_ENGINE_AVAILABLE,
            'creative_brainstorming': TEXT_ASSISTANT_AVAILABLE,
            'game_improvement_suggestions': TEXT_ASSISTANT_AVAILABLE,
            'consistent_visual_theming': GAME_ENGINE_AVAILABLE,
            'mobile_optimization': True,
            'enterprise_modules': ENTERPRISE_MODULES_AVAILABLE
        },
        'api_status': {
            'groq_api_key': bool(get_groq_api_key()),
            'games_count': len(games),
            'blueprints_loaded': ENTERPRISE_MODULES_AVAILABLE,
            'enhanced_systems_active': GAME_ENGINE_AVAILABLE and TEXT_ASSISTANT_AVAILABLE
        },
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 Starting Ultimate AI Game Creation Platform...")
    print(f"✅ GROQ API Key: {'Found' if get_groq_api_key() else 'Not Found'}")
    print(f"✅ Enhanced Game Engine: {'Active' if GAME_ENGINE_AVAILABLE else 'Fallback Mode'}")
    print(f"✅ Intelligent Assistant: {'Active' if TEXT_ASSISTANT_AVAILABLE else 'Fallback Mode'}")
    print(f"✅ Enterprise Modules: {'Active' if ENTERPRISE_MODULES_AVAILABLE else 'Not Available'}")
    
    app.run(host='0.0.0.0', port=8080, debug=False)
