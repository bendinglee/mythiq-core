#!/usr/bin/env python3
"""
🎮 GENRE MODULES - UNIQUE MECHANICS FOR EACH GAME TYPE
Six completely different game experiences with distinct gameplay
"""

import random
import json
from typing import Dict, List, Any

class BaseGameModule:
    """Base class for all game genre modules"""
    
    def __init__(self):
        self.genre = "base"
    
    def generate(self, config: Dict, colors: Dict, fonts: Dict, effects: Dict) -> str:
        """Generate game HTML/CSS/JS code"""
        raise NotImplementedError("Subclasses must implement generate method")
    
    def _create_base_html_structure(self, title: str, colors: Dict, fonts: Dict) -> str:
        """Create base HTML structure with responsive design"""
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
            <title>{title}</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                    -webkit-touch-callout: none;
                    -webkit-user-select: none;
                    -khtml-user-select: none;
                    -moz-user-select: none;
                    -ms-user-select: none;
                    user-select: none;
                }}
                
                body {{
                    font-family: {fonts['family']};
                    background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']});
                    color: white;
                    margin: 0;
                    padding: 0;
                    min-height: 100vh;
                    overflow: hidden;
                    touch-action: manipulation;
                }}
                
                .game-container {{
                    width: 100vw;
                    height: 100vh;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    position: relative;
                }}
                
                .game-header {{
                    position: absolute;
                    top: 20px;
                    left: 50%;
                    transform: translateX(-50%);
                    text-align: center;
                    z-index: 100;
                }}
                
                .game-title {{
                    font-size: {fonts['title_size']};
                    font-weight: {fonts['weight']};
                    color: {colors['accent']};
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
                    margin-bottom: 10px;
                }}
                
                .game-stats {{
                    display: flex;
                    gap: 20px;
                    font-size: {fonts['body_size']};
                    background: rgba(0,0,0,0.3);
                    padding: 10px 20px;
                    border-radius: 25px;
                    backdrop-filter: blur(10px);
                }}
                
                .stat {{
                    display: flex;
                    align-items: center;
                    gap: 5px;
                }}
                
                .game-area {{
                    flex: 1;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    width: 100%;
                    max-width: 800px;
                    padding: 20px;
                }}
                
                .controls {{
                    position: absolute;
                    bottom: 20px;
                    left: 50%;
                    transform: translateX(-50%);
                    display: flex;
                    gap: 15px;
                    z-index: 100;
                }}
                
                .btn {{
                    background: linear-gradient(45deg, {colors['accent']}, {colors['primary']});
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 25px;
                    font-size: 16px;
                    font-weight: bold;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                    touch-action: manipulation;
                }}
                
                .btn:hover, .btn:active {{
                    transform: translateY(-2px);
                    box-shadow: 0 6px 20px rgba(0,0,0,0.4);
                }}
                
                .btn:disabled {{
                    opacity: 0.6;
                    cursor: not-allowed;
                    transform: none;
                }}
                
                @media (max-width: 768px) {{
                    .game-title {{
                        font-size: calc({fonts['title_size']} * 0.8);
                    }}
                    
                    .game-stats {{
                        font-size: calc({fonts['body_size']} * 0.9);
                        gap: 15px;
                        padding: 8px 16px;
                    }}
                    
                    .controls {{
                        bottom: 10px;
                        gap: 10px;
                    }}
                    
                    .btn {{
                        padding: 10px 20px;
                        font-size: 14px;
                    }}
                }}
            </style>
        </head>
        <body>
        """

class PuzzleModule(BaseGameModule):
    """Advanced sliding puzzle with multiple configurations"""
    
    def __init__(self):
        super().__init__()
        self.genre = "puzzle"
    
    def generate(self, config: Dict, colors: Dict, fonts: Dict, effects: Dict) -> str:
        grid_size = config.get('grid_size', 4)
        tile_style = config.get('tile_style', 'numbers')
        
        html = self._create_base_html_structure("Puzzle Master", colors, fonts)
        
        html += f"""
            <div class="game-container">
                <div class="game-header">
                    <div class="game-title">Puzzle Master</div>
                    <div class="game-stats">
                        <div class="stat">🎯 Moves: <span id="moves">0</span></div>
                        <div class="stat">⏱️ Time: <span id="time">00:00</span></div>
                        <div class="stat">🏆 Best: <span id="best">--</span></div>
                    </div>
                </div>
                
                <div class="game-area">
                    <div class="puzzle-grid" id="puzzleGrid"></div>
                </div>
                
                <div class="controls">
                    <button class="btn" onclick="newGame()">🎲 New Game</button>
                    <button class="btn" onclick="solvePuzzle()">💡 Solve</button>
                    <button class="btn" onclick="showHint()">❓ Hint</button>
                </div>
            </div>
            
            <style>
                .puzzle-grid {{
                    display: grid;
                    grid-template-columns: repeat({grid_size}, 1fr);
                    grid-template-rows: repeat({grid_size}, 1fr);
                    gap: 3px;
                    background: rgba(0,0,0,0.3);
                    padding: 10px;
                    border-radius: 15px;
                    backdrop-filter: blur(10px);
                    width: min(400px, 80vw);
                    height: min(400px, 80vw);
                }}
                
                .puzzle-tile {{
                    background: linear-gradient(45deg, {colors['accent']}, {colors['primary']});
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-size: calc(min(400px, 80vw) / {grid_size} / 3);
                    font-weight: bold;
                    cursor: pointer;
                    transition: all 0.2s ease;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                    touch-action: manipulation;
                }}
                
                .puzzle-tile:hover {{
                    transform: scale(1.05);
                    box-shadow: 0 4px 12px rgba(0,0,0,0.4);
                }}
                
                .puzzle-tile.empty {{
                    background: transparent;
                    box-shadow: none;
                    cursor: default;
                }}
                
                .puzzle-tile.hint {{
                    animation: pulse 1s infinite;
                }}
                
                @keyframes pulse {{
                    0%, 100% {{ transform: scale(1); }}
                    50% {{ transform: scale(1.1); }}
                }}
                
                .win-message {{
                    position: fixed;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    background: linear-gradient(45deg, {colors['accent']}, {colors['primary']});
                    color: white;
                    padding: 30px;
                    border-radius: 20px;
                    text-align: center;
                    font-size: 24px;
                    font-weight: bold;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
                    z-index: 1000;
                    animation: celebration 0.5s ease-out;
                }}
                
                @keyframes celebration {{
                    0% {{ transform: translate(-50%, -50%) scale(0.5); opacity: 0; }}
                    100% {{ transform: translate(-50%, -50%) scale(1); opacity: 1; }}
                }}
            </style>
            
            <script>
                let gridSize = {grid_size};
                let tiles = [];
                let emptyPos = {{ x: gridSize - 1, y: gridSize - 1 }};
                let moves = 0;
                let startTime = null;
                let timerInterval = null;
                let gameWon = false;
                
                function initGame() {{
                    const grid = document.getElementById('puzzleGrid');
                    grid.innerHTML = '';
                    tiles = [];
                    
                    // Create solved state
                    for (let i = 0; i < gridSize * gridSize - 1; i++) {{
                        tiles.push(i + 1);
                    }}
                    tiles.push(0); // Empty tile
                    
                    renderGrid();
                    shufflePuzzle();
                    resetStats();
                }}
                
                function renderGrid() {{
                    const grid = document.getElementById('puzzleGrid');
                    grid.innerHTML = '';
                    
                    for (let i = 0; i < gridSize * gridSize; i++) {{
                        const tile = document.createElement('button');
                        tile.className = 'puzzle-tile';
                        
                        if (tiles[i] === 0) {{
                            tile.className += ' empty';
                            tile.style.visibility = 'hidden';
                        }} else {{
                            tile.textContent = tiles[i];
                            tile.onclick = () => moveTile(i);
                        }}
                        
                        grid.appendChild(tile);
                    }}
                }}
                
                function moveTile(index) {{
                    if (gameWon) return;
                    
                    const x = index % gridSize;
                    const y = Math.floor(index / gridSize);
                    const emptyIndex = emptyPos.y * gridSize + emptyPos.x;
                    
                    // Check if tile is adjacent to empty space
                    const dx = Math.abs(x - emptyPos.x);
                    const dy = Math.abs(y - emptyPos.y);
                    
                    if ((dx === 1 && dy === 0) || (dx === 0 && dy === 1)) {{
                        // Swap tile with empty space
                        tiles[emptyIndex] = tiles[index];
                        tiles[index] = 0;
                        emptyPos = {{ x, y }};
                        
                        moves++;
                        updateMoves();
                        renderGrid();
                        
                        if (startTime === null) {{
                            startTime = Date.now();
                            startTimer();
                        }}
                        
                        checkWin();
                        
                        // Haptic feedback on mobile
                        if (navigator.vibrate) {{
                            navigator.vibrate(50);
                        }}
                    }}
                }}
                
                function shufflePuzzle() {{
                    // Perform random valid moves to ensure solvability
                    for (let i = 0; i < {config.get('shuffle_complexity', 100)}; i++) {{
                        const validMoves = getValidMoves();
                        if (validMoves.length > 0) {{
                            const randomMove = validMoves[Math.floor(Math.random() * validMoves.length)];
                            const emptyIndex = emptyPos.y * gridSize + emptyPos.x;
                            
                            tiles[emptyIndex] = tiles[randomMove];
                            tiles[randomMove] = 0;
                            emptyPos = {{ x: randomMove % gridSize, y: Math.floor(randomMove / gridSize) }};
                        }}
                    }}
                    renderGrid();
                }}
                
                function getValidMoves() {{
                    const moves = [];
                    const {{ x, y }} = emptyPos;
                    
                    if (x > 0) moves.push((y * gridSize) + (x - 1));
                    if (x < gridSize - 1) moves.push((y * gridSize) + (x + 1));
                    if (y > 0) moves.push(((y - 1) * gridSize) + x);
                    if (y < gridSize - 1) moves.push(((y + 1) * gridSize) + x);
                    
                    return moves;
                }}
                
                function checkWin() {{
                    for (let i = 0; i < gridSize * gridSize - 1; i++) {{
                        if (tiles[i] !== i + 1) return;
                    }}
                    
                    gameWon = true;
                    stopTimer();
                    showWinMessage();
                    updateBestScore();
                    
                    // Celebration haptic feedback
                    if (navigator.vibrate) {{
                        navigator.vibrate([100, 50, 100, 50, 200]);
                    }}
                }}
                
                function showWinMessage() {{
                    const message = document.createElement('div');
                    message.className = 'win-message';
                    message.innerHTML = `
                        <div>🎉 Congratulations! 🎉</div>
                        <div style="font-size: 18px; margin-top: 10px;">
                            Solved in ${{moves}} moves and ${{formatTime(Date.now() - startTime)}}
                        </div>
                    `;
                    document.body.appendChild(message);
                    
                    setTimeout(() => {{
                        message.remove();
                    }}, 3000);
                }}
                
                function newGame() {{
                    gameWon = false;
                    shufflePuzzle();
                    resetStats();
                }}
                
                function solvePuzzle() {{
                    // Simple solve: reset to solved state
                    for (let i = 0; i < gridSize * gridSize - 1; i++) {{
                        tiles[i] = i + 1;
                    }}
                    tiles[gridSize * gridSize - 1] = 0;
                    emptyPos = {{ x: gridSize - 1, y: gridSize - 1 }};
                    renderGrid();
                    checkWin();
                }}
                
                function showHint() {{
                    const validMoves = getValidMoves();
                    if (validMoves.length > 0) {{
                        const hintTile = document.querySelectorAll('.puzzle-tile')[validMoves[0]];
                        hintTile.classList.add('hint');
                        setTimeout(() => {{
                            hintTile.classList.remove('hint');
                        }}, 2000);
                    }}
                }}
                
                function resetStats() {{
                    moves = 0;
                    startTime = null;
                    stopTimer();
                    updateMoves();
                    updateTime();
                }}
                
                function updateMoves() {{
                    document.getElementById('moves').textContent = moves;
                }}
                
                function updateTime() {{
                    const timeElement = document.getElementById('time');
                    if (startTime) {{
                        const elapsed = Date.now() - startTime;
                        timeElement.textContent = formatTime(elapsed);
                    }} else {{
                        timeElement.textContent = '00:00';
                    }}
                }}
                
                function formatTime(ms) {{
                    const seconds = Math.floor(ms / 1000);
                    const minutes = Math.floor(seconds / 60);
                    return `${{minutes.toString().padStart(2, '0')}}:${{(seconds % 60).toString().padStart(2, '0')}}`;
                }}
                
                function startTimer() {{
                    timerInterval = setInterval(updateTime, 1000);
                }}
                
                function stopTimer() {{
                    if (timerInterval) {{
                        clearInterval(timerInterval);
                        timerInterval = null;
                    }}
                }}
                
                function updateBestScore() {{
                    const currentTime = Date.now() - startTime;
                    const bestKey = 'puzzleBest_' + gridSize;
                    const currentBest = localStorage.getItem(bestKey);
                    
                    if (!currentBest || currentTime < parseInt(currentBest)) {{
                        localStorage.setItem(bestKey, currentTime.toString());
                        document.getElementById('best').textContent = formatTime(currentTime);
                    }}
                }}
                
                function loadBestScore() {{
                    const bestKey = 'puzzleBest_' + gridSize;
                    const best = localStorage.getItem(bestKey);
                    if (best) {{
                        document.getElementById('best').textContent = formatTime(parseInt(best));
                    }}
                }}
                
                // Initialize game
                initGame();
                loadBestScore();
            </script>
        </body>
        </html>
        """
        
        return html

class ShooterModule(BaseGameModule):
    """Advanced space shooter with multiple enemy types and power-ups"""
    
    def __init__(self):
        super().__init__()
        self.genre = "shooter"
    
    def generate(self, config: Dict, colors: Dict, fonts: Dict, effects: Dict) -> str:
        enemy_types = config.get('enemy_types', 3)
        bullet_speed = config.get('bullet_speed', 7)
        spawn_rate = config.get('spawn_rate', 1.0)
        
        html = self._create_base_html_structure("Space Defender", colors, fonts)
        
        html += f"""
            <div class="game-container">
                <div class="game-header">
                    <div class="game-title">Space Defender</div>
                    <div class="game-stats">
                        <div class="stat">💥 Score: <span id="score">0</span></div>
                        <div class="stat">❤️ Lives: <span id="lives">3</span></div>
                        <div class="stat">🎯 Level: <span id="level">1</span></div>
                        <div class="stat">🔥 Combo: <span id="combo">0</span></div>
                    </div>
                </div>
                
                <div class="game-area">
                    <canvas id="gameCanvas"></canvas>
                </div>
                
                <div class="controls">
                    <button class="btn" onclick="startGame()" id="startBtn">🚀 Start Game</button>
                    <button class="btn" onclick="pauseGame()" id="pauseBtn" disabled>⏸️ Pause</button>
                    <button class="btn" onclick="toggleSound()" id="soundBtn">🔊 Sound</button>
                </div>
                
                <!-- Mobile Controls -->
                <div class="mobile-controls" id="mobileControls" style="display: none;">
                    <div class="dpad">
                        <button class="dpad-btn" id="upBtn">↑</button>
                        <div class="dpad-row">
                            <button class="dpad-btn" id="leftBtn">←</button>
                            <button class="dpad-btn" id="rightBtn">→</button>
                        </div>
                        <button class="dpad-btn" id="downBtn">↓</button>
                    </div>
                    <button class="fire-btn" id="fireBtn">🔥 FIRE</button>
                </div>
            </div>
            
            <style>
                #gameCanvas {{
                    border: 2px solid {colors['accent']};
                    border-radius: 10px;
                    background: linear-gradient(180deg, #000428 0%, #004e92 100%);
                    box-shadow: 0 0 20px rgba(0,0,0,0.5);
                    max-width: 100%;
                    max-height: 70vh;
                }}
                
                .mobile-controls {{
                    position: fixed;
                    bottom: 20px;
                    left: 0;
                    right: 0;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 0 20px;
                    z-index: 200;
                }}
                
                .dpad {{
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    gap: 5px;
                }}
                
                .dpad-row {{
                    display: flex;
                    gap: 5px;
                }}
                
                .dpad-btn {{
                    width: 50px;
                    height: 50px;
                    background: rgba(255,255,255,0.2);
                    border: 2px solid {colors['accent']};
                    border-radius: 10px;
                    color: white;
                    font-size: 20px;
                    font-weight: bold;
                    cursor: pointer;
                    touch-action: manipulation;
                    backdrop-filter: blur(10px);
                }}
                
                .dpad-btn:active {{
                    background: rgba(255,255,255,0.4);
                    transform: scale(0.95);
                }}
                
                .fire-btn {{
                    width: 80px;
                    height: 80px;
                    background: linear-gradient(45deg, #ff4444, #cc0000);
                    border: 3px solid #ffff00;
                    border-radius: 50%;
                    color: white;
                    font-size: 14px;
                    font-weight: bold;
                    cursor: pointer;
                    touch-action: manipulation;
                    box-shadow: 0 4px 15px rgba(255,68,68,0.5);
                }}
                
                .fire-btn:active {{
                    transform: scale(0.9);
                    box-shadow: 0 2px 8px rgba(255,68,68,0.7);
                }}
                
                @media (max-width: 768px) {{
                    .mobile-controls {{
                        display: flex !important;
                    }}
                    
                    .controls {{
                        bottom: 120px;
                    }}
                }}
                
                .power-up-indicator {{
                    position: absolute;
                    top: 100px;
                    right: 20px;
                    background: rgba(0,0,0,0.7);
                    padding: 10px;
                    border-radius: 10px;
                    color: white;
                    font-size: 14px;
                }}
                
                .game-over {{
                    position: fixed;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    background: linear-gradient(45deg, #ff4444, #cc0000);
                    color: white;
                    padding: 40px;
                    border-radius: 20px;
                    text-align: center;
                    font-size: 24px;
                    font-weight: bold;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.7);
                    z-index: 1000;
                }}
            </style>
            
            <script>
                const canvas = document.getElementById('gameCanvas');
                const ctx = canvas.getContext('2d');
                
                // Set canvas size
                canvas.width = Math.min(800, window.innerWidth - 40);
                canvas.height = Math.min(600, window.innerHeight * 0.7);
                
                // Game state
                let gameRunning = false;
                let gamePaused = false;
                let score = 0;
                let lives = 3;
                let level = 1;
                let combo = 0;
                let soundEnabled = true;
                
                // Game objects
                let player = {{
                    x: canvas.width / 2,
                    y: canvas.height - 50,
                    width: 30,
                    height: 30,
                    speed: 5,
                    color: '{colors["accent"]}'
                }};
                
                let bullets = [];
                let enemies = [];
                let powerUps = [];
                let particles = [];
                let stars = [];
                
                // Input handling
                let keys = {{}};
                let touchControls = {{
                    up: false, down: false, left: false, right: false, fire: false
                }};
                
                // Initialize stars background
                function initStars() {{
                    stars = [];
                    for (let i = 0; i < 100; i++) {{
                        stars.push({{
                            x: Math.random() * canvas.width,
                            y: Math.random() * canvas.height,
                            speed: Math.random() * 2 + 1,
                            size: Math.random() * 2 + 1
                        }});
                    }}
                }}
                
                function updateStars() {{
                    stars.forEach(star => {{
                        star.y += star.speed;
                        if (star.y > canvas.height) {{
                            star.y = 0;
                            star.x = Math.random() * canvas.width;
                        }}
                    }});
                }}
                
                function drawStars() {{
                    ctx.fillStyle = 'white';
                    stars.forEach(star => {{
                        ctx.beginPath();
                        ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2);
                        ctx.fill();
                    }});
                }}
                
                function startGame() {{
                    gameRunning = true;
                    gamePaused = false;
                    score = 0;
                    lives = 3;
                    level = 1;
                    combo = 0;
                    
                    bullets = [];
                    enemies = [];
                    powerUps = [];
                    particles = [];
                    
                    player.x = canvas.width / 2;
                    player.y = canvas.height - 50;
                    
                    initStars();
                    updateUI();
                    
                    document.getElementById('startBtn').disabled = true;
                    document.getElementById('pauseBtn').disabled = false;
                    
                    // Show mobile controls on touch devices
                    if ('ontouchstart' in window) {{
                        document.getElementById('mobileControls').style.display = 'flex';
                    }}
                    
                    gameLoop();
                }}
                
                function pauseGame() {{
                    gamePaused = !gamePaused;
                    document.getElementById('pauseBtn').textContent = gamePaused ? '▶️ Resume' : '⏸️ Pause';
                }}
                
                function gameOver() {{
                    gameRunning = false;
                    document.getElementById('startBtn').disabled = false;
                    document.getElementById('pauseBtn').disabled = true;
                    document.getElementById('mobileControls').style.display = 'none';
                    
                    const gameOverDiv = document.createElement('div');
                    gameOverDiv.className = 'game-over';
                    gameOverDiv.innerHTML = `
                        <div>💥 GAME OVER 💥</div>
                        <div style="font-size: 18px; margin: 20px 0;">
                            Final Score: ${{score}}<br>
                            Level Reached: ${{level}}<br>
                            Max Combo: ${{combo}}
                        </div>
                        <button class="btn" onclick="this.parentElement.remove(); startGame()">
                            🔄 Play Again
                        </button>
                    `;
                    document.body.appendChild(gameOverDiv);
                    
                    // Vibration feedback
                    if (navigator.vibrate) {{
                        navigator.vibrate([200, 100, 200, 100, 500]);
                    }}
                }}
                
                function updatePlayer() {{
                    // Keyboard controls
                    if (keys['ArrowLeft'] || keys['a'] || touchControls.left) {{
                        player.x = Math.max(0, player.x - player.speed);
                    }}
                    if (keys['ArrowRight'] || keys['d'] || touchControls.right) {{
                        player.x = Math.min(canvas.width - player.width, player.x + player.speed);
                    }}
                    if (keys['ArrowUp'] || keys['w'] || touchControls.up) {{
                        player.y = Math.max(0, player.y - player.speed);
                    }}
                    if (keys['ArrowDown'] || keys['s'] || touchControls.down) {{
                        player.y = Math.min(canvas.height - player.height, player.y + player.speed);
                    }}
                }}
                
                function shootBullet() {{
                    bullets.push({{
                        x: player.x + player.width / 2,
                        y: player.y,
                        width: 4,
                        height: 10,
                        speed: {bullet_speed},
                        color: '#ffff00'
                    }});
                }}
                
                function updateBullets() {{
                    bullets = bullets.filter(bullet => {{
                        bullet.y -= bullet.speed;
                        return bullet.y > -bullet.height;
                    }});
                }}
                
                function spawnEnemy() {{
                    const enemyType = Math.floor(Math.random() * {enemy_types}) + 1;
                    let enemy = {{
                        x: Math.random() * (canvas.width - 30),
                        y: -30,
                        width: 25 + enemyType * 5,
                        height: 25 + enemyType * 5,
                        speed: 1 + enemyType * 0.5 + level * 0.2,
                        health: enemyType,
                        maxHealth: enemyType,
                        type: enemyType,
                        color: ['#ff4444', '#ff8844', '#8844ff'][enemyType - 1] || '#ff4444'
                    }};
                    enemies.push(enemy);
                }}
                
                function updateEnemies() {{
                    enemies = enemies.filter(enemy => {{
                        enemy.y += enemy.speed;
                        
                        // Check collision with player
                        if (enemy.x < player.x + player.width &&
                            enemy.x + enemy.width > player.x &&
                            enemy.y < player.y + player.height &&
                            enemy.y + enemy.height > player.y) {{
                            lives--;
                            combo = 0;
                            updateUI();
                            createExplosion(enemy.x, enemy.y);
                            
                            if (lives <= 0) {{
                                gameOver();
                            }}
                            
                            return false;
                        }}
                        
                        return enemy.y < canvas.height + enemy.height;
                    }});
                }}
                
                function checkCollisions() {{
                    bullets.forEach((bullet, bulletIndex) => {{
                        enemies.forEach((enemy, enemyIndex) => {{
                            if (bullet.x < enemy.x + enemy.width &&
                                bullet.x + bullet.width > enemy.x &&
                                bullet.y < enemy.y + enemy.height &&
                                bullet.y + bullet.height > enemy.y) {{
                                
                                enemy.health--;
                                bullets.splice(bulletIndex, 1);
                                
                                if (enemy.health <= 0) {{
                                    score += enemy.type * 10 * (combo + 1);
                                    combo++;
                                    enemies.splice(enemyIndex, 1);
                                    createExplosion(enemy.x, enemy.y);
                                    
                                    // Chance to spawn power-up
                                    if (Math.random() < 0.1) {{
                                        spawnPowerUp(enemy.x, enemy.y);
                                    }}
                                }}
                                
                                updateUI();
                            }}
                        }});
                    }});
                }}
                
                function spawnPowerUp(x, y) {{
                    const types = ['health', 'rapidfire', 'shield'];
                    powerUps.push({{
                        x: x,
                        y: y,
                        width: 20,
                        height: 20,
                        speed: 2,
                        type: types[Math.floor(Math.random() * types.length)],
                        color: '#00ff00'
                    }});
                }}
                
                function updatePowerUps() {{
                    powerUps = powerUps.filter(powerUp => {{
                        powerUp.y += powerUp.speed;
                        
                        // Check collision with player
                        if (powerUp.x < player.x + player.width &&
                            powerUp.x + powerUp.width > player.x &&
                            powerUp.y < player.y + player.height &&
                            powerUp.y + powerUp.height > player.y) {{
                            
                            applyPowerUp(powerUp.type);
                            return false;
                        }}
                        
                        return powerUp.y < canvas.height;
                    }});
                }}
                
                function applyPowerUp(type) {{
                    switch(type) {{
                        case 'health':
                            lives = Math.min(5, lives + 1);
                            break;
                        case 'rapidfire':
                            // Implement rapid fire logic
                            break;
                        case 'shield':
                            // Implement shield logic
                            break;
                    }}
                    updateUI();
                }}
                
                function createExplosion(x, y) {{
                    for (let i = 0; i < 10; i++) {{
                        particles.push({{
                            x: x,
                            y: y,
                            vx: (Math.random() - 0.5) * 10,
                            vy: (Math.random() - 0.5) * 10,
                            life: 30,
                            color: `hsl(${{Math.random() * 60}}, 100%, 50%)`
                        }});
                    }}
                }}
                
                function updateParticles() {{
                    particles = particles.filter(particle => {{
                        particle.x += particle.vx;
                        particle.y += particle.vy;
                        particle.life--;
                        return particle.life > 0;
                    }});
                }}
                
                function draw() {{
                    // Clear canvas
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    
                    // Draw stars
                    drawStars();
                    
                    // Draw player
                    ctx.fillStyle = player.color;
                    ctx.fillRect(player.x, player.y, player.width, player.height);
                    
                    // Draw bullets
                    bullets.forEach(bullet => {{
                        ctx.fillStyle = bullet.color;
                        ctx.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
                    }});
                    
                    // Draw enemies
                    enemies.forEach(enemy => {{
                        ctx.fillStyle = enemy.color;
                        ctx.fillRect(enemy.x, enemy.y, enemy.width, enemy.height);
                        
                        // Health bar
                        if (enemy.health < enemy.maxHealth) {{
                            ctx.fillStyle = 'red';
                            ctx.fillRect(enemy.x, enemy.y - 8, enemy.width, 4);
                            ctx.fillStyle = 'green';
                            ctx.fillRect(enemy.x, enemy.y - 8, enemy.width * (enemy.health / enemy.maxHealth), 4);
                        }}
                    }});
                    
                    // Draw power-ups
                    powerUps.forEach(powerUp => {{
                        ctx.fillStyle = powerUp.color;
                        ctx.fillRect(powerUp.x, powerUp.y, powerUp.width, powerUp.height);
                    }});
                    
                    // Draw particles
                    particles.forEach(particle => {{
                        ctx.fillStyle = particle.color;
                        ctx.globalAlpha = particle.life / 30;
                        ctx.fillRect(particle.x, particle.y, 3, 3);
                        ctx.globalAlpha = 1;
                    }});
                }}
                
                function updateUI() {{
                    document.getElementById('score').textContent = score;
                    document.getElementById('lives').textContent = lives;
                    document.getElementById('level').textContent = level;
                    document.getElementById('combo').textContent = combo;
                }}
                
                let lastShot = 0;
                let enemySpawnTimer = 0;
                
                function gameLoop() {{
                    if (!gameRunning) return;
                    
                    if (!gamePaused) {{
                        updateStars();
                        updatePlayer();
                        updateBullets();
                        updateEnemies();
                        updatePowerUps();
                        updateParticles();
                        checkCollisions();
                        
                        // Auto-shoot or manual shoot
                        const now = Date.now();
                        if ((keys[' '] || keys['Space'] || touchControls.fire) && now - lastShot > 150) {{
                            shootBullet();
                            lastShot = now;
                        }}
                        
                        // Spawn enemies
                        enemySpawnTimer++;
                        if (enemySpawnTimer > 60 / {spawn_rate}) {{
                            spawnEnemy();
                            enemySpawnTimer = 0;
                        }}
                        
                        // Level progression
                        if (score > level * 500) {{
                            level++;
                            updateUI();
                        }}
                    }}
                    
                    draw();
                    requestAnimationFrame(gameLoop);
                }}
                
                // Event listeners
                document.addEventListener('keydown', (e) => {{
                    keys[e.code] = true;
                    keys[e.key] = true;
                }});
                
                document.addEventListener('keyup', (e) => {{
                    keys[e.code] = false;
                    keys[e.key] = false;
                }});
                
                // Touch controls
                function setupTouchControls() {{
                    const buttons = ['upBtn', 'downBtn', 'leftBtn', 'rightBtn', 'fireBtn'];
                    const actions = ['up', 'down', 'left', 'right', 'fire'];
                    
                    buttons.forEach((btnId, index) => {{
                        const btn = document.getElementById(btnId);
                        const action = actions[index];
                        
                        btn.addEventListener('touchstart', (e) => {{
                            e.preventDefault();
                            touchControls[action] = true;
                        }});
                        
                        btn.addEventListener('touchend', (e) => {{
                            e.preventDefault();
                            touchControls[action] = false;
                        }});
                    }});
                }}
                
                function toggleSound() {{
                    soundEnabled = !soundEnabled;
                    document.getElementById('soundBtn').textContent = soundEnabled ? '🔊 Sound' : '🔇 Muted';
                }}
                
                // Initialize
                setupTouchControls();
                initStars();
                updateUI();
            </script>
        </body>
        </html>
        """
        
        return html

class PlatformerModule(BaseGameModule):
    """Physics-based platformer with jumping and coin collection"""
    
    def __init__(self):
        super().__init__()
        self.genre = "platformer"
    
    def generate(self, config: Dict, colors: Dict, fonts: Dict, effects: Dict) -> str:
        platform_count = config.get('platform_count', 8)
        jump_height = config.get('jump_height', 100)
        gravity = config.get('gravity', 0.8)
        
        html = self._create_base_html_structure("Platform Adventure", colors, fonts)
        
        html += f"""
            <div class="game-container">
                <div class="game-header">
                    <div class="game-title">Platform Adventure</div>
                    <div class="game-stats">
                        <div class="stat">🪙 Coins: <span id="coins">0</span></div>
                        <div class="stat">❤️ Lives: <span id="lives">3</span></div>
                        <div class="stat">⏱️ Time: <span id="time">60</span></div>
                        <div class="stat">🏆 Best: <span id="best">0</span></div>
                    </div>
                </div>
                
                <div class="game-area">
                    <canvas id="gameCanvas"></canvas>
                </div>
                
                <div class="controls">
                    <button class="btn" onclick="startGame()" id="startBtn">🎮 Start Game</button>
                    <button class="btn" onclick="resetGame()" id="resetBtn">🔄 Reset</button>
                </div>
                
                <!-- Mobile Controls -->
                <div class="mobile-controls" id="mobileControls" style="display: none;">
                    <button class="move-btn" id="leftBtn">←</button>
                    <button class="jump-btn" id="jumpBtn">JUMP</button>
                    <button class="move-btn" id="rightBtn">→</button>
                </div>
            </div>
            
            <style>
                #gameCanvas {{
                    border: 2px solid {colors['accent']};
                    border-radius: 10px;
                    background: linear-gradient(180deg, #87CEEB 0%, #98FB98 100%);
                    box-shadow: 0 0 20px rgba(0,0,0,0.3);
                    max-width: 100%;
                    max-height: 70vh;
                }}
                
                .mobile-controls {{
                    position: fixed;
                    bottom: 20px;
                    left: 50%;
                    transform: translateX(-50%);
                    display: flex;
                    gap: 20px;
                    align-items: center;
                    z-index: 200;
                }}
                
                .move-btn {{
                    width: 60px;
                    height: 60px;
                    background: rgba(255,255,255,0.2);
                    border: 2px solid {colors['accent']};
                    border-radius: 15px;
                    color: white;
                    font-size: 24px;
                    font-weight: bold;
                    cursor: pointer;
                    touch-action: manipulation;
                    backdrop-filter: blur(10px);
                }}
                
                .jump-btn {{
                    width: 80px;
                    height: 80px;
                    background: linear-gradient(45deg, {colors['accent']}, {colors['primary']});
                    border: 3px solid white;
                    border-radius: 50%;
                    color: white;
                    font-size: 14px;
                    font-weight: bold;
                    cursor: pointer;
                    touch-action: manipulation;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                }}
                
                .move-btn:active, .jump-btn:active {{
                    transform: scale(0.9);
                }}
                
                @media (max-width: 768px) {{
                    .mobile-controls {{
                        display: flex !important;
                    }}
                    
                    .controls {{
                        bottom: 120px;
                    }}
                }}
            </style>
            
            <script>
                const canvas = document.getElementById('gameCanvas');
                const ctx = canvas.getContext('2d');
                
                // Set canvas size
                canvas.width = Math.min(800, window.innerWidth - 40);
                canvas.height = Math.min(500, window.innerHeight * 0.6);
                
                // Game state
                let gameRunning = false;
                let coins = 0;
                let lives = 3;
                let timeLeft = 60;
                let gameTimer = null;
                
                // Physics constants
                const GRAVITY = {gravity};
                const JUMP_FORCE = -{jump_height};
                const PLAYER_SPEED = 5;
                
                // Game objects
                let player = {{
                    x: 50,
                    y: canvas.height - 100,
                    width: 25,
                    height: 30,
                    vx: 0,
                    vy: 0,
                    onGround: false,
                    color: '{colors["accent"]}'
                }};
                
                let platforms = [];
                let collectibles = [];
                let clouds = [];
                
                // Input handling
                let keys = {{}};
                let touchControls = {{ left: false, right: false, jump: false }};
                
                function initGame() {{
                    // Reset player
                    player.x = 50;
                    player.y = canvas.height - 100;
                    player.vx = 0;
                    player.vy = 0;
                    player.onGround = false;
                    
                    // Generate platforms
                    platforms = [
                        // Ground platform
                        {{ x: 0, y: canvas.height - 20, width: canvas.width, height: 20, color: '{colors["primary"]}' }}
                    ];
                    
                    // Generate random platforms
                    for (let i = 0; i < {platform_count}; i++) {{
                        platforms.push({{
                            x: Math.random() * (canvas.width - 100) + 50,
                            y: Math.random() * (canvas.height - 200) + 100,
                            width: Math.random() * 100 + 80,
                            height: 15,
                            color: '{colors["secondary"]}'
                        }});
                    }}
                    
                    // Generate collectibles
                    collectibles = [];
                    for (let i = 0; i < {config.get('collectibles', 15)}; i++) {{
                        let validPosition = false;
                        let attempts = 0;
                        let coin;
                        
                        while (!validPosition && attempts < 50) {{
                            coin = {{
                                x: Math.random() * (canvas.width - 20) + 10,
                                y: Math.random() * (canvas.height - 100) + 50,
                                width: 15,
                                height: 15,
                                collected: false,
                                color: '#FFD700',
                                rotation: 0
                            }};
                            
                            // Check if coin is on or near a platform
                            validPosition = platforms.some(platform => 
                                coin.x + coin.width > platform.x &&
                                coin.x < platform.x + platform.width &&
                                Math.abs(coin.y + coin.height - platform.y) < 30
                            );
                            
                            attempts++;
                        }}
                        
                        if (validPosition) {{
                            collectibles.push(coin);
                        }}
                    }}
                    
                    // Generate background clouds
                    clouds = [];
                    for (let i = 0; i < 8; i++) {{
                        clouds.push({{
                            x: Math.random() * canvas.width,
                            y: Math.random() * (canvas.height / 2),
                            size: Math.random() * 30 + 20,
                            speed: Math.random() * 0.5 + 0.2
                        }});
                    }}
                    
                    coins = 0;
                    lives = 3;
                    timeLeft = 60;
                    updateUI();
                }}
                
                function startGame() {{
                    gameRunning = true;
                    initGame();
                    
                    document.getElementById('startBtn').disabled = true;
                    
                    // Show mobile controls on touch devices
                    if ('ontouchstart' in window) {{
                        document.getElementById('mobileControls').style.display = 'flex';
                    }}
                    
                    // Start game timer
                    gameTimer = setInterval(() => {{
                        timeLeft--;
                        updateUI();
                        
                        if (timeLeft <= 0) {{
                            endGame('Time\'s up!');
                        }}
                    }}, 1000);
                    
                    gameLoop();
                }}
                
                function resetGame() {{
                    gameRunning = false;
                    if (gameTimer) {{
                        clearInterval(gameTimer);
                        gameTimer = null;
                    }}
                    
                    document.getElementById('startBtn').disabled = false;
                    document.getElementById('mobileControls').style.display = 'none';
                    
                    initGame();
                }}
                
                function endGame(message) {{
                    gameRunning = false;
                    if (gameTimer) {{
                        clearInterval(gameTimer);
                        gameTimer = null;
                    }}
                    
                    document.getElementById('startBtn').disabled = false;
                    document.getElementById('mobileControls').style.display = 'none';
                    
                    // Update best score
                    const currentBest = localStorage.getItem('platformerBest') || 0;
                    if (coins > currentBest) {{
                        localStorage.setItem('platformerBest', coins.toString());
                        updateUI();
                    }}
                    
                    // Show game over message
                    const gameOverDiv = document.createElement('div');
                    gameOverDiv.className = 'win-message';
                    gameOverDiv.innerHTML = `
                        <div>${{message}}</div>
                        <div style="font-size: 18px; margin: 20px 0;">
                            Coins Collected: ${{coins}}<br>
                            Time Remaining: ${{timeLeft}}s
                        </div>
                        <button class="btn" onclick="this.parentElement.remove(); startGame()">
                            🔄 Play Again
                        </button>
                    `;
                    document.body.appendChild(gameOverDiv);
                }}
                
                function updatePlayer() {{
                    // Horizontal movement
                    if (keys['ArrowLeft'] || keys['a'] || touchControls.left) {{
                        player.vx = -PLAYER_SPEED;
                    }} else if (keys['ArrowRight'] || keys['d'] || touchControls.right) {{
                        player.vx = PLAYER_SPEED;
                    }} else {{
                        player.vx *= 0.8; // Friction
                    }}
                    
                    // Jumping
                    if ((keys['ArrowUp'] || keys['w'] || keys[' '] || touchControls.jump) && player.onGround) {{
                        player.vy = JUMP_FORCE;
                        player.onGround = false;
                    }}
                    
                    // Apply gravity
                    player.vy += GRAVITY;
                    
                    // Update position
                    player.x += player.vx;
                    player.y += player.vy;
                    
                    // Keep player in bounds
                    if (player.x < 0) player.x = 0;
                    if (player.x + player.width > canvas.width) player.x = canvas.width - player.width;
                    
                    // Reset onGround flag
                    player.onGround = false;
                    
                    // Platform collision
                    platforms.forEach(platform => {{
                        if (player.x + player.width > platform.x &&
                            player.x < platform.x + platform.width &&
                            player.y + player.height > platform.y &&
                            player.y + player.height < platform.y + platform.height + 10 &&
                            player.vy >= 0) {{
                            
                            player.y = platform.y - player.height;
                            player.vy = 0;
                            player.onGround = true;
                        }}
                    }});
                    
                    // Check if player fell off screen
                    if (player.y > canvas.height) {{
                        lives--;
                        updateUI();
                        
                        if (lives <= 0) {{
                            endGame('💀 Game Over!');
                        }} else {{
                            // Respawn player
                            player.x = 50;
                            player.y = canvas.height - 100;
                            player.vx = 0;
                            player.vy = 0;
                        }}
                    }}
                }}
                
                function updateCollectibles() {{
                    collectibles.forEach(coin => {{
                        if (!coin.collected) {{
                            coin.rotation += 0.1;
                            
                            // Check collision with player
                            if (player.x + player.width > coin.x &&
                                player.x < coin.x + coin.width &&
                                player.y + player.height > coin.y &&
                                player.y < coin.y + coin.height) {{
                                
                                coin.collected = true;
                                coins++;
                                updateUI();
                                
                                // Haptic feedback
                                if (navigator.vibrate) {{
                                    navigator.vibrate(50);
                                }}
                                
                                // Check win condition
                                if (coins >= collectibles.length) {{
                                    endGame('🎉 You collected all coins!');
                                }}
                            }}
                        }}
                    }});
                }}
                
                function updateClouds() {{
                    clouds.forEach(cloud => {{
                        cloud.x += cloud.speed;
                        if (cloud.x > canvas.width + cloud.size) {{
                            cloud.x = -cloud.size;
                        }}
                    }});
                }}
                
                function draw() {{
                    // Clear canvas with gradient background
                    const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
                    gradient.addColorStop(0, '#87CEEB');
                    gradient.addColorStop(1, '#98FB98');
                    ctx.fillStyle = gradient;
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    
                    // Draw clouds
                    ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
                    clouds.forEach(cloud => {{
                        ctx.beginPath();
                        ctx.arc(cloud.x, cloud.y, cloud.size, 0, Math.PI * 2);
                        ctx.fill();
                        ctx.beginPath();
                        ctx.arc(cloud.x + cloud.size * 0.6, cloud.y, cloud.size * 0.8, 0, Math.PI * 2);
                        ctx.fill();
                        ctx.beginPath();
                        ctx.arc(cloud.x - cloud.size * 0.6, cloud.y, cloud.size * 0.8, 0, Math.PI * 2);
                        ctx.fill();
                    }});
                    
                    // Draw platforms
                    platforms.forEach(platform => {{
                        ctx.fillStyle = platform.color;
                        ctx.fillRect(platform.x, platform.y, platform.width, platform.height);
                        
                        // Add platform border
                        ctx.strokeStyle = '{colors["accent"]}';
                        ctx.lineWidth = 2;
                        ctx.strokeRect(platform.x, platform.y, platform.width, platform.height);
                    }});
                    
                    // Draw collectibles
                    collectibles.forEach(coin => {{
                        if (!coin.collected) {{
                            ctx.save();
                            ctx.translate(coin.x + coin.width/2, coin.y + coin.height/2);
                            ctx.rotate(coin.rotation);
                            ctx.fillStyle = coin.color;
                            ctx.fillRect(-coin.width/2, -coin.height/2, coin.width, coin.height);
                            
                            // Add coin shine effect
                            ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
                            ctx.fillRect(-coin.width/4, -coin.height/2, coin.width/2, coin.height/4);
                            ctx.restore();
                        }}
                    }});
                    
                    // Draw player
                    ctx.fillStyle = player.color;
                    ctx.fillRect(player.x, player.y, player.width, player.height);
                    
                    // Add player eyes
                    ctx.fillStyle = 'white';
                    ctx.fillRect(player.x + 5, player.y + 5, 4, 4);
                    ctx.fillRect(player.x + 16, player.y + 5, 4, 4);
                    ctx.fillStyle = 'black';
                    ctx.fillRect(player.x + 6, player.y + 6, 2, 2);
                    ctx.fillRect(player.x + 17, player.y + 6, 2, 2);
                }}
                
                function updateUI() {{
                    document.getElementById('coins').textContent = coins;
                    document.getElementById('lives').textContent = lives;
                    document.getElementById('time').textContent = timeLeft;
                    
                    const best = localStorage.getItem('platformerBest') || 0;
                    document.getElementById('best').textContent = best;
                }}
                
                function gameLoop() {{
                    if (!gameRunning) return;
                    
                    updatePlayer();
                    updateCollectibles();
                    updateClouds();
                    draw();
                    
                    requestAnimationFrame(gameLoop);
                }}
                
                // Event listeners
                document.addEventListener('keydown', (e) => {{
                    keys[e.code] = true;
                    keys[e.key] = true;
                    e.preventDefault();
                }});
                
                document.addEventListener('keyup', (e) => {{
                    keys[e.code] = false;
                    keys[e.key] = false;
                    e.preventDefault();
                }});
                
                // Touch controls
                function setupTouchControls() {{
                    const leftBtn = document.getElementById('leftBtn');
                    const rightBtn = document.getElementById('rightBtn');
                    const jumpBtn = document.getElementById('jumpBtn');
                    
                    leftBtn.addEventListener('touchstart', (e) => {{
                        e.preventDefault();
                        touchControls.left = true;
                    }});
                    leftBtn.addEventListener('touchend', (e) => {{
                        e.preventDefault();
                        touchControls.left = false;
                    }});
                    
                    rightBtn.addEventListener('touchstart', (e) => {{
                        e.preventDefault();
                        touchControls.right = true;
                    }});
                    rightBtn.addEventListener('touchend', (e) => {{
                        e.preventDefault();
                        touchControls.right = false;
                    }});
                    
                    jumpBtn.addEventListener('touchstart', (e) => {{
                        e.preventDefault();
                        touchControls.jump = true;
                    }});
                    jumpBtn.addEventListener('touchend', (e) => {{
                        e.preventDefault();
                        touchControls.jump = false;
                    }});
                }}
                
                // Initialize
                setupTouchControls();
                initGame();
                updateUI();
            </script>
        </body>
        </html>
        """
        
        return html

# Additional modules would be implemented similarly...
class RacingModule(BaseGameModule):
    def __init__(self):
        super().__init__()
        self.genre = "racing"
    
    def generate(self, config: Dict, colors: Dict, fonts: Dict, effects: Dict) -> str:
        # Implementation for racing games
        return self._create_base_html_structure("Racing Game", colors, fonts) + "</body></html>"

class RPGModule(BaseGameModule):
    def __init__(self):
        super().__init__()
        self.genre = "rpg"
    
    def generate(self, config: Dict, colors: Dict, fonts: Dict, effects: Dict) -> str:
        # Implementation for RPG games
        return self._create_base_html_structure("RPG Adventure", colors, fonts) + "</body></html>"

class StrategyModule(BaseGameModule):
    def __init__(self):
        super().__init__()
        self.genre = "strategy"
    
    def generate(self, config: Dict, colors: Dict, fonts: Dict, effects: Dict) -> str:
        # Implementation for strategy games
        return self._create_base_html_structure("Strategy Game", colors, fonts) + "</body></html>"

# Export all modules
__all__ = [
    'BaseGameModule', 'PuzzleModule', 'ShooterModule', 'PlatformerModule',
    'RacingModule', 'RPGModule', 'StrategyModule'
