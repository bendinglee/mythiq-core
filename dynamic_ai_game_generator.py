#!/usr/bin/env python3
"""
🤖 DYNAMIC AI GAME GENERATOR
Creates completely unique games from any user prompt using AI
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
    Generate a completely unique game based on any user description
    Uses AI to create custom game mechanics, rules, and code
    """
    try:
        # Clean and analyze the description
        description = description.strip()
        if not description:
            description = "a fun game"
        
        # Generate unique game ID
        timestamp = str(int(time.time()))
        game_id = f"game_{timestamp}_{hashlib.md5(description.encode()).hexdigest()[:6]}"
        
        # Use AI to generate the complete game
        game_data = generate_ai_game(description, game_id)
        
        if game_data:
            return {
                "success": True,
                "game_id": game_id,
                "title": game_data["title"],
                "description": game_data["description"],
                "genre": game_data["genre"],
                "html": game_data["html"],
                "created_at": datetime.now().isoformat()
            }
        else:
            # Fallback if AI fails
            return create_intelligent_fallback(description, game_id)
            
    except Exception as e:
        print(f"Game generation error: {e}")
        return create_intelligent_fallback(description, game_id)

def generate_ai_game(description, game_id):
    """
    Use AI to generate a completely custom game from the description
    """
    try:
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            return None
            
        # Create a comprehensive prompt for AI game generation
        prompt = create_game_generation_prompt(description)
        
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
            
            # Parse the AI response
            return parse_ai_game_response(content, game_id)
            
    except Exception as e:
        print(f"AI generation error: {e}")
    
    return None

def create_game_generation_prompt(description):
    """
    Create a comprehensive prompt for AI game generation
    """
    return f"""You are an expert game developer. Create a complete, playable HTML5 game based on this description: "{description}"

IMPORTANT: Respond with ONLY a JSON object in this exact format:
{{
    "title": "Game Title (2-4 words)",
    "description": "Brief game description (1 sentence)",
    "genre": "detected genre",
    "mechanics": "core game mechanics description",
    "html": "complete HTML game code"
}}

GAME REQUIREMENTS:
1. Create a UNIQUE game that matches the user's description exactly
2. Include complete HTML, CSS, and JavaScript in the "html" field
3. Make it fully playable with proper game mechanics
4. Add mobile touch controls AND keyboard controls
5. Include scoring, win/lose conditions, and proper game loop
6. Use modern CSS with gradients and animations
7. Make it responsive for all screen sizes

GAME MECHANICS GUIDELINES:
- If description mentions specific mechanics, implement them exactly
- If description is vague, create interesting mechanics that fit the theme
- Always include player interaction, objectives, and feedback
- Add sound effects using Web Audio API if possible
- Include particle effects or animations for polish

TECHNICAL REQUIREMENTS:
- Complete HTML document with <!DOCTYPE html>
- Embedded CSS in <style> tags
- Embedded JavaScript in <script> tags
- Canvas-based games for complex graphics
- DOM-based games for simpler mechanics
- Mobile-first responsive design
- Touch event handling for mobile
- Keyboard event handling for desktop

EXAMPLES OF WHAT TO CREATE:
- "A game about collecting stars" → Create a character that moves around collecting falling stars with obstacles
- "A typing game" → Create a typing challenge with falling words to type
- "A memory game" → Create a card matching or sequence memory game
- "A tower defense game" → Create towers that shoot at moving enemies
- "A fishing game" → Create a fishing mechanic with different fish and timing
- "A cooking game" → Create ingredient mixing and timing mechanics

Remember: Create a COMPLETELY UNIQUE game that matches the user's exact description. Don't use templates - generate fresh, creative gameplay!

Respond with ONLY the JSON object, no other text."""

def parse_ai_game_response(content, game_id):
    """
    Parse the AI response and extract game data
    """
    try:
        # Clean up the response
        content = content.strip()
        
        # Remove code blocks if present
        if content.startswith('```json'):
            content = content.replace('```json', '').replace('```', '').strip()
        elif content.startswith('```'):
            content = content.replace('```', '').strip()
        
        # Try to find JSON in the response
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            content = json_match.group()
        
        # Parse JSON
        game_data = json.loads(content)
        
        # Validate required fields
        required_fields = ['title', 'description', 'genre', 'html']
        for field in required_fields:
            if field not in game_data:
                return None
        
        # Enhance the HTML with proper structure
        html = game_data['html']
        if not html.startswith('<!DOCTYPE html>'):
            html = enhance_html_structure(html, game_data['title'], game_data['description'])
        
        return {
            'title': game_data['title'][:50],  # Limit title length
            'description': game_data['description'][:200],  # Limit description length
            'genre': game_data.get('genre', 'custom'),
            'html': html
        }
        
    except Exception as e:
        print(f"Parse error: {e}")
        return None

def enhance_html_structure(html_content, title, description):
    """
    Enhance HTML with proper structure if needed
    """
    if '<!DOCTYPE html>' in html_content:
        return html_content
    
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

def create_intelligent_fallback(description, game_id):
    """
    Create an intelligent fallback game based on description analysis
    """
    # Analyze the description for key elements
    description_lower = description.lower()
    
    # Extract key concepts
    concepts = extract_game_concepts(description_lower)
    
    # Generate a custom game based on concepts
    if 'collect' in concepts or 'gather' in concepts:
        return create_collection_game(description, game_id, concepts)
    elif 'avoid' in concepts or 'dodge' in concepts:
        return create_avoidance_game(description, game_id, concepts)
    elif 'shoot' in concepts or 'fire' in concepts:
        return create_shooting_game(description, game_id, concepts)
    elif 'jump' in concepts or 'platform' in concepts:
        return create_jumping_game(description, game_id, concepts)
    elif 'match' in concepts or 'memory' in concepts:
        return create_matching_game(description, game_id, concepts)
    elif 'type' in concepts or 'word' in concepts:
        return create_typing_game(description, game_id, concepts)
    elif 'build' in concepts or 'create' in concepts:
        return create_building_game(description, game_id, concepts)
    else:
        return create_adaptive_game(description, game_id, concepts)

def extract_game_concepts(description):
    """
    Extract game concepts from description
    """
    concepts = []
    
    # Action words
    action_words = ['collect', 'gather', 'avoid', 'dodge', 'shoot', 'fire', 'jump', 'run', 'fly', 
                   'match', 'memory', 'type', 'write', 'build', 'create', 'destroy', 'fight',
                   'race', 'drive', 'swim', 'climb', 'solve', 'puzzle', 'strategy']
    
    # Object words
    object_words = ['star', 'coin', 'gem', 'enemy', 'alien', 'monster', 'car', 'plane', 'ship',
                   'ball', 'block', 'tile', 'card', 'word', 'letter', 'number', 'color',
                   'animal', 'food', 'treasure', 'key', 'door', 'platform', 'obstacle']
    
    # Environment words
    env_words = ['space', 'ocean', 'forest', 'city', 'desert', 'mountain', 'cave', 'sky',
                'underwater', 'underground', 'castle', 'house', 'school', 'park', 'beach']
    
    all_words = action_words + object_words + env_words
    
    for word in all_words:
        if word in description:
            concepts.append(word)
    
    return concepts

def create_collection_game(description, game_id, concepts):
    """
    Create a dynamic collection game based on the description
    """
    # Determine what to collect
    collectible = 'stars'
    if 'coin' in concepts: collectible = 'coins'
    elif 'gem' in concepts: collectible = 'gems'
    elif 'treasure' in concepts: collectible = 'treasures'
    elif 'food' in concepts: collectible = 'food items'
    
    # Determine environment
    bg_color = '#667eea'
    if 'space' in concepts: bg_color = '#0c0c0c'
    elif 'ocean' in concepts: bg_color = '#74b9ff'
    elif 'forest' in concepts: bg_color = '#00b894'
    
    title = f"{collectible.title()} Collector"
    desc = f"Collect as many {collectible} as possible while avoiding obstacles!"
    
    html = create_collection_game_html(title, desc, collectible, bg_color)
    
    return {
        "success": True,
        "game_id": game_id,
        "title": title,
        "description": desc,
        "genre": "collection",
        "html": html,
        "created_at": datetime.now().isoformat()
    }

def create_collection_game_html(title, description, collectible, bg_color):
    """
    Generate HTML for a collection game
    """
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
            background: linear-gradient(135deg, {bg_color} 0%, #764ba2 100%);
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
            gap: 20px;
        }}
        .control-btn {{
            background: rgba(240, 147, 251, 0.2);
            border: 2px solid #f093fb;
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            font-size: 1.1em;
            cursor: pointer;
            user-select: none;
        }}
        .control-btn:active {{
            background: rgba(240, 147, 251, 0.4);
        }}
        @media (max-width: 768px) {{
            .mobile-controls {{ display: flex; flex-wrap: wrap; justify-content: center; }}
            .controls {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="game-header">
        <h1 class="game-title">{title}</h1>
        <p class="game-description">{description}</p>
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
        <button class="control-btn" id="leftBtn">← Left</button>
        <button class="control-btn" id="rightBtn">Right →</button>
        <button class="control-btn" id="upBtn">⬆ Up</button>
        <button class="control-btn" id="downBtn">⬇ Down</button>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        
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
            speed: 4
        }};
        
        // Collectibles and obstacles
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
        
        document.addEventListener('keydown', (e) => {{
            keys[e.code] = true;
        }});
        
        document.addEventListener('keyup', (e) => {{
            keys[e.code] = false;
        }});
        
        // Mobile controls
        ['left', 'right', 'up', 'down'].forEach(direction => {{
            const btn = document.getElementById(direction + 'Btn');
            btn.addEventListener('touchstart', (e) => {{
                e.preventDefault();
                mobileControls[direction] = true;
            }});
            btn.addEventListener('touchend', (e) => {{
                e.preventDefault();
                mobileControls[direction] = false;
            }});
        }});
        
        function spawnCollectible() {{
            if (Math.random() < 0.03) {{
                collectibles.push({{
                    x: Math.random() * (canvas.width - 15),
                    y: Math.random() * (canvas.height - 15),
                    width: 15,
                    height: 15,
                    collected: false
                }});
            }}
        }}
        
        function spawnObstacle() {{
            if (Math.random() < 0.01) {{
                obstacles.push({{
                    x: Math.random() * (canvas.width - 20),
                    y: -20,
                    width: 20,
                    height: 20,
                    speed: 2 + Math.random() * 2
                }});
            }}
        }}
        
        function update() {{
            if (!gameRunning) return;
            
            // Move player
            if (keys['ArrowLeft'] || mobileControls.left) {{
                player.x = Math.max(0, player.x - player.speed);
            }}
            if (keys['ArrowRight'] || mobileControls.right) {{
                player.x = Math.min(canvas.width - player.width, player.x + player.speed);
            }}
            if (keys['ArrowUp'] || mobileControls.up) {{
                player.y = Math.max(0, player.y - player.speed);
            }}
            if (keys['ArrowDown'] || mobileControls.down) {{
                player.y = Math.min(canvas.height - player.height, player.y + player.speed);
            }}
            
            // Spawn items
            spawnCollectible();
            spawnObstacle();
            
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
                    alert(`Game Over! You collected ${{collected}} {collectible} and scored ${{score}} points!`);
                }}
            }});
        }}
        
        function draw() {{
            // Clear canvas
            ctx.fillStyle = 'rgba(0,0,0,0.1)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Draw collectibles
            ctx.fillStyle = '#f1c40f';
            collectibles.forEach(item => {{
                if (!item.collected) {{
                    ctx.beginPath();
                    ctx.arc(item.x + item.width/2, item.y + item.height/2, item.width/2, 0, Math.PI * 2);
                    ctx.fill();
                }}
            }});
            
            // Draw obstacles
            ctx.fillStyle = '#e74c3c';
            obstacles.forEach(obstacle => {{
                ctx.fillRect(obstacle.x, obstacle.y, obstacle.width, obstacle.height);
            }});
            
            // Draw player
            ctx.fillStyle = '#3498db';
            ctx.fillRect(player.x, player.y, player.width, player.height);
            
            // Player highlight
            ctx.fillStyle = '#74b9ff';
            ctx.fillRect(player.x + 2, player.y + 2, player.width - 4, 4);
        }}
        
        function gameLoop() {{
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }}
        
        // Timer
        setInterval(() => {{
            if (gameRunning && timeLeft > 0) {{
                timeLeft--;
                document.getElementById('timer').textContent = timeLeft;
                if (timeLeft <= 0) {{
                    gameRunning = false;
                    alert(`Time's up! You collected ${{collected}} {collectible} and scored ${{score}} points!`);
                }}
            }}
        }}, 1000);
        
        // Start the game
        gameLoop();
    </script>
</body>
</html>"""

def create_adaptive_game(description, game_id, concepts):
    """
    Create an adaptive game when no specific pattern is detected
    """
    title = "Custom Adventure"
    desc = f"A unique game inspired by: {description[:50]}..."
    
    # Create a simple but engaging game
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
        }}
        .action-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }}
        .score {{
            font-size: 1.5em;
            margin: 20px 0;
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
        <div id="gameText">Welcome to your custom adventure! Click to start exploring.</div>
        <button class="action-btn" onclick="playGame()">🎮 Play</button>
        <button class="action-btn" onclick="resetGame()">🔄 Reset</button>
    </div>

    <script>
        let score = 0;
        let gameState = 0;
        
        const gameTexts = [
            "You find yourself in a mysterious world inspired by your imagination...",
            "A challenge appears! Do you accept it?",
            "You discover something amazing! Your score increases!",
            "The adventure continues... What will you do next?",
            "You've mastered this challenge! Ready for the next one?"
        ];
        
        function playGame() {{
            score += Math.floor(Math.random() * 20) + 10;
            gameState = (gameState + 1) % gameTexts.length;
            
            document.getElementById('score').textContent = score;
            document.getElementById('gameText').textContent = gameTexts[gameState];
            
            if (score >= 100) {{
                document.getElementById('gameText').textContent = "🎉 Congratulations! You've completed your custom adventure!";
            }}
        }}
        
        function resetGame() {{
            score = 0;
            gameState = 0;
            document.getElementById('score').textContent = score;
            document.getElementById('gameText').textContent = gameTexts[0];
        }}
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

# Additional game creation functions would go here...
# (create_avoidance_game, create_shooting_game, etc.)

# Export the main function
__all__ = ['generate_game']
