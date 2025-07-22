#!/usr/bin/env python3
"""
🚀 Mythiq Gateway - Complete AI Game Creation Platform
Fixed version with proper POST method configuration
"""

import os
import json
import time
import random
import string
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify, redirect, url_for
from flask_cors import CORS

# Import AI engines
try:
    from ultimate_ai_game_engine import generate_game, get_game_suggestions
    AI_ENGINE_LOADED = True
    print("✅ Ultimate AI Game Engine loaded successfully")
except ImportError as e:
    AI_ENGINE_LOADED = False
    print(f"❌ Failed to import Ultimate AI Game Engine: {e}")

try:
    from intelligent_text_assistant import TextAssistant
    text_assistant = TextAssistant()
    TEXT_ASSISTANT_LOADED = True
    print("✅ Intelligent Text Assistant loaded successfully")
except ImportError as e:
    TEXT_ASSISTANT_LOADED = False
    print(f"❌ Failed to import Intelligent Text Assistant: {e}")

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load existing blueprints
try:
    from branches.auth_gate.routes import auth_bp
    from branches.pro_router.routes import pro_router_bp
    from branches.quota.routes import quota_bp
    from branches.memory.routes import memory_bp
    from branches.reasoning.routes import reasoning_bp
    from branches.self_validate.routes import validation_bp
    from branches.system.routes import system_bp
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(pro_router_bp, url_prefix='/api/pro')
    app.register_blueprint(quota_bp, url_prefix='/api/quota')
    app.register_blueprint(memory_bp, url_prefix='/api/memory')
    app.register_blueprint(reasoning_bp, url_prefix='/api/reasoning')
    app.register_blueprint(validation_bp, url_prefix='/api/validate')
    app.register_blueprint(system_bp, url_prefix='/api/system')
    
    print("✅ All blueprints registered successfully")
    BLUEPRINTS_LOADED = True
except Exception as e:
    print(f"❌ Blueprint registration error: {e}")
    BLUEPRINTS_LOADED = False

# Check GROQ API key
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
if GROQ_API_KEY:
    print(f"✅ GROQ API Key found: {GROQ_API_KEY[:10]}...")
    GROQ_AVAILABLE = True
else:
    print("❌ GROQ API Key not found")
    GROQ_AVAILABLE = False

# Simple file-based storage for games
GAMES_FILE = 'games_data.json'

def load_games():
    """Load games from JSON file"""
    try:
        if os.path.exists(GAMES_FILE):
            with open(GAMES_FILE, 'r') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Error loading games: {e}")
        return []

def save_games(games):
    """Save games to JSON file"""
    try:
        with open(GAMES_FILE, 'w') as f:
            json.dump(games, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving games: {e}")
        return False

def generate_game_id():
    """Generate unique game ID"""
    timestamp = str(int(time.time()))
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"game_{timestamp}_{random_str}"

# Main homepage with dual-panel interface
@app.route('/')
def home():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Mythiq Gateway - AI Game Studio</title>
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
            padding: 40px 20px;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
        }
        
        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header .subtitle {
            font-size: 1.3em;
            opacity: 0.9;
            margin-bottom: 10px;
        }
        
        .header .tagline {
            font-size: 1.1em;
            opacity: 0.8;
        }
        
        .main-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            padding: 30px;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .panel {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .panel h2 {
            font-size: 2em;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .ai-welcome {
            background: rgba(255, 255, 255, 0.2);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 20px;
            border-left: 4px solid #ff6b6b;
        }
        
        .ai-welcome h3 {
            margin-bottom: 15px;
            color: #ff6b6b;
        }
        
        .ai-welcome ul {
            list-style: none;
            margin: 15px 0;
        }
        
        .ai-welcome li {
            margin: 8px 0;
            padding-left: 20px;
            position: relative;
        }
        
        .ai-welcome li:before {
            content: "✨";
            position: absolute;
            left: 0;
        }
        
        .chat-input {
            display: flex;
            gap: 10px;
            margin-top: 20px;
        }
        
        .chat-input input {
            flex: 1;
            padding: 12px;
            border: none;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            font-size: 16px;
        }
        
        .chat-input input::placeholder {
            color: rgba(255, 255, 255, 0.7);
        }
        
        .chat-input button {
            padding: 12px 20px;
            border: none;
            border-radius: 10px;
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            color: white;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        .chat-input button:hover {
            transform: translateY(-2px);
        }
        
        .game-description {
            width: 100%;
            height: 120px;
            padding: 15px;
            border: none;
            border-radius: 15px;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            font-size: 16px;
            resize: vertical;
            margin-bottom: 20px;
        }
        
        .game-description::placeholder {
            color: rgba(255, 255, 255, 0.7);
        }
        
        .create-btn {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 15px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            margin-bottom: 20px;
        }
        
        .create-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }
        
        .quick-actions {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-bottom: 20px;
        }
        
        .quick-btn {
            padding: 10px;
            border: none;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            cursor: pointer;
            transition: all 0.2s;
            font-size: 14px;
        }
        
        .quick-btn:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }
        
        .showcase-link {
            display: block;
            text-align: center;
            padding: 15px;
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            color: white;
            text-decoration: none;
            border-radius: 15px;
            font-weight: bold;
            transition: transform 0.2s;
        }
        
        .showcase-link:hover {
            transform: translateY(-2px);
            color: white;
        }
        
        @media (max-width: 768px) {
            .main-container {
                grid-template-columns: 1fr;
                padding: 15px;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .quick-actions {
                grid-template-columns: 1fr;
            }
        }
        
        .status-indicator {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(0, 255, 0, 0.8);
            color: white;
            padding: 10px 15px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="status-indicator">🟢 AI Systems Online</div>
    
    <div class="header">
        <h1>🚀 Mythiq Gateway</h1>
        <div class="subtitle">AI-Powered Game Creation Studio</div>
        <div class="tagline">Create • Play • Share • Improve</div>
    </div>
    
    <div class="main-container">
        <!-- AI Assistant Panel -->
        <div class="panel">
            <h2>🧠 AI Assistant</h2>
            
            <div class="ai-welcome">
                <h3>👋 Welcome to Mythiq Gateway!</h3>
                <p>I'm your AI game creation assistant. I can help you:</p>
                <ul>
                    <li>Create unique games from any description</li>
                    <li>Improve existing games with your feedback</li>
                    <li>Answer questions about game development</li>
                </ul>
                
                <p><strong>Try saying:</strong></p>
                <ul>
                    <li>"Create a space shooter game"</li>
                    <li>"Make a puzzle game with colors"</li>
                    <li>"How do I make games?"</li>
                </ul>
                
                <p><strong>What would you like to create today?</strong></p>
            </div>
            
            <div class="chat-input">
                <input type="text" id="chatInput" placeholder="Ask me anything about game creation...">
                <button onclick="sendChatMessage()">Send</button>
            </div>
        </div>
        
        <!-- Game Creator Panel -->
        <div class="panel">
            <h2>🎮 Game Creator</h2>
            
            <textarea class="game-description" id="gameDescription" placeholder="Describe your game idea in detail...

Examples:
• A cooking game where you make pizza by dragging ingredients
• A space adventure where you pilot a ship through asteroid fields
• A puzzle game where you match colors to clear the board
• A racing game on a futuristic city track"></textarea>
            
            <button class="create-btn" onclick="createGame()">✨ Create Game</button>
            
            <div class="quick-actions">
                <button class="quick-btn" onclick="setGameType('space shooter')">🚀 Space Shooter</button>
                <button class="quick-btn" onclick="setGameType('puzzle game')">🧩 Puzzle Game</button>
                <button class="quick-btn" onclick="setGameType('racing game')">🏎️ Racing Game</button>
                <button class="quick-btn" onclick="setGameType('cooking game')">👨‍🍳 Cooking Game</button>
            </div>
            
            <a href="/games/showcase" class="showcase-link">🎯 View Game Showcase</a>
        </div>
    </div>
    
    <script>
        function sendChatMessage() {
            const input = document.getElementById('chatInput');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Clear input
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
                if (data.response) {
                    alert('AI Assistant: ' + data.response);
                }
            })
            .catch(error => {
                console.error('Chat error:', error);
                alert('AI Assistant is currently unavailable. Please try again later.');
            });
        }
        
        function setGameType(type) {
            const description = document.getElementById('gameDescription');
            const prompts = {
                'space shooter': 'A space shooter game where you pilot a spaceship and defend Earth from alien invaders. Include enemy ships, power-ups, and increasing difficulty levels.',
                'puzzle game': 'A puzzle game where you solve challenging brain teasers by matching patterns, colors, or shapes. Include multiple levels with increasing complexity.',
                'racing game': 'A racing game where you drive high-speed cars through challenging tracks. Include obstacles, power-ups, and time challenges.',
                'cooking game': 'A cooking game where you prepare delicious meals by following recipes and managing time. Include ingredient selection and cooking techniques.'
            };
            
            description.value = prompts[type] || `A ${type} with engaging gameplay and beautiful graphics.`;
        }
        
        function createGame() {
            const description = document.getElementById('gameDescription').value.trim();
            
            if (!description) {
                alert('Please describe your game idea first!');
                return;
            }
            
            // Show loading state
            const btn = document.querySelector('.create-btn');
            const originalText = btn.textContent;
            btn.textContent = '🎮 Creating Game...';
            btn.disabled = true;
            
            // Send game creation request
            fetch('/api/games/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    description: description,
                    timestamp: new Date().toISOString()
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(`🎉 Game "${data.game.title}" created successfully!`);
                    // Redirect to showcase or game page
                    if (data.game.id) {
                        window.location.href = `/games/play/${data.game.id}`;
                    } else {
                        window.location.href = '/games/showcase';
                    }
                } else {
                    alert('❌ Game creation failed: ' + (data.error || 'Unknown error'));
                }
            })
            .catch(error => {
                console.error('Game creation error:', error);
                alert('❌ Game creation failed. Please try again.');
            })
            .finally(() => {
                // Restore button
                btn.textContent = originalText;
                btn.disabled = false;
            });
        }
        
        // Enter key support for chat
        document.getElementById('chatInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendChatMessage();
            }
        });
    </script>
</body>
</html>
    ''')

# API Routes

@app.route('/api/health')
def health_check():
    """System health and status check"""
    games = load_games()
    
    return jsonify({
        "api_status": {
            "blueprints_loaded": BLUEPRINTS_LOADED,
            "games_count": len(games),
            "groq_api_key": GROQ_AVAILABLE
        },
        "features": {
            "ai_game_creation": AI_ENGINE_LOADED,
            "game_improvement": TEXT_ASSISTANT_LOADED,
            "mobile_optimization": True,
            "text_assistant": TEXT_ASSISTANT_LOADED
        },
        "status": "healthy",
        "system_info": {
            "deployment": "Railway",
            "flask_version": "2.3.3",
            "python_version": "3.11+",
            "version": "3.0.0"
        },
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/chat', methods=['POST'])
def chat_with_assistant():
    """Chat with AI assistant"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({"error": "No message provided"}), 400
        
        if TEXT_ASSISTANT_LOADED:
            response = text_assistant.process_message(message)
            return jsonify({"response": response, "success": True})
        else:
            # Fallback response
            fallback_responses = {
                "how": "I can help you create amazing games! Just describe what you want and I'll generate it for you.",
                "what": "I'm an AI assistant that helps create games from your descriptions. Try asking me to create a specific type of game!",
                "create": "Great! To create a game, just describe what you want in detail. For example: 'Create a space shooter where you defend Earth from aliens.'",
                "help": "I'm here to help you create games! Describe any game idea and I'll bring it to life. What would you like to create?"
            }
            
            # Simple keyword matching for fallback
            response = "I'm your AI game creation assistant! I can help you create unique games from any description. What would you like to create today?"
            for keyword, reply in fallback_responses.items():
                if keyword in message.lower():
                    response = reply
                    break
            
            return jsonify({"response": response, "success": True})
            
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({"error": "Chat service unavailable", "success": False}), 500

@app.route('/api/games/create', methods=['POST'])
def create_game():
    """Create a new game using AI"""
    try:
        data = request.get_json()
        description = data.get('description', '').strip()
        
        if not description:
            return jsonify({"error": "No game description provided", "success": False}), 400
        
        print(f"🎮 Creating game from description: {description[:100]}...")
        
        # Generate game using AI engine
        if AI_ENGINE_LOADED:
            game_data = generate_game(description)
        else:
            # Fallback game generation
            game_data = {
                "title": "Custom Game",
                "description": f"A game based on: {description}",
                "genre": "puzzle",
                "html_content": create_fallback_game(description)
            }
        
        # Generate unique game ID
        game_id = generate_game_id()
        
        # Create game record
        game_record = {
            "id": game_id,
            "title": game_data.get("title", "Untitled Game"),
            "description": game_data.get("description", description),
            "genre": game_data.get("genre", "puzzle"),
            "html_content": game_data.get("html_content", ""),
            "created_at": datetime.now().isoformat(),
            "plays": 0,
            "likes": 0,
            "user_description": description
        }
        
        # Save to games database
        games = load_games()
        games.append(game_record)
        
        if save_games(games):
            print(f"✅ Game '{game_record['title']}' created successfully with ID: {game_id}")
            return jsonify({
                "success": True,
                "game": {
                    "id": game_id,
                    "title": game_record["title"],
                    "description": game_record["description"],
                    "genre": game_record["genre"]
                },
                "message": "Game created successfully!"
            })
        else:
            return jsonify({"error": "Failed to save game", "success": False}), 500
            
    except Exception as e:
        print(f"❌ Game creation error: {e}")
        return jsonify({"error": f"Game creation failed: {str(e)}", "success": False}), 500

def create_fallback_game(description):
    """Create a fallback game when AI engine is unavailable"""
    # Simple keyword-based game selection
    description_lower = description.lower()
    
    if any(word in description_lower for word in ['space', 'shooter', 'alien', 'ship']):
        return create_space_shooter_game()
    elif any(word in description_lower for word in ['puzzle', 'match', 'brain', 'solve']):
        return create_puzzle_game()
    elif any(word in description_lower for word in ['race', 'car', 'speed', 'drive']):
        return create_racing_game()
    else:
        return create_puzzle_game()  # Default to puzzle

def create_space_shooter_game():
    """Create a space shooter game"""
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Space Shooter</title>
    <style>
        body { margin: 0; padding: 20px; background: #000; color: white; font-family: Arial; }
        canvas { border: 2px solid #fff; display: block; margin: 0 auto; background: linear-gradient(to bottom, #000428, #004e92); }
        .controls { text-align: center; margin: 20px; }
        .score { font-size: 24px; margin: 10px; }
    </style>
</head>
<body>
    <div class="controls">
        <div class="score">Score: <span id="score">0</span> | Lives: <span id="lives">3</span></div>
        <p>Use arrow keys to move, spacebar to shoot!</p>
    </div>
    <canvas id="gameCanvas" width="800" height="600"></canvas>
    
    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        
        let score = 0;
        let lives = 3;
        let gameRunning = true;
        
        // Player
        const player = { x: 375, y: 550, width: 50, height: 30, speed: 5 };
        
        // Bullets
        let bullets = [];
        
        // Enemies
        let enemies = [];
        
        // Controls
        const keys = {};
        
        document.addEventListener('keydown', (e) => keys[e.code] = true);
        document.addEventListener('keyup', (e) => keys[e.code] = false);
        
        function createEnemy() {
            enemies.push({
                x: Math.random() * (canvas.width - 40),
                y: -40,
                width: 40,
                height: 40,
                speed: 2 + Math.random() * 2
            });
        }
        
        function update() {
            if (!gameRunning) return;
            
            // Move player
            if (keys['ArrowLeft'] && player.x > 0) player.x -= player.speed;
            if (keys['ArrowRight'] && player.x < canvas.width - player.width) player.x += player.speed;
            if (keys['ArrowUp'] && player.y > 0) player.y -= player.speed;
            if (keys['ArrowDown'] && player.y < canvas.height - player.height) player.y += player.speed;
            
            // Shoot
            if (keys['Space']) {
                bullets.push({ x: player.x + player.width/2, y: player.y, speed: 7 });
                keys['Space'] = false; // Prevent rapid fire
            }
            
            // Update bullets
            bullets = bullets.filter(bullet => {
                bullet.y -= bullet.speed;
                return bullet.y > 0;
            });
            
            // Update enemies
            enemies = enemies.filter(enemy => {
                enemy.y += enemy.speed;
                return enemy.y < canvas.height;
            });
            
            // Check collisions
            bullets.forEach((bullet, bulletIndex) => {
                enemies.forEach((enemy, enemyIndex) => {
                    if (bullet.x < enemy.x + enemy.width &&
                        bullet.x + 5 > enemy.x &&
                        bullet.y < enemy.y + enemy.height &&
                        bullet.y + 10 > enemy.y) {
                        bullets.splice(bulletIndex, 1);
                        enemies.splice(enemyIndex, 1);
                        score += 10;
                    }
                });
            });
            
            // Check player-enemy collision
            enemies.forEach((enemy, index) => {
                if (player.x < enemy.x + enemy.width &&
                    player.x + player.width > enemy.x &&
                    player.y < enemy.y + enemy.height &&
                    player.y + player.height > enemy.y) {
                    enemies.splice(index, 1);
                    lives--;
                    if (lives <= 0) {
                        gameRunning = false;
                        alert('Game Over! Final Score: ' + score);
                    }
                }
            });
            
            // Spawn enemies
            if (Math.random() < 0.02) createEnemy();
            
            // Update UI
            document.getElementById('score').textContent = score;
            document.getElementById('lives').textContent = lives;
        }
        
        function draw() {
            // Clear canvas
            ctx.fillStyle = 'rgba(0, 4, 40, 0.1)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Draw stars
            for (let i = 0; i < 50; i++) {
                ctx.fillStyle = 'white';
                ctx.fillRect(Math.random() * canvas.width, Math.random() * canvas.height, 1, 1);
            }
            
            // Draw player
            ctx.fillStyle = '#00ff00';
            ctx.fillRect(player.x, player.y, player.width, player.height);
            
            // Draw bullets
            ctx.fillStyle = '#ffff00';
            bullets.forEach(bullet => {
                ctx.fillRect(bullet.x, bullet.y, 5, 10);
            });
            
            // Draw enemies
            ctx.fillStyle = '#ff0000';
            enemies.forEach(enemy => {
                ctx.fillRect(enemy.x, enemy.y, enemy.width, enemy.height);
            });
        }
        
        function gameLoop() {
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }
        
        gameLoop();
    </script>
</body>
</html>
    '''

def create_puzzle_game():
    """Create a puzzle game"""
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Sliding Puzzle</title>
    <style>
        body { margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); font-family: Arial; color: white; }
        .game-container { max-width: 500px; margin: 0 auto; text-align: center; }
        .puzzle-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 5px; margin: 20px auto; width: 320px; height: 320px; }
        .tile { width: 75px; height: 75px; background: linear-gradient(45deg, #ff6b6b, #ee5a24); border: none; border-radius: 10px; font-size: 24px; font-weight: bold; color: white; cursor: pointer; transition: all 0.2s; }
        .tile:hover { transform: scale(1.05); }
        .empty { background: transparent !important; }
        .controls { margin: 20px; }
        .btn { padding: 10px 20px; margin: 5px; border: none; border-radius: 10px; background: rgba(255,255,255,0.2); color: white; cursor: pointer; }
        .stats { font-size: 18px; margin: 10px; }
    </style>
</head>
<body>
    <div class="game-container">
        <h1>🧩 Sliding Puzzle</h1>
        <div class="stats">
            <div>Moves: <span id="moves">0</span></div>
            <div>Time: <span id="time">00:00</span></div>
        </div>
        <div class="puzzle-grid" id="puzzleGrid"></div>
        <div class="controls">
            <button class="btn" onclick="newGame()">New Game</button>
            <button class="btn" onclick="solve()">Solve</button>
        </div>
    </div>
    
    <script>
        let tiles = [];
        let emptyIndex = 15;
        let moves = 0;
        let startTime = Date.now();
        let timer;
        
        function initGame() {
            tiles = Array.from({length: 16}, (_, i) => i);
            shuffle();
            render();
            startTimer();
        }
        
        function shuffle() {
            for (let i = 0; i < 1000; i++) {
                const validMoves = getValidMoves();
                const randomMove = validMoves[Math.floor(Math.random() * validMoves.length)];
                moveTile(randomMove, false);
            }
            moves = 0;
            updateStats();
        }
        
        function getValidMoves() {
            const moves = [];
            const row = Math.floor(emptyIndex / 4);
            const col = emptyIndex % 4;
            
            if (row > 0) moves.push(emptyIndex - 4); // Up
            if (row < 3) moves.push(emptyIndex + 4); // Down
            if (col > 0) moves.push(emptyIndex - 1); // Left
            if (col < 3) moves.push(emptyIndex + 1); // Right
            
            return moves;
        }
        
        function moveTile(index, countMove = true) {
            const validMoves = getValidMoves();
            if (validMoves.includes(index)) {
                [tiles[index], tiles[emptyIndex]] = [tiles[emptyIndex], tiles[index]];
                emptyIndex = index;
                if (countMove) {
                    moves++;
                    updateStats();
                    checkWin();
                }
            }
        }
        
        function render() {
            const grid = document.getElementById('puzzleGrid');
            grid.innerHTML = '';
            
            tiles.forEach((tile, index) => {
                const button = document.createElement('button');
                button.className = 'tile';
                if (tile === 0) {
                    button.className += ' empty';
                } else {
                    button.textContent = tile;
                    button.onclick = () => moveTile(index);
                }
                grid.appendChild(button);
            });
        }
        
        function updateStats() {
            document.getElementById('moves').textContent = moves;
        }
        
        function startTimer() {
            timer = setInterval(() => {
                const elapsed = Math.floor((Date.now() - startTime) / 1000);
                const minutes = Math.floor(elapsed / 60).toString().padStart(2, '0');
                const seconds = (elapsed % 60).toString().padStart(2, '0');
                document.getElementById('time').textContent = `${minutes}:${seconds}`;
            }, 1000);
        }
        
        function checkWin() {
            const solved = tiles.every((tile, index) => tile === (index + 1) % 16);
            if (solved) {
                clearInterval(timer);
                setTimeout(() => {
                    alert(`🎉 Congratulations! You solved it in ${moves} moves!`);
                }, 100);
            }
        }
        
        function newGame() {
            clearInterval(timer);
            startTime = Date.now();
            initGame();
        }
        
        function solve() {
            tiles = Array.from({length: 16}, (_, i) => i);
            emptyIndex = 15;
            render();
            clearInterval(timer);
            alert('🎉 Puzzle solved!');
        }
        
        initGame();
    </script>
</body>
</html>
    '''

def create_racing_game():
    """Create a racing game"""
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Racing Game</title>
    <style>
        body { margin: 0; padding: 20px; background: #222; color: white; font-family: Arial; }
        canvas { border: 2px solid #fff; display: block; margin: 0 auto; background: #333; }
        .controls { text-align: center; margin: 20px; }
        .stats { font-size: 18px; margin: 10px; }
    </style>
</head>
<body>
    <div class="controls">
        <div class="stats">Speed: <span id="speed">0</span> mph | Distance: <span id="distance">0</span> m</div>
        <p>Use arrow keys to steer and accelerate!</p>
    </div>
    <canvas id="gameCanvas" width="400" height="600"></canvas>
    
    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        
        let speed = 0;
        let distance = 0;
        let roadOffset = 0;
        
        const player = { x: 175, y: 500, width: 50, height: 80 };
        let obstacles = [];
        
        const keys = {};
        document.addEventListener('keydown', (e) => keys[e.code] = true);
        document.addEventListener('keyup', (e) => keys[e.code] = false);
        
        function createObstacle() {
            obstacles.push({
                x: Math.random() * (canvas.width - 60),
                y: -100,
                width: 60,
                height: 100,
                speed: 3 + speed / 20
            });
        }
        
        function update() {
            // Player controls
            if (keys['ArrowLeft'] && player.x > 0) player.x -= 5;
            if (keys['ArrowRight'] && player.x < canvas.width - player.width) player.x += 5;
            if (keys['ArrowUp']) speed = Math.min(speed + 0.5, 100);
            if (keys['ArrowDown']) speed = Math.max(speed - 1, 0);
            
            // Update road
            roadOffset += speed / 10;
            
            // Update distance
            distance += speed / 10;
            
            // Update obstacles
            obstacles = obstacles.filter(obstacle => {
                obstacle.y += obstacle.speed + speed / 10;
                return obstacle.y < canvas.height;
            });
            
            // Spawn obstacles
            if (Math.random() < 0.01 + speed / 10000) createObstacle();
            
            // Check collisions
            obstacles.forEach(obstacle => {
                if (player.x < obstacle.x + obstacle.width &&
                    player.x + player.width > obstacle.x &&
                    player.y < obstacle.y + obstacle.height &&
                    player.y + player.height > obstacle.y) {
                    speed = Math.max(speed - 20, 0);
                    alert('Crash! Speed reduced!');
                }
            });
            
            // Update UI
            document.getElementById('speed').textContent = Math.floor(speed);
            document.getElementById('distance').textContent = Math.floor(distance);
        }
        
        function draw() {
            // Clear canvas
            ctx.fillStyle = '#333';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Draw road
            ctx.fillStyle = '#666';
            ctx.fillRect(50, 0, canvas.width - 100, canvas.height);
            
            // Draw road lines
            ctx.fillStyle = '#fff';
            for (let i = -1; i < 20; i++) {
                const y = (i * 60 + roadOffset % 60);
                ctx.fillRect(canvas.width / 2 - 2, y, 4, 30);
            }
            
            // Draw player car
            ctx.fillStyle = '#00ff00';
            ctx.fillRect(player.x, player.y, player.width, player.height);
            
            // Draw obstacles
            ctx.fillStyle = '#ff0000';
            obstacles.forEach(obstacle => {
                ctx.fillRect(obstacle.x, obstacle.y, obstacle.width, obstacle.height);
            });
        }
        
        function gameLoop() {
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }
        
        gameLoop();
    </script>
</body>
</html>
    '''

# Game showcase and play routes
@app.route('/games/showcase')
def games_showcase():
    """Display all created games"""
    games = load_games()
    
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎮 Game Showcase - Mythiq Gateway</title>
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
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .back-link {
            display: inline-block;
            padding: 10px 20px;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            text-decoration: none;
            border-radius: 10px;
            margin-bottom: 30px;
            transition: all 0.2s;
        }
        
        .back-link:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }
        
        .create-section {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 40px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .create-section h2 {
            font-size: 2em;
            margin-bottom: 15px;
        }
        
        .create-section p {
            font-size: 1.1em;
            margin-bottom: 20px;
            opacity: 0.9;
        }
        
        .game-description {
            width: 100%;
            max-width: 600px;
            height: 100px;
            padding: 15px;
            border: none;
            border-radius: 15px;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            font-size: 16px;
            resize: vertical;
            margin-bottom: 20px;
        }
        
        .game-description::placeholder {
            color: rgba(255, 255, 255, 0.7);
        }
        
        .create-btn {
            padding: 15px 30px;
            border: none;
            border-radius: 15px;
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            color: white;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .create-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }
        
        .games-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 30px;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .game-card {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 25px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.3s;
        }
        
        .game-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        }
        
        .game-title {
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 10px;
            color: #ff6b6b;
        }
        
        .game-genre {
            display: inline-block;
            padding: 5px 12px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            font-size: 0.9em;
            margin-bottom: 15px;
        }
        
        .game-description-text {
            font-size: 1em;
            line-height: 1.5;
            margin-bottom: 20px;
            opacity: 0.9;
        }
        
        .game-stats {
            display: flex;
            justify-content: space-between;
            margin-bottom: 20px;
            font-size: 0.9em;
            opacity: 0.8;
        }
        
        .game-actions {
            display: flex;
            gap: 10px;
        }
        
        .play-btn, .share-btn {
            flex: 1;
            padding: 12px;
            border: none;
            border-radius: 10px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.2s;
            text-decoration: none;
            text-align: center;
            display: block;
        }
        
        .play-btn {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
        }
        
        .share-btn {
            background: rgba(255, 255, 255, 0.2);
            color: white;
        }
        
        .play-btn:hover, .share-btn:hover {
            transform: translateY(-2px);
        }
        
        .no-games {
            text-align: center;
            padding: 60px 20px;
        }
        
        .no-games .icon {
            font-size: 4em;
            margin-bottom: 20px;
            opacity: 0.5;
        }
        
        .no-games h3 {
            font-size: 2em;
            margin-bottom: 15px;
        }
        
        .no-games p {
            font-size: 1.2em;
            opacity: 0.8;
        }
        
        @media (max-width: 768px) {
            .games-grid {
                grid-template-columns: 1fr;
                padding: 0 10px;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .game-actions {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <a href="/" class="back-link">← Back to Home</a>
    
    <div class="header">
        <h1>🎮 Game Showcase</h1>
        <p>Discover amazing games created by AI • Play, Share, and Enjoy!</p>
    </div>
    
    <div class="create-section">
        <h2>🚀 Create Your Game</h2>
        <p>Describe your game idea and watch AI bring it to life!</p>
        
        <textarea class="game-description" id="gameDescription" placeholder="Describe your game idea in detail...

Examples:
• A space shooter where you defend Earth from alien invasion
• A puzzle game where you match colors to clear the board
• A racing game through a futuristic city with obstacles"></textarea>
        
        <button class="create-btn" onclick="createGame()">✨ Create Game</button>
    </div>
    
    {% if games %}
    <div class="games-grid">
        {% for game in games %}
        <div class="game-card">
            <div class="game-title">{{ game.title }}</div>
            <div class="game-genre">{{ game.genre.title() }}</div>
            <div class="game-description-text">{{ game.description }}</div>
            <div class="game-stats">
                <span>🎮 {{ game.plays }} plays</span>
                <span>❤️ {{ game.likes }} likes</span>
                <span>📅 {{ game.created_at[:10] }}</span>
            </div>
            <div class="game-actions">
                <a href="/games/play/{{ game.id }}" class="play-btn">🎮 Play Game</a>
                <button class="share-btn" onclick="shareGame('{{ game.id }}', '{{ game.title }}')">📤 Share</button>
            </div>
        </div>
        {% endfor %}
    </div>
    {% else %}
    <div class="no-games">
        <div class="icon">🎮</div>
        <h3>No games yet!</h3>
        <p>Be the first to create an amazing AI-generated game!</p>
    </div>
    {% endif %}
    
    <script>
        function createGame() {
            const description = document.getElementById('gameDescription').value.trim();
            
            if (!description) {
                alert('Please describe your game idea first!');
                return;
            }
            
            // Show loading state
            const btn = document.querySelector('.create-btn');
            const originalText = btn.textContent;
            btn.textContent = '🎮 Creating Game...';
            btn.disabled = true;
            
            // Send game creation request
            fetch('/api/games/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    description: description,
                    timestamp: new Date().toISOString()
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(`🎉 Game "${data.game.title}" created successfully!`);
                    // Reload page to show new game
                    window.location.reload();
                } else {
                    alert('❌ Game creation failed: ' + (data.error || 'Unknown error'));
                }
            })
            .catch(error => {
                console.error('Game creation error:', error);
                alert('❌ Game creation failed. Please try again.');
            })
            .finally(() => {
                // Restore button
                btn.textContent = originalText;
                btn.disabled = false;
            });
        }
        
        function shareGame(gameId, gameTitle) {
            const url = window.location.origin + '/games/play/' + gameId;
            
            if (navigator.share) {
                navigator.share({
                    title: gameTitle,
                    text: 'Check out this AI-generated game!',
                    url: url
                });
            } else {
                // Fallback: copy to clipboard
                navigator.clipboard.writeText(url).then(() => {
                    alert('Game link copied to clipboard!');
                }).catch(() => {
                    prompt('Copy this link to share:', url);
                });
            }
        }
    </script>
</body>
</html>
    ''', games=games)

@app.route('/games/play/<game_id>')
def play_game(game_id):
    """Play a specific game"""
    games = load_games()
    game = next((g for g in games if g['id'] == game_id), None)
    
    if not game:
        return "Game not found", 404
    
    # Increment play count
    game['plays'] += 1
    save_games(games)
    
    # Return the game HTML content
    return game['html_content']

if __name__ == '__main__':
    print("🚀 Starting Mythiq Gateway - Complete AI Game Creation Platform")
    print(f"✅ AI Engine Loaded: {AI_ENGINE_LOADED}")
    print(f"✅ Text Assistant Loaded: {TEXT_ASSISTANT_LOADED}")
    print(f"✅ Blueprints Loaded: {BLUEPRINTS_LOADED}")
    print(f"✅ GROQ API Available: {GROQ_AVAILABLE}")
    
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
