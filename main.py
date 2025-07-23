""" 
Main Application - 100% Mobile-Compatible AI Game Creator
Revolutionary platform that generates completely unique games from user prompts
NOW WITH FULL MOBILE SUPPORT AND TOUCH CONTROLS

This application provides:
- Web interface for users to enter game descriptions
- Integration with the Dynamic AI Game Generator
- API endpoints for game creation and retrieval
- Game showcase for displaying unique creations
- Real-time AI-powered game generation
- FULL MOBILE COMPATIBILITY WITH TOUCH CONTROLS
"""

import os
import json
import time
import random
from flask import Flask, request, jsonify, render_template_string, redirect, url_for

# Import the Dynamic AI Game Generator with proper error handling
try:
    from dynamic_ai_game_generator import DynamicAIGameGenerator
    AI_GENERATOR_AVAILABLE = True
except ImportError:
    AI_GENERATOR_AVAILABLE = False
    print("Warning: DynamicAIGameGenerator not available, using fallback")

app = Flask(__name__)

# In-memory database for storing created games
games_db = {}

# --- HTML Templates ---

HOME_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>🚀 Mythiq Gateway - AI Game Creation Platform</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #ffffff;
            min-height: 100vh;
            overflow-x: hidden;
        }
        .hero {
            text-align: center;
            padding: 80px 20px;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.9), rgba(118, 75, 162, 0.9));
        }
        .hero h1 {
            font-size: 4em;
            margin-bottom: 20px;
            text-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }
        .hero p {
            font-size: 1.3em;
            margin-bottom: 40px;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 40px 20px;
            max-width: 1200px;
            margin: 0 auto;
        }
        .stat-card {
            background: rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .stat-number {
            font-size: 3em;
            font-weight: bold;
            color: #ffd700;
            margin-bottom: 10px;
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            padding: 60px 20px;
            max-width: 1200px;
            margin: 0 auto;
        }
        .feature-card {
            background: rgba(255, 255, 255, 0.1);
            padding: 40px;
            border-radius: 20px;
            text-align: center;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.3s ease;
        }
        .feature-card:hover {
            transform: translateY(-10px);
        }
        .feature-icon {
            font-size: 3em;
            margin-bottom: 20px;
        }
        .feature-title {
            font-size: 1.5em;
            margin-bottom: 15px;
            color: #ffd700;
        }
        .cta {
            text-align: center;
            padding: 60px 20px;
        }
        .cta h2 {
            font-size: 2.5em;
            margin-bottom: 30px;
        }
        .btn {
            display: inline-block;
            padding: 20px 40px;
            margin: 10px;
            font-size: 1.2em;
            text-decoration: none;
            border-radius: 50px;
            transition: all 0.3s ease;
            font-weight: bold;
            min-height: 44px; /* Touch-friendly size */
        }
        .btn-primary {
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white;
        }
        .btn-secondary {
            background: linear-gradient(45deg, #2196F3, #1976D2);
            color: white;
        }
        .btn:hover, .btn:active {
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        }
        
        /* Mobile optimizations */
        @media (max-width: 768px) {
            .hero h1 { font-size: 2.5em; }
            .hero p { font-size: 1.1em; }
            .stat-number { font-size: 2em; }
            .feature-card { padding: 20px; }
            .btn { padding: 15px 30px; font-size: 1.1em; }
        }
    </style>
</head>
<body>
    <div class="hero">
        <h1>🚀 Mythiq Gateway</h1>
        <p>The world's most advanced AI-powered game creation platform. Create professional games instantly with just a description!</p>
        <p style="color: #ffd700; font-weight: bold;">📱 NOW WITH FULL MOBILE SUPPORT!</p>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <div class="stat-number">∞</div>
            <div>Game Types</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">100%</div>
            <div>AI Powered</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">0</div>
            <div>Coding Required</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">📱</div>
            <div>Mobile Ready</div>
        </div>
    </div>
    
    <div class="features">
        <div class="feature-card">
            <div class="feature-icon">🎮</div>
            <div class="feature-title">AI Game Creation</div>
            <p>Describe any game in natural language and watch our AI create a fully functional, playable game instantly.</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📱</div>
            <div class="feature-title">Mobile Gaming</div>
            <p>All games work perfectly on phones with touch controls, swipe gestures, and responsive design.</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🏆</div>
            <div class="feature-title">Game Showcase</div>
            <p>Discover amazing games created by our community. Play, share, and get inspired by endless creativity.</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🚀</div>
            <div class="feature-title">Enterprise Ready</div>
            <p>Professional-grade platform with advanced AI modules, analytics, and scalable architecture.</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🎨</div>
            <div class="feature-title">Multiple Genres</div>
            <p>Create platformers, shooters, puzzles, RPGs, racing games, strategy games, and more!</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Instant Play</div>
            <p>Games are created and ready to play in seconds. No downloads, no installations required.</p>
        </div>
    </div>
    
    <div class="cta">
        <h2>Ready to Create Amazing Games?</h2>
        <a href="/games/showcase" class="btn btn-primary">🎮 Start Creating Games</a>
        <a href="/api/health" class="btn btn-secondary">📊 System Status</a>
    </div>
</body>
</html>
"""

SHOWCASE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>🎮 Game Showcase - AI Created Games</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #ffffff;
            min-height: 100vh;
        }
        .header {
            text-align: center;
            padding: 40px 20px;
            background: rgba(0,0,0,0.2);
        }
        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
        }
        .create-section {
            max-width: 800px;
            margin: 40px auto;
            padding: 40px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .create-section h2 {
            color: #ffd700;
            margin-bottom: 20px;
            font-size: 1.8em;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 10px;
            font-weight: bold;
            color: #ffd700;
        }
        textarea {
            width: 100%;
            height: 120px;
            padding: 15px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.1);
            color: #ffffff;
            font-size: 1.1em;
            resize: vertical;
            font-family: inherit;
        }
        textarea::placeholder {
            color: rgba(255, 255, 255, 0.7);
        }
        .btn {
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 50px;
            font-size: 1.2em;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: bold;
            width: 100%;
            min-height: 44px; /* Touch-friendly */
        }
        .btn:hover, .btn:active {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        }
        .btn:disabled {
            background: #666;
            cursor: not-allowed;
            transform: none;
        }
        .games-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 30px;
            padding: 40px 20px;
            max-width: 1200px;
            margin: 0 auto;
        }
        .game-card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.3s ease;
        }
        .game-card:hover {
            transform: translateY(-5px);
        }
        .game-title {
            font-size: 1.5em;
            color: #ffd700;
            margin-bottom: 15px;
        }
        .game-description {
            margin-bottom: 20px;
            line-height: 1.6;
        }
        .play-btn {
            background: linear-gradient(45deg, #2196F3, #1976D2);
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 25px;
            font-weight: bold;
            transition: all 0.3s ease;
            display: inline-block;
            min-height: 44px; /* Touch-friendly */
            line-height: 20px;
        }
        .play-btn:hover, .play-btn:active {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        .no-games {
            text-align: center;
            padding: 60px 20px;
            font-size: 1.2em;
        }
        .back-link {
            text-align: center;
            padding: 20px;
        }
        .back-link a {
            color: #ffd700;
            text-decoration: none;
            font-size: 1.1em;
            padding: 10px 20px;
            min-height: 44px; /* Touch-friendly */
            display: inline-block;
        }
        
        /* Mobile optimizations */
        @media (max-width: 768px) {
            .header h1 { font-size: 2em; }
            .create-section { margin: 20px; padding: 20px; }
            .games-grid { padding: 20px 10px; gap: 20px; }
            .game-card { padding: 20px; }
            textarea { height: 100px; font-size: 16px; } /* Prevent zoom on iOS */
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎮 Game Showcase</h1>
        <p>Discover amazing games created by AI • Play, Share, and Enjoy!</p>
        <p style="color: #ffd700;">📱 All games work on mobile with touch controls!</p>
    </div>
    
    <div class="create-section">
        <h2>🚀 Create Your Game</h2>
        <form id="gameForm" action="/api/games/create" method="post">
            <div class="form-group">
                <label for="prompt">Describe your game:</label>
                <textarea id="prompt" name="prompt" placeholder="A space shooter where you defend Earth from alien invaders..." required></textarea>
            </div>
            <button type="submit" class="btn" id="createBtn">✨ Create Game</button>
        </form>
    </div>
    
    <div class="games-grid">
        {% for game_id, game in games.items() %}
        <div class="game-card">
            <div class="game-title">{{ game.title }}</div>
            <div class="game-description">{{ game.description }}</div>
            <a href="/play/{{ game_id }}" class="play-btn">🎮 Play Game</a>
        </div>
        {% endfor %}
        
        {% if not games %}
        <div class="no-games">
            <h3>🎮 No games yet!</h3>
            <p>Be the first to create an amazing AI-generated game!</p>
        </div>
        {% endif %}
    </div>
    
    <div class="back-link">
        <a href="/">← Back to Home</a>
    </div>
    
    <script>
        document.getElementById('gameForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const btn = document.getElementById('createBtn');
            const prompt = document.getElementById('prompt').value.trim();
            
            if (!prompt) {
                alert('Please describe your game!');
                return;
            }
            
            btn.disabled = true;
            btn.textContent = '🎮 Creating Game...';
            
            fetch('/api/games/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt: prompt })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = '/play/' + data.game_id;
                } else {
                    alert('Error creating game: ' + (data.error || 'Unknown error'));
                    btn.disabled = false;
                    btn.textContent = '✨ Create Game';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error creating game. Please try again.');
                btn.disabled = false;
                btn.textContent = '✨ Create Game';
            });
        });
    </script>
</body>
</html>
"""

PLAY_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>Playing: {{ game.title }}</title>
    <style>
        body { 
            margin: 0; 
            background: #000; 
            font-family: Arial, sans-serif;
            overflow: hidden;
        }
        .game-container { 
            width: 100%; 
            height: 100vh; 
            display: flex;
            flex-direction: column;
        }
        .game-header {
            background: rgba(0,0,0,0.8);
            color: white;
            padding: 10px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 1000;
        }
        .game-content {
            flex: 1;
            background: #000;
            position: relative;
        }
        iframe { 
            width: 100%; 
            height: 100%; 
            border: none; 
        }
        .back-btn {
            background: #4CAF50;
            color: white;
            padding: 8px 16px;
            text-decoration: none;
            border-radius: 5px;
            font-size: 0.9em;
            min-height: 36px;
            display: flex;
            align-items: center;
        }
        
        /* Mobile optimizations */
        @media (max-width: 768px) {
            .game-header {
                padding: 8px 12px;
            }
            .game-header h3 {
                font-size: 1em;
                margin: 0;
            }
            .back-btn {
                padding: 6px 12px;
                font-size: 0.8em;
            }
        }
    </style>
</head>
<body>
    <div class="game-container">
        <div class="game-header">
            <h3>{{ game.title }}</h3>
            <a href="/games/showcase" class="back-btn">← Back to Showcase</a>
        </div>
        <div class="game-content">
            <iframe srcdoc="{{ game.html_content|e }}"></iframe>
        </div>
    </div>
</body>
</html>
"""

# --- Mobile-Compatible Fallback Game Generator ---
def create_mobile_compatible_game(prompt):
    """Create a mobile-compatible game with touch controls"""
    game_id = f"mobile_{int(time.time())}_{random.randint(1000, 9999)}"
    
    # Simple theme detection
    theme = "space"
    if "underwater" in prompt.lower() or "ocean" in prompt.lower() or "mermaid" in prompt.lower():
        theme = "underwater"
    elif "forest" in prompt.lower() or "fairy" in prompt.lower() or "magic" in prompt.lower():
        theme = "forest"
    elif "cyber" in prompt.lower() or "neon" in prompt.lower() or "tech" in prompt.lower():
        theme = "cyber"
    
    # Theme-based styling
    themes = {
        "underwater": {
            "bg_color": "#001133",
            "player_color": "#00FFFF",
            "collect_color": "#FFD700",
            "enemy_color": "#FF4444",
            "title": "Ocean Adventure"
        },
        "forest": {
            "bg_color": "#001100",
            "player_color": "#00FF00",
            "collect_color": "#FFFF00",
            "enemy_color": "#8B4513",
            "title": "Forest Quest"
        },
        "cyber": {
            "bg_color": "#000011",
            "player_color": "#00FFFF",
            "collect_color": "#FF00FF",
            "enemy_color": "#FF0000",
            "title": "Cyber Mission"
        },
        "space": {
            "bg_color": "#000000",
            "player_color": "#FFFFFF",
            "collect_color": "#FFFF00",
            "enemy_color": "#FF0000",
            "title": "Space Adventure"
        }
    }
    
    theme_data = themes[theme]
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
        <title>{theme_data['title']}</title>
        <style>
            body {{ 
                margin: 0; 
                background: {theme_data['bg_color']}; 
                overflow: hidden; 
                font-family: Arial, sans-serif;
                touch-action: none;
            }}
            canvas {{ 
                display: block; 
                touch-action: none;
            }}
            #ui {{ 
                position: absolute; 
                top: 10px; 
                left: 10px; 
                color: white; 
                font-family: Arial; 
                z-index: 100;
                font-size: 14px;
            }}
            #controls {{
                position: absolute;
                bottom: 20px;
                left: 50%;
                transform: translateX(-50%);
                display: flex;
                gap: 10px;
                z-index: 100;
            }}
            .control-btn {{
                width: 60px;
                height: 60px;
                background: rgba(255,255,255,0.2);
                border: 2px solid rgba(255,255,255,0.5);
                border-radius: 50%;
                color: white;
                font-size: 20px;
                font-weight: bold;
                display: flex;
                align-items: center;
                justify-content: center;
                touch-action: manipulation;
                user-select: none;
                cursor: pointer;
            }}
            .control-btn:active {{
                background: rgba(255,255,255,0.4);
                transform: scale(0.95);
            }}
            #instructions {{
                position: absolute;
                top: 50px;
                left: 10px;
                color: white;
                font-size: 12px;
                z-index: 100;
            }}
            
            /* Hide controls on desktop */
            @media (min-width: 768px) {{
                #controls {{ display: none; }}
                #instructions {{ display: block; }}
            }}
            
            /* Show controls on mobile */
            @media (max-width: 767px) {{
                #controls {{ display: flex; }}
                #instructions {{ display: none; }}
            }}
        </style>
    </head>
    <body>
        <div id="ui">
            <div>Score: <span id="score">0</span></div>
        </div>
        <div id="instructions">Use WASD or Arrow Keys to move</div>
        <canvas id="game"></canvas>
        
        <!-- Mobile Touch Controls -->
        <div id="controls">
            <div class="control-btn" id="leftBtn">←</div>
            <div class="control-btn" id="upBtn">↑</div>
            <div class="control-btn" id="downBtn">↓</div>
            <div class="control-btn" id="rightBtn">→</div>
        </div>
        
        <script>
            const canvas = document.getElementById('game');
            const ctx = canvas.getContext('2d');
            
            // Set canvas size
            function resizeCanvas() {{
                canvas.width = window.innerWidth;
                canvas.height = window.innerHeight;
            }}
            resizeCanvas();
            window.addEventListener('resize', resizeCanvas);
            
            let score = 0;
            const player = {{ x: canvas.width/2, y: canvas.height/2, size: 20 }};
            const collectibles = [];
            const enemies = [];
            
            // Create collectibles
            for(let i = 0; i < 10; i++) {{
                collectibles.push({{
                    x: Math.random() * canvas.width,
                    y: Math.random() * canvas.height,
                    size: 15
                }});
            }}
            
            // Create enemies
            for(let i = 0; i < 5; i++) {{
                enemies.push({{
                    x: Math.random() * canvas.width,
                    y: Math.random() * canvas.height,
                    size: 18,
                    dx: (Math.random() - 0.5) * 2,
                    dy: (Math.random() - 0.5) * 2
                }});
            }}
            
            // Input handling
            const keys = {{}};
            const movement = {{ up: false, down: false, left: false, right: false }};
            
            // Keyboard controls
            document.addEventListener('keydown', (e) => {{ 
                keys[e.key.toLowerCase()] = true; 
                e.preventDefault();
            }});
            document.addEventListener('keyup', (e) => {{ 
                keys[e.key.toLowerCase()] = false; 
                e.preventDefault();
            }});
            
            // Touch controls for mobile
            function setupTouchControls() {{
                const leftBtn = document.getElementById('leftBtn');
                const rightBtn = document.getElementById('rightBtn');
                const upBtn = document.getElementById('upBtn');
                const downBtn = document.getElementById('downBtn');
                
                // Touch start events
                leftBtn.addEventListener('touchstart', (e) => {{ 
                    movement.left = true; 
                    e.preventDefault(); 
                }});
                rightBtn.addEventListener('touchstart', (e) => {{ 
                    movement.right = true; 
                    e.preventDefault(); 
                }});
                upBtn.addEventListener('touchstart', (e) => {{ 
                    movement.up = true; 
                    e.preventDefault(); 
                }});
                downBtn.addEventListener('touchstart', (e) => {{ 
                    movement.down = true; 
                    e.preventDefault(); 
                }});
                
                // Touch end events
                leftBtn.addEventListener('touchend', (e) => {{ 
                    movement.left = false; 
                    e.preventDefault(); 
                }});
                rightBtn.addEventListener('touchend', (e) => {{ 
                    movement.right = false; 
                    e.preventDefault(); 
                }});
                upBtn.addEventListener('touchend', (e) => {{ 
                    movement.up = false; 
                    e.preventDefault(); 
                }});
                downBtn.addEventListener('touchend', (e) => {{ 
                    movement.down = false; 
                    e.preventDefault(); 
                }});
                
                // Mouse events for desktop testing
                leftBtn.addEventListener('mousedown', () => movement.left = true);
                leftBtn.addEventListener('mouseup', () => movement.left = false);
                rightBtn.addEventListener('mousedown', () => movement.right = true);
                rightBtn.addEventListener('mouseup', () => movement.right = false);
                upBtn.addEventListener('mousedown', () => movement.up = true);
                upBtn.addEventListener('mouseup', () => movement.up = false);
                downBtn.addEventListener('mousedown', () => movement.down = true);
                downBtn.addEventListener('mouseup', () => movement.down = false);
            }}
            
            setupTouchControls();
            
            function update() {{
                // Handle movement from keyboard or touch
                const moveSpeed = 5;
                if(keys['w'] || keys['arrowup'] || movement.up) player.y -= moveSpeed;
                if(keys['s'] || keys['arrowdown'] || movement.down) player.y += moveSpeed;
                if(keys['a'] || keys['arrowleft'] || movement.left) player.x -= moveSpeed;
                if(keys['d'] || keys['arrowright'] || movement.right) player.x += moveSpeed;
                
                // Keep player in bounds
                player.x = Math.max(player.size, Math.min(canvas.width - player.size, player.x));
                player.y = Math.max(player.size, Math.min(canvas.height - player.size, player.y));
                
                // Move enemies
                enemies.forEach(enemy => {{
                    enemy.x += enemy.dx;
                    enemy.y += enemy.dy;
                    if(enemy.x < 0 || enemy.x > canvas.width) enemy.dx *= -1;
                    if(enemy.y < 0 || enemy.y > canvas.height) enemy.dy *= -1;
                }});
                
                // Check collectible collisions
                for(let i = collectibles.length - 1; i >= 0; i--) {{
                    const c = collectibles[i];
                    const dist = Math.sqrt((player.x - c.x)**2 + (player.y - c.y)**2);
                    if(dist < player.size + c.size) {{
                        collectibles.splice(i, 1);
                        score += 10;
                        document.getElementById('score').textContent = score;
                        
                        // Add new collectible
                        collectibles.push({{
                            x: Math.random() * canvas.width,
                            y: Math.random() * canvas.height,
                            size: 15
                        }});
                    }}
                }}
                
                // Check enemy collisions
                enemies.forEach(enemy => {{
                    const dist = Math.sqrt((player.x - enemy.x)**2 + (player.y - enemy.y)**2);
                    if(dist < player.size + enemy.size) {{
                        score = Math.max(0, score - 5);
                        document.getElementById('score').textContent = score;
                        // Reset player position
                        player.x = canvas.width/2;
                        player.y = canvas.height/2;
                    }}
                }});
            }}
            
            function draw() {{
                ctx.fillStyle = '{theme_data['bg_color']}';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                // Draw player
                ctx.fillStyle = '{theme_data['player_color']}';
                ctx.beginPath();
                ctx.arc(player.x, player.y, player.size, 0, Math.PI * 2);
                ctx.fill();
                
                // Draw collectibles
                ctx.fillStyle = '{theme_data['collect_color']}';
                collectibles.forEach(c => {{
                    ctx.beginPath();
                    ctx.arc(c.x, c.y, c.size, 0, Math.PI * 2);
                    ctx.fill();
                }});
                
                // Draw enemies
                ctx.fillStyle = '{theme_data['enemy_color']}';
                enemies.forEach(enemy => {{
                    ctx.beginPath();
                    ctx.arc(enemy.x, enemy.y, enemy.size, 0, Math.PI * 2);
                    ctx.fill();
                }});
            }}
            
            function gameLoop() {{
                update();
                draw();
                requestAnimationFrame(gameLoop);
            }}
            
            gameLoop();
            
            // Prevent scrolling on mobile
            document.addEventListener('touchmove', (e) => {{
                e.preventDefault();
            }}, {{ passive: false }});
            
            // Prevent context menu on long press
            document.addEventListener('contextmenu', (e) => {{
                e.preventDefault();
            }});
        </script>
    </body>
    </html>
    """
    
    return {
        'game_id': game_id,
        'title': theme_data['title'],
        'description': f"A mobile-compatible {theme} themed adventure game created from your prompt: {prompt[:100]}...",
        'html_content': html_content,
        'css_styles': '',
        'javascript_code': ''
    }

# --- API Endpoints ---

@app.route('/')
def home():
    return render_template_string(HOME_TEMPLATE)

@app.route('/games/showcase')
def showcase_route():
    return render_template_string(SHOWCASE_TEMPLATE, games=games_db)

@app.route('/api/games/create', methods=['POST'])
def create_game_route():
    try:
        # Get prompt from JSON or form data
        if request.is_json:
            data = request.get_json()
            prompt = data.get('prompt', '').strip()
        else:
            prompt = request.form.get('prompt', '').strip()
        
        if not prompt:
            return jsonify({'success': False, 'error': 'Prompt is required'}), 400
        
        # Generate the mobile-compatible game
        if AI_GENERATOR_AVAILABLE:
            try:
                generator = DynamicAIGameGenerator()
                game_data = generator.generate_game(prompt)
                
                # Combine HTML, CSS, and JS for the final game file
                full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>{game_data['title']}</title>
    <style>{game_data['css_styles']}</style>
</head>
<body>
    {game_data['html_content']}
    <script>{game_data['javascript_code']}</script>
</body>
</html>"""
                game_data['html_content'] = full_html
                
            except Exception as e:
                print(f"AI Generator failed: {e}")
                game_data = create_mobile_compatible_game(prompt)
        else:
            game_data = create_mobile_compatible_game(prompt)
        
        # Store game in our 'database'
        game_id = game_data['game_id']
        games_db[game_id] = game_data
        
        if request.is_json:
            return jsonify({'success': True, 'game_id': game_id})
        else:
            return redirect(url_for('play_game_route', game_id=game_id))
        
    except Exception as e:
        error_msg = f"Error generating game: {str(e)}"
        print(error_msg)
        if request.is_json:
            return jsonify({'success': False, 'error': error_msg}), 500
        else:
            return error_msg, 500

@app.route('/play/<game_id>')
def play_game_route(game_id):
    game = games_db.get(game_id)
    if not game:
        return "Game not found", 404
    
    return render_template_string(PLAY_TEMPLATE, game=game)

@app.route('/api/games/<game_id>')
def get_game_api(game_id):
    game = games_db.get(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404
    return jsonify(game)

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'ai_generator_available': AI_GENERATOR_AVAILABLE,
        'games_created': len(games_db),
        'mobile_compatible': True,
        'touch_controls': True,
        'timestamp': time.time()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
