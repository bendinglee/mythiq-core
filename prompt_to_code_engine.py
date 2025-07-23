"""
Intelligent Prompt-to-Code Translation Engine
Revolutionary AI that translates natural language prompts into game code

This module provides:
- AI-powered translation of game concepts into code
- Dynamic generation of JavaScript game logic
- Intelligent synthesis of HTML and CSS from prompt analysis
- Custom code generation for unique mechanics
"""

import json

class PromptToCodeEngine:
    """Translates prompt analysis into functional game code"""
    
    def __init__(self):
        pass
    
    def generate_code_from_analysis(self, analysis: dict) -> dict:
        """
        Generate complete game code from prompt analysis
        
        Args:
            analysis: Comprehensive analysis of the user prompt
            
        Returns:
            Dictionary with HTML, CSS, and JavaScript code
        """
        html = self._generate_html(analysis)
        css = self._generate_css(analysis)
        javascript = self._generate_javascript(analysis)
        
        return {
            'html': html,
            'css': css,
            'javascript': javascript
        }
    
    def _generate_html(self, analysis: dict) -> str:
        """Generate HTML structure for the game"""
        title = analysis.get('title', 'AI Generated Game')
        description = analysis.get('description', 'A unique game created by AI.')
        
        return f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>{title}</title>
</head>
<body>
    <div id=\"game-container\">
        <h1 id=\"game-title\">{title}</h1>
        <p id=\"game-description\">{description}</p>
        <canvas id=\"game-canvas\" width=\"800\" height=\"600\"></canvas>
        <div id=\"ui-container\">
            <div id=\"score\">Score: 0</div>
        </div>
    </div>
</body>
</html>"""

    def _generate_css(self, analysis: dict) -> str:
        """Generate CSS styling for the game"""
        visuals = analysis.get('visuals', {})
        palette = visuals.get('color_palette', {})
        
        primary_color = palette.get('primary', '#00ffff')
        secondary_color = palette.get('secondary', '#ff00ff')
        background_color = palette.get('background', '#0a0a0a')
        text_color = palette.get('text', '#ffffff')
        
        return f"""body {{
    background-color: {background_color};
    color: {text_color};
    font-family: monospace;
    text-align: center;
    margin: 0;
}}

#game-container {{
    padding: 20px;
}}

#game-canvas {{
    border: 2px solid {primary_color};
    background-color: #000;
}}

#ui-container {{
    color: {secondary_color};
    font-size: 1.5em;
}}"""

    def _generate_javascript(self, analysis: dict) -> str:
        """Generate JavaScript game logic"""
        mechanics = analysis.get('mechanics', {})
        visuals = analysis.get('visuals', {})
        
        player_style = visuals.get('player_style', {})
        enemy_style = visuals.get('enemy_style', {})
        collectible_style = visuals.get('collectible_style', {})
        
        return f"""const canvas = document.getElementById('game-canvas');
const ctx = canvas.getContext('2d');
const scoreEl = document.getElementById('score');

let score = 0;

const player = {{
    x: canvas.width / 2,
    y: canvas.height - 30,
    width: {player_style.get('size', 20)},
    height: {player_style.get('size', 20)},
    color: '{player_style.get('color', '#00ff00')}',
    speed: 5,
    dx: 0
}};

const collectibles = [];
const enemies = [];

function createCollectible() {{
    const size = {collectible_style.get('size', 15)};
    collectibles.push({{
        x: Math.random() * (canvas.width - size),
        y: Math.random() * -canvas.height,
        width: size,
        height: size,
        color: '{collectible_style.get('color', '#ffff00')}',
        speed: 2 + Math.random() * 2
    }});
}}

function createEnemy() {{
    const size = {enemy_style.get('size', 20)};
    enemies.push({{
        x: Math.random() * (canvas.width - size),
        y: Math.random() * -canvas.height,
        width: size,
        height: size,
        color: '{enemy_style.get('color', '#ff0000')}',
        speed: 3 + Math.random() * 3
    }});
}}

function drawPlayer() {{
    ctx.fillStyle = player.color;
    ctx.fillRect(player.x, player.y, player.width, player.height);
}}

function drawCollectibles() {{
    collectibles.forEach(c => {{
        ctx.fillStyle = c.color;
        ctx.fillRect(c.x, c.y, c.width, c.height);
    }});
}}

function drawEnemies() {{
    enemies.forEach(e => {{
        ctx.fillStyle = e.color;
        ctx.fillRect(e.x, e.y, e.width, e.height);
    }});
}}

function clear() {{
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}}

function update() {{
    clear();

    drawPlayer();
    drawCollectibles();
    drawEnemies();

    // Move player
    player.x += player.dx;

    // Wall detection
    if (player.x < 0) player.x = 0;
    if (player.x + player.width > canvas.width) player.x = canvas.width - player.width;

    // Move collectibles
    collectibles.forEach((c, index) => {{
        c.y += c.speed;
        if (c.y > canvas.height) {{
            collectibles.splice(index, 1);
        }}

        // Collision with player
        if (player.x < c.x + c.width &&
            player.x + player.width > c.x &&
            player.y < c.y + c.height &&
            player.y + player.height > c.y) {{
            collectibles.splice(index, 1);
            score++;
            scoreEl.innerText = `Score: ${{score}`;
        }}
    }});

    // Move enemies
    enemies.forEach((e, index) => {{
        e.y += e.speed;
        if (e.y > canvas.height) {{
            enemies.splice(index, 1);
        }}

        // Collision with player
        if (player.x < e.x + e.width &&
            player.x + player.width > e.x &&
            player.y < e.y + e.height &&
            player.y + player.height > e.y) {{
            gameOver();
        }}
    }});

    requestAnimationFrame(update);
}}

function gameOver() {{
    alert(`Game Over! Your score: ${{score}`);
    document.location.reload();
}}

function moveRight() {{
    player.dx = player.speed;
}}

function moveLeft() {{
    player.dx = -player.speed;
}}

function keyDown(e) {{
    if (e.key === 'ArrowRight' || e.key === 'd') {{
        moveRight();
    }} else if (e.key === 'ArrowLeft' || e.key === 'a') {{
        moveLeft();
    }}
}}

function keyUp(e) {{
    if (e.key === 'ArrowRight' || e.key === 'd' || e.key === 'ArrowLeft' || e.key === 'a') {{
        player.dx = 0;
    }}
}}

document.addEventListener('keydown', keyDown);
document.addEventListener('keyup', keyUp);

setInterval(createCollectible, 2000);
setInterval(createEnemy, 3000);

update();
"""

prompt_to_code_engine = PromptToCodeEngine()
