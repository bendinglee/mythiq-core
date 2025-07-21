#!/usr/bin/env python3
"""
🎮 AI Game Creation Engine
Integrates with Mythiq Gateway to provide game generation capabilities
"""

import os
import json
import time
import random
import requests
from typing import Dict, List, Optional, Any

class AIGameEngine:
    """AI-powered game creation engine"""
    
    def __init__(self):
        self.groq_api_key = os.environ.get('GROQ_API_KEY')
        self.groq_api_base = "https://api.groq.com/openai/v1"
        
        # Game templates for different types
        self.game_templates = {
            'platformer': self._get_platformer_template(),
            'puzzle': self._get_puzzle_template(),
            'shooter': self._get_shooter_template(),
            'rpg': self._get_rpg_template(),
            'racing': self._get_racing_template(),
            'strategy': self._get_strategy_template()
        }
        
        # Asset libraries
        self.sprite_library = self._init_sprite_library()
        self.sound_library = self._init_sound_library()
    
    def generate_game_concept(self, user_prompt: str) -> Dict[str, Any]:
        """Generate a complete game concept from user description"""
        
        system_prompt = """You are an expert game designer. Create a detailed game concept based on the user's description. 
        
        Return a JSON object with:
        - title: Game title
        - genre: Game genre (platformer, puzzle, shooter, rpg, racing, strategy)
        - description: 2-3 sentence game description
        - mechanics: List of core game mechanics
        - objectives: List of player objectives
        - difficulty: Easy, Medium, or Hard
        - estimated_playtime: In minutes
        - target_audience: Age range and type
        - monetization: How the game could make money
        - technical_requirements: What's needed to build it
        
        Make it creative, fun, and commercially viable."""
        
        try:
            response = self._call_ai(system_prompt, user_prompt)
            concept = json.loads(response)
            
            # Add generated metadata
            concept['id'] = f"game_{int(time.time())}"
            concept['created_at'] = time.time()
            concept['status'] = 'concept'
            
            return {
                'status': 'success',
                'concept': concept,
                'cost': '$0.01'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f"Failed to generate concept: {str(e)}",
                'cost': '$0.00'
            }
    
    def generate_game_code(self, concept: Dict[str, Any]) -> Dict[str, Any]:
        """Generate playable HTML5 game code from concept"""
        
        genre = concept.get('genre', 'puzzle').lower()
        template = self.game_templates.get(genre, self.game_templates['puzzle'])
        
        # Customize template based on concept
        customized_code = self._customize_template(template, concept)
        
        return {
            'status': 'success',
            'code': {
                'html': customized_code['html'],
                'css': customized_code['css'],
                'javascript': customized_code['js']
            },
            'assets': self._generate_game_assets(concept),
            'instructions': self._generate_instructions(concept),
            'cost': '$0.02'
        }
    
    def create_complete_game(self, user_prompt: str) -> Dict[str, Any]:
        """Create a complete playable game from user description"""
        
        # Step 1: Generate concept
        concept_result = self.generate_game_concept(user_prompt)
        if concept_result['status'] != 'success':
            return concept_result
        
        concept = concept_result['concept']
        
        # Step 2: Generate code
        code_result = self.generate_game_code(concept)
        if code_result['status'] != 'success':
            return code_result
        
        # Step 3: Create complete package
        game_package = {
            'id': concept['id'],
            'title': concept['title'],
            'concept': concept,
            'code': code_result['code'],
            'assets': code_result['assets'],
            'instructions': code_result['instructions'],
            'created_at': time.time(),
            'play_url': f"/games/play/{concept['id']}",
            'share_url': f"/games/share/{concept['id']}",
            'status': 'ready'
        }
        
        return {
            'status': 'success',
            'game': game_package,
            'message': f"Successfully created '{concept['title']}'!",
            'cost': '$0.03'
        }
    
    def _call_ai(self, system_prompt: str, user_prompt: str) -> str:
        """Call AI API for content generation"""
        
        if not self.groq_api_key:
            raise Exception("GROQ_API_KEY not configured")
        
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.8,
            "max_tokens": 2000
        }
        
        response = requests.post(f"{self.groq_api_base}/chat/completions", 
                               headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            raise Exception(f"API Error: {response.status_code}")
    
    def _get_platformer_template(self) -> Dict[str, str]:
        """HTML5 platformer game template"""
        return {
            'html': '''<!DOCTYPE html>
<html>
<head>
    <title>{{GAME_TITLE}}</title>
    <style>{{CSS_CONTENT}}</style>
</head>
<body>
    <div id="gameContainer">
        <h1>{{GAME_TITLE}}</h1>
        <canvas id="gameCanvas" width="800" height="400"></canvas>
        <div id="controls">
            <p>Use ARROW KEYS to move and SPACE to jump!</p>
            <button onclick="startGame()">Start Game</button>
            <button onclick="resetGame()">Reset</button>
        </div>
        <div id="score">Score: <span id="scoreValue">0</span></div>
    </div>
    <script>{{JS_CONTENT}}</script>
</body>
</html>''',
            
            'css': '''body {
    margin: 0;
    padding: 20px;
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    text-align: center;
}

#gameContainer {
    max-width: 800px;
    margin: 0 auto;
    background: rgba(255,255,255,0.1);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
}

#gameCanvas {
    border: 3px solid #fff;
    border-radius: 10px;
    background: #87CEEB;
    display: block;
    margin: 20px auto;
}

#controls {
    margin: 20px 0;
}

button {
    padding: 10px 20px;
    margin: 5px;
    border: none;
    border-radius: 5px;
    background: #4CAF50;
    color: white;
    cursor: pointer;
    font-size: 16px;
}

button:hover {
    background: #45a049;
}

#score {
    font-size: 24px;
    font-weight: bold;
}''',
            
            'js': '''const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let game = {
    player: { x: 50, y: 300, width: 30, height: 30, velY: 0, jumping: false, grounded: false },
    platforms: [
        { x: 0, y: 370, width: 800, height: 30 },
        { x: 200, y: 300, width: 100, height: 20 },
        { x: 400, y: 250, width: 100, height: 20 },
        { x: 600, y: 200, width: 100, height: 20 }
    ],
    coins: [
        { x: 230, y: 270, width: 20, height: 20, collected: false },
        { x: 430, y: 220, width: 20, height: 20, collected: false },
        { x: 630, y: 170, width: 20, height: 20, collected: false }
    ],
    score: 0,
    keys: {},
    gravity: 0.5,
    friction: 0.8,
    running: false
};

// Event listeners
document.addEventListener('keydown', (e) => {
    game.keys[e.code] = true;
});

document.addEventListener('keyup', (e) => {
    game.keys[e.code] = false;
});

function startGame() {
    game.running = true;
    gameLoop();
}

function resetGame() {
    game.player = { x: 50, y: 300, width: 30, height: 30, velY: 0, jumping: false, grounded: false };
    game.score = 0;
    game.coins.forEach(coin => coin.collected = false);
    document.getElementById('scoreValue').textContent = game.score;
}

function update() {
    if (!game.running) return;
    
    // Player movement
    if (game.keys['ArrowLeft']) {
        game.player.x -= 5;
    }
    if (game.keys['ArrowRight']) {
        game.player.x += 5;
    }
    if (game.keys['Space'] && game.player.grounded) {
        game.player.velY = -12;
        game.player.jumping = true;
        game.player.grounded = false;
    }
    
    // Apply gravity
    game.player.velY += game.gravity;
    game.player.y += game.player.velY;
    
    // Platform collision
    game.player.grounded = false;
    game.platforms.forEach(platform => {
        if (game.player.x < platform.x + platform.width &&
            game.player.x + game.player.width > platform.x &&
            game.player.y < platform.y + platform.height &&
            game.player.y + game.player.height > platform.y) {
            
            if (game.player.velY > 0) {
                game.player.y = platform.y - game.player.height;
                game.player.velY = 0;
                game.player.jumping = false;
                game.player.grounded = true;
            }
        }
    });
    
    // Coin collection
    game.coins.forEach(coin => {
        if (!coin.collected &&
            game.player.x < coin.x + coin.width &&
            game.player.x + game.player.width > coin.x &&
            game.player.y < coin.y + coin.height &&
            game.player.y + game.player.height > coin.y) {
            
            coin.collected = true;
            game.score += 10;
            document.getElementById('scoreValue').textContent = game.score;
        }
    });
    
    // Boundary check
    if (game.player.x < 0) game.player.x = 0;
    if (game.player.x > canvas.width - game.player.width) game.player.x = canvas.width - game.player.width;
    if (game.player.y > canvas.height) resetGame();
}

function draw() {
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw platforms
    ctx.fillStyle = '#8B4513';
    game.platforms.forEach(platform => {
        ctx.fillRect(platform.x, platform.y, platform.width, platform.height);
    });
    
    // Draw coins
    ctx.fillStyle = '#FFD700';
    game.coins.forEach(coin => {
        if (!coin.collected) {
            ctx.beginPath();
            ctx.arc(coin.x + coin.width/2, coin.y + coin.height/2, coin.width/2, 0, Math.PI * 2);
            ctx.fill();
        }
    });
    
    // Draw player
    ctx.fillStyle = '#FF6B6B';
    ctx.fillRect(game.player.x, game.player.y, game.player.width, game.player.height);
    
    // Draw eyes
    ctx.fillStyle = '#000';
    ctx.fillRect(game.player.x + 5, game.player.y + 5, 5, 5);
    ctx.fillRect(game.player.x + 20, game.player.y + 5, 5, 5);
}

function gameLoop() {
    if (game.running) {
        update();
        draw();
        requestAnimationFrame(gameLoop);
    }
}'''
        }
    
    def _get_puzzle_template(self) -> Dict[str, str]:
        """HTML5 puzzle game template"""
        return {
            'html': '''<!DOCTYPE html>
<html>
<head>
    <title>{{GAME_TITLE}}</title>
    <style>{{CSS_CONTENT}}</style>
</head>
<body>
    <div id="gameContainer">
        <h1>{{GAME_TITLE}}</h1>
        <div id="gameBoard"></div>
        <div id="controls">
            <button onclick="newGame()">New Game</button>
            <button onclick="showSolution()">Show Solution</button>
        </div>
        <div id="score">Moves: <span id="moveCount">0</span></div>
        <div id="timer">Time: <span id="timeValue">0</span>s</div>
    </div>
    <script>{{JS_CONTENT}}</script>
</body>
</html>''',
            
            'css': '''body {
    margin: 0;
    padding: 20px;
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    text-align: center;
}

#gameContainer {
    max-width: 600px;
    margin: 0 auto;
    background: rgba(255,255,255,0.1);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
}

#gameBoard {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 5px;
    max-width: 400px;
    margin: 20px auto;
    padding: 10px;
    background: rgba(255,255,255,0.2);
    border-radius: 10px;
}

.tile {
    aspect-ratio: 1;
    background: linear-gradient(45deg, #4ECDC4, #44A08D);
    border: 2px solid #fff;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
}

.tile:hover {
    transform: scale(1.05);
    background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
}

.tile.empty {
    background: transparent;
    border: 2px dashed rgba(255,255,255,0.3);
}

button {
    padding: 10px 20px;
    margin: 5px;
    border: none;
    border-radius: 5px;
    background: #4CAF50;
    color: white;
    cursor: pointer;
    font-size: 16px;
}

button:hover {
    background: #45a049;
}

#score, #timer {
    font-size: 18px;
    margin: 10px;
}''',
            
            'js': '''let puzzle = {
    board: [],
    size: 4,
    moves: 0,
    startTime: null,
    timer: null,
    solved: false
};

function initGame() {
    // Create solved board
    puzzle.board = [];
    for (let i = 1; i < puzzle.size * puzzle.size; i++) {
        puzzle.board.push(i);
    }
    puzzle.board.push(0); // Empty space
    
    // Shuffle board
    for (let i = 0; i < 1000; i++) {
        makeRandomMove();
    }
    
    puzzle.moves = 0;
    puzzle.startTime = Date.now();
    puzzle.solved = false;
    
    updateDisplay();
    startTimer();
}

function makeRandomMove() {
    const emptyIndex = puzzle.board.indexOf(0);
    const possibleMoves = getPossibleMoves(emptyIndex);
    if (possibleMoves.length > 0) {
        const randomMove = possibleMoves[Math.floor(Math.random() * possibleMoves.length)];
        swapTiles(emptyIndex, randomMove);
    }
}

function getPossibleMoves(emptyIndex) {
    const moves = [];
    const row = Math.floor(emptyIndex / puzzle.size);
    const col = emptyIndex % puzzle.size;
    
    // Up
    if (row > 0) moves.push(emptyIndex - puzzle.size);
    // Down
    if (row < puzzle.size - 1) moves.push(emptyIndex + puzzle.size);
    // Left
    if (col > 0) moves.push(emptyIndex - 1);
    // Right
    if (col < puzzle.size - 1) moves.push(emptyIndex + 1);
    
    return moves;
}

function swapTiles(index1, index2) {
    [puzzle.board[index1], puzzle.board[index2]] = [puzzle.board[index2], puzzle.board[index1]];
}

function moveTile(index) {
    if (puzzle.solved) return;
    
    const emptyIndex = puzzle.board.indexOf(0);
    const possibleMoves = getPossibleMoves(emptyIndex);
    
    if (possibleMoves.includes(index)) {
        swapTiles(emptyIndex, index);
        puzzle.moves++;
        updateDisplay();
        
        if (isSolved()) {
            puzzle.solved = true;
            clearInterval(puzzle.timer);
            setTimeout(() => {
                alert(`Congratulations! You solved it in ${puzzle.moves} moves and ${Math.floor((Date.now() - puzzle.startTime) / 1000)} seconds!`);
            }, 100);
        }
    }
}

function isSolved() {
    for (let i = 0; i < puzzle.board.length - 1; i++) {
        if (puzzle.board[i] !== i + 1) return false;
    }
    return puzzle.board[puzzle.board.length - 1] === 0;
}

function updateDisplay() {
    const gameBoard = document.getElementById('gameBoard');
    gameBoard.innerHTML = '';
    
    puzzle.board.forEach((value, index) => {
        const tile = document.createElement('div');
        tile.className = value === 0 ? 'tile empty' : 'tile';
        tile.textContent = value === 0 ? '' : value;
        tile.onclick = () => moveTile(index);
        gameBoard.appendChild(tile);
    });
    
    document.getElementById('moveCount').textContent = puzzle.moves;
}

function startTimer() {
    puzzle.timer = setInterval(() => {
        const elapsed = Math.floor((Date.now() - puzzle.startTime) / 1000);
        document.getElementById('timeValue').textContent = elapsed;
    }, 1000);
}

function newGame() {
    if (puzzle.timer) clearInterval(puzzle.timer);
    initGame();
}

function showSolution() {
    // Create solved state
    puzzle.board = [];
    for (let i = 1; i < puzzle.size * puzzle.size; i++) {
        puzzle.board.push(i);
    }
    puzzle.board.push(0);
    puzzle.solved = true;
    updateDisplay();
    clearInterval(puzzle.timer);
}

// Initialize game on load
window.onload = initGame;'''
        }
    
    def _get_shooter_template(self) -> Dict[str, str]:
        """HTML5 shooter game template"""
        return {
            'html': '''<!DOCTYPE html>
<html>
<head>
    <title>{{GAME_TITLE}}</title>
    <style>{{CSS_CONTENT}}</style>
</head>
<body>
    <div id="gameContainer">
        <h1>{{GAME_TITLE}}</h1>
        <canvas id="gameCanvas" width="800" height="600"></canvas>
        <div id="controls">
            <p>Use ARROW KEYS to move and SPACE to shoot!</p>
            <button onclick="startGame()">Start Game</button>
            <button onclick="pauseGame()">Pause</button>
        </div>
        <div id="stats">
            <div>Score: <span id="scoreValue">0</span></div>
            <div>Lives: <span id="livesValue">3</span></div>
            <div>Level: <span id="levelValue">1</span></div>
        </div>
    </div>
    <script>{{JS_CONTENT}}</script>
</body>
</html>''',
            
            'css': '''body {
    margin: 0;
    padding: 20px;
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
    color: white;
    text-align: center;
}

#gameContainer {
    max-width: 800px;
    margin: 0 auto;
    background: rgba(255,255,255,0.1);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
}

#gameCanvas {
    border: 3px solid #fff;
    border-radius: 10px;
    background: #000;
    display: block;
    margin: 20px auto;
}

#controls {
    margin: 20px 0;
}

button {
    padding: 10px 20px;
    margin: 5px;
    border: none;
    border-radius: 5px;
    background: #e74c3c;
    color: white;
    cursor: pointer;
    font-size: 16px;
}

button:hover {
    background: #c0392b;
}

#stats {
    display: flex;
    justify-content: space-around;
    font-size: 18px;
    font-weight: bold;
}''',
            
            'js': '''const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let game = {
    player: { x: 375, y: 550, width: 50, height: 30, speed: 5 },
    bullets: [],
    enemies: [],
    particles: [],
    score: 0,
    lives: 3,
    level: 1,
    running: false,
    paused: false,
    keys: {},
    enemySpawnTimer: 0,
    enemySpawnRate: 60
};

// Event listeners
document.addEventListener('keydown', (e) => {
    game.keys[e.code] = true;
});

document.addEventListener('keyup', (e) => {
    game.keys[e.code] = false;
});

function startGame() {
    game.running = true;
    game.paused = false;
    gameLoop();
}

function pauseGame() {
    game.paused = !game.paused;
}

function spawnEnemy() {
    game.enemies.push({
        x: Math.random() * (canvas.width - 40),
        y: -40,
        width: 40,
        height: 30,
        speed: 1 + game.level * 0.5,
        health: 1
    });
}

function spawnParticle(x, y, color) {
    for (let i = 0; i < 5; i++) {
        game.particles.push({
            x: x,
            y: y,
            vx: (Math.random() - 0.5) * 10,
            vy: (Math.random() - 0.5) * 10,
            life: 30,
            color: color
        });
    }
}

function update() {
    if (!game.running || game.paused) return;
    
    // Player movement
    if (game.keys['ArrowLeft'] && game.player.x > 0) {
        game.player.x -= game.player.speed;
    }
    if (game.keys['ArrowRight'] && game.player.x < canvas.width - game.player.width) {
        game.player.x += game.player.speed;
    }
    if (game.keys['ArrowUp'] && game.player.y > canvas.height / 2) {
        game.player.y -= game.player.speed;
    }
    if (game.keys['ArrowDown'] && game.player.y < canvas.height - game.player.height) {
        game.player.y += game.player.speed;
    }
    
    // Shooting
    if (game.keys['Space']) {
        if (game.bullets.length === 0 || game.bullets[game.bullets.length - 1].y < game.player.y - 20) {
            game.bullets.push({
                x: game.player.x + game.player.width / 2 - 2,
                y: game.player.y,
                width: 4,
                height: 10,
                speed: 8
            });
        }
    }
    
    // Update bullets
    game.bullets = game.bullets.filter(bullet => {
        bullet.y -= bullet.speed;
        return bullet.y > -bullet.height;
    });
    
    // Spawn enemies
    game.enemySpawnTimer++;
    if (game.enemySpawnTimer >= game.enemySpawnRate) {
        spawnEnemy();
        game.enemySpawnTimer = 0;
    }
    
    // Update enemies
    game.enemies = game.enemies.filter(enemy => {
        enemy.y += enemy.speed;
        
        // Check collision with player
        if (enemy.x < game.player.x + game.player.width &&
            enemy.x + enemy.width > game.player.x &&
            enemy.y < game.player.y + game.player.height &&
            enemy.y + enemy.height > game.player.y) {
            
            game.lives--;
            spawnParticle(enemy.x + enemy.width/2, enemy.y + enemy.height/2, '#ff0000');
            updateStats();
            
            if (game.lives <= 0) {
                gameOver();
            }
            
            return false;
        }
        
        return enemy.y < canvas.height + enemy.height;
    });
    
    // Bullet-enemy collision
    game.bullets.forEach((bullet, bulletIndex) => {
        game.enemies.forEach((enemy, enemyIndex) => {
            if (bullet.x < enemy.x + enemy.width &&
                bullet.x + bullet.width > enemy.x &&
                bullet.y < enemy.y + enemy.height &&
                bullet.y + bullet.height > enemy.y) {
                
                // Remove bullet and enemy
                game.bullets.splice(bulletIndex, 1);
                game.enemies.splice(enemyIndex, 1);
                
                // Add score and particles
                game.score += 10;
                spawnParticle(enemy.x + enemy.width/2, enemy.y + enemy.height/2, '#00ff00');
                updateStats();
                
                // Level up
                if (game.score > 0 && game.score % 200 === 0) {
                    game.level++;
                    game.enemySpawnRate = Math.max(20, game.enemySpawnRate - 5);
                    updateStats();
                }
            }
        });
    });
    
    // Update particles
    game.particles = game.particles.filter(particle => {
        particle.x += particle.vx;
        particle.y += particle.vy;
        particle.life--;
        return particle.life > 0;
    });
}

function draw() {
    // Clear canvas
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Draw stars
    ctx.fillStyle = '#fff';
    for (let i = 0; i < 50; i++) {
        const x = (i * 37) % canvas.width;
        const y = (i * 73 + Date.now() * 0.1) % canvas.height;
        ctx.fillRect(x, y, 1, 1);
    }
    
    // Draw player
    ctx.fillStyle = '#00ff00';
    ctx.fillRect(game.player.x, game.player.y, game.player.width, game.player.height);
    
    // Draw bullets
    ctx.fillStyle = '#ffff00';
    game.bullets.forEach(bullet => {
        ctx.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
    });
    
    // Draw enemies
    ctx.fillStyle = '#ff0000';
    game.enemies.forEach(enemy => {
        ctx.fillRect(enemy.x, enemy.y, enemy.width, enemy.height);
    });
    
    // Draw particles
    game.particles.forEach(particle => {
        ctx.fillStyle = particle.color;
        ctx.globalAlpha = particle.life / 30;
        ctx.fillRect(particle.x, particle.y, 3, 3);
        ctx.globalAlpha = 1;
    });
}

function updateStats() {
    document.getElementById('scoreValue').textContent = game.score;
    document.getElementById('livesValue').textContent = game.lives;
    document.getElementById('levelValue').textContent = game.level;
}

function gameOver() {
    game.running = false;
    setTimeout(() => {
        alert(`Game Over! Final Score: ${game.score}`);
    }, 100);
}

function gameLoop() {
    if (game.running) {
        update();
        draw();
        requestAnimationFrame(gameLoop);
    }
}

// Initialize
updateStats();'''
        }
    
    def _get_rpg_template(self) -> Dict[str, str]:
        """Simple RPG template"""
        return self._get_puzzle_template()  # Simplified for now
    
    def _get_racing_template(self) -> Dict[str, str]:
        """Simple racing template"""
        return self._get_platformer_template()  # Simplified for now
    
    def _get_strategy_template(self) -> Dict[str, str]:
        """Simple strategy template"""
        return self._get_puzzle_template()  # Simplified for now
    
    def _customize_template(self, template: Dict[str, str], concept: Dict[str, Any]) -> Dict[str, str]:
        """Customize game template based on concept"""
        
        title = concept.get('title', 'AI Generated Game')
        
        # Replace placeholders
        html = template['html'].replace('{{GAME_TITLE}}', title)
        html = html.replace('{{CSS_CONTENT}}', template['css'])
        html = html.replace('{{JS_CONTENT}}', template['js'])
        
        return {
            'html': html,
            'css': template['css'],
            'js': template['js']
        }
    
    def _generate_game_assets(self, concept: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate game assets (sprites, sounds, etc.)"""
        
        genre = concept.get('genre', 'puzzle').lower()
        
        return {
            'sprites': self.sprite_library.get(genre, []),
            'sounds': self.sound_library.get(genre, []),
            'music': [f"background_music_{genre}.mp3"],
            'fonts': ["Arial", "Helvetica", "sans-serif"]
        }
    
    def _generate_instructions(self, concept: Dict[str, Any]) -> Dict[str, str]:
        """Generate game instructions and help"""
        
        return {
            'how_to_play': f"Welcome to {concept.get('title', 'the game')}! Use the controls to play and have fun!",
            'controls': "Use arrow keys to move and space bar for actions.",
            'objective': concept.get('objectives', ['Have fun!'])[0] if concept.get('objectives') else 'Have fun!',
            'tips': "Practice makes perfect! Try different strategies to improve your score."
        }
    
    def _init_sprite_library(self) -> Dict[str, List[str]]:
        """Initialize sprite library"""
        return {
            'platformer': ['player.png', 'platform.png', 'coin.png', 'enemy.png'],
            'puzzle': ['tile.png', 'background.png'],
            'shooter': ['player_ship.png', 'enemy_ship.png', 'bullet.png', 'explosion.png'],
            'rpg': ['hero.png', 'monster.png', 'treasure.png', 'potion.png'],
            'racing': ['car.png', 'track.png', 'finish_line.png'],
            'strategy': ['unit.png', 'building.png', 'resource.png']
        }
    
    def _init_sound_library(self) -> Dict[str, List[str]]:
        """Initialize sound library"""
        return {
            'platformer': ['jump.wav', 'coin.wav', 'hit.wav'],
            'puzzle': ['move.wav', 'success.wav', 'error.wav'],
            'shooter': ['shoot.wav', 'explosion.wav', 'powerup.wav'],
            'rpg': ['sword.wav', 'magic.wav', 'treasure.wav'],
            'racing': ['engine.wav', 'brake.wav', 'finish.wav'],
            'strategy': ['build.wav', 'attack.wav', 'victory.wav']
        }

# Global instance
game_engine = AIGameEngine()
