"""
Modular Game Generator - Revolutionary AI-Driven Game Creation System
Dynamic assembly system that creates unique HTML5 games from GameConfig specifications

This module provides:
- Genre-specific game engines with unique mechanics
- Dynamic HTML/CSS/JavaScript assembly
- Mobile-first responsive design
- Theme-based visual generation
- Procedural content creation
- Real-time game compilation
"""

import json
import random
import math
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from advanced_prompt_interpreter import GameConfig

@dataclass
class GameAssets:
    """Container for all generated game assets"""
    html_content: str
    css_styles: str
    javascript_code: str
    title: str
    description: str
    instructions: str
    metadata: Dict[str, Any]

class BaseGameEngine:
    """Base class for all genre-specific game engines"""
    
    def __init__(self, config: GameConfig):
        self.config = config
        self.canvas_width = 800
        self.canvas_height = 600
        self.mobile_breakpoint = 768
        
    def generate_game(self) -> GameAssets:
        """Generate complete game assets"""
        html = self._generate_html()
        css = self._generate_css()
        js = self._generate_javascript()
        title = self._generate_title()
        description = self._generate_description()
        instructions = self._generate_instructions()
        metadata = self._generate_metadata()
        
        return GameAssets(
            html_content=html,
            css_styles=css,
            javascript_code=js,
            title=title,
            description=description,
            instructions=instructions,
            metadata=metadata
        )
    
    def _generate_html(self) -> str:
        """Generate HTML structure for the game"""
        return f"""
        <div id="gameContainer" class="game-container">
            <div id="gameHeader" class="game-header">
                <h1 id="gameTitle">{self._generate_title()}</h1>
                <div id="gameStats" class="game-stats">
                    <span id="score">Score: 0</span>
                    <span id="level">Level: 1</span>
                </div>
            </div>
            <div id="gameArea" class="game-area">
                <canvas id="gameCanvas" class="game-canvas"></canvas>
                <div id="gameUI" class="game-ui">
                    {self._generate_ui_elements()}
                </div>
            </div>
            <div id="mobileControls" class="mobile-controls">
                {self._generate_mobile_controls()}
            </div>
            <div id="gameInstructions" class="game-instructions">
                <p>{self._generate_instructions()}</p>
            </div>
        </div>
        """
    
    def _generate_css(self) -> str:
        """Generate CSS styles based on theme and visual style"""
        color_palette = self._get_color_palette()
        
        return f"""
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: {color_palette['background']};
            color: {color_palette['text']};
            overflow: hidden;
            touch-action: none;
        }}
        
        .game-container {{
            width: 100vw;
            height: 100vh;
            display: flex;
            flex-direction: column;
            background: linear-gradient(135deg, {color_palette['primary']}, {color_palette['secondary']});
        }}
        
        .game-header {{
            padding: 10px 20px;
            background: rgba(0, 0, 0, 0.8);
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 1000;
        }}
        
        .game-header h1 {{
            color: {color_palette['accent']};
            font-size: 1.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }}
        
        .game-stats {{
            display: flex;
            gap: 20px;
            color: {color_palette['text']};
            font-weight: bold;
        }}
        
        .game-area {{
            flex: 1;
            position: relative;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        
        .game-canvas {{
            background: {color_palette['canvas_bg']};
            border: 2px solid {color_palette['border']};
            border-radius: 8px;
            max-width: 100%;
            max-height: 100%;
            touch-action: none;
        }}
        
        .game-ui {{
            position: absolute;
            top: 10px;
            left: 10px;
            z-index: 100;
            color: {color_palette['ui_text']};
            font-size: 14px;
        }}
        
        .mobile-controls {{
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            display: none;
            gap: 15px;
            z-index: 1000;
        }}
        
        .control-btn {{
            width: 60px;
            height: 60px;
            background: rgba(255, 255, 255, 0.2);
            border: 2px solid rgba(255, 255, 255, 0.5);
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
            backdrop-filter: blur(10px);
            transition: all 0.2s ease;
        }}
        
        .control-btn:active {{
            background: rgba(255, 255, 255, 0.4);
            transform: scale(0.95);
        }}
        
        .game-instructions {{
            position: absolute;
            bottom: 10px;
            left: 10px;
            color: {color_palette['text']};
            font-size: 12px;
            opacity: 0.8;
            z-index: 100;
        }}
        
        /* Mobile Responsive Design */
        @media (max-width: {self.mobile_breakpoint}px) {{
            .mobile-controls {{
                display: flex;
            }}
            
            .game-instructions {{
                display: none;
            }}
            
            .game-header h1 {{
                font-size: 1.2em;
            }}
            
            .game-stats {{
                gap: 10px;
                font-size: 0.9em;
            }}
            
            .control-btn {{
                width: 50px;
                height: 50px;
                font-size: 18px;
            }}
        }}
        
        /* Theme-specific styles */
        {self._generate_theme_specific_css()}
        
        /* Visual style enhancements */
        {self._generate_visual_style_css()}
        """
    
    def _generate_javascript(self) -> str:
        """Generate JavaScript game logic - to be overridden by specific engines"""
        return """
        // Base game initialization
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        
        // Set canvas size
        function resizeCanvas() {
            const container = document.querySelector('.game-area');
            const maxWidth = Math.min(800, container.clientWidth - 40);
            const maxHeight = Math.min(600, container.clientHeight - 40);
            
            canvas.width = maxWidth;
            canvas.height = maxHeight;
        }
        
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);
        
        // Game state
        let gameState = {
            score: 0,
            level: 1,
            paused: false,
            gameOver: false
        };
        
        // Input handling
        const input = {
            keys: {},
            touch: { up: false, down: false, left: false, right: false }
        };
        
        // Keyboard events
        document.addEventListener('keydown', (e) => {
            input.keys[e.key.toLowerCase()] = true;
            e.preventDefault();
        });
        
        document.addEventListener('keyup', (e) => {
            input.keys[e.key.toLowerCase()] = false;
            e.preventDefault();
        });
        
        // Touch controls setup
        function setupTouchControls() {
            const controls = ['up', 'down', 'left', 'right'];
            
            controls.forEach(direction => {
                const btn = document.getElementById(direction + 'Btn');
                if (btn) {
                    btn.addEventListener('touchstart', (e) => {
                        input.touch[direction] = true;
                        e.preventDefault();
                    });
                    
                    btn.addEventListener('touchend', (e) => {
                        input.touch[direction] = false;
                        e.preventDefault();
                    });
                    
                    // Mouse events for desktop testing
                    btn.addEventListener('mousedown', () => input.touch[direction] = true);
                    btn.addEventListener('mouseup', () => input.touch[direction] = false);
                }
            });
        }
        
        setupTouchControls();
        
        // Prevent scrolling and context menu
        document.addEventListener('touchmove', (e) => e.preventDefault(), { passive: false });
        document.addEventListener('contextmenu', (e) => e.preventDefault());
        
        // Update UI
        function updateUI() {
            document.getElementById('score').textContent = `Score: ${gameState.score}`;
            document.getElementById('level').textContent = `Level: ${gameState.level}`;
        }
        
        // Game loop placeholder - to be overridden
        function gameLoop() {
            if (!gameState.paused && !gameState.gameOver) {
                update();
                render();
            }
            requestAnimationFrame(gameLoop);
        }
        
        function update() {
            // Override in specific game engines
        }
        
        function render() {
            // Override in specific game engines
        }
        
        // Start the game
        gameLoop();
        """
    
    def _generate_ui_elements(self) -> str:
        """Generate UI elements specific to the game type"""
        return """
        <div class="power-ups"></div>
        <div class="mini-map"></div>
        """
    
    def _generate_mobile_controls(self) -> str:
        """Generate mobile touch controls"""
        return """
        <div class="control-btn" id="leftBtn">←</div>
        <div class="control-btn" id="upBtn">↑</div>
        <div class="control-btn" id="downBtn">↓</div>
        <div class="control-btn" id="rightBtn">→</div>
        """
    
    def _generate_title(self) -> str:
        """Generate creative title based on config"""
        theme_adjectives = {
            'fantasy': ['Mystical', 'Enchanted', 'Magical', 'Legendary'],
            'sci-fi': ['Cosmic', 'Stellar', 'Quantum', 'Galactic'],
            'cyberpunk': ['Neon', 'Digital', 'Cyber', 'Neural'],
            'underwater': ['Aquatic', 'Deep', 'Ocean', 'Marine'],
            'forest': ['Woodland', 'Nature\'s', 'Wild', 'Emerald']
        }
        
        genre_nouns = {
            'platformer': ['Adventure', 'Quest', 'Journey', 'Odyssey'],
            'shooter': ['Assault', 'Defense', 'Battle', 'War'],
            'puzzle': ['Challenge', 'Mystery', 'Enigma', 'Riddle'],
            'racing': ['Rush', 'Speed', 'Circuit', 'Grand Prix'],
            'rpg': ['Chronicles', 'Saga', 'Legend', 'Epic']
        }
        
        adjective = random.choice(theme_adjectives.get(self.config.theme, ['Epic']))
        noun = random.choice(genre_nouns.get(self.config.genre, ['Adventure']))
        
        return f"{adjective} {noun}"
    
    def _generate_description(self) -> str:
        """Generate game description"""
        return f"An exciting {self.config.genre} game set in a {self.config.theme} world featuring {self.config.protagonist} characters."
    
    def _generate_instructions(self) -> str:
        """Generate game instructions"""
        return "Use WASD or Arrow Keys to move. Touch the control buttons on mobile devices."
    
    def _generate_metadata(self) -> Dict[str, Any]:
        """Generate game metadata"""
        return {
            'genre': self.config.genre,
            'theme': self.config.theme,
            'difficulty': self.config.difficulty,
            'mobile_compatible': True,
            'created_timestamp': random.randint(1000000000, 9999999999)
        }
    
    def _get_color_palette(self) -> Dict[str, str]:
        """Get color palette based on theme and mood"""
        palettes = {
            'fantasy': {
                'primary': '#4A148C',
                'secondary': '#7B1FA2',
                'accent': '#FFD700',
                'background': '#1A0033',
                'text': '#FFFFFF',
                'canvas_bg': '#2D1B69',
                'border': '#9C27B0',
                'ui_text': '#E1BEE7'
            },
            'sci-fi': {
                'primary': '#0D47A1',
                'secondary': '#1976D2',
                'accent': '#00E5FF',
                'background': '#000051',
                'text': '#FFFFFF',
                'canvas_bg': '#1A237E',
                'border': '#2196F3',
                'ui_text': '#BBDEFB'
            },
            'cyberpunk': {
                'primary': '#000000',
                'secondary': '#1A1A1A',
                'accent': '#00FFFF',
                'background': '#0A0A0A',
                'text': '#00FF00',
                'canvas_bg': '#111111',
                'border': '#FF00FF',
                'ui_text': '#00FFFF'
            },
            'underwater': {
                'primary': '#006064',
                'secondary': '#00838F',
                'accent': '#FFD54F',
                'background': '#001B3D',
                'text': '#FFFFFF',
                'canvas_bg': '#004D5C',
                'border': '#00BCD4',
                'ui_text': '#B2EBF2'
            },
            'forest': {
                'primary': '#1B5E20',
                'secondary': '#388E3C',
                'accent': '#FFEB3B',
                'background': '#0D2818',
                'text': '#FFFFFF',
                'canvas_bg': '#2E7D32',
                'border': '#4CAF50',
                'ui_text': '#C8E6C9'
            }
        }
        
        return palettes.get(self.config.theme, palettes['fantasy'])
    
    def _generate_theme_specific_css(self) -> str:
        """Generate CSS specific to the theme"""
        if self.config.theme == 'cyberpunk':
            return """
            .game-container {
                box-shadow: inset 0 0 100px rgba(0, 255, 255, 0.1);
            }
            
            .control-btn {
                box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
            }
            
            .game-header h1 {
                text-shadow: 0 0 10px #00FFFF;
            }
            """
        elif self.config.theme == 'fantasy':
            return """
            .game-container {
                background-image: radial-gradient(circle at 50% 50%, rgba(255, 215, 0, 0.1) 0%, transparent 50%);
            }
            
            .control-btn {
                background: linear-gradient(45deg, rgba(255, 215, 0, 0.2), rgba(147, 112, 219, 0.2));
            }
            """
        else:
            return ""
    
    def _generate_visual_style_css(self) -> str:
        """Generate CSS based on visual style"""
        if self.config.visual_style == 'pixel':
            return """
            .game-canvas {
                image-rendering: pixelated;
                image-rendering: -moz-crisp-edges;
                image-rendering: crisp-edges;
            }
            
            * {
                font-family: 'Courier New', monospace;
            }
            """
        elif self.config.visual_style == 'neon':
            return """
            .game-header h1 {
                animation: neonGlow 2s ease-in-out infinite alternate;
            }
            
            @keyframes neonGlow {
                from { text-shadow: 0 0 5px currentColor; }
                to { text-shadow: 0 0 20px currentColor, 0 0 30px currentColor; }
            }
            """
        else:
            return ""

class PlatformerEngine(BaseGameEngine):
    """Specialized engine for platformer games"""
    
    def _generate_javascript(self) -> str:
        base_js = super()._generate_javascript()
        
        platformer_js = """
        // Platformer-specific game logic
        const player = {
            x: 100,
            y: 400,
            width: 30,
            height: 30,
            velocityX: 0,
            velocityY: 0,
            speed: 5,
            jumpPower: 15,
            onGround: false,
            color: '#FFD700'
        };
        
        const platforms = [
            { x: 0, y: canvas.height - 40, width: canvas.width, height: 40 },
            { x: 200, y: 400, width: 150, height: 20 },
            { x: 450, y: 300, width: 150, height: 20 },
            { x: 100, y: 200, width: 100, height: 20 }
        ];
        
        const collectibles = [];
        const enemies = [];
        
        // Initialize collectibles
        for (let i = 0; i < 8; i++) {
            collectibles.push({
                x: Math.random() * (canvas.width - 20),
                y: Math.random() * (canvas.height - 100),
                width: 15,
                height: 15,
                collected: false,
                color: '#00FF00'
            });
        }
        
        // Initialize enemies
        for (let i = 0; i < 3; i++) {
            enemies.push({
                x: Math.random() * (canvas.width - 30),
                y: 100,
                width: 25,
                height: 25,
                velocityX: (Math.random() - 0.5) * 4,
                color: '#FF4444'
            });
        }
        
        function update() {
            // Player input
            if (input.keys['a'] || input.keys['arrowleft'] || input.touch.left) {
                player.velocityX = -player.speed;
            } else if (input.keys['d'] || input.keys['arrowright'] || input.touch.right) {
                player.velocityX = player.speed;
            } else {
                player.velocityX *= 0.8; // Friction
            }
            
            if ((input.keys['w'] || input.keys['arrowup'] || input.keys[' '] || input.touch.up) && player.onGround) {
                player.velocityY = -player.jumpPower;
                player.onGround = false;
            }
            
            // Gravity
            player.velocityY += 0.8;
            
            // Update player position
            player.x += player.velocityX;
            player.y += player.velocityY;
            
            // Platform collision
            player.onGround = false;
            platforms.forEach(platform => {
                if (player.x < platform.x + platform.width &&
                    player.x + player.width > platform.x &&
                    player.y < platform.y + platform.height &&
                    player.y + player.height > platform.y) {
                    
                    if (player.velocityY > 0) { // Falling
                        player.y = platform.y - player.height;
                        player.velocityY = 0;
                        player.onGround = true;
                    }
                }
            });
            
            // Boundary collision
            if (player.x < 0) player.x = 0;
            if (player.x + player.width > canvas.width) player.x = canvas.width - player.width;
            if (player.y > canvas.height) {
                // Reset player position
                player.x = 100;
                player.y = 400;
                player.velocityX = 0;
                player.velocityY = 0;
            }
            
            // Collectible collision
            collectibles.forEach(collectible => {
                if (!collectible.collected &&
                    player.x < collectible.x + collectible.width &&
                    player.x + player.width > collectible.x &&
                    player.y < collectible.y + collectible.height &&
                    player.y + player.height > collectible.y) {
                    
                    collectible.collected = true;
                    gameState.score += 10;
                    updateUI();
                }
            });
            
            // Enemy movement
            enemies.forEach(enemy => {
                enemy.x += enemy.velocityX;
                
                // Bounce off walls
                if (enemy.x <= 0 || enemy.x + enemy.width >= canvas.width) {
                    enemy.velocityX *= -1;
                }
                
                // Enemy collision with player
                if (player.x < enemy.x + enemy.width &&
                    player.x + player.width > enemy.x &&
                    player.y < enemy.y + enemy.height &&
                    player.y + player.height > enemy.y) {
                    
                    // Reset player position
                    player.x = 100;
                    player.y = 400;
                    player.velocityX = 0;
                    player.velocityY = 0;
                    gameState.score = Math.max(0, gameState.score - 5);
                    updateUI();
                }
            });
        }
        
        function render() {
            // Clear canvas
            ctx.fillStyle = '#87CEEB';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Draw platforms
            ctx.fillStyle = '#8B4513';
            platforms.forEach(platform => {
                ctx.fillRect(platform.x, platform.y, platform.width, platform.height);
            });
            
            // Draw collectibles
            collectibles.forEach(collectible => {
                if (!collectible.collected) {
                    ctx.fillStyle = collectible.color;
                    ctx.fillRect(collectible.x, collectible.y, collectible.width, collectible.height);
                }
            });
            
            // Draw enemies
            ctx.fillStyle = '#FF4444';
            enemies.forEach(enemy => {
                ctx.fillRect(enemy.x, enemy.y, enemy.width, enemy.height);
            });
            
            // Draw player
            ctx.fillStyle = player.color;
            ctx.fillRect(player.x, player.y, player.width, player.height);
        }
        """
        
        return base_js + platformer_js
    
    def _generate_instructions(self) -> str:
        return "Use A/D or Arrow Keys to move, W/Space to jump. Collect green items and avoid red enemies!"

class ShooterEngine(BaseGameEngine):
    """Specialized engine for shooter games"""
    
    def _generate_javascript(self) -> str:
        base_js = super()._generate_javascript()
        
        shooter_js = """
        // Shooter-specific game logic
        const player = {
            x: canvas.width / 2,
            y: canvas.height - 60,
            width: 40,
            height: 40,
            speed: 7,
            color: '#00FFFF'
        };
        
        const bullets = [];
        const enemies = [];
        const powerUps = [];
        
        let lastShot = 0;
        let shootCooldown = 200;
        
        // Spawn enemies
        function spawnEnemy() {
            enemies.push({
                x: Math.random() * (canvas.width - 30),
                y: -30,
                width: 30,
                height: 30,
                speed: 2 + Math.random() * 3,
                color: '#FF4444',
                health: 1
            });
        }
        
        // Spawn power-ups occasionally
        function spawnPowerUp() {
            if (Math.random() < 0.1) {
                powerUps.push({
                    x: Math.random() * (canvas.width - 20),
                    y: -20,
                    width: 20,
                    height: 20,
                    speed: 2,
                    color: '#FFD700',
                    type: 'rapid_fire'
                });
            }
        }
        
        setInterval(spawnEnemy, 1000);
        setInterval(spawnPowerUp, 5000);
        
        function update() {
            const now = Date.now();
            
            // Player movement
            if (input.keys['a'] || input.keys['arrowleft'] || input.touch.left) {
                player.x -= player.speed;
            }
            if (input.keys['d'] || input.keys['arrowright'] || input.touch.right) {
                player.x += player.speed;
            }
            if (input.keys['w'] || input.keys['arrowup'] || input.touch.up) {
                player.y -= player.speed;
            }
            if (input.keys['s'] || input.keys['arrowdown'] || input.touch.down) {
                player.y += player.speed;
            }
            
            // Keep player in bounds
            player.x = Math.max(0, Math.min(canvas.width - player.width, player.x));
            player.y = Math.max(0, Math.min(canvas.height - player.height, player.y));
            
            // Auto-shoot
            if (now - lastShot > shootCooldown) {
                bullets.push({
                    x: player.x + player.width / 2 - 2,
                    y: player.y,
                    width: 4,
                    height: 10,
                    speed: 10,
                    color: '#FFFF00'
                });
                lastShot = now;
            }
            
            // Update bullets
            for (let i = bullets.length - 1; i >= 0; i--) {
                const bullet = bullets[i];
                bullet.y -= bullet.speed;
                
                if (bullet.y < 0) {
                    bullets.splice(i, 1);
                }
            }
            
            // Update enemies
            for (let i = enemies.length - 1; i >= 0; i--) {
                const enemy = enemies[i];
                enemy.y += enemy.speed;
                
                if (enemy.y > canvas.height) {
                    enemies.splice(i, 1);
                    continue;
                }
                
                // Check collision with player
                if (player.x < enemy.x + enemy.width &&
                    player.x + player.width > enemy.x &&
                    player.y < enemy.y + enemy.height &&
                    player.y + player.height > enemy.y) {
                    
                    gameState.score = Math.max(0, gameState.score - 10);
                    enemies.splice(i, 1);
                    updateUI();
                    continue;
                }
                
                // Check collision with bullets
                for (let j = bullets.length - 1; j >= 0; j--) {
                    const bullet = bullets[j];
                    
                    if (bullet.x < enemy.x + enemy.width &&
                        bullet.x + bullet.width > enemy.x &&
                        bullet.y < enemy.y + enemy.height &&
                        bullet.y + bullet.height > enemy.y) {
                        
                        bullets.splice(j, 1);
                        enemy.health--;
                        
                        if (enemy.health <= 0) {
                            enemies.splice(i, 1);
                            gameState.score += 20;
                            updateUI();
                        }
                        break;
                    }
                }
            }
            
            // Update power-ups
            for (let i = powerUps.length - 1; i >= 0; i--) {
                const powerUp = powerUps[i];
                powerUp.y += powerUp.speed;
                
                if (powerUp.y > canvas.height) {
                    powerUps.splice(i, 1);
                    continue;
                }
                
                // Check collision with player
                if (player.x < powerUp.x + powerUp.width &&
                    player.x + player.width > powerUp.x &&
                    player.y < powerUp.y + powerUp.height &&
                    player.y + player.height > powerUp.y) {
                    
                    if (powerUp.type === 'rapid_fire') {
                        shootCooldown = 100;
                        setTimeout(() => { shootCooldown = 200; }, 5000);
                    }
                    
                    powerUps.splice(i, 1);
                    gameState.score += 5;
                    updateUI();
                }
            }
        }
        
        function render() {
            // Clear canvas with space background
            ctx.fillStyle = '#000011';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Draw stars
            ctx.fillStyle = '#FFFFFF';
            for (let i = 0; i < 50; i++) {
                const x = (i * 37) % canvas.width;
                const y = (i * 73) % canvas.height;
                ctx.fillRect(x, y, 1, 1);
            }
            
            // Draw player
            ctx.fillStyle = player.color;
            ctx.fillRect(player.x, player.y, player.width, player.height);
            
            // Draw bullets
            bullets.forEach(bullet => {
                ctx.fillStyle = bullet.color;
                ctx.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
            });
            
            // Draw enemies
            enemies.forEach(enemy => {
                ctx.fillStyle = enemy.color;
                ctx.fillRect(enemy.x, enemy.y, enemy.width, enemy.height);
            });
            
            // Draw power-ups
            powerUps.forEach(powerUp => {
                ctx.fillStyle = powerUp.color;
                ctx.fillRect(powerUp.x, powerUp.y, powerUp.width, powerUp.height);
            });
        }
        """
        
        return base_js + shooter_js
    
    def _generate_instructions(self) -> str:
        return "Use WASD or Arrow Keys to move. Auto-shooting enabled. Collect gold power-ups!"

class PuzzleEngine(BaseGameEngine):
    """Specialized engine for puzzle games"""
    
    def _generate_javascript(self) -> str:
        base_js = super()._generate_javascript()
        
        puzzle_js = """
        // Puzzle-specific game logic (Sliding Puzzle)
        const gridSize = 4;
        const tileSize = Math.min(canvas.width, canvas.height) / (gridSize + 1);
        const offsetX = (canvas.width - gridSize * tileSize) / 2;
        const offsetY = (canvas.height - gridSize * tileSize) / 2;
        
        let tiles = [];
        let emptyTile = { x: gridSize - 1, y: gridSize - 1 };
        let moves = 0;
        let solved = false;
        
        // Initialize puzzle
        function initPuzzle() {
            tiles = [];
            for (let y = 0; y < gridSize; y++) {
                tiles[y] = [];
                for (let x = 0; x < gridSize; x++) {
                    if (x === gridSize - 1 && y === gridSize - 1) {
                        tiles[y][x] = 0; // Empty tile
                    } else {
                        tiles[y][x] = y * gridSize + x + 1;
                    }
                }
            }
            
            // Shuffle the puzzle
            for (let i = 0; i < 1000; i++) {
                const directions = [];
                if (emptyTile.x > 0) directions.push({ x: -1, y: 0 });
                if (emptyTile.x < gridSize - 1) directions.push({ x: 1, y: 0 });
                if (emptyTile.y > 0) directions.push({ x: 0, y: -1 });
                if (emptyTile.y < gridSize - 1) directions.push({ x: 0, y: 1 });
                
                const dir = directions[Math.floor(Math.random() * directions.length)];
                moveTile(emptyTile.x + dir.x, emptyTile.y + dir.y, false);
            }
            
            moves = 0;
            solved = false;
            updateUI();
        }
        
        function moveTile(x, y, countMove = true) {
            if (x < 0 || x >= gridSize || y < 0 || y >= gridSize) return false;
            
            const dx = Math.abs(x - emptyTile.x);
            const dy = Math.abs(y - emptyTile.y);
            
            if ((dx === 1 && dy === 0) || (dx === 0 && dy === 1)) {
                tiles[emptyTile.y][emptyTile.x] = tiles[y][x];
                tiles[y][x] = 0;
                emptyTile.x = x;
                emptyTile.y = y;
                
                if (countMove) {
                    moves++;
                    checkSolved();
                    updateUI();
                }
                return true;
            }
            return false;
        }
        
        function checkSolved() {
            let correct = 0;
            for (let y = 0; y < gridSize; y++) {
                for (let x = 0; x < gridSize; x++) {
                    const expectedValue = (y * gridSize + x + 1) % (gridSize * gridSize);
                    if (tiles[y][x] === expectedValue) {
                        correct++;
                    }
                }
            }
            
            if (correct === gridSize * gridSize) {
                solved = true;
                gameState.score = Math.max(gameState.score, 1000 - moves * 10);
                updateUI();
            }
        }
        
        // Mouse/touch input for puzzle
        canvas.addEventListener('click', (e) => {
            const rect = canvas.getBoundingClientRect();
            const clickX = e.clientX - rect.left;
            const clickY = e.clientY - rect.top;
            
            const tileX = Math.floor((clickX - offsetX) / tileSize);
            const tileY = Math.floor((clickY - offsetY) / tileSize);
            
            moveTile(tileX, tileY);
        });
        
        canvas.addEventListener('touchstart', (e) => {
            e.preventDefault();
            const rect = canvas.getBoundingClientRect();
            const touch = e.touches[0];
            const clickX = touch.clientX - rect.left;
            const clickY = touch.clientY - rect.top;
            
            const tileX = Math.floor((clickX - offsetX) / tileSize);
            const tileY = Math.floor((clickY - offsetY) / tileSize);
            
            moveTile(tileX, tileY);
        });
        
        function update() {
            // Puzzle doesn't need continuous updates
            document.getElementById('score').textContent = `Moves: ${moves}`;
            if (solved) {
                document.getElementById('level').textContent = 'SOLVED!';
            }
        }
        
        function render() {
            // Clear canvas
            ctx.fillStyle = '#2E7D32';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Draw puzzle grid
            for (let y = 0; y < gridSize; y++) {
                for (let x = 0; x < gridSize; x++) {
                    const tileValue = tiles[y][x];
                    const tileX = offsetX + x * tileSize;
                    const tileY = offsetY + y * tileSize;
                    
                    if (tileValue !== 0) {
                        // Draw tile
                        ctx.fillStyle = solved ? '#4CAF50' : '#81C784';
                        ctx.fillRect(tileX + 2, tileY + 2, tileSize - 4, tileSize - 4);
                        
                        // Draw tile border
                        ctx.strokeStyle = '#2E7D32';
                        ctx.lineWidth = 2;
                        ctx.strokeRect(tileX + 2, tileY + 2, tileSize - 4, tileSize - 4);
                        
                        // Draw tile number
                        ctx.fillStyle = '#FFFFFF';
                        ctx.font = `${tileSize / 3}px Arial`;
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'middle';
                        ctx.fillText(
                            tileValue.toString(),
                            tileX + tileSize / 2,
                            tileY + tileSize / 2
                        );
                    } else {
                        // Draw empty space
                        ctx.fillStyle = '#1B5E20';
                        ctx.fillRect(tileX + 2, tileY + 2, tileSize - 4, tileSize - 4);
                    }
                }
            }
            
            // Draw grid lines
            ctx.strokeStyle = '#1B5E20';
            ctx.lineWidth = 4;
            for (let i = 0; i <= gridSize; i++) {
                // Vertical lines
                ctx.beginPath();
                ctx.moveTo(offsetX + i * tileSize, offsetY);
                ctx.lineTo(offsetX + i * tileSize, offsetY + gridSize * tileSize);
                ctx.stroke();
                
                // Horizontal lines
                ctx.beginPath();
                ctx.moveTo(offsetX, offsetY + i * tileSize);
                ctx.lineTo(offsetX + gridSize * tileSize, offsetY + i * tileSize);
                ctx.stroke();
            }
            
            if (solved) {
                ctx.fillStyle = 'rgba(255, 215, 0, 0.8)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                ctx.fillStyle = '#000000';
                ctx.font = '48px Arial';
                ctx.textAlign = 'center';
                ctx.fillText('PUZZLE SOLVED!', canvas.width / 2, canvas.height / 2);
            }
        }
        
        // Initialize the puzzle
        initPuzzle();
        """
        
        return base_js + puzzle_js
    
    def _generate_instructions(self) -> str:
        return "Click or tap tiles adjacent to the empty space to move them. Arrange numbers in order!"
    
    def _generate_mobile_controls(self) -> str:
        return """
        <div class="control-btn" id="hintBtn">💡</div>
        <div class="control-btn" id="resetBtn">🔄</div>
        """

class RacingEngine(BaseGameEngine):
    """Specialized engine for racing games"""
    
    def _generate_javascript(self) -> str:
        base_js = super()._generate_javascript()
        
        racing_js = """
        // Racing-specific game logic
        const car = {
            x: canvas.width / 2 - 15,
            y: canvas.height - 80,
            width: 30,
            height: 50,
            speed: 0,
            maxSpeed: 8,
            acceleration: 0.3,
            friction: 0.1,
            color: '#FFD700'
        };
        
        const obstacles = [];
        const roadLines = [];
        let roadOffset = 0;
        let distance = 0;
        let lap = 1;
        
        // Initialize road lines
        for (let i = 0; i < 10; i++) {
            roadLines.push({
                y: i * 80 - 400
            });
        }
        
        // Spawn obstacles
        function spawnObstacle() {
            if (Math.random() < 0.02) {
                obstacles.push({
                    x: Math.random() * (canvas.width - 60) + 30,
                    y: -50,
                    width: 30,
                    height: 50,
                    speed: 3,
                    color: '#FF4444'
                });
            }
        }
        
        function update() {
            // Car controls
            if (input.keys['a'] || input.keys['arrowleft'] || input.touch.left) {
                car.x -= 5;
            }
            if (input.keys['d'] || input.keys['arrowright'] || input.touch.right) {
                car.x += 5;
            }
            if (input.keys['w'] || input.keys['arrowup'] || input.touch.up) {
                car.speed = Math.min(car.maxSpeed, car.speed + car.acceleration);
            } else if (input.keys['s'] || input.keys['arrowdown'] || input.touch.down) {
                car.speed = Math.max(-car.maxSpeed / 2, car.speed - car.acceleration);
            } else {
                car.speed *= (1 - car.friction);
            }
            
            // Keep car on road
            car.x = Math.max(50, Math.min(canvas.width - 50 - car.width, car.x));
            
            // Update road animation
            roadOffset += car.speed;
            distance += car.speed;
            
            // Update road lines
            roadLines.forEach(line => {
                line.y += car.speed * 2;
                if (line.y > canvas.height) {
                    line.y = -80;
                }
            });
            
            // Spawn and update obstacles
            spawnObstacle();
            for (let i = obstacles.length - 1; i >= 0; i--) {
                const obstacle = obstacles[i];
                obstacle.y += obstacle.speed + car.speed;
                
                if (obstacle.y > canvas.height) {
                    obstacles.splice(i, 1);
                    gameState.score += 10;
                    continue;
                }
                
                // Check collision
                if (car.x < obstacle.x + obstacle.width &&
                    car.x + car.width > obstacle.x &&
                    car.y < obstacle.y + obstacle.height &&
                    car.y + car.height > obstacle.y) {
                    
                    car.speed *= 0.5; // Slow down on collision
                    obstacles.splice(i, 1);
                    gameState.score = Math.max(0, gameState.score - 20);
                }
            }
            
            // Update lap counter
            if (distance > 2000) {
                distance = 0;
                lap++;
                gameState.level = lap;
            }
            
            updateUI();
        }
        
        function render() {
            // Clear canvas with road background
            ctx.fillStyle = '#333333';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Draw road edges
            ctx.fillStyle = '#228B22';
            ctx.fillRect(0, 0, 50, canvas.height);
            ctx.fillRect(canvas.width - 50, 0, 50, canvas.height);
            
            // Draw road lines
            ctx.fillStyle = '#FFFF00';
            roadLines.forEach(line => {
                ctx.fillRect(canvas.width / 2 - 2, line.y, 4, 40);
            });
            
            // Draw car
            ctx.fillStyle = car.color;
            ctx.fillRect(car.x, car.y, car.width, car.height);
            
            // Draw obstacles
            obstacles.forEach(obstacle => {
                ctx.fillStyle = obstacle.color;
                ctx.fillRect(obstacle.x, obstacle.y, obstacle.width, obstacle.height);
            });
            
            // Draw speedometer
            ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
            ctx.fillRect(canvas.width - 120, 10, 110, 60);
            
            ctx.fillStyle = '#FFFFFF';
            ctx.font = '14px Arial';
            ctx.textAlign = 'left';
            ctx.fillText(`Speed: ${Math.round(car.speed * 10)}`, canvas.width - 115, 30);
            ctx.fillText(`Lap: ${lap}`, canvas.width - 115, 50);
        }
        """
        
        return base_js + racing_js
    
    def _generate_instructions(self) -> str:
        return "Use A/D to steer, W to accelerate, S to brake. Avoid red cars and complete laps!"

class ModularGameGenerator:
    """Main generator that orchestrates game creation based on genre"""
    
    def __init__(self):
        self.engines = {
            'platformer': PlatformerEngine,
            'shooter': ShooterEngine,
            'puzzle': PuzzleEngine,
            'racing': RacingEngine,
            'action': PlatformerEngine,  # Fallback to platformer
            'rpg': PlatformerEngine,     # Fallback to platformer
            'strategy': PuzzleEngine,    # Fallback to puzzle
            'simulation': RacingEngine,  # Fallback to racing
            'survival': ShooterEngine,   # Fallback to shooter
            'horror': ShooterEngine      # Fallback to shooter
        }
    
    def generate_game(self, config: GameConfig) -> GameAssets:
        """Generate a complete game based on the configuration"""
        engine_class = self.engines.get(config.genre, PlatformerEngine)
        engine = engine_class(config)
        
        return engine.generate_game()
    
    def get_supported_genres(self) -> List[str]:
        """Get list of supported game genres"""
        return list(self.engines.keys())
    
    def create_complete_game_html(self, config: GameConfig) -> str:
        """Create a complete, standalone HTML game file"""
        assets = self.generate_game(config)
        
        complete_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>{assets.title}</title>
    <style>
        {assets.css_styles}
    </style>
</head>
<body>
    {assets.html_content}
    <script>
        {assets.javascript_code}
    </script>
</body>
</html>"""
        
        return complete_html

# Example usage and testing
if __name__ == "__main__":
    from advanced_prompt_interpreter import AdvancedPromptInterpreter
    
    interpreter = AdvancedPromptInterpreter()
    generator = ModularGameGenerator()
    
    # Test game generation
    test_prompts = [
        "a platformer where a cat travels through dreams",
        "a space shooter defending Earth from alien invaders",
        "a sliding puzzle with mystical fantasy theme",
        "a cyberpunk racing game with neon lights"
    ]
    
    for prompt in test_prompts:
        print(f"\nGenerating game for: '{prompt}'")
        print("=" * 60)
        
        config = interpreter.interpret_prompt(prompt)
        assets = generator.generate_game(config)
        
        print(f"Title: {assets.title}")
        print(f"Description: {assets.description}")
        print(f"Instructions: {assets.instructions}")
        print(f"Genre: {config.genre}")
        print(f"Theme: {config.theme}")
        print(f"Mobile Compatible: {assets.metadata['mobile_compatible']}")
        print("\n" + "="*80)
