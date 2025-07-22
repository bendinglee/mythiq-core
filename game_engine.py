#!/usr/bin/env python3
"""
🤖 COMPATIBLE AI GAME ENGINE
Works with existing Mythiq Gateway architecture while providing true AI game generation
"""

import json
import random
import hashlib
import time
from datetime import datetime
import os
import requests
import re

def generate_game(description):
    """
    Generate a completely unique game based on user description
    Compatible with existing Mythiq Gateway architecture
    """
    try:
        # Clean and validate description
        description = description.strip()
        if not description:
            description = "a fun game"
        
        # Generate unique game ID
        timestamp = str(int(time.time()))
        game_id = f"game_{timestamp}_{hashlib.md5(description.encode()).hexdigest()[:6]}"
        
        print(f"🎮 Generating game for: {description}")
        
        # Try AI generation first
        ai_result = generate_ai_powered_game(description, game_id)
        if ai_result and ai_result.get('success'):
            print("✅ AI generation successful")
            return ai_result
        
        # Fallback to intelligent template system
        print("🔄 Using intelligent fallback system")
        return generate_intelligent_game(description, game_id)
        
    except Exception as e:
        print(f"❌ Game generation error: {e}")
        return generate_simple_fallback(description, game_id)

def generate_ai_powered_game(description, game_id):
    """
    Use GROQ AI to generate completely custom games
    """
    try:
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            print("⚠️ GROQ API key not found")
            return None
        
        print("🤖 Calling GROQ AI for game generation...")
        
        # Create AI prompt for game generation
        prompt = f"""Create a complete HTML5 game based on this description: "{description}"

You must respond with ONLY a JSON object in this exact format:
{{
    "title": "Game Title (2-4 words)",
    "description": "Brief description (1 sentence)",
    "genre": "game genre",
    "html": "complete HTML game code"
}}

Requirements:
1. Create a UNIQUE game that matches the description exactly
2. Include complete HTML with embedded CSS and JavaScript
3. Make it fully playable with proper game mechanics
4. Add mobile touch controls AND keyboard controls
5. Include scoring and win/lose conditions
6. Use canvas or DOM elements as appropriate
7. Make it responsive for all screen sizes

Examples:
- "fairy collecting mushrooms" → Create a character that moves around collecting items while avoiding enemies
- "typing game" → Create falling words that player must type correctly
- "memory game" → Create card matching or sequence memory challenge
- "tower defense" → Create towers that shoot at moving enemies

Create a completely functional game with unique mechanics that match the user's description. Respond with ONLY the JSON object."""

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            "messages": [{"role": "user", "content": prompt}],
            "model": "llama3-8b-8192",
            "temperature": 0.8,
            "max_tokens": 4000
        }
        
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content'].strip()
            
            print(f"🤖 AI Response received: {len(content)} characters")
            
            # Parse AI response
            game_data = parse_ai_response(content, game_id)
            if game_data:
                print("✅ AI response parsed successfully")
                return {
                    "success": True,
                    "game_id": game_id,
                    "title": game_data["title"],
                    "description": game_data["description"],
                    "genre": game_data.get("genre", "custom"),
                    "html": game_data["html"],
                    "created_at": datetime.now().isoformat()
                }
            else:
                print("❌ Failed to parse AI response")
        else:
            print(f"❌ GROQ API error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ AI generation error: {e}")
    
    return None

def parse_ai_response(content, game_id):
    """
    Parse AI response and extract game data
    """
    try:
        # Clean up response
        content = content.strip()
        
        # Remove code blocks
        if content.startswith('```json'):
            content = content.replace('```json', '').replace('```', '').strip()
        elif content.startswith('```'):
            content = content.replace('```', '').strip()
        
        # Find JSON in response
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            content = json_match.group()
        
        # Parse JSON
        game_data = json.loads(content)
        
        # Validate required fields
        if not all(field in game_data for field in ['title', 'description', 'html']):
            return None
        
        # Enhance HTML if needed
        html = game_data['html']
        if not html.startswith('<!DOCTYPE html>'):
            html = wrap_html(html, game_data['title'], game_data['description'])
        
        return {
            'title': clean_text(game_data['title'], 50),
            'description': clean_text(game_data['description'], 200),
            'genre': game_data.get('genre', 'custom'),
            'html': html
        }
        
    except Exception as e:
        print(f"❌ Parse error: {e}")
        return None

def clean_text(text, max_length):
    """Clean and limit text length"""
    text = str(text).strip()
    if len(text) > max_length:
        text = text[:max_length-3] + "..."
    return text

def wrap_html(html_content, title, description):
    """Wrap HTML content with proper structure"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-family: 'Arial', sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
        }}
        .game-header {{
            text-align: center;
            margin-bottom: 20px;
        }}
        .game-title {{
            font-size: 2.5em;
            margin: 0;
            background: linear-gradient(45deg, #f093fb, #f5576c);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }}
        .game-description {{
            font-size: 1.1em;
            margin: 10px 0;
            opacity: 0.9;
        }}
    </style>
</head>
<body>
    <div class="game-header">
        <h1 class="game-title">{title}</h1>
        <p class="game-description">{description}</p>
    </div>
    
    {html_content}
</body>
</html>"""

def generate_intelligent_game(description, game_id):
    """
    Generate intelligent games based on description analysis
    """
    description_lower = description.lower()
    
    # Analyze description for game type
    if any(word in description_lower for word in ['collect', 'gather', 'pick', 'find']):
        return create_collection_game(description, game_id)
    elif any(word in description_lower for word in ['avoid', 'dodge', 'escape', 'run']):
        return create_avoidance_game(description, game_id)
    elif any(word in description_lower for word in ['shoot', 'fire', 'blast', 'destroy']):
        return create_shooter_game(description, game_id)
    elif any(word in description_lower for word in ['jump', 'platform', 'climb', 'leap']):
        return create_platformer_game(description, game_id)
    elif any(word in description_lower for word in ['match', 'memory', 'remember', 'pair']):
        return create_memory_game(description, game_id)
    elif any(word in description_lower for word in ['type', 'word', 'letter', 'spell']):
        return create_typing_game(description, game_id)
    elif any(word in description_lower for word in ['race', 'drive', 'speed', 'fast']):
        return create_racing_game(description, game_id)
    else:
        return create_adventure_game(description, game_id)

def create_collection_game(description, game_id):
    """Create a collection-based game"""
    
    # Extract theme elements
    theme = extract_theme(description)
    
    title = f"{theme['collectible'].title()} Quest"
    desc = f"Collect {theme['collectible']} while avoiding {theme['obstacles']} in this {theme['environment']} adventure!"
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            background: {theme['bg_gradient']};
            color: white;
            font-family: 'Arial', sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
        }}
        .game-header {{
            text-align: center;
            margin-bottom: 20px;
        }}
        .game-title {{
            font-size: 2.5em;
            margin: 0;
            background: linear-gradient(45deg, #f093fb, #f5576c);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }}
        .game-description {{
            font-size: 1.1em;
            margin: 10px 0;
            opacity: 0.9;
        }}
        #gameCanvas {{
            border: 3px solid #f093fb;
            border-radius: 10px;
            background: rgba(0,0,0,0.3);
            box-shadow: 0 0 20px rgba(240, 147, 251, 0.3);
        }}
        .game-info {{
            display: flex;
            justify-content: space-between;
            width: 600px;
            max-width: 90vw;
            margin: 10px 0;
            font-size: 1.2em;
        }}
        .controls {{
            margin-top: 20px;
            text-align: center;
            opacity: 0.8;
        }}
        .mobile-controls {{
            display: none;
            margin-top: 20px;
            gap: 10px;
            flex-wrap: wrap;
            justify-content: center;
        }}
        .control-btn {{
            background: rgba(240, 147, 251, 0.2);
            border: 2px solid #f093fb;
            color: white;
            padding: 15px 20px;
            border-radius: 10px;
            font-size: 1em;
            cursor: pointer;
            user-select: none;
            touch-action: manipulation;
        }}
        .control-btn:active {{
            background: rgba(240, 147, 251, 0.4);
        }}
        @media (max-width: 768px) {{
            .mobile-controls {{ display: flex; }}
            .controls {{ display: none; }}
            #gameCanvas {{ width: 90vw; height: 60vh; }}
        }}
    </style>
</head>
<body>
    <div class="game-header">
        <h1 class="game-title">{title}</h1>
        <p class="game-description">{desc}</p>
    </div>
    
    <div class="game-info">
        <div>Score: <span id="score">0</span></div>
        <div>Collected: <span id="collected">0</span></div>
        <div>Time: <span id="timer">60</span>s</div>
    </div>
    
    <canvas id="gameCanvas" width="600" height="400"></canvas>
    
    <div class="controls">
        <p>🎮 Controls: Arrow Keys to Move</p>
    </div>
    
    <div class="mobile-controls">
        <button class="control-btn" id="leftBtn">⬅️</button>
        <button class="control-btn" id="upBtn">⬆️</button>
        <button class="control-btn" id="downBtn">⬇️</button>
        <button class="control-btn" id="rightBtn">➡️</button>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        
        // Responsive canvas
        function resizeCanvas() {{
            if (window.innerWidth <= 768) {{
                canvas.width = Math.min(window.innerWidth * 0.9, 600);
                canvas.height = Math.min(window.innerHeight * 0.6, 400);
            }}
        }}
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);
        
        // Game state
        let score = 0;
        let collected = 0;
        let timeLeft = 60;
        let gameRunning = true;
        
        // Player
        const player = {{
            x: canvas.width / 2,
            y: canvas.height / 2,
            width: 20,
            height: 20,
            speed: 4,
            color: '{theme['player_color']}'
        }};
        
        // Game objects
        let collectibles = [];
        let obstacles = [];
        
        // Input handling
        const keys = {{}};
        let mobileControls = {{
            left: false,
            right: false,
            up: false,
            down: false
        }};
        
        // Keyboard controls
        document.addEventListener('keydown', (e) => {{
            keys[e.code] = true;
            e.preventDefault();
        }});
        
        document.addEventListener('keyup', (e) => {{
            keys[e.code] = false;
            e.preventDefault();
        }});
        
        // Mobile controls
        ['left', 'right', 'up', 'down'].forEach(direction => {{
            const btn = document.getElementById(direction + 'Btn');
            if (btn) {{
                btn.addEventListener('touchstart', (e) => {{
                    e.preventDefault();
                    mobileControls[direction] = true;
                    btn.style.background = 'rgba(240, 147, 251, 0.4)';
                }});
                btn.addEventListener('touchend', (e) => {{
                    e.preventDefault();
                    mobileControls[direction] = false;
                    btn.style.background = 'rgba(240, 147, 251, 0.2)';
                }});
                btn.addEventListener('mousedown', (e) => {{
                    e.preventDefault();
                    mobileControls[direction] = true;
                    btn.style.background = 'rgba(240, 147, 251, 0.4)';
                }});
                btn.addEventListener('mouseup', (e) => {{
                    e.preventDefault();
                    mobileControls[direction] = false;
                    btn.style.background = 'rgba(240, 147, 251, 0.2)';
                }});
            }}
        }});
        
        function spawnCollectible() {{
            if (Math.random() < 0.03 && collectibles.length < 5) {{
                collectibles.push({{
                    x: Math.random() * (canvas.width - 15),
                    y: Math.random() * (canvas.height - 15),
                    width: 15,
                    height: 15,
                    color: '{theme['collectible_color']}',
                    collected: false,
                    pulse: 0
                }});
            }}
        }}
        
        function spawnObstacle() {{
            if (Math.random() < 0.015 && obstacles.length < 3) {{
                obstacles.push({{
                    x: Math.random() * (canvas.width - 20),
                    y: -20,
                    width: 20,
                    height: 20,
                    speed: 2 + Math.random() * 2,
                    color: '{theme['obstacle_color']}'
                }});
            }}
        }}
        
        function update() {{
            if (!gameRunning) return;
            
            // Move player
            let newX = player.x;
            let newY = player.y;
            
            if (keys['ArrowLeft'] || keys['KeyA'] || mobileControls.left) {{
                newX = Math.max(0, player.x - player.speed);
            }}
            if (keys['ArrowRight'] || keys['KeyD'] || mobileControls.right) {{
                newX = Math.min(canvas.width - player.width, player.x + player.speed);
            }}
            if (keys['ArrowUp'] || keys['KeyW'] || mobileControls.up) {{
                newY = Math.max(0, player.y - player.speed);
            }}
            if (keys['ArrowDown'] || keys['KeyS'] || mobileControls.down) {{
                newY = Math.min(canvas.height - player.height, player.y + player.speed);
            }}
            
            player.x = newX;
            player.y = newY;
            
            // Spawn items
            spawnCollectible();
            spawnObstacle();
            
            // Update collectibles
            collectibles.forEach(item => {{
                item.pulse += 0.1;
            }});
            
            // Move obstacles
            obstacles.forEach(obstacle => {{
                obstacle.y += obstacle.speed;
            }});
            
            // Remove off-screen obstacles
            obstacles = obstacles.filter(obstacle => obstacle.y < canvas.height + 50);
            
            // Check collectible collisions
            collectibles.forEach((item, index) => {{
                if (!item.collected &&
                    player.x < item.x + item.width &&
                    player.x + player.width > item.x &&
                    player.y < item.y + item.height &&
                    player.y + player.height > item.y) {{
                    item.collected = true;
                    collected++;
                    score += 10;
                    document.getElementById('collected').textContent = collected;
                    document.getElementById('score').textContent = score;
                    
                    // Haptic feedback
                    if (navigator.vibrate) {{
                        navigator.vibrate(50);
                    }}
                }}
            }});
            
            // Remove collected items
            collectibles = collectibles.filter(item => !item.collected);
            
            // Check obstacle collisions
            obstacles.forEach(obstacle => {{
                if (player.x < obstacle.x + obstacle.width &&
                    player.x + player.width > obstacle.x &&
                    player.y < obstacle.y + obstacle.height &&
                    player.y + player.height > obstacle.y) {{
                    gameRunning = false;
                    if (navigator.vibrate) {{
                        navigator.vibrate([100, 50, 100]);
                    }}
                    setTimeout(() => {{
                        alert(`Game Over! You collected ${{collected}} {theme['collectible']} and scored ${{score}} points!`);
                    }}, 100);
                }}
            }});
        }}
        
        function draw() {{
            // Clear canvas with fade effect
            ctx.fillStyle = 'rgba(0,0,0,0.1)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Draw collectibles with pulse effect
            collectibles.forEach(item => {{
                if (!item.collected) {{
                    const pulseSize = 2 + Math.sin(item.pulse) * 2;
                    ctx.fillStyle = item.color;
                    ctx.beginPath();
                    ctx.arc(
                        item.x + item.width/2, 
                        item.y + item.height/2, 
                        item.width/2 + pulseSize, 
                        0, Math.PI * 2
                    );
                    ctx.fill();
                    
                    // Glow effect
                    ctx.shadowColor = item.color;
                    ctx.shadowBlur = 10;
                    ctx.fill();
                    ctx.shadowBlur = 0;
                }}
            }});
            
            // Draw obstacles
            ctx.fillStyle = obstacles[0]?.color || '#e74c3c';
            obstacles.forEach(obstacle => {{
                ctx.fillRect(obstacle.x, obstacle.y, obstacle.width, obstacle.height);
                
                // Add danger glow
                ctx.shadowColor = obstacle.color;
                ctx.shadowBlur = 5;
                ctx.fillRect(obstacle.x, obstacle.y, obstacle.width, obstacle.height);
                ctx.shadowBlur = 0;
            }});
            
            // Draw player with glow
            ctx.fillStyle = player.color;
            ctx.shadowColor = player.color;
            ctx.shadowBlur = 10;
            ctx.fillRect(player.x, player.y, player.width, player.height);
            ctx.shadowBlur = 0;
            
            // Player highlight
            ctx.fillStyle = 'rgba(255,255,255,0.3)';
            ctx.fillRect(player.x + 2, player.y + 2, player.width - 4, 4);
        }}
        
        function gameLoop() {{
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }}
        
        // Timer
        const timer = setInterval(() => {{
            if (gameRunning && timeLeft > 0) {{
                timeLeft--;
                document.getElementById('timer').textContent = timeLeft;
                if (timeLeft <= 0) {{
                    gameRunning = false;
                    clearInterval(timer);
                    setTimeout(() => {{
                        alert(`Time's up! You collected ${{collected}} {theme['collectible']} and scored ${{score}} points!`);
                    }}, 100);
                }}
            }}
        }}, 1000);
        
        // Start the game
        gameLoop();
        
        // Prevent scrolling on mobile
        document.addEventListener('touchmove', (e) => {{
            e.preventDefault();
        }}, {{ passive: false }});
    </script>
</body>
</html>"""
    
    return {
        "success": True,
        "game_id": game_id,
        "title": title,
        "description": desc,
        "genre": "collection",
        "html": html,
        "created_at": datetime.now().isoformat()
    }

def extract_theme(description):
    """Extract theme elements from description"""
    description_lower = description.lower()
    
    # Default theme
    theme = {
        'collectible': 'stars',
        'obstacles': 'meteors',
        'environment': 'space',
        'bg_gradient': 'linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 100%)',
        'player_color': '#74b9ff',
        'collectible_color': '#f1c40f',
        'obstacle_color': '#e74c3c'
    }
    
    # Fairy/magical theme
    if any(word in description_lower for word in ['fairy', 'magic', 'forest', 'mushroom', 'spirit']):
        theme.update({
            'collectible': 'magical mushrooms',
            'obstacles': 'dark spirits',
            'environment': 'enchanted forest',
            'bg_gradient': 'linear-gradient(135deg, #2d5016 0%, #0f3460 100%)',
            'player_color': '#ff7675',
            'collectible_color': '#00b894',
            'obstacle_color': '#2d3436'
        })
    
    # Ocean theme
    elif any(word in description_lower for word in ['ocean', 'sea', 'fish', 'underwater', 'coral']):
        theme.update({
            'collectible': 'pearls',
            'obstacles': 'sharks',
            'environment': 'underwater',
            'bg_gradient': 'linear-gradient(135deg, #0984e3 0%, #00cec9 100%)',
            'player_color': '#fd79a8',
            'collectible_color': '#f8f9fa',
            'obstacle_color': '#636e72'
        })
    
    # Space theme
    elif any(word in description_lower for word in ['space', 'alien', 'planet', 'rocket', 'galaxy']):
        theme.update({
            'collectible': 'crystals',
            'obstacles': 'asteroids',
            'environment': 'deep space',
            'bg_gradient': 'linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 100%)',
            'player_color': '#00cec9',
            'collectible_color': '#fd79a8',
            'obstacle_color': '#e17055'
        })
    
    return theme

def create_adventure_game(description, game_id):
    """Create a simple adventure game"""
    title = "Custom Adventure"
    desc = f"An adventure inspired by: {description[:50]}..."
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-family: 'Arial', sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
        }}
        .game-header {{
            text-align: center;
            margin-bottom: 20px;
        }}
        .game-title {{
            font-size: 2.5em;
            margin: 0;
            background: linear-gradient(45deg, #f093fb, #f5576c);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }}
        .game-description {{
            font-size: 1.1em;
            margin: 10px 0;
            opacity: 0.9;
        }}
        .game-area {{
            background: rgba(0,0,0,0.3);
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            max-width: 500px;
            min-height: 300px;
        }}
        .action-btn {{
            background: linear-gradient(135deg, #f093fb, #f5576c);
            border: none;
            color: white;
            padding: 15px 30px;
            border-radius: 25px;
            font-size: 1.1em;
            cursor: pointer;
            margin: 10px;
            transition: all 0.3s ease;
            touch-action: manipulation;
        }}
        .action-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }}
        .action-btn:active {{
            transform: translateY(0);
        }}
        .score {{
            font-size: 1.5em;
            margin: 20px 0;
        }}
        .story-text {{
            font-size: 1.2em;
            line-height: 1.6;
            margin: 20px 0;
            min-height: 100px;
        }}
    </style>
</head>
<body>
    <div class="game-header">
        <h1 class="game-title">{title}</h1>
        <p class="game-description">{desc}</p>
    </div>
    
    <div class="game-area">
        <div class="score">Score: <span id="score">0</span></div>
        <div class="story-text" id="gameText">Welcome to your custom adventure! Your journey begins now...</div>
        <button class="action-btn" onclick="playGame()">🎮 Continue Adventure</button>
        <button class="action-btn" onclick="resetGame()">🔄 Start Over</button>
    </div>

    <script>
        let score = 0;
        let gameState = 0;
        
        const gameTexts = [
            "You find yourself in a world inspired by your imagination: {description[:100]}...",
            "A mysterious challenge appears before you. Do you accept it?",
            "You discover something amazing! Your adventure continues...",
            "The path ahead splits in two directions. Which way will you go?",
            "You've overcome the challenge! Your skills are improving.",
            "A new discovery awaits! What secrets will you uncover?",
            "The adventure reaches its climax. Are you ready for the final challenge?",
            "🎉 Congratulations! You've completed your custom adventure!"
        ];
        
        function playGame() {{
            if (gameState < gameTexts.length - 1) {{
                score += Math.floor(Math.random() * 20) + 10;
                gameState++;
                
                document.getElementById('score').textContent = score;
                document.getElementById('gameText').textContent = gameTexts[gameState];
                
                // Haptic feedback
                if (navigator.vibrate) {{
                    navigator.vibrate(50);
                }}
                
                if (gameState >= gameTexts.length - 1) {{
                    document.querySelector('.action-btn').textContent = '🏆 Adventure Complete!';
                }}
            }}
        }}
        
        function resetGame() {{
            score = 0;
            gameState = 0;
            document.getElementById('score').textContent = score;
            document.getElementById('gameText').textContent = gameTexts[0];
            document.querySelector('.action-btn').textContent = '🎮 Continue Adventure';
            
            // Haptic feedback
            if (navigator.vibrate) {{
                navigator.vibrate(100);
            }}
        }}
        
        // Auto-start the adventure
        setTimeout(() => {{
            document.getElementById('gameText').textContent = gameTexts[0];
        }}, 1000);
    </script>
</body>
</html>"""
    
    return {
        "success": True,
        "game_id": game_id,
        "title": title,
        "description": desc,
        "genre": "adventure",
        "html": html,
        "created_at": datetime.now().isoformat()
    }

def generate_simple_fallback(description, game_id):
    """Simple fallback when everything else fails"""
    return {
        "success": True,
        "game_id": game_id,
        "title": "Simple Game",
        "description": f"A simple game based on: {description[:50]}...",
        "genre": "simple",
        "html": """<!DOCTYPE html>
<html><head><title>Simple Game</title></head>
<body style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-align: center; padding: 50px;">
<h1>🎮 Simple Game</h1>
<p>Click the button to play!</p>
<button onclick="alert('You scored ' + Math.floor(Math.random()*100) + ' points!')" style="padding: 20px; font-size: 20px; background: #f093fb; color: white; border: none; border-radius: 10px; cursor: pointer;">Play Game</button>
</body></html>""",
        "created_at": datetime.now().isoformat()
    }

# Additional game creation functions can be added here...
# (create_avoidance_game, create_shooter_game, etc.)

# Export the main function
__all__ = ['generate_game']
