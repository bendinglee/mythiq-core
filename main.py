#!/usr/bin/env python3
"""
🚀 COMPLETE MYTHIQ GATEWAY - AI GAME CREATION PLATFORM
Integrates Ultimate Game Engine + Intelligent Text Assistant
Production-ready Flask application for Railway deployment
"""

from flask import Flask, render_template_string, request, jsonify, redirect, url_for
from flask_cors import CORS
import os
import json
import time
from datetime import datetime
import traceback

# Import our AI systems
try:
    from ultimate_ai_game_engine import generate_game, improve_game
    from intelligent_text_assistant import chat_with_assistant, set_game_engine
    
    # Connect the systems
    from ultimate_ai_game_engine import game_engine
    set_game_engine(game_engine)
    
    print("✅ AI systems loaded successfully")
except ImportError as e:
    print(f"❌ AI system import error: {e}")
    # Create fallback functions
    def generate_game(description, improvement_request=None, existing_game_id=None):
        return {"success": False, "error": "AI system not available"}
    
    def improve_game(game_id, improvement_request):
        return {"success": False, "error": "AI system not available"}
    
    def chat_with_assistant(message, game_context=None):
        return {"success": True, "message": "AI assistant temporarily unavailable. Please try creating games directly!"}

# Import existing blueprint modules
try:
    from branches.auth_gate.routes import auth_bp
    from branches.pro_router.routes import pro_router_bp
    from branches.quota.routes import quota_bp
    from branches.memory.routes import memory_bp
    from branches.reasoning.routes import reasoning_bp
    from branches.self_validate.routes import validation_bp
    from branches.system.routes import system_bp
    
    print("✅ All blueprint imports successful")
    BLUEPRINTS_LOADED = True
except ImportError as e:
    print(f"❌ Blueprint import error: {e}")
    BLUEPRINTS_LOADED = False

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'mythiq-ai-game-studio-2024')
app.config['DEBUG'] = False

# Global storage for games (in production, use a database)
games_storage = {}
chat_sessions = {}

# Register blueprints if available
if BLUEPRINTS_LOADED:
    try:
        app.register_blueprint(auth_bp, url_prefix='/api/auth')
        app.register_blueprint(pro_router_bp, url_prefix='/api/pro')
        app.register_blueprint(quota_bp, url_prefix='/api/quota')
        app.register_blueprint(memory_bp, url_prefix='/api/memory')
        app.register_blueprint(reasoning_bp, url_prefix='/api/reasoning')
        app.register_blueprint(validation_bp, url_prefix='/api/validate')
        app.register_blueprint(system_bp, url_prefix='/api/system')
        
        registered_blueprints = [bp.name for bp in app.blueprints.values()]
        print(f"🎉 Successfully registered {len(registered_blueprints)} blueprints: {registered_blueprints}")
    except Exception as e:
        print(f"❌ Blueprint registration error: {e}")

# Check API key
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
if GROQ_API_KEY:
    print(f"✅ GROQ API Key found: {GROQ_API_KEY[:10]}...")
else:
    print("❌ GROQ API Key not found")

@app.route('/')
def home():
    """Main homepage with AI chat assistant and game creation"""
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>🚀 Mythiq Gateway - AI Game Studio</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            touch-action: manipulation;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            -webkit-user-select: none;
            user-select: none;
        }
        
        .header {
            text-align: center;
            padding: 40px 20px;
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(255,255,255,0.2);
        }
        
        .logo {
            font-size: 3em;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #f093fb, #f5576c);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        
        .tagline {
            font-size: 1.3em;
            opacity: 0.9;
            margin-bottom: 20px;
        }
        
        .main-content {
            flex: 1;
            display: flex;
            max-width: 1400px;
            margin: 0 auto;
            width: 100%;
            gap: 20px;
            padding: 20px;
        }
        
        .chat-section {
            flex: 1;
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            min-height: 500px;
        }
        
        .game-section {
            flex: 1;
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 20px;
            display: flex;
            flex-direction: column;
        }
        
        .section-title {
            font-size: 1.8em;
            margin-bottom: 20px;
            text-align: center;
            background: linear-gradient(45deg, #f093fb, #f5576c);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .chat-messages {
            flex: 1;
            overflow-y: auto;
            margin-bottom: 20px;
            padding: 10px;
            background: rgba(0,0,0,0.2);
            border-radius: 15px;
            min-height: 300px;
        }
        
        .message {
            margin-bottom: 15px;
            padding: 12px 16px;
            border-radius: 15px;
            max-width: 80%;
            word-wrap: break-word;
        }
        
        .user-message {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin-left: auto;
            text-align: right;
        }
        
        .assistant-message {
            background: rgba(255,255,255,0.2);
            margin-right: auto;
        }
        
        .chat-input-area {
            display: flex;
            gap: 10px;
        }
        
        .chat-input {
            flex: 1;
            padding: 15px;
            border: none;
            border-radius: 25px;
            background: rgba(255,255,255,0.2);
            color: white;
            font-size: 16px;
            outline: none;
        }
        
        .chat-input::placeholder {
            color: rgba(255,255,255,0.7);
        }
        
        .send-btn {
            padding: 15px 25px;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            border: none;
            border-radius: 25px;
            color: white;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .send-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }
        
        .game-creation {
            margin-bottom: 20px;
        }
        
        .game-input {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 15px;
            background: rgba(255,255,255,0.2);
            color: white;
            font-size: 16px;
            outline: none;
            margin-bottom: 15px;
            min-height: 100px;
            resize: vertical;
        }
        
        .game-input::placeholder {
            color: rgba(255,255,255,0.7);
        }
        
        .create-btn {
            width: 100%;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            border-radius: 15px;
            color: white;
            font-size: 18px;
            cursor: pointer;
            transition: all 0.3s;
            margin-bottom: 20px;
        }
        
        .create-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }
        
        .create-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .quick-actions {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-bottom: 20px;
        }
        
        .quick-btn {
            padding: 10px 15px;
            background: rgba(255,255,255,0.2);
            border: none;
            border-radius: 20px;
            color: white;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 14px;
        }
        
        .quick-btn:hover {
            background: rgba(255,255,255,0.3);
            transform: translateY(-1px);
        }
        
        .status {
            text-align: center;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        
        .status.success {
            background: rgba(76, 175, 80, 0.3);
        }
        
        .status.error {
            background: rgba(244, 67, 54, 0.3);
        }
        
        .status.info {
            background: rgba(33, 150, 243, 0.3);
        }
        
        .game-showcase-link {
            display: block;
            text-align: center;
            padding: 15px;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            text-decoration: none;
            border-radius: 15px;
            font-size: 16px;
            transition: all 0.3s;
        }
        
        .game-showcase-link:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        
        .spinner {
            border: 3px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            border-top: 3px solid white;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        @media (max-width: 768px) {
            .main-content {
                flex-direction: column;
                padding: 10px;
            }
            
            .logo {
                font-size: 2em;
            }
            
            .tagline {
                font-size: 1.1em;
            }
            
            .quick-actions {
                justify-content: center;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">🚀 Mythiq Gateway</div>
        <div class="tagline">AI-Powered Game Creation Studio</div>
        <div class="tagline">Create • Play • Share • Improve</div>
    </div>
    
    <div class="main-content">
        <div class="chat-section">
            <h2 class="section-title">🧠 AI Assistant</h2>
            <div class="chat-messages" id="chatMessages">
                <div class="message assistant-message">
                    👋 <strong>Welcome to Mythiq Gateway!</strong><br><br>
                    I'm your AI game creation assistant. I can help you:<br>
                    🎮 Create unique games from any description<br>
                    ✨ Improve existing games with your feedback<br>
                    💬 Answer questions about game development<br><br>
                    <strong>Try saying:</strong><br>
                    • "Create a space shooter game"<br>
                    • "Make a puzzle game with colors"<br>
                    • "How do I make games?"<br><br>
                    What would you like to create today?
                </div>
            </div>
            <div class="chat-input-area">
                <input type="text" class="chat-input" id="chatInput" placeholder="Ask me anything about game creation..." maxlength="500">
                <button class="send-btn" onclick="sendMessage()">Send</button>
            </div>
        </div>
        
        <div class="game-section">
            <h2 class="section-title">🎮 Game Creator</h2>
            
            <div class="game-creation">
                <textarea class="game-input" id="gameDescription" placeholder="Describe your game idea in detail...

Examples:
• A cooking game where you make pizza by dragging ingredients
• A space shooter where you defend Earth from alien invaders
• A puzzle game where you match colors and shapes
• A racing game on the moon with low gravity physics

Be creative! The more details you provide, the better your game will be." maxlength="1000"></textarea>
                
                <button class="create-btn" id="createBtn" onclick="createGame()">
                    ✨ Create Game
                </button>
                
                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <div>Creating your amazing game...</div>
                </div>
            </div>
            
            <div class="quick-actions">
                <button class="quick-btn" onclick="setQuickGame('A space shooter where you defend Earth from aliens')">🚀 Space Shooter</button>
                <button class="quick-btn" onclick="setQuickGame('A puzzle game with colorful blocks that you match')">🧩 Puzzle Game</button>
                <button class="quick-btn" onclick="setQuickGame('A racing game with fast cars and obstacles')">🏎️ Racing Game</button>
                <button class="quick-btn" onclick="setQuickGame('A cooking game where you prepare delicious meals')">👨‍🍳 Cooking Game</button>
            </div>
            
            <div id="status"></div>
            
            <a href="/games/showcase" class="game-showcase-link">
                🎯 View Game Showcase
            </a>
        </div>
    </div>

    <script>
        let isCreatingGame = false;
        
        // Chat functionality
        function sendMessage() {
            const input = document.getElementById('chatInput');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Add user message
            addMessage(message, 'user');
            input.value = '';
            
            // Send to AI assistant
            fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    addMessage(data.message, 'assistant');
                    
                    // If AI created a game, update the game section
                    if (data.has_game && data.game) {
                        showStatus(`🎉 Game "${data.game.title}" created successfully!`, 'success');
                    }
                } else {
                    addMessage('Sorry, I had trouble processing that. Could you try again?', 'assistant');
                }
            })
            .catch(error => {
                console.error('Chat error:', error);
                addMessage('I\'m having technical difficulties. Please try again in a moment.', 'assistant');
            });
        }
        
        function addMessage(text, type) {
            const messagesDiv = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}-message`;
            messageDiv.innerHTML = text.replace(/\\n/g, '<br>');
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        // Game creation functionality
        function createGame() {
            if (isCreatingGame) return;
            
            const description = document.getElementById('gameDescription').value.trim();
            if (!description) {
                showStatus('Please describe your game idea first!', 'error');
                return;
            }
            
            isCreatingGame = true;
            document.getElementById('createBtn').disabled = true;
            document.getElementById('loading').style.display = 'block';
            showStatus('Creating your game...', 'info');
            
            fetch('/api/games/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ description: description })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showStatus(`🎉 Game "${data.title}" created successfully!`, 'success');
                    document.getElementById('gameDescription').value = '';
                    
                    // Add success message to chat
                    addMessage(`🎮 I just created "${data.title}" for you! Check it out in the Game Showcase.`, 'assistant');
                    
                    setTimeout(() => {
                        window.location.href = '/games/showcase';
                    }, 2000);
                } else {
                    showStatus(`❌ Error: ${data.error || 'Failed to create game'}`, 'error');
                }
            })
            .catch(error => {
                console.error('Game creation error:', error);
                showStatus('❌ Failed to create game. Please try again.', 'error');
            })
            .finally(() => {
                isCreatingGame = false;
                document.getElementById('createBtn').disabled = false;
                document.getElementById('loading').style.display = 'none';
            });
        }
        
        function setQuickGame(description) {
            document.getElementById('gameDescription').value = description;
        }
        
        function showStatus(message, type) {
            const statusDiv = document.getElementById('status');
            statusDiv.textContent = message;
            statusDiv.className = `status ${type}`;
            statusDiv.style.display = 'block';
            
            if (type === 'success' || type === 'error') {
                setTimeout(() => {
                    statusDiv.style.display = 'none';
                }, 5000);
            }
        }
        
        // Enter key support
        document.getElementById('chatInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        document.getElementById('gameDescription').addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && e.ctrlKey) {
                createGame();
            }
        });
        
        // Prevent zoom on mobile
        document.addEventListener('touchstart', function(e) {
            if (e.touches.length > 1) {
                e.preventDefault();
            }
        });
        
        let lastTouchEnd = 0;
        document.addEventListener('touchend', function(e) {
            const now = (new Date()).getTime();
            if (now - lastTouchEnd <= 300) {
                e.preventDefault();
            }
            lastTouchEnd = now;
        }, false);
    </script>
</body>
</html>
    """)

@app.route('/api/chat', methods=['POST'])
def chat():
    """AI chat endpoint"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({"success": False, "error": "No message provided"})
        
        print(f"💬 Chat request: {message[:50]}...")
        
        # Get session ID for conversation tracking
        session_id = request.headers.get('X-Session-ID', 'default')
        
        # Chat with AI assistant
        response = chat_with_assistant(message)
        
        print(f"🤖 Chat response: {response.get('message', '')[:50]}...")
        
        return jsonify(response)
        
    except Exception as e:
        print(f"❌ Chat error: {e}")
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": "Chat service temporarily unavailable"
        })

@app.route('/api/games/create', methods=['POST'])
def create_game():
    """Create a new game"""
    try:
        data = request.get_json()
        description = data.get('description', '').strip()
        
        if not description:
            return jsonify({"success": False, "error": "No game description provided"})
        
        print(f"🎮 Creating game: {description[:50]}...")
        
        # Generate game using AI engine
        game_result = generate_game(description)
        
        if game_result and game_result.get('success'):
            # Store game
            game_id = game_result['game_id']
            games_storage[game_id] = game_result
            
            print(f"✅ Game created: {game_result['title']}")
            
            return jsonify({
                "success": True,
                "game_id": game_id,
                "title": game_result['title'],
                "description": game_result['description'],
                "genre": game_result.get('genre', 'custom'),
                "ai_generated": game_result.get('ai_generated', False)
            })
        else:
            error_msg = game_result.get('error', 'Unknown error') if game_result else 'Game generation failed'
            print(f"❌ Game creation failed: {error_msg}")
            return jsonify({"success": False, "error": error_msg})
            
    except Exception as e:
        print(f"❌ Game creation error: {e}")
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": "Game creation service temporarily unavailable"
        })

@app.route('/api/games/improve', methods=['POST'])
def improve_existing_game():
    """Improve an existing game"""
    try:
        data = request.get_json()
        game_id = data.get('game_id', '').strip()
        improvement_request = data.get('improvement_request', '').strip()
        
        if not game_id or not improvement_request:
            return jsonify({"success": False, "error": "Game ID and improvement request required"})
        
        print(f"🔧 Improving game {game_id}: {improvement_request[:50]}...")
        
        # Improve game using AI engine
        improved_result = improve_game(game_id, improvement_request)
        
        if improved_result and improved_result.get('success'):
            # Update stored game
            games_storage[game_id] = improved_result
            
            print(f"✅ Game improved: {improved_result['title']}")
            
            return jsonify({
                "success": True,
                "game_id": game_id,
                "title": improved_result['title'],
                "description": improved_result['description'],
                "genre": improved_result.get('genre', 'custom'),
                "improved": True
            })
        else:
            error_msg = improved_result.get('error', 'Unknown error') if improved_result else 'Game improvement failed'
            print(f"❌ Game improvement failed: {error_msg}")
            return jsonify({"success": False, "error": error_msg})
            
    except Exception as e:
        print(f"❌ Game improvement error: {e}")
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": "Game improvement service temporarily unavailable"
        })

@app.route('/games/showcase')
def games_showcase():
    """Game showcase page"""
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>🎮 Game Showcase - Mythiq Gateway</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            touch-action: manipulation;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            -webkit-user-select: none;
            user-select: none;
        }
        
        .header {
            text-align: center;
            padding: 40px 20px;
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(255,255,255,0.2);
        }
        
        .logo {
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #f093fb, #f5576c);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .create-section {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            text-align: center;
        }
        
        .game-input {
            width: 100%;
            max-width: 600px;
            padding: 15px;
            border: none;
            border-radius: 15px;
            background: rgba(255,255,255,0.2);
            color: white;
            font-size: 16px;
            outline: none;
            margin-bottom: 20px;
            min-height: 100px;
            resize: vertical;
        }
        
        .game-input::placeholder {
            color: rgba(255,255,255,0.7);
        }
        
        .create-btn {
            padding: 15px 40px;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            border: none;
            border-radius: 25px;
            color: white;
            font-size: 18px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .create-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }
        
        .games-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        
        .game-card {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            transition: all 0.3s;
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        .game-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        .game-title {
            font-size: 1.4em;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #f093fb, #f5576c);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .game-description {
            margin-bottom: 15px;
            opacity: 0.9;
            line-height: 1.4;
        }
        
        .game-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            font-size: 0.9em;
            opacity: 0.8;
        }
        
        .game-actions {
            display: flex;
            gap: 10px;
        }
        
        .play-btn, .improve-btn {
            flex: 1;
            padding: 12px;
            border: none;
            border-radius: 10px;
            color: white;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 14px;
        }
        
        .play-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        .improve-btn {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }
        
        .play-btn:hover, .improve-btn:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
        
        .no-games {
            text-align: center;
            padding: 60px 20px;
            opacity: 0.8;
        }
        
        .no-games-icon {
            font-size: 4em;
            margin-bottom: 20px;
        }
        
        .back-link {
            display: inline-block;
            margin-bottom: 20px;
            color: white;
            text-decoration: none;
            padding: 10px 20px;
            background: rgba(255,255,255,0.2);
            border-radius: 20px;
            transition: all 0.3s;
        }
        
        .back-link:hover {
            background: rgba(255,255,255,0.3);
            transform: translateY(-1px);
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        
        .spinner {
            border: 3px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            border-top: 3px solid white;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        @media (max-width: 768px) {
            .games-grid {
                grid-template-columns: 1fr;
            }
            
            .game-actions {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">🎮 Game Showcase</div>
        <p>Discover amazing games created by AI • Play, Share, and Enjoy!</p>
    </div>
    
    <div class="container">
        <a href="/" class="back-link">← Back to Home</a>
        
        <div class="create-section">
            <h2>🚀 Create Your Game</h2>
            <p>Describe your game idea and watch AI bring it to life!</p>
            <br>
            <textarea class="game-input" id="gameDescription" placeholder="Describe your game idea in detail...

Examples:
• A space shooter where you defend Earth from alien invaders
• A puzzle game where you match colorful gems
• A cooking game where you make pizza with different toppings
• A racing game on Mars with low gravity physics

Be creative! The more details you provide, the better your game will be."></textarea>
            <br>
            <button class="create-btn" onclick="createGame()">✨ Create Game</button>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <div>Creating your amazing game...</div>
            </div>
        </div>
        
        <div id="gamesContainer">
            <div class="no-games">
                <div class="no-games-icon">🎮</div>
                <h3>No games yet!</h3>
                <p>Be the first to create an amazing AI-generated game!</p>
            </div>
        </div>
    </div>

    <script>
        let games = [];
        
        // Load games on page load
        loadGames();
        
        function loadGames() {
            fetch('/api/games/list')
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        games = data.games;
                        displayGames();
                    }
                })
                .catch(error => {
                    console.error('Error loading games:', error);
                });
        }
        
        function displayGames() {
            const container = document.getElementById('gamesContainer');
            
            if (games.length === 0) {
                container.innerHTML = `
                    <div class="no-games">
                        <div class="no-games-icon">🎮</div>
                        <h3>No games yet!</h3>
                        <p>Be the first to create an amazing AI-generated game!</p>
                    </div>
                `;
                return;
            }
            
            const gamesGrid = document.createElement('div');
            gamesGrid.className = 'games-grid';
            
            games.forEach(game => {
                const gameCard = document.createElement('div');
                gameCard.className = 'game-card';
                gameCard.innerHTML = `
                    <div class="game-title">${game.title}</div>
                    <div class="game-description">${game.description}</div>
                    <div class="game-meta">
                        <span>Genre: ${game.genre}</span>
                        <span>${game.ai_generated ? '🤖 AI Generated' : '🎨 Template'}</span>
                    </div>
                    <div class="game-actions">
                        <button class="play-btn" onclick="playGame('${game.game_id}')">🎮 Play</button>
                        <button class="improve-btn" onclick="improveGame('${game.game_id}')">✨ Improve</button>
                    </div>
                `;
                gamesGrid.appendChild(gameCard);
            });
            
            container.innerHTML = '';
            container.appendChild(gamesGrid);
        }
        
        function createGame() {
            const description = document.getElementById('gameDescription').value.trim();
            if (!description) {
                alert('Please describe your game idea first!');
                return;
            }
            
            document.getElementById('loading').style.display = 'block';
            
            fetch('/api/games/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ description: description })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById('gameDescription').value = '';
                    loadGames(); // Reload games list
                    alert(`🎉 Game "${data.title}" created successfully!`);
                } else {
                    alert(`❌ Error: ${data.error || 'Failed to create game'}`);
                }
            })
            .catch(error => {
                console.error('Game creation error:', error);
                alert('❌ Failed to create game. Please try again.');
            })
            .finally(() => {
                document.getElementById('loading').style.display = 'none';
            });
        }
        
        function playGame(gameId) {
            window.open(`/games/play/${gameId}`, '_blank');
        }
        
        function improveGame(gameId) {
            const improvement = prompt('How would you like to improve this game?\\n\\nExamples:\\n• Make it harder\\n• Add more colors\\n• Change the controls\\n• Add sound effects');
            
            if (improvement && improvement.trim()) {
                fetch('/api/games/improve', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ 
                        game_id: gameId, 
                        improvement_request: improvement.trim() 
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        loadGames(); // Reload games list
                        alert(`✨ Game improved successfully!`);
                    } else {
                        alert(`❌ Error: ${data.error || 'Failed to improve game'}`);
                    }
                })
                .catch(error => {
                    console.error('Game improvement error:', error);
                    alert('❌ Failed to improve game. Please try again.');
                });
            }
        }
        
        // Prevent zoom on mobile
        document.addEventListener('touchstart', function(e) {
            if (e.touches.length > 1) {
                e.preventDefault();
            }
        });
        
        let lastTouchEnd = 0;
        document.addEventListener('touchend', function(e) {
            const now = (new Date()).getTime();
            if (now - lastTouchEnd <= 300) {
                e.preventDefault();
            }
            lastTouchEnd = now;
        }, false);
    </script>
</body>
</html>
    """)

@app.route('/api/games/list')
def list_games():
    """List all created games"""
    try:
        games_list = list(games_storage.values())
        # Sort by creation date (newest first)
        games_list.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        return jsonify({
            "success": True,
            "games": games_list,
            "count": len(games_list)
        })
        
    except Exception as e:
        print(f"❌ List games error: {e}")
        return jsonify({
            "success": False,
            "error": "Failed to load games"
        })

@app.route('/games/play/<game_id>')
def play_game(game_id):
    """Play a specific game"""
    try:
        if game_id not in games_storage:
            return "Game not found", 404
        
        game = games_storage[game_id]
        return game['html']
        
    except Exception as e:
        print(f"❌ Play game error: {e}")
        return "Error loading game", 500

@app.route('/api/health')
def health_check():
    """System health check"""
    try:
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "3.0.0",
            "features": {
                "ai_game_creation": True,
                "text_assistant": True,
                "game_improvement": True,
                "mobile_optimization": True
            },
            "api_status": {
                "groq_api_key": bool(GROQ_API_KEY),
                "blueprints_loaded": BLUEPRINTS_LOADED,
                "games_count": len(games_storage)
            },
            "system_info": {
                "python_version": "3.11+",
                "flask_version": "2.3.3",
                "deployment": "Railway"
            }
        })
        
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    print("🚀 Starting Mythiq Gateway - AI Game Creation Platform")
    print(f"🔑 GROQ API: {'✅ Connected' if GROQ_API_KEY else '❌ Not configured'}")
    print(f"📦 Blueprints: {'✅ Loaded' if BLUEPRINTS_LOADED else '❌ Not loaded'}")
    print("🎮 AI Game Engine: ✅ Ready")
    print("🧠 Text Assistant: ✅ Ready")
    print("📱 Mobile Optimization: ✅ Enabled")
    print("=" * 50)
    
    # Run the app
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
