#!/usr/bin/env python3
"""
🤖 Ultimate AI Game Engine - Final Version
Creates completely unique games from user descriptions using GROQ AI
Contains the exact functions that main.py expects
"""

import os
import json
import re
import random
import requests
from datetime import datetime

class TrueAIGameGenerator:
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.groq_api_url = "https://api.groq.com/openai/v1/chat/completions"

    def generate_game(self, description):
        """Generate a completely unique game from user description"""
        try:
            print(f"🎮 Generating unique game from: {description[:100]}...")
            if self.groq_api_key:
                return self._generate_with_ai(description)
            else:
                return self._generate_fallback(description)
        except Exception as e:
            print(f"❌ Game generation error: {e}")
            return self._generate_fallback(description)

    def _generate_with_ai(self, description):
        """Generate game using GROQ AI"""
        try:
            prompt = self._create_game_prompt(description)
            headers = {
                "Authorization": f"Bearer {self.groq_api_key}",
                "Content-Type": "application/json",
            }
            data = {
                "model": "llama3-8b-8192",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert game developer who creates complete HTML5 games from descriptions. You generate fully functional games with unique mechanics, visuals, and gameplay that exactly match the user's request.",
                    },
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.8,
                "max_tokens": 4000,
            }
            response = requests.post(
                self.groq_api_url, headers=headers, json=data, timeout=30
            )
            if response.status_code == 200:
                result = response.json()
                ai_response = result["choices"][0]["message"]["content"]
                return self._parse_ai_response(ai_response, description)
            else:
                print(f"❌ GROQ API error: {response.status_code}")
                return self._generate_fallback(description)
        except Exception as e:
            print(f"❌ AI generation error: {e}")
            return self._generate_fallback(description)

    def _create_game_prompt(self, description):
        """Create detailed prompt for AI game generation"""
        return f"""
Create a complete HTML5 game based on this description: "{description}"

Requirements:
1. Generate a unique game title that matches the description
2. Create custom game mechanics that fit the theme
3. Include appropriate visuals, colors, and styling
4. Make it fully playable with clear objectives
5. Add mobile touch controls AND keyboard controls
6. Include scoring, win conditions, and game feedback

The game should be a complete HTML file with embedded CSS and JavaScript.
Make the game mechanics unique to the description - don't use generic templates.

For example:
- If it's about "fairy collecting mushrooms", create a character that moves around collecting items
- If it's about "space adventure", create spaceship movement and obstacles
- If it's about "cooking", create ingredient selection and cooking mechanics
- If it's about "puzzle", create unique puzzle mechanics that fit the theme

Return ONLY the complete HTML code for the game, starting with <!DOCTYPE html> and ending with </html>.
Make sure the game is fully functional and matches the user's description exactly.
"""

    def _parse_ai_response(self, ai_response, description):
        """Parse AI response and extract game data"""
        try:
            html_match = re.search(
                r"<!DOCTYPE html>.*?</html>", ai_response, re.DOTALL | re.IGNORECASE
            )
            if html_match:
                html_content = html_match.group(0)
                title_match = re.search(
                    r"<title>(.*?)</title>", html_content, re.IGNORECASE
                )
                title = (
                    title_match.group(1)
                    if title_match
                    else self._generate_title_from_description(description)
                )
                genre = self._determine_genre(description)
                return {
                    "title": title,
                    "description": f"A unique {genre} game: {description}",
                    "genre": genre,
                    "html_content": html_content,
                }
            else:
                print("❌ No valid HTML found in AI response")
                return self._generate_fallback(description)
        except Exception as e:
            print(f"❌ Error parsing AI response: {e}")
            return self._generate_fallback(description)

    def _generate_title_from_description(self, description):
        """Generate a creative title from the description"""
        words = description.lower().split()
        if any(word in words for word in ["fairy", "magic", "forest", "enchanted"]):
            return "Enchanted Forest Quest"
        elif any(word in words for word in ["space", "alien", "ship", "galaxy"]):
            return "Galactic Adventure"
        elif any(word in words for word in ["cook", "recipe", "kitchen", "food"]):
            return "Master Chef Challenge"
        elif any(word in words for word in ["race", "car", "speed", "track"]):
            return "Speed Racer Pro"
        elif any(word in words for word in ["puzzle", "brain", "solve", "logic"]):
            return "Mind Bender"
        else:
            return "Custom Adventure Game"

    def _determine_genre(self, description):
        """Determine game genre from description"""
        description_lower = description.lower()
        if any(
            word in description_lower
            for word in ["shoot", "battle", "fight", "combat", "alien", "enemy"]
        ):
            return "action"
        elif any(
            word in description_lower
            for word in ["puzzle", "solve", "brain", "logic", "match"]
        ):
            return "puzzle"
        elif any(
            word in description_lower
            for word in ["race", "car", "speed", "drive", "track"]
        ):
            return "racing"
        elif any(
            word in description_lower
            for word in ["cook", "recipe", "kitchen", "food", "chef"]
        ):
            return "simulation"
        elif any(
            word in description_lower
            for word in ["adventure", "quest", "explore", "journey"]
        ):
            return "adventure"
        elif any(
            word in description_lower for word in ["jump", "platform", "run", "climb"]
        ):
            return "platformer"
        else:
            return "casual"

    def _generate_fallback(self, description):
        """Generate themed game when AI is unavailable"""
        print("🔄 Using fallback game generation...")
        description_lower = description.lower()
        title = self._generate_title_from_description(description)
        genre = self._determine_genre(description)
        if any(
            word in description_lower
            for word in ["fairy", "magic", "forest", "mushroom", "enchanted"]
        ):
            html_content = self._create_fairy_collection_game(description)
        elif any(
            word in description_lower for word in ["space", "alien", "ship", "galaxy", "star"]
        ):
            html_content = self._create_space_adventure_game(description)
        elif any(
            word in description_lower for word in ["cook", "recipe", "kitchen", "food", "chef"]
        ):
            html_content = self._create_cooking_game(description)
        elif any(word in description_lower for word in ["race", "car", "speed", "drive"]):
            html_content = self._create_racing_game(description)
        else:
            html_content = self._create_adventure_game(description)
        return {
            "title": title,
            "description": f"A custom {genre} game based on your description: {description}",
            "genre": genre,
            "html_content": html_content,
        }

    def _create_fairy_collection_game(self, description):
        """Create a fairy mushroom collection game"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Enchanted Forest Quest</title>
    <style>
        body {{ margin: 0; padding: 20px; background: linear-gradient(135deg, #2d5016, #3e7b27, #4a9c2a); font-family: 'Arial', sans-serif; color: white; overflow: hidden; }}
        .game-container {{ text-align: center; position: relative; }}
        .game-title {{ font-size: 2.5em; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); color: #ffeb3b; }}
        canvas {{ border: 3px solid #4a9c2a; border-radius: 15px; background: linear-gradient(45deg, #1a4c0a, #2d5016); box-shadow: 0 10px 30px rgba(0,0,0,0.3); }}
        .stats {{ display: flex; justify-content: space-around; margin: 20px 0; font-size: 1.3em; }}
        .stat {{ background: rgba(255,255,255,0.2); padding: 10px 20px; border-radius: 20px; backdrop-filter: blur(10px); }}
    </style>
</head>
<body>
    <div class="game-container">
        <h1 class="game-title">🧚‍♀️ Enchanted Forest Quest</h1>
        <p>Help the fairy collect glowing mushrooms while avoiding dark spirits!</p>
        <div class="stats">
            <div class="stat">🍄 Mushrooms: <span id="mushrooms">0</span></div>
            <div class="stat">💖 Lives: <span id="lives">3</span></div>
            <div class="stat">⭐ Score: <span id="score">0</span></div>
        </div>
        <canvas id="gameCanvas" width="800" height="600"></canvas>
        <div class="instructions">
            <p>🎮 Use arrow keys or touch to move the fairy</p>
            <p>🍄 Collect glowing mushrooms for points</p>
            <p>👻 Avoid the dark spirits that chase you!</p>
        </div>
    </div>
    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        let gameRunning = true, score = 0, lives = 3, mushroomsCollected = 0;
        const fairy = {{ x: 400, y: 300, size: 25, speed: 4, color: '#ff69b4' }};
        let mushrooms = [], spirits = [], particles = [];
        const keys = {{}};
        let touchStartX = 0, touchStartY = 0;
        document.addEventListener('keydown', (e) => keys[e.code] = true);
        document.addEventListener('keyup', (e) => keys[e.code] = false);
        canvas.addEventListener('touchstart', (e) => {{ e.preventDefault(); const touch = e.touches[0]; const rect = canvas.getBoundingClientRect(); touchStartX = touch.clientX - rect.left; touchStartY = touch.clientY - rect.top; }});
        canvas.addEventListener('touchmove', (e) => {{ e.preventDefault(); const touch = e.touches[0]; const rect = canvas.getBoundingClientRect(); const touchX = touch.clientX - rect.left; const touchY = touch.clientY - rect.top; const dx = touchX - fairy.x; const dy = touchY - fairy.y; const distance = Math.sqrt(dx * dx + dy * dy); if (distance > 10) {{ fairy.x += (dx / distance) * fairy.speed; fairy.y += (dy / distance) * fairy.speed; }} }});
        function createMushroom() {{ mushrooms.push({{ x: Math.random() * (canvas.width - 40) + 20, y: Math.random() * (canvas.height - 40) + 20, size: 15, glow: 0, collected: false }}); }}
        function createSpirit() {{ spirits.push({{ x: Math.random() * canvas.width, y: Math.random() * canvas.height, size: 20, speed: 1.5 + Math.random(), angle: Math.random() * Math.PI * 2 }}); }}
        function createParticle(x, y, color) {{ for (let i = 0; i < 5; i++) {{ particles.push({{ x: x, y: y, vx: (Math.random() - 0.5) * 4, vy: (Math.random() - 0.5) * 4, life: 30, color: color }}); }} }}
        function update() {{
            if (!gameRunning) return;
            if (keys['ArrowLeft'] && fairy.x > fairy.size) fairy.x -= fairy.speed;
            if (keys['ArrowRight'] && fairy.x < canvas.width - fairy.size) fairy.x += fairy.speed;
            if (keys['ArrowUp'] && fairy.y > fairy.size) fairy.y -= fairy.speed;
            if (keys['ArrowDown'] && fairy.y < canvas.height - fairy.size) fairy.y += fairy.speed;
            spirits.forEach(spirit => {{ const dx = fairy.x - spirit.x; const dy = fairy.y - spirit.y; const distance = Math.sqrt(dx * dx + dy * dy); if (distance > 0) {{ spirit.x += (dx / distance) * spirit.speed; spirit.y += (dy / distance) * spirit.speed; }} if (distance < fairy.size + spirit.size) {{ lives--; createParticle(fairy.x, fairy.y, '#ff0000'); if (lives <= 0) {{ gameRunning = false; alert(`Game Over! Final Score: ${{score}}`); }} else {{ fairy.x = 400; fairy.y = 300; }} }} }});
            mushrooms.forEach((mushroom, index) => {{ if (!mushroom.collected) {{ const dx = fairy.x - mushroom.x; const dy = fairy.y - mushroom.y; const distance = Math.sqrt(dx * dx + dy * dy); if (distance < fairy.size + mushroom.size) {{ mushroom.collected = true; mushroomsCollected++; score += 10; createParticle(mushroom.x, mushroom.y, '#ffeb3b'); mushrooms.splice(index, 1); }} }} mushroom.glow += 0.1; }});
            particles = particles.filter(particle => {{ particle.x += particle.vx; particle.y += particle.vy; particle.life--; return particle.life > 0; }});
            if (mushrooms.length < 5 && Math.random() < 0.02) createMushroom();
            if (spirits.length < 3 && Math.random() < 0.01) createSpirit();
            document.getElementById('mushrooms').textContent = mushroomsCollected;
            document.getElementById('lives').textContent = lives;
            document.getElementById('score').textContent = score;
        }}
        function draw() {{
            ctx.fillStyle = '#1a4c0a'; ctx.fillRect(0, 0, canvas.width, canvas.height);
            for (let i = 0; i < 20; i++) {{ const x = (i * 50) % canvas.width; const y = Math.sin(i) * 50 + canvas.height - 100; ctx.fillStyle = '#0d2818'; ctx.fillRect(x, y, 30, 80); ctx.fillStyle = '#2d5016'; ctx.beginPath(); ctx.arc(x + 15, y, 25, 0, Math.PI * 2); ctx.fill(); }}
            mushrooms.forEach(mushroom => {{ const glowSize = 5 + Math.sin(mushroom.glow) * 3; ctx.shadowColor = '#ffeb3b'; ctx.shadowBlur = glowSize; ctx.fillStyle = '#f5f5dc'; ctx.fillRect(mushroom.x - 3, mushroom.y, 6, 15); ctx.fillStyle = '#ff4444'; ctx.beginPath(); ctx.arc(mushroom.x, mushroom.y - 5, mushroom.size, 0, Math.PI * 2); ctx.fill(); ctx.fillStyle = 'white'; ctx.beginPath(); ctx.arc(mushroom.x - 5, mushroom.y - 8, 2, 0, Math.PI * 2); ctx.arc(mushroom.x + 3, mushroom.y - 3, 1.5, 0, Math.PI * 2); ctx.fill(); ctx.shadowBlur = 0; }});
            spirits.forEach(spirit => {{ ctx.fillStyle = 'rgba(50, 0, 50, 0.8)'; ctx.shadowColor = '#800080'; ctx.shadowBlur = 10; ctx.beginPath(); ctx.arc(spirit.x, spirit.y, spirit.size, 0, Math.PI * 2); ctx.fill(); ctx.fillStyle = '#ff0000'; ctx.beginPath(); ctx.arc(spirit.x - 5, spirit.y - 5, 2, 0, Math.PI * 2); ctx.arc(spirit.x + 5, spirit.y - 5, 2, 0, Math.PI * 2); ctx.fill(); ctx.shadowBlur = 0; }});
            ctx.fillStyle = fairy.color; ctx.shadowColor = fairy.color; ctx.shadowBlur = 15; ctx.beginPath(); ctx.arc(fairy.x, fairy.y, fairy.size, 0, Math.PI * 2); ctx.fill(); ctx.fillStyle = 'rgba(255, 255, 255, 0.6)'; ctx.beginPath(); ctx.ellipse(fairy.x - 15, fairy.y - 10, 8, 15, -0.3, 0, Math.PI * 2); ctx.ellipse(fairy.x + 15, fairy.y - 10, 8, 15, 0.3, 0, Math.PI * 2); ctx.fill(); ctx.shadowBlur = 0;
            particles.forEach(particle => {{ ctx.fillStyle = particle.color; ctx.globalAlpha = particle.life / 30; ctx.beginPath(); ctx.arc(particle.x, particle.y, 2, 0, Math.PI * 2); ctx.fill(); ctx.globalAlpha = 1; }});
        }}
        function gameLoop() {{ update(); draw(); requestAnimationFrame(gameLoop); }}
        createMushroom(); createMushroom(); createSpirit();
        gameLoop();
    </script>
</body>
</html>
"""

    def _create_space_adventure_game(self, description):
        """Create a space adventure game"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Galactic Adventure</title>
    <style>
        body {{ margin: 0; padding: 20px; background: linear-gradient(135deg, #000428, #004e92); font-family: 'Arial', sans-serif; color: white; overflow: hidden; }}
        .game-container {{ text-align: center; position: relative; }}
        canvas {{ border: 3px solid #00ffff; border-radius: 15px; background: linear-gradient(45deg, #000428, #004e92); box-shadow: 0 10px 30px rgba(0,255,255,0.3); }}
        .stats {{ display: flex; justify-content: space-around; margin: 20px 0; font-size: 1.3em; }}
        .stat {{ background: rgba(0,255,255,0.2); padding: 10px 20px; border-radius: 20px; backdrop-filter: blur(10px); }}
    </style>
</head>
<body>
    <div class="game-container">
        <h1 style="color: #00ffff;">🚀 Galactic Adventure</h1>
        <p>Navigate through space, collect energy crystals, and avoid asteroids!</p>
        <div class="stats">
            <div class="stat">⚡ Energy: <span id="energy">0</span></div>
            <div class="stat">🛡️ Shield: <span id="shield">100</span></div>
            <div class="stat">⭐ Score: <span id="score">0</span></div>
        </div>
        <canvas id="gameCanvas" width="800" height="600"></canvas>
        <p>🎮 Arrow keys to move, Spacebar to boost</p>
    </div>
    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        let score = 0, energy = 0, shield = 100;
        const ship = {{ x: 400, y: 500, size: 20, speed: 5 }};
        let crystals = [], asteroids = [], stars = [];
        const keys = {{}};
        document.addEventListener('keydown', (e) => keys[e.code] = true);
        document.addEventListener('keyup', (e) => keys[e.code] = false);
        for (let i = 0; i < 100; i++) {{ stars.push({{ x: Math.random() * canvas.width, y: Math.random() * canvas.height, speed: Math.random() * 2 + 1 }}); }}
        function createCrystal() {{ crystals.push({{ x: Math.random() * (canvas.width - 40) + 20, y: -20, size: 15, speed: 2, glow: 0 }}); }}
        function createAsteroid() {{ asteroids.push({{ x: Math.random() * (canvas.width - 60) + 30, y: -30, size: 25 + Math.random() * 20, speed: 1.5 + Math.random() * 2, rotation: 0 }}); }}
        function update() {{
            if (keys['ArrowLeft'] && ship.x > ship.size) ship.x -= ship.speed;
            if (keys['ArrowRight'] && ship.x < canvas.width - ship.size) ship.x += ship.speed;
            if (keys['ArrowUp'] && ship.y > ship.size) ship.y -= ship.speed;
            if (keys['ArrowDown'] && ship.y < canvas.height - ship.size) ship.y += ship.speed;
            if (keys['Space'] && energy > 0) {{ ship.speed = 8; energy--; }} else {{ ship.speed = 5; }}
            stars.forEach(star => {{ star.y += star.speed; if (star.y > canvas.height) {{ star.y = 0; star.x = Math.random() * canvas.width; }} }});
            crystals = crystals.filter(crystal => {{ crystal.y += crystal.speed; crystal.glow += 0.1; const dx = ship.x - crystal.x; const dy = ship.y - crystal.y; const distance = Math.sqrt(dx * dx + dy * dy); if (distance < ship.size + crystal.size) {{ energy += 10; score += 50; return false; }} return crystal.y < canvas.height; }});
            asteroids = asteroids.filter(asteroid => {{ asteroid.y += asteroid.speed; asteroid.rotation += 0.05; const dx = ship.x - asteroid.x; const dy = ship.y - asteroid.y; const distance = Math.sqrt(dx * dx + dy * dy); if (distance < ship.size + asteroid.size) {{ shield -= 20; if (shield <= 0) {{ alert(`Game Over! Final Score: ${{score}}`); location.reload(); }} return false; }} return asteroid.y < canvas.height; }});
            if (Math.random() < 0.02) createCrystal();
            if (Math.random() < 0.015) createAsteroid();
            document.getElementById('energy').textContent = energy;
            document.getElementById('shield').textContent = shield;
            document.getElementById('score').textContent = score;
        }}
        function draw() {{
            ctx.fillStyle = '#000428'; ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = 'white'; stars.forEach(star => {{ ctx.beginPath(); ctx.arc(star.x, star.y, 1, 0, Math.PI * 2); ctx.fill(); }});
            crystals.forEach(crystal => {{ ctx.shadowColor = '#00ffff'; ctx.shadowBlur = 10 + Math.sin(crystal.glow) * 5; ctx.fillStyle = '#00ffff'; ctx.save(); ctx.translate(crystal.x, crystal.y); ctx.rotate(crystal.glow); ctx.fillRect(-crystal.size/2, -crystal.size/2, crystal.size, crystal.size); ctx.restore(); ctx.shadowBlur = 0; }});
            asteroids.forEach(asteroid => {{ ctx.fillStyle = '#8B4513'; ctx.save(); ctx.translate(asteroid.x, asteroid.y); ctx.rotate(asteroid.rotation); ctx.beginPath(); ctx.arc(0, 0, asteroid.size, 0, Math.PI * 2); ctx.fill(); ctx.restore(); }});
            ctx.fillStyle = '#00ff00'; ctx.shadowColor = '#00ff00'; ctx.shadowBlur = 15; ctx.save(); ctx.translate(ship.x, ship.y); ctx.beginPath(); ctx.moveTo(0, -ship.size); ctx.lineTo(-ship.size/2, ship.size); ctx.lineTo(ship.size/2, ship.size); ctx.closePath(); ctx.fill(); ctx.restore(); ctx.shadowBlur = 0;
        }}
        function gameLoop() {{ update(); draw(); requestAnimationFrame(gameLoop); }}
        gameLoop();
    </script>
</body>
</html>
"""

    def _create_cooking_game(self, description):
        """Create a cooking game"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Master Chef Challenge</title>
    <style>
        body {{ margin: 0; padding: 20px; background: linear-gradient(135deg, #ff6b35, #f7931e); font-family: 'Arial', sans-serif; color: white; }}
        .game-container {{ text-align: center; max-width: 800px; margin: 0 auto; }}
        .kitchen {{ background: rgba(255,255,255,0.1); border-radius: 20px; padding: 30px; margin: 20px 0; }}
        .ingredients {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); gap: 15px; margin: 20px 0; }}
        .ingredient {{ background: rgba(255,255,255,0.2); border: none; border-radius: 15px; padding: 15px; font-size: 2em; cursor: pointer; transition: all 0.2s; }}
        .ingredient:hover {{ transform: scale(1.1); background: rgba(255,255,255,0.3); }}
        .recipe {{ background: rgba(255,255,255,0.2); border-radius: 15px; padding: 20px; margin: 20px 0; }}
        .cooking-area {{ background: rgba(0,0,0,0.2); border-radius: 15px; padding: 20px; margin: 20px 0; min-height: 100px; }}
        .stats {{ display: flex; justify-content: space-around; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="game-container">
        <h1>👨‍🍳 Master Chef Challenge</h1>
        <p>Create delicious recipes by combining ingredients!</p>
        <div class="stats">
            <div>🍽️ Dishes: <span id="dishes">0</span></div>
            <div>⭐ Score: <span id="score">0</span></div>
            <div>⏰ Time: <span id="time">60</span>s</div>
        </div>
        <div class="kitchen">
            <h3>🥘 Current Recipe: <span id="currentRecipe">Pizza</span></h3>
            <div class="recipe"><p>Required: <span id="requiredIngredients">🍅 🧀 🍞</span></p></div>
            <div class="cooking-area">
                <h4>Your Dish:</h4>
                <div id="selectedIngredients"></div>
                <button onclick="cookDish()" style="margin-top: 10px; padding: 10px 20px; border: none; border-radius: 10px; background: #4CAF50; color: white; cursor: pointer;">🔥 Cook!</button>
            </div>
            <div class="ingredients">
                <button class="ingredient" onclick="addIngredient('🍅')">🍅</button>
                <button class="ingredient" onclick="addIngredient('🧀')">🧀</button>
                <button class="ingredient" onclick="addIngredient('🍞')">🍞</button>
                <button class="ingredient" onclick="addIngredient('🥩')">🥩</button>
                <button class="ingredient" onclick="addIngredient('🥬')">🥬</button>
                <button class="ingredient" onclick="addIngredient('🥕')">🥕</button>
                <button class="ingredient" onclick="addIngredient('🧅')">🧅</button>
                <button class="ingredient" onclick="addIngredient('🌶️')">🌶️</button>
            </div>
        </div>
    </div>
    <script>
        let score = 0, dishes = 0, timeLeft = 60, selectedIngredients = [];
        const recipes = [
            {{ name: "Pizza", ingredients: ["🍅", "🧀", "🍞"] }},
            {{ name: "Burger", ingredients: ["🥩", "🍞", "🥬"] }},
            {{ name: "Salad", ingredients: ["🥬", "🥕", "🍅"] }},
            {{ name: "Soup", ingredients: ["🥕", "🧅", "🥩"] }},
            {{ name: "Sandwich", ingredients: ["🍞", "🥩", "🧀"] }}
        ];
        let currentRecipe = recipes[0];
        function addIngredient(ingredient) {{ selectedIngredients.push(ingredient); updateDisplay(); }}
        function updateDisplay() {{ document.getElementById('selectedIngredients').innerHTML = selectedIngredients.join(' '); document.getElementById('currentRecipe').textContent = currentRecipe.name; document.getElementById('requiredIngredients').textContent = currentRecipe.ingredients.join(' '); document.getElementById('score').textContent = score; document.getElementById('dishes').textContent = dishes; document.getElementById('time').textContent = timeLeft; }}
        function cookDish() {{ const required = [...currentRecipe.ingredients].sort(); const selected = [...selectedIngredients].sort(); if (JSON.stringify(required) === JSON.stringify(selected)) {{ score += 100; dishes++; alert(`🎉 Perfect! You made a delicious ${{currentRecipe.name}}!`); currentRecipe = recipes[Math.floor(Math.random() * recipes.length)]; }} else {{ score -= 20; alert(`❌ That's not quite right. Try again!`); }} selectedIngredients = []; updateDisplay(); }}
        setInterval(() => {{ timeLeft--; if (timeLeft <= 0) {{ alert(`⏰ Time's up! You made ${{dishes}} dishes with a score of ${{score}}!`); location.reload(); }} updateDisplay(); }}, 1000);
        updateDisplay();
    </script>
</body>
</html>
"""

    def _create_racing_game(self, description):
        """Create a racing game"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Speed Racer Pro</title>
    <style>
        body {{ margin: 0; padding: 20px; background: linear-gradient(135deg, #1e3c72, #2a5298); font-family: 'Arial', sans-serif; color: white; }}
        .game-container {{ text-align: center; }}
        canvas {{ border: 3px solid #fff; border-radius: 15px; background: #333; }}
        .stats {{ display: flex; justify-content: space-around; margin: 20px 0; font-size: 1.2em; }}
    </style>
</head>
<body>
    <div class="game-container">
        <h1>🏎️ Speed Racer Pro</h1>
        <p>Race through traffic and collect speed boosts!</p>
        <div class="stats">
            <div>🏁 Distance: <span id="distance">0</span>m</div>
            <div>⚡ Speed: <span id="speed">0</span> mph</div>
            <div>⭐ Score: <span id="score">0</span></div>
        </div>
        <canvas id="gameCanvas" width="400" height="600"></canvas>
        <p>🎮 Arrow keys to steer and accelerate!</p>
    </div>
    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        let speed = 0, distance = 0, score = 0, roadOffset = 0;
        const player = {{ x: 175, y: 500, width: 50, height: 80 }};
        let obstacles = [], powerups = [];
        const keys = {{}};
        document.addEventListener('keydown', (e) => keys[e.code] = true);
        document.addEventListener('keyup', (e) => keys[e.code] = false);
        function createObstacle() {{ obstacles.push({{ x: Math.random() * (canvas.width - 60), y: -100, width: 60, height: 100, speed: 3 + speed / 20 }}); }}
        function createPowerup() {{ powerups.push({{ x: Math.random() * (canvas.width - 30), y: -50, size: 20, speed: 2 + speed / 30 }}); }}
        function update() {{
            if (keys['ArrowLeft'] && player.x > 0) player.x -= 5;
            if (keys['ArrowRight'] && player.x < canvas.width - player.width) player.x += 5;
            if (keys['ArrowUp']) speed = Math.min(speed + 0.5, 100);
            if (keys['ArrowDown']) speed = Math.max(speed - 1, 0);
            roadOffset += speed / 10; distance += speed / 10; score += Math.floor(speed / 10);
            obstacles = obstacles.filter(obstacle => {{ obstacle.y += obstacle.speed + speed / 10; if (player.x < obstacle.x + obstacle.width && player.x + player.width > obstacle.x && player.y < obstacle.y + obstacle.height && player.y + player.height > obstacle.y) {{ speed = Math.max(speed - 30, 0); alert('Crash! Speed reduced!'); }} return obstacle.y < canvas.height; }});
            powerups = powerups.filter(powerup => {{ powerup.y += powerup.speed + speed / 10; const dx = player.x + player.width/2 - powerup.x; const dy = player.y + player.height/2 - powerup.y; const distance = Math.sqrt(dx * dx + dy * dy); if (distance < 30) {{ speed = Math.min(speed + 20, 120); score += 50; return false; }} return powerup.y < canvas.height; }});
            if (Math.random() < 0.02) createObstacle();
            if (Math.random() < 0.01) createPowerup();
            document.getElementById('distance').textContent = Math.floor(distance);
            document.getElementById('speed').textContent = Math.floor(speed);
            document.getElementById('score').textContent = score;
        }}
        function draw() {{
            ctx.fillStyle = '#333'; ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#666'; ctx.fillRect(50, 0, canvas.width - 100, canvas.height);
            ctx.fillStyle = '#fff'; for (let i = -1; i < 20; i++) {{ const y = (i * 60 + roadOffset % 60); ctx.fillRect(canvas.width / 2 - 2, y, 4, 30); }}
            ctx.fillStyle = '#00ff00'; ctx.fillRect(player.x, player.y, player.width, player.height);
            ctx.fillStyle = '#ff0000'; obstacles.forEach(obstacle => {{ ctx.fillRect(obstacle.x, obstacle.y, obstacle.width, obstacle.height); }});
            ctx.fillStyle = '#ffff00'; powerups.forEach(powerup => {{ ctx.beginPath(); ctx.arc(powerup.x, powerup.y, powerup.size, 0, Math.PI * 2); ctx.fill(); }});
        }}
        function gameLoop() {{ update(); draw(); requestAnimationFrame(gameLoop); }}
        gameLoop();
    </script>
</body>
</html>
"""

    def _create_adventure_game(self, description):
        """Create a generic adventure game"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Custom Adventure</title>
    <style>
        body {{ margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea, #764ba2); font-family: 'Arial', sans-serif; color: white; }}
        .game-container {{ text-align: center; max-width: 800px; margin: 0 auto; }}
        canvas {{ border: 3px solid #fff; border-radius: 15px; background: linear-gradient(45deg, #1a1a2e, #16213e); }}
        .stats {{ display: flex; justify-content: space-around; margin: 20px 0; font-size: 1.2em; }}
    </style>
</head>
<body>
    <div class="game-container">
        <h1>🎮 Custom Adventure</h1>
        <p>Based on: {description}</p>
        <div class="stats">
            <div>⭐ Score: <span id="score">0</span></div>
            <div>🎯 Items: <span id="items">0</span></div>
            <div>💖 Health: <span id="health">100</span></div>
        </div>
        <canvas id="gameCanvas" width="800" height="600"></canvas>
        <p>🎮 Arrow keys to move, Spacebar to interact</p>
    </div>
    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        let score = 0, items = 0, health = 100;
        const player = {{ x: 400, y: 300, size: 20, speed: 4 }};
        let collectibles = [], obstacles = [];
        const keys = {{}};
        document.addEventListener('keydown', (e) => keys[e.code] = true);
        document.addEventListener('keyup', (e) => keys[e.code] = false);
        function createCollectible() {{ collectibles.push({{ x: Math.random() * (canvas.width - 40) + 20, y: Math.random() * (canvas.height - 40) + 20, size: 15, collected: false }}); }}
        function createObstacle() {{ obstacles.push({{ x: Math.random() * (canvas.width - 60) + 30, y: Math.random() * (canvas.height - 60) + 30, size: 25 }}); }}
        function update() {{
            if (keys['ArrowLeft'] && player.x > player.size) player.x -= player.speed;
            if (keys['ArrowRight'] && player.x < canvas.width - player.size) player.x += player.speed;
            if (keys['ArrowUp'] && player.y > player.size) player.y -= player.speed;
            if (keys['ArrowDown'] && player.y < canvas.height - player.size) player.y += player.speed;
            collectibles.forEach((collectible, index) => {{ if (!collectible.collected) {{ const dx = player.x - collectible.x; const dy = player.y - collectible.y; const distance = Math.sqrt(dx * dx + dy * dy); if (distance < player.size + collectible.size) {{ collectible.collected = true; items++; score += 10; collectibles.splice(index, 1); }} }} }});
            obstacles.forEach(obstacle => {{ const dx = player.x - obstacle.x; const dy = player.y - obstacle.y; const distance = Math.sqrt(dx * dx + dy * dy); if (distance < player.size + obstacle.size) {{ health -= 1; if (health <= 0) {{ alert(`Game Over! Final Score: ${{score}}`); location.reload(); }} }} }});
            if (collectibles.length < 5 && Math.random() < 0.02) createCollectible();
            if (obstacles.length < 3 && Math.random() < 0.01) createObstacle();
            document.getElementById('score').textContent = score;
            document.getElementById('items').textContent = items;
            document.getElementById('health').textContent = health;
        }}
        function draw() {{
            ctx.fillStyle = '#1a1a2e'; ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#ffeb3b'; collectibles.forEach(collectible => {{ ctx.beginPath(); ctx.arc(collectible.x, collectible.y, collectible.size, 0, Math.PI * 2); ctx.fill(); }});
            ctx.fillStyle = '#f44336'; obstacles.forEach(obstacle => {{ ctx.beginPath(); ctx.arc(obstacle.x, obstacle.y, obstacle.size, 0, Math.PI * 2); ctx.fill(); }});
            ctx.fillStyle = '#4caf50'; ctx.beginPath(); ctx.arc(player.x, player.y, player.size, 0, Math.PI * 2); ctx.fill();
        }}
        function gameLoop() {{ update(); draw(); requestAnimationFrame(gameLoop); }}
        createCollectible(); createCollectible(); createObstacle();
        gameLoop();
    </script>
</body>
</html>
"""


# ===== REQUIRED FUNCTIONS FOR MAIN.PY =====

def get_game_suggestions(prompt):
    """Function that main.py expects - provides game suggestions"""
    try:
        generator = TrueAIGameGenerator()
        suggestions = []
        prompt_lower = prompt.lower()
        if any(word in prompt_lower for word in ["fairy", "magic", "forest", "enchanted"]):
            suggestions.append(
                "🧚‍♀️ Enchanted Forest Adventure - Collect magical items while avoiding dark spirits"
            )
            suggestions.append(
                "🍄 Mushroom Quest - Gather glowing mushrooms in a mystical woodland"
            )
            suggestions.append(
                "✨ Fairy Tale Puzzle - Solve magical riddles to save the kingdom"
            )
        elif any(word in prompt_lower for word in ["space", "alien", "galaxy", "star"]):
            suggestions.append(
                "🚀 Galactic Explorer - Navigate through asteroid fields and collect crystals"
            )
            suggestions.append("👽 Alien Defense - Protect Earth from invading spacecraft")
            suggestions.append(
                "🌟 Star Collector - Gather cosmic energy while avoiding black holes"
            )
        elif any(word in prompt_lower for word in ["cook", "recipe", "kitchen", "food"]):
            suggestions.append(
                "👨‍🍳 Master Chef Challenge - Create recipes under time pressure"
            )
            suggestions.append("🍕 Pizza Maker - Build custom pizzas for demanding customers")
            suggestions.append(
                "🥘 Restaurant Rush - Manage a busy kitchen and serve customers"
            )
        elif any(word in prompt_lower for word in ["race", "car", "speed", "drive"]):
            suggestions.append(
                "🏎️ Speed Racer - Race through traffic and collect power-ups"
            )
            suggestions.append("🏁 Circuit Champion - Complete laps while avoiding obstacles")
            suggestions.append("🚗 Highway Rush - Drive at high speeds through busy roads")
        else:
            suggestions.append("🎮 Custom Adventure - A unique game based on your description")
            suggestions.append("🎯 Challenge Mode - Test your skills in a personalized game")
            suggestions.append("🌟 Creative Quest - An original game matching your vision")
        return {
            "suggestions": suggestions,
            "can_create": True,
            "message": f"Based on '{prompt}', here are some game ideas I can create for you!",
        }
    except Exception as e:
        print(f"❌ Error getting suggestions: {e}")
        return {
            "suggestions": [
                "🎮 Adventure Game - A classic adventure experience",
                "🧩 Puzzle Challenge - Test your problem-solving skills",
                "🏃 Action Game - Fast-paced excitement and challenges",
            ],
            "can_create": True,
            "message": "I can create a custom game based on your description!",
        }


def generate_game(description):
    """Main function to generate games - used by main.py"""
    generator = TrueAIGameGenerator()
    return generator.generate_game(description)


# Export both functions for main.py
__all__ = ["get_game_suggestions", "generate_game", "TrueAIGameGenerator"]
