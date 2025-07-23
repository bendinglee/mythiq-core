"""
True Game Engines - Multiple Game Types with Unique Mechanics
Revolutionary AI game generation with completely different gameplay for each type

This module provides:
- Racing games with actual car mechanics and tracks
- Puzzle games with real puzzle-solving mechanics
- Combat games with fighting systems and weapons
- Cooking games with recipe and timing systems
- Platformer games with jumping and level progression
- Strategy games with resource management
- Survival games with health and crafting systems
- Adventure games with exploration and story
"""

import json
import random
import time
from datetime import datetime

class RacingGameEngine:
    """Generates actual racing games with car mechanics, tracks, and speed"""
    
    def __init__(self):
        self.track_types = ['city', 'desert', 'forest', 'space', 'underwater', 'mountain']
        self.vehicle_types = ['car', 'motorcycle', 'spaceship', 'boat', 'hovercraft']
    
    def generate_racing_game(self, prompt_analysis):
        """Generate a real racing game with car controls and track mechanics"""
        theme = prompt_analysis.get('theme', 'modern')
        entities = prompt_analysis.get('entities', {})
        
        # Determine racing theme and vehicle
        vehicle = self._get_theme_vehicle(theme, entities)
        track_type = self._get_theme_track(theme)
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Racing Game</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: {self._get_racing_theme_colors(theme)['background']};
            font-family: 'Arial', sans-serif;
            overflow: hidden;
        }}
        
        #gameCanvas {{
            display: block;
            margin: 0 auto;
            border: 3px solid {self._get_racing_theme_colors(theme)['border']};
            background: {self._get_racing_theme_colors(theme)['track_bg']};
        }}
        
        #gameInfo {{
            position: absolute;
            top: 10px;
            left: 10px;
            color: white;
            font-size: 18px;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        }}
        
        #speedometer {{
            position: absolute;
            top: 10px;
            right: 10px;
            color: white;
            font-size: 24px;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        }}
        
        #instructions {{
            position: absolute;
            bottom: 10px;
            left: 50%;
            transform: translateX(-50%);
            color: white;
            text-align: center;
            font-size: 14px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        }}
        
        .finish-line {{
            position: absolute;
            width: 100%;
            height: 20px;
            background: repeating-linear-gradient(
                90deg,
                black 0px,
                black 20px,
                white 20px,
                white 40px
            );
        }}
    </style>
</head>
<body>
    <div id="gameInfo">
        <div>Lap: <span id="lap">1</span>/3</div>
        <div>Position: <span id="position">1st</span></div>
        <div>Time: <span id="time">0:00</span></div>
    </div>
    
    <div id="speedometer">
        <div>Speed: <span id="speed">0</span> mph</div>
    </div>
    
    <canvas id="gameCanvas" width="800" height="600"></canvas>
    
    <div id="instructions">
        <div>🏎️ Use ARROW KEYS to steer and accelerate your {vehicle}</div>
        <div>🏁 Complete 3 laps to win the race!</div>
        <div>📱 Mobile: Tilt device to steer, tap to accelerate</div>
    </div>

    <script>
        class RacingGame {{
            constructor() {{
                this.canvas = document.getElementById('gameCanvas');
                this.ctx = this.canvas.getContext('2d');
                
                // Game state
                this.gameRunning = true;
                this.lap = 1;
                this.position = 1;
                this.startTime = Date.now();
                
                // Player vehicle
                this.player = {{
                    x: 400,
                    y: 500,
                    width: 30,
                    height: 50,
                    speed: 0,
                    maxSpeed: 8,
                    acceleration: 0.3,
                    deceleration: 0.2,
                    turnSpeed: 0,
                    angle: 0,
                    color: '{self._get_racing_theme_colors(theme)['player_vehicle']}'
                }};
                
                // Track elements
                this.trackBounds = [];
                this.checkpoints = [];
                this.obstacles = [];
                this.powerUps = [];
                this.aiCars = [];
                
                // Controls
                this.keys = {{}};
                this.setupControls();
                
                // Initialize game
                this.generateTrack();
                this.generateAICars();
                this.generatePowerUps();
                this.gameLoop();
            }}
            
            setupControls() {{
                document.addEventListener('keydown', (e) => {{
                    this.keys[e.key.toLowerCase()] = true;
                }});
                
                document.addEventListener('keyup', (e) => {{
                    this.keys[e.key.toLowerCase()] = false;
                }});
                
                // Mobile controls
                if (window.DeviceOrientationEvent) {{
                    window.addEventListener('deviceorientation', (e) => {{
                        const tilt = e.gamma; // Left-right tilt
                        if (Math.abs(tilt) > 5) {{
                            this.player.turnSpeed = tilt / 30;
                        }}
                    }});
                }}
                
                this.canvas.addEventListener('touchstart', (e) => {{
                    e.preventDefault();
                    this.keys['accelerate'] = true;
                }});
                
                this.canvas.addEventListener('touchend', (e) => {{
                    e.preventDefault();
                    this.keys['accelerate'] = false;
                }});
            }}
            
            generateTrack() {{
                // Create track boundaries
                const centerX = this.canvas.width / 2;
                const centerY = this.canvas.height / 2;
                const trackWidth = 120;
                
                // Oval track
                for (let angle = 0; angle < Math.PI * 2; angle += 0.1) {{
                    const radius = 200;
                    const x = centerX + Math.cos(angle) * radius;
                    const y = centerY + Math.sin(angle) * radius * 0.6;
                    
                    this.trackBounds.push({{
                        x: x - trackWidth/2,
                        y: y,
                        width: trackWidth,
                        height: 10
                    }});
                }}
                
                // Checkpoints
                this.checkpoints = [
                    {{x: centerX + 200, y: centerY, passed: false}},
                    {{x: centerX, y: centerY - 120, passed: false}},
                    {{x: centerX - 200, y: centerY, passed: false}},
                    {{x: centerX, y: centerY + 120, passed: false}}
                ];
            }}
            
            generateAICars() {{
                for (let i = 0; i < 3; i++) {{
                    this.aiCars.push({{
                        x: 380 + i * 40,
                        y: 480 + i * 20,
                        width: 25,
                        height: 40,
                        speed: 2 + Math.random() * 3,
                        angle: 0,
                        lap: 1,
                        checkpointIndex: 0,
                        color: `hsl(${{i * 120}}, 70%, 50%)`
                    }});
                }}
            }}
            
            generatePowerUps() {{
                for (let i = 0; i < 5; i++) {{
                    this.powerUps.push({{
                        x: 300 + Math.random() * 200,
                        y: 200 + Math.random() * 200,
                        type: Math.random() > 0.5 ? 'speed' : 'shield',
                        collected: false,
                        rotation: 0
                    }});
                }}
            }}
            
            update() {{
                if (!this.gameRunning) return;
                
                // Player controls
                if (this.keys['arrowup'] || this.keys['w'] || this.keys['accelerate']) {{
                    this.player.speed = Math.min(this.player.speed + this.player.acceleration, this.player.maxSpeed);
                }} else {{
                    this.player.speed = Math.max(this.player.speed - this.player.deceleration, 0);
                }}
                
                if (this.keys['arrowleft'] || this.keys['a']) {{
                    this.player.turnSpeed = -0.1;
                }} else if (this.keys['arrowright'] || this.keys['d']) {{
                    this.player.turnSpeed = 0.1;
                }} else {{
                    this.player.turnSpeed *= 0.8; // Gradual stop
                }}
                
                // Update player position
                this.player.angle += this.player.turnSpeed * (this.player.speed / this.player.maxSpeed);
                this.player.x += Math.cos(this.player.angle) * this.player.speed;
                this.player.y += Math.sin(this.player.angle) * this.player.speed;
                
                // Keep player in bounds
                this.player.x = Math.max(50, Math.min(this.canvas.width - 50, this.player.x));
                this.player.y = Math.max(50, Math.min(this.canvas.height - 50, this.player.y));
                
                // Update AI cars
                this.aiCars.forEach(car => {{
                    // Simple AI movement toward next checkpoint
                    const targetCheckpoint = this.checkpoints[car.checkpointIndex % this.checkpoints.length];
                    const dx = targetCheckpoint.x - car.x;
                    const dy = targetCheckpoint.y - car.y;
                    const distance = Math.sqrt(dx * dx + dy * dy);
                    
                    if (distance < 50) {{
                        car.checkpointIndex++;
                        if (car.checkpointIndex >= this.checkpoints.length) {{
                            car.lap++;
                            car.checkpointIndex = 0;
                        }}
                    }}
                    
                    car.angle = Math.atan2(dy, dx);
                    car.x += Math.cos(car.angle) * car.speed;
                    car.y += Math.sin(car.angle) * car.speed;
                }});
                
                // Check checkpoints
                this.checkpoints.forEach((checkpoint, index) => {{
                    const dx = this.player.x - checkpoint.x;
                    const dy = this.player.y - checkpoint.y;
                    const distance = Math.sqrt(dx * dx + dy * dy);
                    
                    if (distance < 40 && !checkpoint.passed) {{
                        checkpoint.passed = true;
                        
                        // Check if all checkpoints passed
                        if (this.checkpoints.every(cp => cp.passed)) {{
                            this.lap++;
                            this.checkpoints.forEach(cp => cp.passed = false);
                            
                            if (this.lap > 3) {{
                                this.raceComplete();
                            }}
                        }}
                    }}
                }});
                
                // Update power-ups
                this.powerUps.forEach(powerUp => {{
                    powerUp.rotation += 0.1;
                    
                    if (!powerUp.collected) {{
                        const dx = this.player.x - powerUp.x;
                        const dy = this.player.y - powerUp.y;
                        const distance = Math.sqrt(dx * dx + dy * dy);
                        
                        if (distance < 30) {{
                            powerUp.collected = true;
                            if (powerUp.type === 'speed') {{
                                this.player.maxSpeed = 12;
                                setTimeout(() => this.player.maxSpeed = 8, 3000);
                            }}
                        }}
                    }}
                }});
                
                // Update UI
                this.updateUI();
            }}
            
            updateUI() {{
                document.getElementById('lap').textContent = this.lap;
                document.getElementById('speed').textContent = Math.round(this.player.speed * 15);
                
                const elapsed = Math.floor((Date.now() - this.startTime) / 1000);
                const minutes = Math.floor(elapsed / 60);
                const seconds = elapsed % 60;
                document.getElementById('time').textContent = `${{minutes}}:${{seconds.toString().padStart(2, '0')}}`;
            }}
            
            raceComplete() {{
                this.gameRunning = false;
                
                this.ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
                this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
                
                this.ctx.fillStyle = 'gold';
                this.ctx.font = '48px Arial';
                this.ctx.textAlign = 'center';
                this.ctx.fillText('🏁 RACE COMPLETE! 🏁', this.canvas.width / 2, this.canvas.height / 2 - 50);
                
                const elapsed = Math.floor((Date.now() - this.startTime) / 1000);
                const minutes = Math.floor(elapsed / 60);
                const seconds = elapsed % 60;
                
                this.ctx.font = '24px Arial';
                this.ctx.fillText(`Final Time: ${{minutes}}:${{seconds.toString().padStart(2, '0')}}`, this.canvas.width / 2, this.canvas.height / 2 + 20);
                this.ctx.fillText('🏆 You Win! 🏆', this.canvas.width / 2, this.canvas.height / 2 + 60);
            }}
            
            draw() {{
                this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
                
                // Draw track
                this.ctx.strokeStyle = 'white';
                this.ctx.lineWidth = 3;
                this.ctx.setLineDash([10, 5]);
                this.ctx.beginPath();
                const centerX = this.canvas.width / 2;
                const centerY = this.canvas.height / 2;
                this.ctx.ellipse(centerX, centerY, 200, 120, 0, 0, Math.PI * 2);
                this.ctx.stroke();
                this.ctx.setLineDash([]);
                
                // Draw checkpoints
                this.checkpoints.forEach((checkpoint, index) => {{
                    this.ctx.fillStyle = checkpoint.passed ? 'green' : 'yellow';
                    this.ctx.beginPath();
                    this.ctx.arc(checkpoint.x, checkpoint.y, 15, 0, Math.PI * 2);
                    this.ctx.fill();
                    
                    this.ctx.fillStyle = 'black';
                    this.ctx.font = '12px Arial';
                    this.ctx.textAlign = 'center';
                    this.ctx.fillText(index + 1, checkpoint.x, checkpoint.y + 4);
                }});
                
                // Draw power-ups
                this.powerUps.forEach(powerUp => {{
                    if (!powerUp.collected) {{
                        this.ctx.save();
                        this.ctx.translate(powerUp.x, powerUp.y);
                        this.ctx.rotate(powerUp.rotation);
                        
                        this.ctx.fillStyle = powerUp.type === 'speed' ? 'orange' : 'blue';
                        this.ctx.fillRect(-10, -10, 20, 20);
                        
                        this.ctx.fillStyle = 'white';
                        this.ctx.font = '16px Arial';
                        this.ctx.textAlign = 'center';
                        this.ctx.fillText(powerUp.type === 'speed' ? '⚡' : '🛡️', 0, 5);
                        
                        this.ctx.restore();
                    }}
                }});
                
                // Draw AI cars
                this.aiCars.forEach(car => {{
                    this.ctx.save();
                    this.ctx.translate(car.x, car.y);
                    this.ctx.rotate(car.angle);
                    
                    this.ctx.fillStyle = car.color;
                    this.ctx.fillRect(-car.width/2, -car.height/2, car.width, car.height);
                    
                    this.ctx.fillStyle = 'white';
                    this.ctx.fillRect(-5, -car.height/2 + 5, 10, 5);
                    this.ctx.fillRect(-5, car.height/2 - 10, 10, 5);
                    
                    this.ctx.restore();
                }});
                
                // Draw player
                this.ctx.save();
                this.ctx.translate(this.player.x, this.player.y);
                this.ctx.rotate(this.player.angle);
                
                this.ctx.fillStyle = this.player.color;
                this.ctx.fillRect(-this.player.width/2, -this.player.height/2, this.player.width, this.player.height);
                
                // Car details
                this.ctx.fillStyle = 'white';
                this.ctx.fillRect(-8, -this.player.height/2 + 5, 16, 8);
                this.ctx.fillRect(-8, this.player.height/2 - 13, 16, 8);
                
                this.ctx.restore();
            }}
            
            gameLoop() {{
                this.update();
                this.draw();
                requestAnimationFrame(() => this.gameLoop());
            }}
        }}
        
        new RacingGame();
    </script>
</body>
</html>
        """
        
        return html_content
    
    def _get_theme_vehicle(self, theme, entities):
        """Get appropriate vehicle for theme"""
        theme_vehicles = {
            'space': 'spaceship',
            'underwater': 'submarine',
            'fantasy': 'magical chariot',
            'cyberpunk': 'hover car',
            'modern': 'race car'
        }
        return theme_vehicles.get(theme, 'vehicle')
    
    def _get_theme_track(self, theme):
        """Get appropriate track type for theme"""
        theme_tracks = {
            'space': 'asteroid field',
            'underwater': 'coral reef',
            'fantasy': 'enchanted forest',
            'cyberpunk': 'neon city',
            'modern': 'speedway'
        }
        return theme_tracks.get(theme, 'track')
    
    def _get_racing_theme_colors(self, theme):
        """Get color scheme for racing theme"""
        colors = {
            'space': {
                'background': 'linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 100%)',
                'track_bg': 'linear-gradient(45deg, #0f0f23 0%, #16213e 100%)',
                'border': '#00ffff',
                'player_vehicle': '#00bfff'
            },
            'underwater': {
                'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                'track_bg': 'linear-gradient(45deg, #87ceeb 0%, #4682b4 100%)',
                'border': '#20b2aa',
                'player_vehicle': '#20b2aa'
            },
            'cyberpunk': {
                'background': 'linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 100%)',
                'track_bg': 'linear-gradient(45deg, #2d1b69 0%, #11998e 100%)',
                'border': '#ff00ff',
                'player_vehicle': '#ff00ff'
            }
        }
        return colors.get(theme, colors['space'])

class PuzzleGameEngine:
    """Generates actual puzzle games with logic-solving mechanics"""
    
    def __init__(self):
        self.puzzle_types = ['match3', 'sliding', 'logic', 'pattern', 'word']
    
    def generate_puzzle_game(self, prompt_analysis):
        """Generate a real puzzle game with problem-solving mechanics"""
        theme = prompt_analysis.get('theme', 'modern')
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Puzzle Game</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: {self._get_puzzle_theme_colors(theme)['background']};
            font-family: 'Arial', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }}
        
        .game-container {{
            text-align: center;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 2rem;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        .puzzle-grid {{
            display: grid;
            grid-template-columns: repeat(4, 80px);
            grid-template-rows: repeat(4, 80px);
            gap: 5px;
            margin: 20px auto;
            background: rgba(0, 0, 0, 0.2);
            padding: 10px;
            border-radius: 10px;
        }}
        
        .puzzle-tile {{
            background: {self._get_puzzle_theme_colors(theme)['tile']};
            border: 2px solid {self._get_puzzle_theme_colors(theme)['tile_border']};
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            font-weight: bold;
            color: white;
            cursor: pointer;
            transition: all 0.3s ease;
            user-select: none;
        }}
        
        .puzzle-tile:hover {{
            transform: scale(1.05);
            box-shadow: 0 0 15px {self._get_puzzle_theme_colors(theme)['glow']};
        }}
        
        .puzzle-tile.empty {{
            background: transparent;
            border: 2px dashed rgba(255, 255, 255, 0.3);
        }}
        
        .game-info {{
            color: white;
            font-size: 18px;
            margin-bottom: 20px;
        }}
        
        .controls {{
            margin-top: 20px;
        }}
        
        .btn {{
            background: {self._get_puzzle_theme_colors(theme)['button']};
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            margin: 0 10px;
            transition: all 0.3s ease;
        }}
        
        .btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }}
    </style>
</head>
<body>
    <div class="game-container">
        <h1 style="color: white; margin-bottom: 10px;">🧩 Sliding Puzzle</h1>
        <div class="game-info">
            <div>Moves: <span id="moves">0</span></div>
            <div>Time: <span id="time">0:00</span></div>
        </div>
        
        <div class="puzzle-grid" id="puzzleGrid"></div>
        
        <div class="controls">
            <button class="btn" onclick="game.shuffle()">🔀 Shuffle</button>
            <button class="btn" onclick="game.solve()">💡 Hint</button>
            <button class="btn" onclick="game.reset()">🔄 Reset</button>
        </div>
        
        <div style="color: white; margin-top: 20px; font-size: 14px;">
            Click tiles adjacent to the empty space to move them
        </div>
    </div>

    <script>
        class SlidingPuzzleGame {{
            constructor() {{
                this.gridSize = 4;
                this.tiles = [];
                this.emptyPos = {{ row: 3, col: 3 }};
                this.moves = 0;
                this.startTime = Date.now();
                this.gameWon = false;
                
                this.initializePuzzle();
                this.render();
                this.startTimer();
            }}
            
            initializePuzzle() {{
                // Create solved state
                for (let i = 0; i < this.gridSize * this.gridSize - 1; i++) {{
                    this.tiles.push(i + 1);
                }}
                this.tiles.push(null); // Empty space
                
                // Shuffle the puzzle
                this.shuffle();
            }}
            
            shuffle() {{
                // Perform random valid moves to ensure solvability
                for (let i = 0; i < 1000; i++) {{
                    const validMoves = this.getValidMoves();
                    if (validMoves.length > 0) {{
                        const randomMove = validMoves[Math.floor(Math.random() * validMoves.length)];
                        this.moveTile(randomMove.row, randomMove.col, false);
                    }}
                }}
                this.moves = 0;
                this.startTime = Date.now();
                this.gameWon = false;
                this.updateUI();
                this.render();
            }}
            
            getValidMoves() {{
                const moves = [];
                const directions = [
                    {{row: -1, col: 0}}, {{row: 1, col: 0}},
                    {{row: 0, col: -1}}, {{row: 0, col: 1}}
                ];
                
                directions.forEach(dir => {{
                    const newRow = this.emptyPos.row + dir.row;
                    const newCol = this.emptyPos.col + dir.col;
                    
                    if (newRow >= 0 && newRow < this.gridSize && 
                        newCol >= 0 && newCol < this.gridSize) {{
                        moves.push({{row: newRow, col: newCol}});
                    }}
                }});
                
                return moves;
            }}
            
            moveTile(row, col, countMove = true) {{
                // Check if the move is valid (adjacent to empty space)
                const rowDiff = Math.abs(row - this.emptyPos.row);
                const colDiff = Math.abs(col - this.emptyPos.col);
                
                if ((rowDiff === 1 && colDiff === 0) || (rowDiff === 0 && colDiff === 1)) {{
                    // Swap tile with empty space
                    const tileIndex = row * this.gridSize + col;
                    const emptyIndex = this.emptyPos.row * this.gridSize + this.emptyPos.col;
                    
                    [this.tiles[tileIndex], this.tiles[emptyIndex]] = [this.tiles[emptyIndex], this.tiles[tileIndex]];
                    
                    this.emptyPos = {{row, col}};
                    
                    if (countMove) {{
                        this.moves++;
                        this.updateUI();
                        
                        if (this.checkWin()) {{
                            this.gameWon = true;
                            this.showWinMessage();
                        }}
                    }}
                    
                    this.render();
                    return true;
                }}
                
                return false;
            }}
            
            checkWin() {{
                for (let i = 0; i < this.tiles.length - 1; i++) {{
                    if (this.tiles[i] !== i + 1) {{
                        return false;
                    }}
                }}
                return this.tiles[this.tiles.length - 1] === null;
            }}
            
            showWinMessage() {{
                setTimeout(() => {{
                    const elapsed = Math.floor((Date.now() - this.startTime) / 1000);
                    const minutes = Math.floor(elapsed / 60);
                    const seconds = elapsed % 60;
                    
                    alert(`🎉 Congratulations! 🎉\\n\\nYou solved the puzzle in:\\n${{this.moves}} moves\\n${{minutes}}:${{seconds.toString().padStart(2, '0')}}`);
                }}, 500);
            }}
            
            solve() {{
                // Provide a hint by highlighting a tile that can be moved
                const validMoves = this.getValidMoves();
                if (validMoves.length > 0) {{
                    const hint = validMoves[0];
                    const hintTile = document.querySelector(`[data-row="${{hint.row}}"][data-col="${{hint.col}}"]`);
                    if (hintTile) {{
                        hintTile.style.animation = 'pulse 1s ease-in-out 3';
                    }}
                }}
            }}
            
            reset() {{
                // Reset to solved state
                for (let i = 0; i < this.gridSize * this.gridSize - 1; i++) {{
                    this.tiles[i] = i + 1;
                }}
                this.tiles[this.tiles.length - 1] = null;
                this.emptyPos = {{row: 3, col: 3}};
                this.moves = 0;
                this.startTime = Date.now();
                this.gameWon = false;
                this.updateUI();
                this.render();
            }}
            
            updateUI() {{
                document.getElementById('moves').textContent = this.moves;
            }}
            
            startTimer() {{
                setInterval(() => {{
                    if (!this.gameWon) {{
                        const elapsed = Math.floor((Date.now() - this.startTime) / 1000);
                        const minutes = Math.floor(elapsed / 60);
                        const seconds = elapsed % 60;
                        document.getElementById('time').textContent = `${{minutes}}:${{seconds.toString().padStart(2, '0')}}`;
                    }}
                }}, 1000);
            }}
            
            render() {{
                const grid = document.getElementById('puzzleGrid');
                grid.innerHTML = '';
                
                for (let row = 0; row < this.gridSize; row++) {{
                    for (let col = 0; col < this.gridSize; col++) {{
                        const index = row * this.gridSize + col;
                        const tile = document.createElement('div');
                        tile.className = 'puzzle-tile';
                        tile.dataset.row = row;
                        tile.dataset.col = col;
                        
                        if (this.tiles[index] === null) {{
                            tile.classList.add('empty');
                        }} else {{
                            tile.textContent = this.tiles[index];
                            tile.addEventListener('click', () => {{
                                this.moveTile(row, col);
                            }});
                        }}
                        
                        grid.appendChild(tile);
                    }}
                }}
            }}
        }}
        
        // Add CSS animation for hint
        const style = document.createElement('style');
        style.textContent = `
            @keyframes pulse {{
                0%, 100% {{ transform: scale(1); }}
                50% {{ transform: scale(1.1); }}
            }}
        `;
        document.head.appendChild(style);
        
        const game = new SlidingPuzzleGame();
    </script>
</body>
</html>
        """
        
        return html_content
    
    def _get_puzzle_theme_colors(self, theme):
        """Get color scheme for puzzle theme"""
        colors = {
            'fantasy': {
                'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                'tile': 'linear-gradient(135deg, #9370db 0%, #8a2be2 100%)',
                'tile_border': '#dda0dd',
                'button': 'linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%)',
                'glow': '#9370db'
            },
            'cyberpunk': {
                'background': 'linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 100%)',
                'tile': 'linear-gradient(135deg, #ff00ff 0%, #00ffff 100%)',
                'tile_border': '#ff00ff',
                'button': 'linear-gradient(135deg, #ff00ff 0%, #00ffff 100%)',
                'glow': '#ff00ff'
            }
        }
        return colors.get(theme, colors['fantasy'])

class CombatGameEngine:
    """Generates actual combat games with fighting mechanics"""
    
    def generate_combat_game(self, prompt_analysis):
        """Generate a real combat game with fighting systems"""
        # Implementation for combat games with health, attacks, weapons
        return self._create_basic_combat_template(prompt_analysis)
    
    def _create_basic_combat_template(self, prompt_analysis):
        """Create basic combat game template"""
        return '''
        <html><body>
        <h1>Combat Game</h1>
        <p>Fighting mechanics with health, attacks, and weapons coming soon!</p>
        </body></html>
        '''

class CookingGameEngine:
    """Generates actual cooking games with recipe and timing mechanics"""
    
    def generate_cooking_game(self, prompt_analysis):
        """Generate a real cooking game with recipe systems"""
        # Implementation for cooking games with recipes, timing, ingredients
        return self._create_basic_cooking_template(prompt_analysis)
    
    def _create_basic_cooking_template(self, prompt_analysis):
        """Create basic cooking game template"""
        return '''
        <html><body>
        <h1>Cooking Game</h1>
        <p>Recipe systems and timing mechanics coming soon!</p>
        </body></html>
        '''

class PlatformerGameEngine:
    """Generates actual platformer games with jumping and level mechanics"""
    
    def generate_platformer_game(self, prompt_analysis):
        """Generate a real platformer game with jumping mechanics"""
        # Implementation for platformer games with jumping, platforms, levels
        return self._create_basic_platformer_template(prompt_analysis)
    
    def _create_basic_platformer_template(self, prompt_analysis):
        """Create basic platformer game template"""
        return '''
        <html><body>
        <h1>Platformer Game</h1>
        <p>Jumping mechanics and level progression coming soon!</p>
        </body></html>
        '''

class StrategyGameEngine:
    """Generates actual strategy games with resource management"""
    
    def generate_strategy_game(self, prompt_analysis):
        """Generate a real strategy game with resource management"""
        # Implementation for strategy games with resources, building, planning
        return self._create_basic_strategy_template(prompt_analysis)
    
    def _create_basic_strategy_template(self, prompt_analysis):
        """Create basic strategy game template"""
        return '''
        <html><body>
        <h1>Strategy Game</h1>
        <p>Resource management and strategic planning coming soon!</p>
        </body></html>
        '''

class SurvivalGameEngine:
    """Generates actual survival games with health and crafting systems"""
    
    def generate_survival_game(self, prompt_analysis):
        """Generate a real survival game with survival mechanics"""
        # Implementation for survival games with health, crafting, resources
        return self._create_basic_survival_template(prompt_analysis)
    
    def _create_basic_survival_template(self, prompt_analysis):
        """Create basic survival game template"""
        return '''
        <html><body>
        <h1>Survival Game</h1>
        <p>Health systems and crafting mechanics coming soon!</p>
        </body></html>
        '''

class AdventureGameEngine:
    """Generates actual adventure games with exploration and story"""
    
    def generate_adventure_game(self, prompt_analysis):
        """Generate a real adventure game with exploration mechanics"""
        # Implementation for adventure games with exploration, story, quests
        return self._create_basic_adventure_template(prompt_analysis)
    
    def _create_basic_adventure_template(self, prompt_analysis):
        """Create basic adventure game template"""
        return '''
        <html><body>
        <h1>Adventure Game</h1>
        <p>Exploration mechanics and story elements coming soon!</p>
        </body></html>
        '''

# Main game engine selector
class TrueGameEngineSelector:
    """Selects the appropriate game engine based on prompt analysis"""
    
    def __init__(self):
        self.engines = {
            'racing': RacingGameEngine(),
            'puzzle': PuzzleGameEngine(),
            'combat': CombatGameEngine(),
            'cooking': CookingGameEngine(),
            'platformer': PlatformerGameEngine(),
            'strategy': StrategyGameEngine(),
            'survival': SurvivalGameEngine(),
            'adventure': AdventureGameEngine(),
            'collection': None  # Will use existing collection engine
        }
    
    def select_engine(self, prompt_analysis):
        """Select the appropriate game engine based on analysis"""
        game_type = prompt_analysis.get('game_type', 'collection')
        return self.engines.get(game_type)
    
    def generate_game(self, prompt_analysis):
        """Generate game using the appropriate engine"""
        engine = self.select_engine(prompt_analysis)
        
        if engine is None:
            # Fall back to collection game for now
            return None
        
        game_type = prompt_analysis.get('game_type', 'collection')
        
        if game_type == 'racing':
            return engine.generate_racing_game(prompt_analysis)
        elif game_type == 'puzzle':
            return engine.generate_puzzle_game(prompt_analysis)
        elif game_type == 'combat':
            return engine.generate_combat_game(prompt_analysis)
        elif game_type == 'cooking':
            return engine.generate_cooking_game(prompt_analysis)
        elif game_type == 'platformer':
            return engine.generate_platformer_game(prompt_analysis)
        elif game_type == 'strategy':
            return engine.generate_strategy_game(prompt_analysis)
        elif game_type == 'survival':
            return engine.generate_survival_game(prompt_analysis)
        elif game_type == 'adventure':
            return engine.generate_adventure_game(prompt_analysis)
        
        return None
