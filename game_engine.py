#!/usr/bin/env python3
"""
🎮 REAL AI Game Engine - Generates Unique Games for Each Genre
Creates completely different games, not just themed versions of the same puzzle
"""

import os
import json
import time
import random
import string
import requests
from typing import Dict, Any, List

class RealGameEngine:
    def __init__(self):
        self.groq_api_key = os.environ.get('GROQ_API_KEY')
        self.groq_api_url = "https://api.groq.com/openai/v1/chat/completions"
        
        # Game templates for different genres
        self.game_templates = {
            'puzzle': self.create_puzzle_game,
            'shooter': self.create_shooter_game,
            'platformer': self.create_platformer_game,
            'racing': self.create_racing_game,
            'rpg': self.create_rpg_game,
            'strategy': self.create_strategy_game
        }
    
    def create_complete_game(self, prompt: str) -> Dict[str, Any]:
        """Create a complete game based on user prompt"""
        try:
            # Generate game concept
            concept = self.generate_game_concept(prompt)
            if not concept:
                return self.create_fallback_game(prompt)
            
            # Determine genre
            genre = concept.get('genre', 'puzzle').lower()
            
            # Create the actual game based on genre
            game_creator = self.game_templates.get(genre, self.create_puzzle_game)
            game_code = game_creator(concept)
            
            # Generate unique game ID
            game_id = f"game_{int(time.time())}_{self.generate_random_id()}"
            
            return {
                'status': 'success',
                'game': {
                    'id': game_id,
                    'title': concept.get('title', 'Untitled Game'),
                    'description': concept.get('description', 'A fun game'),
                    'genre': genre,
                    'concept': concept,
                    'code': game_code,
                    'created_at': time.time()
                }
            }
            
        except Exception as e:
            print(f"Error creating game: {e}")
            return self.create_fallback_game(prompt)
    
    def generate_game_concept(self, prompt: str) -> Dict[str, Any]:
        """Generate game concept using AI"""
        if not self.groq_api_key:
            return self.create_simple_concept(prompt)
        
        try:
            headers = {
                'Authorization': f'Bearer {self.groq_api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': 'llama-3.1-8b-instant',
                'messages': [
                    {
                        'role': 'system',
                        'content': '''You are a game designer. Create a game concept based on the user's prompt. 
                        Respond with ONLY a JSON object containing:
                        {
                            "title": "Game Title",
                            "description": "Brief description",
                            "genre": "puzzle|shooter|platformer|racing|rpg|strategy",
                            "theme": "visual theme",
                            "mechanics": "core gameplay mechanics"
                        }'''
                    },
                    {
                        'role': 'user',
                        'content': f'Create a game concept for: {prompt}'
                    }
                ],
                'temperature': 0.7,
                'max_tokens': 200
            }
            
            response = requests.post(self.groq_api_url, headers=headers, json=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content'].strip()
                
                # Try to parse JSON
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    # Extract JSON from response if wrapped in text
                    start = content.find('{')
                    end = content.rfind('}') + 1
                    if start >= 0 and end > start:
                        return json.loads(content[start:end])
                    
        except Exception as e:
            print(f"AI generation error: {e}")
        
        return self.create_simple_concept(prompt)
    
    def create_simple_concept(self, prompt: str) -> Dict[str, Any]:
        """Create a simple concept based on keywords"""
        prompt_lower = prompt.lower()
        
        # Determine genre from keywords
        if any(word in prompt_lower for word in ['shoot', 'gun', 'alien', 'space', 'defend']):
            genre = 'shooter'
            title = 'Space Defender'
            description = 'Defend against alien invaders in this action-packed shooter'
        elif any(word in prompt_lower for word in ['jump', 'platform', 'run', 'coin']):
            genre = 'platformer'
            title = 'Platform Adventure'
            description = 'Jump and run through challenging platforms'
        elif any(word in prompt_lower for word in ['race', 'car', 'speed', 'drive']):
            genre = 'racing'
            title = 'Speed Racer'
            description = 'Race through challenging tracks at high speed'
        elif any(word in prompt_lower for word in ['rpg', 'adventure', 'dungeon', 'quest', 'monster']):
            genre = 'rpg'
            title = 'Epic Quest'
            description = 'Embark on an epic adventure through mysterious lands'
        elif any(word in prompt_lower for word in ['strategy', 'build', 'manage', 'city']):
            genre = 'strategy'
            title = 'City Builder'
            description = 'Build and manage your own thriving city'
        else:
            genre = 'puzzle'
            title = 'Mind Bender'
            description = 'Challenge your mind with this engaging puzzle'
        
        return {
            'title': title,
            'description': description,
            'genre': genre,
            'theme': 'colorful',
            'mechanics': 'interactive gameplay'
        }
    
    def create_puzzle_game(self, concept: Dict[str, Any]) -> Dict[str, str]:
        """Create a sliding puzzle game"""
        title = concept.get('title', 'Puzzle Game')
        description = concept.get('description', 'A challenging puzzle')
        
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .game-container {{
            background: rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 20px;
            text-align: center;
            backdrop-filter: blur(10px);
            max-width: 500px;
            width: 100%;
        }}
        .game-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 5px;
            margin: 20px 0;
            max-width: 320px;
            margin-left: auto;
            margin-right: auto;
        }}
        .tile {{
            width: 70px;
            height: 70px;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: bold;
            color: white;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        .tile:hover {{
            transform: scale(1.05);
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }}
        .empty {{
            background: transparent;
            cursor: default;
        }}
        .stats {{
            display: flex;
            justify-content: space-around;
            margin: 20px 0;
        }}
        .btn {{
            padding: 10px 20px;
            margin: 5px;
            border: none;
            border-radius: 20px;
            background: linear-gradient(45deg, #2ecc71, #27ae60);
            color: white;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        .btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }}
        @media (max-width: 480px) {{
            .tile {{
                width: 60px;
                height: 60px;
                font-size: 16px;
            }}
        }}
    </style>
</head>
<body>
    <div class="game-container">
        <h1>{title}</h1>
        <p>{description}</p>
        
        <div class="stats">
            <div><strong>Moves</strong><br><span id="moves">0</span></div>
            <div><strong>Time</strong><br><span id="time">00:00</span></div>
        </div>
        
        <div class="game-grid" id="gameGrid"></div>
        
        <button class="btn" onclick="newGame()">🎲 New Game</button>
        <button class="btn" onclick="solve()">✨ Solve</button>
    </div>
    
    <script>
        let tiles = [];
        let moves = 0;
        let startTime = Date.now();
        let timer;
        
        function initGame() {{
            tiles = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0];
            shuffle();
            render();
            startTimer();
        }}
        
        function shuffle() {{
            for (let i = 0; i < 1000; i++) {{
                const emptyIndex = tiles.indexOf(0);
                const neighbors = getNeighbors(emptyIndex);
                const randomNeighbor = neighbors[Math.floor(Math.random() * neighbors.length)];
                swap(emptyIndex, randomNeighbor);
            }}
        }}
        
        function getNeighbors(index) {{
            const neighbors = [];
            const row = Math.floor(index / 4);
            const col = index % 4;
            
            if (row > 0) neighbors.push(index - 4);
            if (row < 3) neighbors.push(index + 4);
            if (col > 0) neighbors.push(index - 1);
            if (col < 3) neighbors.push(index + 1);
            
            return neighbors;
        }}
        
        function swap(i, j) {{
            [tiles[i], tiles[j]] = [tiles[j], tiles[i]];
        }}
        
        function render() {{
            const grid = document.getElementById('gameGrid');
            grid.innerHTML = '';
            
            tiles.forEach((tile, index) => {{
                const button = document.createElement('button');
                button.className = tile === 0 ? 'tile empty' : 'tile';
                button.textContent = tile === 0 ? '' : tile;
                button.onclick = () => moveTile(index);
                grid.appendChild(button);
            }});
        }}
        
        function moveTile(index) {{
            const emptyIndex = tiles.indexOf(0);
            const neighbors = getNeighbors(emptyIndex);
            
            if (neighbors.includes(index)) {{
                swap(index, emptyIndex);
                moves++;
                document.getElementById('moves').textContent = moves;
                render();
                
                if (isSolved()) {{
                    clearInterval(timer);
                    setTimeout(() => alert('Congratulations! You solved it!'), 100);
                }}
            }}
        }}
        
        function isSolved() {{
            for (let i = 0; i < 15; i++) {{
                if (tiles[i] !== i + 1) return false;
            }}
            return tiles[15] === 0;
        }}
        
        function newGame() {{
            moves = 0;
            document.getElementById('moves').textContent = moves;
            startTime = Date.now();
            initGame();
        }}
        
        function solve() {{
            tiles = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0];
            render();
            clearInterval(timer);
            alert('Puzzle solved!');
        }}
        
        function startTimer() {{
            timer = setInterval(() => {{
                const elapsed = Math.floor((Date.now() - startTime) / 1000);
                const minutes = Math.floor(elapsed / 60).toString().padStart(2, '0');
                const seconds = (elapsed % 60).toString().padStart(2, '0');
                document.getElementById('time').textContent = `${{minutes}}:${{seconds}}`;
            }}, 1000);
        }}
        
        initGame();
    </script>
</body>
</html>'''
        
        return {'html': html}
    
    def create_shooter_game(self, concept: Dict[str, Any]) -> Dict[str, str]:
        """Create a space shooter game"""
        title = concept.get('title', 'Space Shooter')
        description = concept.get('description', 'Defend against alien invaders')
        
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: #000;
            color: white;
            font-family: Arial, sans-serif;
            overflow: hidden;
        }}
        #gameCanvas {{
            display: block;
            margin: 0 auto;
            background: linear-gradient(180deg, #001122 0%, #000033 100%);
        }}
        .ui {{
            position: absolute;
            top: 10px;
            left: 10px;
            z-index: 10;
        }}
        .controls {{
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 10px;
        }}
        .control-btn {{
            width: 60px;
            height: 60px;
            background: rgba(255,255,255,0.2);
            border: 2px solid rgba(255,255,255,0.5);
            border-radius: 50%;
            color: white;
            font-size: 20px;
            cursor: pointer;
            user-select: none;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .shoot-btn {{
            width: 80px;
            height: 80px;
            background: rgba(255,0,0,0.3);
            border: 2px solid rgba(255,0,0,0.7);
        }}
        @media (min-width: 768px) {{
            .controls {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="ui">
        <div>Score: <span id="score">0</span></div>
        <div>Lives: <span id="lives">3</span></div>
    </div>
    
    <canvas id="gameCanvas" width="800" height="600"></canvas>
    
    <div class="controls">
        <div class="control-btn" id="leftBtn">←</div>
        <div class="control-btn" id="upBtn">↑</div>
        <div class="control-btn" id="downBtn">↓</div>
        <div class="control-btn" id="rightBtn">→</div>
        <div class="control-btn shoot-btn" id="shootBtn">🚀</div>
    </div>
    
    <div style="position: absolute; bottom: 10px; left: 50%; transform: translateX(-50%); text-align: center; font-size: 12px;">
        Desktop: Arrow Keys to Move | Spacebar to Shoot
    </div>
    
    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        
        // Responsive canvas
        function resizeCanvas() {{
            const maxWidth = window.innerWidth;
            const maxHeight = window.innerHeight - 100;
            const aspectRatio = 800 / 600;
            
            if (maxWidth / maxHeight > aspectRatio) {{
                canvas.style.height = maxHeight + 'px';
                canvas.style.width = (maxHeight * aspectRatio) + 'px';
            }} else {{
                canvas.style.width = maxWidth + 'px';
                canvas.style.height = (maxWidth / aspectRatio) + 'px';
            }}
        }}
        
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);
        
        // Game state
        let score = 0;
        let lives = 3;
        let gameRunning = true;
        
        // Player
        const player = {{
            x: 400,
            y: 500,
            width: 40,
            height: 30,
            speed: 5
        }};
        
        // Arrays for game objects
        let bullets = [];
        let enemies = [];
        let stars = [];
        
        // Input handling
        const keys = {{}};
        
        document.addEventListener('keydown', (e) => {{
            keys[e.code] = true;
            if (e.code === 'Space') {{
                e.preventDefault();
                shoot();
            }}
        }});
        
        document.addEventListener('keyup', (e) => {{
            keys[e.code] = false;
        }});
        
        // Mobile controls
        document.getElementById('leftBtn').addEventListener('touchstart', () => keys['ArrowLeft'] = true);
        document.getElementById('leftBtn').addEventListener('touchend', () => keys['ArrowLeft'] = false);
        document.getElementById('rightBtn').addEventListener('touchstart', () => keys['ArrowRight'] = true);
        document.getElementById('rightBtn').addEventListener('touchend', () => keys['ArrowRight'] = false);
        document.getElementById('upBtn').addEventListener('touchstart', () => keys['ArrowUp'] = true);
        document.getElementById('upBtn').addEventListener('touchend', () => keys['ArrowUp'] = false);
        document.getElementById('downBtn').addEventListener('touchstart', () => keys['ArrowDown'] = true);
        document.getElementById('downBtn').addEventListener('touchend', () => keys['ArrowDown'] = false);
        document.getElementById('shootBtn').addEventListener('touchstart', shoot);
        
        // Initialize stars
        for (let i = 0; i < 100; i++) {{
            stars.push({{
                x: Math.random() * 800,
                y: Math.random() * 600,
                speed: Math.random() * 2 + 1
            }});
        }}
        
        function shoot() {{
            bullets.push({{
                x: player.x + player.width / 2 - 2,
                y: player.y,
                width: 4,
                height: 10,
                speed: 7
            }});
        }}
        
        function spawnEnemy() {{
            enemies.push({{
                x: Math.random() * (800 - 30),
                y: -30,
                width: 30,
                height: 30,
                speed: Math.random() * 2 + 1
            }});
        }}
        
        function update() {{
            if (!gameRunning) return;
            
            // Move player
            if (keys['ArrowLeft'] && player.x > 0) player.x -= player.speed;
            if (keys['ArrowRight'] && player.x < 800 - player.width) player.x += player.speed;
            if (keys['ArrowUp'] && player.y > 0) player.y -= player.speed;
            if (keys['ArrowDown'] && player.y < 600 - player.height) player.y += player.speed;
            
            // Move stars
            stars.forEach(star => {{
                star.y += star.speed;
                if (star.y > 600) {{
                    star.y = 0;
                    star.x = Math.random() * 800;
                }}
            }});
            
            // Move bullets
            bullets = bullets.filter(bullet => {{
                bullet.y -= bullet.speed;
                return bullet.y > 0;
            }});
            
            // Move enemies
            enemies = enemies.filter(enemy => {{
                enemy.y += enemy.speed;
                return enemy.y < 600;
            }});
            
            // Spawn enemies
            if (Math.random() < 0.02) {{
                spawnEnemy();
            }}
            
            // Check collisions
            bullets.forEach((bullet, bulletIndex) => {{
                enemies.forEach((enemy, enemyIndex) => {{
                    if (bullet.x < enemy.x + enemy.width &&
                        bullet.x + bullet.width > enemy.x &&
                        bullet.y < enemy.y + enemy.height &&
                        bullet.y + bullet.height > enemy.y) {{
                        bullets.splice(bulletIndex, 1);
                        enemies.splice(enemyIndex, 1);
                        score += 10;
                        document.getElementById('score').textContent = score;
                    }}
                }});
            }});
            
            // Check player-enemy collisions
            enemies.forEach((enemy, enemyIndex) => {{
                if (player.x < enemy.x + enemy.width &&
                    player.x + player.width > enemy.x &&
                    player.y < enemy.y + enemy.height &&
                    player.y + player.height > enemy.y) {{
                    enemies.splice(enemyIndex, 1);
                    lives--;
                    document.getElementById('lives').textContent = lives;
                    if (lives <= 0) {{
                        gameRunning = false;
                        alert('Game Over! Final Score: ' + score);
                    }}
                }}
            }});
        }}
        
        function draw() {{
            // Clear canvas
            ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
            ctx.fillRect(0, 0, 800, 600);
            
            // Draw stars
            ctx.fillStyle = 'white';
            stars.forEach(star => {{
                ctx.fillRect(star.x, star.y, 1, 1);
            }});
            
            // Draw player
            ctx.fillStyle = '#00ff00';
            ctx.fillRect(player.x, player.y, player.width, player.height);
            
            // Draw bullets
            ctx.fillStyle = '#ffff00';
            bullets.forEach(bullet => {{
                ctx.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
            }});
            
            // Draw enemies
            ctx.fillStyle = '#ff0000';
            enemies.forEach(enemy => {{
                ctx.fillRect(enemy.x, enemy.y, enemy.width, enemy.height);
            }});
        }}
        
        function gameLoop() {{
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }}
        
        gameLoop();
    </script>
</body>
</html>'''
        
        return {'html': html}
    
    def create_platformer_game(self, concept: Dict[str, Any]) -> Dict[str, str]:
        """Create a platformer game"""
        title = concept.get('title', 'Platform Adventure')
        description = concept.get('description', 'Jump and run through platforms')
        
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: linear-gradient(180deg, #87CEEB 0%, #98FB98 100%);
            font-family: Arial, sans-serif;
            overflow: hidden;
        }}
        #gameCanvas {{
            display: block;
            margin: 0 auto;
            border: 2px solid #333;
        }}
        .ui {{
            position: absolute;
            top: 10px;
            left: 10px;
            color: #333;
            font-weight: bold;
        }}
        .controls {{
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 10px;
        }}
        .control-btn {{
            width: 60px;
            height: 60px;
            background: rgba(0,0,0,0.2);
            border: 2px solid rgba(0,0,0,0.5);
            border-radius: 10px;
            color: white;
            font-size: 20px;
            cursor: pointer;
            user-select: none;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        @media (min-width: 768px) {{
            .controls {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="ui">
        <div>Score: <span id="score">0</span></div>
        <div>Lives: <span id="lives">3</span></div>
    </div>
    
    <canvas id="gameCanvas" width="800" height="600"></canvas>
    
    <div class="controls">
        <div class="control-btn" id="leftBtn">←</div>
        <div class="control-btn" id="rightBtn">→</div>
        <div class="control-btn" id="jumpBtn">↑</div>
    </div>
    
    <div style="position: absolute; bottom: 10px; left: 50%; transform: translateX(-50%); text-align: center; font-size: 12px;">
        Desktop: Arrow Keys to Move | Space to Jump
    </div>
    
    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        
        // Responsive canvas
        function resizeCanvas() {{
            const maxWidth = window.innerWidth;
            const maxHeight = window.innerHeight - 100;
            const aspectRatio = 800 / 600;
            
            if (maxWidth / maxHeight > aspectRatio) {{
                canvas.style.height = maxHeight + 'px';
                canvas.style.width = (maxHeight * aspectRatio) + 'px';
            }} else {{
                canvas.style.width = maxWidth + 'px';
                canvas.style.height = (maxWidth / aspectRatio) + 'px';
            }}
        }}
        
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);
        
        // Game state
        let score = 0;
        let lives = 3;
        let gameRunning = true;
        
        // Player
        const player = {{
            x: 100,
            y: 400,
            width: 30,
            height: 40,
            velocityX: 0,
            velocityY: 0,
            speed: 5,
            jumpPower: 15,
            onGround: false
        }};
        
        // Platforms
        const platforms = [
            {{x: 0, y: 550, width: 800, height: 50}},
            {{x: 200, y: 450, width: 150, height: 20}},
            {{x: 400, y: 350, width: 150, height: 20}},
            {{x: 600, y: 250, width: 150, height: 20}},
            {{x: 100, y: 150, width: 150, height: 20}}
        ];
        
        // Coins
        let coins = [
            {{x: 250, y: 400, width: 20, height: 20, collected: false}},
            {{x: 450, y: 300, width: 20, height: 20, collected: false}},
            {{x: 650, y: 200, width: 20, height: 20, collected: false}},
            {{x: 150, y: 100, width: 20, height: 20, collected: false}}
        ];
        
        // Input handling
        const keys = {{}};
        
        document.addEventListener('keydown', (e) => {{
            keys[e.code] = true;
        }});
        
        document.addEventListener('keyup', (e) => {{
            keys[e.code] = false;
        }});
        
        // Mobile controls
        document.getElementById('leftBtn').addEventListener('touchstart', () => keys['ArrowLeft'] = true);
        document.getElementById('leftBtn').addEventListener('touchend', () => keys['ArrowLeft'] = false);
        document.getElementById('rightBtn').addEventListener('touchstart', () => keys['ArrowRight'] = true);
        document.getElementById('rightBtn').addEventListener('touchend', () => keys['ArrowRight'] = false);
        document.getElementById('jumpBtn').addEventListener('touchstart', () => keys['Space'] = true);
        document.getElementById('jumpBtn').addEventListener('touchend', () => keys['Space'] = false);
        
        function update() {{
            if (!gameRunning) return;
            
            // Horizontal movement
            if (keys['ArrowLeft']) {{
                player.velocityX = -player.speed;
            }} else if (keys['ArrowRight']) {{
                player.velocityX = player.speed;
            }} else {{
                player.velocityX *= 0.8; // Friction
            }}
            
            // Jumping
            if (keys['Space'] && player.onGround) {{
                player.velocityY = -player.jumpPower;
                player.onGround = false;
            }}
            
            // Apply gravity
            player.velocityY += 0.8;
            
            // Update position
            player.x += player.velocityX;
            player.y += player.velocityY;
            
            // Keep player in bounds
            if (player.x < 0) player.x = 0;
            if (player.x > 800 - player.width) player.x = 800 - player.width;
            
            // Platform collision
            player.onGround = false;
            platforms.forEach(platform => {{
                if (player.x < platform.x + platform.width &&
                    player.x + player.width > platform.x &&
                    player.y < platform.y + platform.height &&
                    player.y + player.height > platform.y) {{
                    
                    // Landing on top
                    if (player.velocityY > 0 && player.y < platform.y) {{
                        player.y = platform.y - player.height;
                        player.velocityY = 0;
                        player.onGround = true;
                    }}
                }}
            }});
            
            // Coin collection
            coins.forEach(coin => {{
                if (!coin.collected &&
                    player.x < coin.x + coin.width &&
                    player.x + player.width > coin.x &&
                    player.y < coin.y + coin.height &&
                    player.y + player.height > coin.y) {{
                    coin.collected = true;
                    score += 100;
                    document.getElementById('score').textContent = score;
                }}
            }});
            
            // Fall off screen
            if (player.y > 600) {{
                lives--;
                document.getElementById('lives').textContent = lives;
                player.x = 100;
                player.y = 400;
                player.velocityX = 0;
                player.velocityY = 0;
                
                if (lives <= 0) {{
                    gameRunning = false;
                    alert('Game Over! Final Score: ' + score);
                }}
            }}
        }}
        
        function draw() {{
            // Clear canvas
            ctx.fillStyle = '#87CEEB';
            ctx.fillRect(0, 0, 800, 600);
            
            // Draw platforms
            ctx.fillStyle = '#8B4513';
            platforms.forEach(platform => {{
                ctx.fillRect(platform.x, platform.y, platform.width, platform.height);
            }});
            
            // Draw coins
            ctx.fillStyle = '#FFD700';
            coins.forEach(coin => {{
                if (!coin.collected) {{
                    ctx.beginPath();
                    ctx.arc(coin.x + coin.width/2, coin.y + coin.height/2, coin.width/2, 0, Math.PI * 2);
                    ctx.fill();
                }}
            }});
            
            // Draw player
            ctx.fillStyle = '#FF6B6B';
            ctx.fillRect(player.x, player.y, player.width, player.height);
        }}
        
        function gameLoop() {{
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }}
        
        gameLoop();
    </script>
</body>
</html>'''
        
        return {'html': html}
    
    def create_racing_game(self, concept: Dict[str, Any]) -> Dict[str, str]:
        """Create a racing game"""
        title = concept.get('title', 'Speed Racer')
        description = concept.get('description', 'Race at high speed')
        
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: #333;
            font-family: Arial, sans-serif;
            overflow: hidden;
        }}
        #gameCanvas {{
            display: block;
            margin: 0 auto;
            background: #444;
        }}
        .ui {{
            position: absolute;
            top: 10px;
            left: 10px;
            color: white;
            font-weight: bold;
        }}
        .controls {{
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 10px;
        }}
        .control-btn {{
            width: 60px;
            height: 60px;
            background: rgba(255,255,255,0.2);
            border: 2px solid rgba(255,255,255,0.5);
            border-radius: 10px;
            color: white;
            font-size: 20px;
            cursor: pointer;
            user-select: none;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        @media (min-width: 768px) {{
            .controls {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="ui">
        <div>Speed: <span id="speed">0</span> mph</div>
        <div>Distance: <span id="distance">0</span> m</div>
        <div>Score: <span id="score">0</span></div>
    </div>
    
    <canvas id="gameCanvas" width="800" height="600"></canvas>
    
    <div class="controls">
        <div class="control-btn" id="leftBtn">←</div>
        <div class="control-btn" id="rightBtn">→</div>
        <div class="control-btn" id="upBtn">↑</div>
        <div class="control-btn" id="downBtn">↓</div>
    </div>
    
    <div style="position: absolute; bottom: 10px; left: 50%; transform: translateX(-50%); text-align: center; font-size: 12px; color: white;">
        Desktop: Arrow Keys to Steer and Accelerate
    </div>
    
    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        
        // Responsive canvas
        function resizeCanvas() {{
            const maxWidth = window.innerWidth;
            const maxHeight = window.innerHeight - 100;
            const aspectRatio = 800 / 600;
            
            if (maxWidth / maxHeight > aspectRatio) {{
                canvas.style.height = maxHeight + 'px';
                canvas.style.width = (maxHeight * aspectRatio) + 'px';
            }} else {{
                canvas.style.width = maxWidth + 'px';
                canvas.style.height = (maxWidth / aspectRatio) + 'px';
            }}
        }}
        
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);
        
        // Game state
        let speed = 0;
        let distance = 0;
        let score = 0;
        let gameRunning = true;
        
        // Player car
        const player = {{
            x: 375,
            y: 450,
            width: 50,
            height: 80,
            speed: 0,
            maxSpeed: 10
        }};
        
        // Road
        let roadOffset = 0;
        const roadWidth = 400;
        const roadX = (800 - roadWidth) / 2;
        
        // Other cars
        let cars = [];
        
        // Road lines
        let roadLines = [];
        for (let i = 0; i < 10; i++) {{
            roadLines.push({{
                y: i * 80
            }});
        }}
        
        // Input handling
        const keys = {{}};
        
        document.addEventListener('keydown', (e) => {{
            keys[e.code] = true;
        }});
        
        document.addEventListener('keyup', (e) => {{
            keys[e.code] = false;
        }});
        
        // Mobile controls
        document.getElementById('leftBtn').addEventListener('touchstart', () => keys['ArrowLeft'] = true);
        document.getElementById('leftBtn').addEventListener('touchend', () => keys['ArrowLeft'] = false);
        document.getElementById('rightBtn').addEventListener('touchstart', () => keys['ArrowRight'] = true);
        document.getElementById('rightBtn').addEventListener('touchend', () => keys['ArrowRight'] = false);
        document.getElementById('upBtn').addEventListener('touchstart', () => keys['ArrowUp'] = true);
        document.getElementById('upBtn').addEventListener('touchend', () => keys['ArrowUp'] = false);
        document.getElementById('downBtn').addEventListener('touchstart', () => keys['ArrowDown'] = true);
        document.getElementById('downBtn').addEventListener('touchend', () => keys['ArrowDown'] = false);
        
        function spawnCar() {{
            cars.push({{
                x: roadX + Math.random() * (roadWidth - 50),
                y: -80,
                width: 50,
                height: 80,
                speed: Math.random() * 3 + 2
            }});
        }}
        
        function update() {{
            if (!gameRunning) return;
            
            // Player movement
            if (keys['ArrowLeft'] && player.x > roadX) {{
                player.x -= 5;
            }}
            if (keys['ArrowRight'] && player.x < roadX + roadWidth - player.width) {{
                player.x += 5;
            }}
            if (keys['ArrowUp'] && player.speed < player.maxSpeed) {{
                player.speed += 0.2;
            }}
            if (keys['ArrowDown'] && player.speed > 0) {{
                player.speed -= 0.3;
            }}
            
            // Natural deceleration
            if (!keys['ArrowUp'] && player.speed > 0) {{
                player.speed -= 0.1;
            }}
            
            speed = Math.floor(player.speed * 10);
            distance += player.speed;
            score = Math.floor(distance / 10);
            
            document.getElementById('speed').textContent = speed;
            document.getElementById('distance').textContent = Math.floor(distance);
            document.getElementById('score').textContent = score;
            
            // Move road lines
            roadLines.forEach(line => {{
                line.y += player.speed * 2;
                if (line.y > 600) {{
                    line.y = -80;
                }}
            }});
            
            // Move other cars
            cars = cars.filter(car => {{
                car.y += car.speed + player.speed;
                return car.y < 600;
            }});
            
            // Spawn new cars
            if (Math.random() < 0.01 && cars.length < 5) {{
                spawnCar();
            }}
            
            // Check collisions
            cars.forEach(car => {{
                if (player.x < car.x + car.width &&
                    player.x + player.width > car.x &&
                    player.y < car.y + car.height &&
                    player.y + player.height > car.y) {{
                    gameRunning = false;
                    alert('Crash! Final Score: ' + score);
                }}
            }});
        }}
        
        function draw() {{
            // Clear canvas
            ctx.fillStyle = '#228B22';
            ctx.fillRect(0, 0, 800, 600);
            
            // Draw road
            ctx.fillStyle = '#555';
            ctx.fillRect(roadX, 0, roadWidth, 600);
            
            // Draw road lines
            ctx.fillStyle = '#FFF';
            roadLines.forEach(line => {{
                ctx.fillRect(roadX + roadWidth/2 - 5, line.y, 10, 40);
            }});
            
            // Draw road edges
            ctx.fillStyle = '#FFF';
            ctx.fillRect(roadX - 5, 0, 5, 600);
            ctx.fillRect(roadX + roadWidth, 0, 5, 600);
            
            // Draw other cars
            ctx.fillStyle = '#FF0000';
            cars.forEach(car => {{
                ctx.fillRect(car.x, car.y, car.width, car.height);
            }});
            
            // Draw player car
            ctx.fillStyle = '#0000FF';
            ctx.fillRect(player.x, player.y, player.width, player.height);
        }}
        
        function gameLoop() {{
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }}
        
        gameLoop();
    </script>
</body>
</html>'''
        
        return {'html': html}
    
    def create_rpg_game(self, concept: Dict[str, Any]) -> Dict[str, str]:
        """Create an RPG game"""
        title = concept.get('title', 'Epic Quest')
        description = concept.get('description', 'Embark on an epic adventure')
        
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: linear-gradient(45deg, #2C1810, #8B4513);
            font-family: Arial, sans-serif;
            color: white;
        }}
        .game-container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        .stats {{
            display: flex;
            justify-content: space-around;
            background: rgba(0,0,0,0.5);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        .game-area {{
            background: rgba(0,0,0,0.3);
            padding: 20px;
            border-radius: 10px;
            min-height: 400px;
        }}
        .actions {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 20px;
        }}
        .btn {{
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            background: linear-gradient(45deg, #8B4513, #A0522D);
            color: white;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.2s ease;
        }}
        .btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }}
        .inventory {{
            background: rgba(0,0,0,0.5);
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
        }}
        .log {{
            background: rgba(0,0,0,0.7);
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            max-height: 200px;
            overflow-y: auto;
        }}
    </style>
</head>
<body>
    <div class="game-container">
        <h1>{title}</h1>
        <p>{description}</p>
        
        <div class="stats">
            <div><strong>Health:</strong> <span id="health">100</span>/100</div>
            <div><strong>Level:</strong> <span id="level">1</span></div>
            <div><strong>XP:</strong> <span id="xp">0</span>/100</div>
            <div><strong>Gold:</strong> <span id="gold">50</span></div>
        </div>
        
        <div class="game-area">
            <h3 id="locationName">Village Square</h3>
            <p id="locationDesc">You stand in the center of a peaceful village. The sun shines down on cobblestone streets, and you can hear the bustle of merchants and townsfolk.</p>
            
            <div class="actions">
                <button class="btn" onclick="explore()">🗺️ Explore</button>
                <button class="btn" onclick="rest()">😴 Rest</button>
                <button class="btn" onclick="shop()">🏪 Shop</button>
                <button class="btn" onclick="fight()">⚔️ Fight Monster</button>
            </div>
        </div>
        
        <div class="inventory">
            <h4>Inventory:</h4>
            <div id="inventoryList">Wooden Sword, Health Potion x2</div>
        </div>
        
        <div class="log">
            <h4>Adventure Log:</h4>
            <div id="gameLog">Welcome to your adventure! Choose an action to begin.</div>
        </div>
    </div>
    
    <script>
        let player = {{
            health: 100,
            maxHealth: 100,
            level: 1,
            xp: 0,
            xpToNext: 100,
            gold: 50,
            inventory: ['Wooden Sword', 'Health Potion', 'Health Potion']
        }};
        
        let currentLocation = 'village';
        
        const locations = {{
            village: {{
                name: 'Village Square',
                desc: 'You stand in the center of a peaceful village. The sun shines down on cobblestone streets.'
            }},
            forest: {{
                name: 'Dark Forest',
                desc: 'Ancient trees tower above you, their branches blocking most sunlight. Strange sounds echo in the distance.'
            }},
            cave: {{
                name: 'Mysterious Cave',
                desc: 'A damp cave with glowing crystals embedded in the walls. You sense danger lurking in the shadows.'
            }},
            mountain: {{
                name: 'Rocky Mountain',
                desc: 'High peaks stretch toward the clouds. The air is thin and cold, but the view is breathtaking.'
            }}
        }};
        
        const monsters = [
            {{name: 'Goblin', health: 30, attack: 15, xp: 25, gold: 10}},
            {{name: 'Orc', health: 50, attack: 20, xp: 40, gold: 20}},
            {{name: 'Dragon', health: 100, attack: 35, xp: 100, gold: 50}},
            {{name: 'Skeleton', health: 40, attack: 18, xp: 30, gold: 15}}
        ];
        
        function updateDisplay() {{
            document.getElementById('health').textContent = player.health;
            document.getElementById('level').textContent = player.level;
            document.getElementById('xp').textContent = player.xp;
            document.getElementById('gold').textContent = player.gold;
            document.getElementById('inventoryList').textContent = player.inventory.join(', ');
        }}
        
        function addToLog(message) {{
            const log = document.getElementById('gameLog');
            log.innerHTML += '<br>' + message;
            log.scrollTop = log.scrollHeight;
        }}
        
        function explore() {{
            const locationKeys = Object.keys(locations);
            const randomLocation = locationKeys[Math.floor(Math.random() * locationKeys.length)];
            currentLocation = randomLocation;
            
            const location = locations[randomLocation];
            document.getElementById('locationName').textContent = location.name;
            document.getElementById('locationDesc').textContent = location.desc;
            
            addToLog(`You explore and discover: ${{location.name}}`);
            
            // Random events
            if (Math.random() < 0.3) {{
                const goldFound = Math.floor(Math.random() * 20) + 5;
                player.gold += goldFound;
                addToLog(`You found ${{goldFound}} gold!`);
                updateDisplay();
            }}
        }}
        
        function rest() {{
            const healAmount = Math.floor(player.maxHealth * 0.3);
            player.health = Math.min(player.maxHealth, player.health + healAmount);
            addToLog(`You rest and recover ${{healAmount}} health.`);
            updateDisplay();
        }}
        
        function shop() {{
            if (player.gold >= 30) {{
                player.gold -= 30;
                player.inventory.push('Health Potion');
                addToLog('You bought a Health Potion for 30 gold.');
            }} else {{
                addToLog('Not enough gold! Health Potions cost 30 gold.');
            }}
            updateDisplay();
        }}
        
        function fight() {{
            const monster = monsters[Math.floor(Math.random() * monsters.length)];
            let monsterHealth = monster.health;
            
            addToLog(`A wild ${{monster.name}} appears!`);
            
            while (monsterHealth > 0 && player.health > 0) {{
                // Player attacks
                const playerDamage = Math.floor(Math.random() * 25) + 10;
                monsterHealth -= playerDamage;
                addToLog(`You deal ${{playerDamage}} damage to the ${{monster.name}}!`);
                
                if (monsterHealth <= 0) {{
                    addToLog(`You defeated the ${{monster.name}}!`);
                    player.xp += monster.xp;
                    player.gold += monster.gold;
                    addToLog(`Gained ${{monster.xp}} XP and ${{monster.gold}} gold!`);
                    
                    // Level up check
                    if (player.xp >= player.xpToNext) {{
                        player.level++;
                        player.xp -= player.xpToNext;
                        player.xpToNext = player.level * 100;
                        player.maxHealth += 20;
                        player.health = player.maxHealth;
                        addToLog(`Level up! You are now level ${{player.level}}!`);
                    }}
                    break;
                }}
                
                // Monster attacks
                const monsterDamage = Math.floor(Math.random() * monster.attack) + 5;
                player.health -= monsterDamage;
                addToLog(`The ${{monster.name}} deals ${{monsterDamage}} damage to you!`);
                
                if (player.health <= 0) {{
                    addToLog('You have been defeated! Game Over!');
                    alert('Game Over! You fought bravely.');
                    // Reset player
                    player.health = player.maxHealth;
                    player.gold = Math.max(10, Math.floor(player.gold * 0.5));
                    addToLog('You wake up in the village, having lost some gold...');
                    break;
                }}
            }}
            
            updateDisplay();
        }}
        
        updateDisplay();
    </script>
</body>
</html>'''
        
        return {'html': html}
    
    def create_strategy_game(self, concept: Dict[str, Any]) -> Dict[str, str]:
        """Create a strategy game"""
        title = concept.get('title', 'City Builder')
        description = concept.get('description', 'Build and manage your city')
        
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #2E8B57, #228B22);
            font-family: Arial, sans-serif;
            color: white;
        }}
        .game-container {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
        }}
        .stats {{
            display: flex;
            justify-content: space-around;
            background: rgba(0,0,0,0.5);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }}
        .city-grid {{
            display: grid;
            grid-template-columns: repeat(8, 1fr);
            gap: 2px;
            background: rgba(0,0,0,0.3);
            padding: 20px;
            border-radius: 10px;
            max-width: 600px;
            margin: 0 auto 20px;
        }}
        .cell {{
            width: 60px;
            height: 60px;
            background: #90EE90;
            border: 1px solid #228B22;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            transition: all 0.2s ease;
        }}
        .cell:hover {{
            background: #98FB98;
            transform: scale(1.05);
        }}
        .building-menu {{
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }}
        .building-btn {{
            padding: 10px 15px;
            border: none;
            border-radius: 5px;
            background: linear-gradient(45deg, #4169E1, #1E90FF);
            color: white;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.2s ease;
        }}
        .building-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }}
        .building-btn.selected {{
            background: linear-gradient(45deg, #FF6347, #FF4500);
        }}
        .info {{
            background: rgba(0,0,0,0.5);
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }}
        @media (max-width: 768px) {{
            .cell {{
                width: 40px;
                height: 40px;
                font-size: 18px;
            }}
            .stats {{
                font-size: 14px;
            }}
        }}
    </style>
</head>
<body>
    <div class="game-container">
        <h1>{title}</h1>
        <p>{description}</p>
        
        <div class="stats">
            <div><strong>Population:</strong> <span id="population">0</span></div>
            <div><strong>Money:</strong> $<span id="money">1000</span></div>
            <div><strong>Happiness:</strong> <span id="happiness">50</span>%</div>
            <div><strong>Power:</strong> <span id="power">0</span>/<span id="powerUsed">0</span></div>
        </div>
        
        <div class="building-menu">
            <button class="building-btn selected" onclick="selectBuilding('empty')">🌱 Empty ($0)</button>
            <button class="building-btn" onclick="selectBuilding('house')">🏠 House ($100)</button>
            <button class="building-btn" onclick="selectBuilding('shop')">🏪 Shop ($200)</button>
            <button class="building-btn" onclick="selectBuilding('factory')">🏭 Factory ($500)</button>
            <button class="building-btn" onclick="selectBuilding('park')">🌳 Park ($150)</button>
            <button class="building-btn" onclick="selectBuilding('power')">⚡ Power Plant ($800)</button>
        </div>
        
        <div class="city-grid" id="cityGrid"></div>
        
        <div class="info">
            <p><strong>Instructions:</strong> Click on empty land to build. Houses increase population, shops generate money, factories produce goods but reduce happiness, parks increase happiness, and power plants provide electricity.</p>
            <p><strong>Current Selection:</strong> <span id="selectedBuilding">Empty Land</span></p>
        </div>
    </div>
    
    <script>
        let gameState = {{
            money: 1000,
            population: 0,
            happiness: 50,
            power: 0,
            powerUsed: 0,
            selectedBuilding: 'empty'
        }};
        
        let cityGrid = Array(64).fill('empty');
        
        const buildings = {{
            empty: {{name: 'Empty Land', cost: 0, emoji: '🌱', population: 0, income: 0, happiness: 0, power: 0}},
            house: {{name: 'House', cost: 100, emoji: '🏠', population: 4, income: 0, happiness: 0, power: -1}},
            shop: {{name: 'Shop', cost: 200, emoji: '🏪', population: 0, income: 50, happiness: 5, power: -2}},
            factory: {{name: 'Factory', cost: 500, emoji: '🏭', population: 0, income: 100, happiness: -10, power: -5}},
            park: {{name: 'Park', cost: 150, emoji: '🌳', population: 0, income: 0, happiness: 15, power: 0}},
            power: {{name: 'Power Plant', cost: 800, emoji: '⚡', population: 0, income: 0, happiness: -5, power: 20}}
        }};
        
        function initGrid() {{
            const grid = document.getElementById('cityGrid');
            grid.innerHTML = '';
            
            for (let i = 0; i < 64; i++) {{
                const cell = document.createElement('div');
                cell.className = 'cell';
                cell.onclick = () => buildOnCell(i);
                cell.textContent = buildings[cityGrid[i]].emoji;
                grid.appendChild(cell);
            }}
        }}
        
        function selectBuilding(type) {{
            gameState.selectedBuilding = type;
            document.getElementById('selectedBuilding').textContent = buildings[type].name;
            
            // Update button styles
            document.querySelectorAll('.building-btn').forEach(btn => {{
                btn.classList.remove('selected');
            }});
            event.target.classList.add('selected');
        }}
        
        function buildOnCell(index) {{
            const buildingType = gameState.selectedBuilding;
            const building = buildings[buildingType];
            
            if (buildingType === 'empty') {{
                cityGrid[index] = 'empty';
                updateStats();
                initGrid();
                return;
            }}
            
            if (gameState.money < building.cost) {{
                alert('Not enough money!');
                return;
            }}
            
            gameState.money -= building.cost;
            cityGrid[index] = buildingType;
            
            updateStats();
            initGrid();
        }}
        
        function updateStats() {{
            let totalPopulation = 0;
            let totalIncome = 0;
            let totalHappiness = 50; // Base happiness
            let totalPower = 0;
            let totalPowerUsed = 0;
            
            cityGrid.forEach(buildingType => {{
                const building = buildings[buildingType];
                totalPopulation += building.population;
                totalIncome += building.income;
                totalHappiness += building.happiness;
                
                if (building.power > 0) {{
                    totalPower += building.power;
                }} else {{
                    totalPowerUsed += Math.abs(building.power);
                }}
            }});
            
            // Apply income
            gameState.money += totalIncome;
            
            // Update display
            gameState.population = totalPopulation;
            gameState.happiness = Math.max(0, Math.min(100, totalHappiness));
            gameState.power = totalPower;
            gameState.powerUsed = totalPowerUsed;
            
            document.getElementById('population').textContent = gameState.population;
            document.getElementById('money').textContent = gameState.money;
            document.getElementById('happiness').textContent = gameState.happiness;
            document.getElementById('power').textContent = gameState.power;
            document.getElementById('powerUsed').textContent = gameState.powerUsed;
            
            // Check power shortage
            if (gameState.powerUsed > gameState.power) {{
                document.getElementById('power').style.color = '#FF6347';
                gameState.happiness = Math.max(0, gameState.happiness - 10);
            }} else {{
                document.getElementById('power').style.color = 'white';
            }}
        }}
        
        // Auto-update every 3 seconds
        setInterval(() => {{
            updateStats();
        }}, 3000);
        
        initGrid();
        updateStats();
    </script>
</body>
</html>'''
        
        return {'html': html}
    
    def create_fallback_game(self, prompt: str) -> Dict[str, Any]:
        """Create a fallback game when AI fails"""
        concept = self.create_simple_concept(prompt)
        game_code = self.create_puzzle_game(concept)
        
        game_id = f"game_{int(time.time())}_{self.generate_random_id()}"
        
        return {
            'status': 'success',
            'game': {
                'id': game_id,
                'title': concept['title'],
                'description': concept['description'],
                'genre': concept['genre'],
                'concept': concept,
                'code': game_code,
                'created_at': time.time()
            }
        }
    
    def generate_random_id(self) -> str:
        """Generate a random ID"""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

# Create global instance
game_engine = RealGameEngine()
