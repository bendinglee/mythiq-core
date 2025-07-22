#!/usr/bin/env python3
"""
🚀 ULTIMATE AI GAME ENGINE
Creates truly unique games from any prompt using advanced AI
Supports game improvement and real-time modifications
"""

import json
import random
import hashlib
import time
from datetime import datetime
import os
import requests
import re
import uuid

class UltimateGameEngine:
    def __init__(self):
        self.api_key = os.getenv('GROQ_API_KEY')
        self.games_db = {}  # In-memory storage for games
        
    def generate_game(self, description, improvement_request=None, existing_game_id=None):
        """
        Generate a completely unique game or improve an existing one
        """
        try:
            # Clean description
            description = description.strip()
            if not description:
                description = "a fun interactive game"
            
            # Generate unique game ID
            if existing_game_id:
                game_id = existing_game_id
            else:
                timestamp = str(int(time.time()))
                unique_id = str(uuid.uuid4())[:8]
                game_id = f"game_{timestamp}_{unique_id}"
            
            print(f"🎮 Generating game: {description}")
            
            # Try AI generation first
            if self.api_key:
                ai_result = self._generate_ai_game(description, game_id, improvement_request, existing_game_id)
                if ai_result and ai_result.get('success'):
                    print("✅ AI generation successful")
                    self.games_db[game_id] = ai_result
                    return ai_result
            
            # Fallback to advanced template system
            print("🔄 Using advanced template system")
            fallback_result = self._generate_advanced_game(description, game_id)
            self.games_db[game_id] = fallback_result
            return fallback_result
            
        except Exception as e:
            print(f"❌ Game generation error: {e}")
            return self._generate_simple_fallback(description, game_id)
    
    def improve_game(self, game_id, improvement_request):
        """
        Improve an existing game based on user feedback
        """
        if game_id not in self.games_db:
            return {"success": False, "error": "Game not found"}
        
        existing_game = self.games_db[game_id]
        original_description = existing_game.get('description', '')
        
        # Create improvement prompt
        improvement_description = f"{original_description} - IMPROVE: {improvement_request}"
        
        return self.generate_game(improvement_description, improvement_request, game_id)
    
    def _generate_ai_game(self, description, game_id, improvement_request=None, existing_game_id=None):
        """
        Use GROQ AI to generate completely custom games
        """
        try:
            print("🤖 Calling GROQ AI for game generation...")
            
            # Create comprehensive AI prompt
            if improvement_request and existing_game_id:
                prompt = self._create_improvement_prompt(description, improvement_request, existing_game_id)
            else:
                prompt = self._create_generation_prompt(description)
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                "messages": [{"role": "user", "content": prompt}],
                "model": "llama3-8b-8192",
                "temperature": 0.9,  # Higher creativity
                "max_tokens": 4000
            }
            
            response = requests.post(
                'https://api.groq.com/openai/v1/chat/completions',
                headers=headers,
                json=data,
                timeout=45
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content'].strip()
                
                print(f"🤖 AI Response: {len(content)} characters")
                
                # Parse AI response
                game_data = self._parse_ai_response(content, game_id)
                if game_data:
                    print("✅ AI response parsed successfully")
                    return {
                        "success": True,
                        "game_id": game_id,
                        "title": game_data["title"],
                        "description": game_data["description"],
                        "genre": game_data.get("genre", "custom"),
                        "html": game_data["html"],
                        "ai_generated": True,
                        "created_at": datetime.now().isoformat(),
                        "improved": bool(improvement_request)
                    }
                else:
                    print("❌ Failed to parse AI response")
            else:
                print(f"❌ GROQ API error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ AI generation error: {e}")
        
        return None
    
    def _create_generation_prompt(self, description):
        """Create comprehensive prompt for AI game generation"""
        return f"""You are an expert game developer. Create a complete, unique, playable HTML5 game based on this description: "{description}"

CRITICAL: Respond with ONLY a JSON object in this EXACT format:
{{
    "title": "Creative Game Title (2-4 words)",
    "description": "Engaging description (1-2 sentences)",
    "genre": "detected genre",
    "html": "complete HTML game code"
}}

GAME REQUIREMENTS:
1. Create a COMPLETELY UNIQUE game that matches the description exactly
2. Include full HTML document with embedded CSS and JavaScript
3. Make it fully playable with proper game mechanics and objectives
4. Add both mobile touch controls AND keyboard controls
5. Include scoring system, win/lose conditions, and game loop
6. Use modern CSS with gradients, animations, and effects
7. Make it responsive for all screen sizes
8. Add sound effects using Web Audio API when possible

CREATIVITY GUIDELINES:
- If description mentions specific mechanics, implement them exactly
- If description is vague, create innovative mechanics that fit the theme
- Always include player interaction, clear objectives, and feedback
- Add particle effects, animations, or visual polish
- Make the game engaging and fun to play

TECHNICAL REQUIREMENTS:
- Complete HTML document starting with <!DOCTYPE html>
- Embedded CSS in <style> tags with modern styling
- Embedded JavaScript in <script> tags with full game logic
- Canvas-based for complex graphics OR DOM-based for simpler games
- Mobile-first responsive design with touch event handling
- Keyboard event handling for desktop users
- Proper game state management and error handling

EXAMPLES OF UNIQUE GAMES TO CREATE:
- "A cooking game with pizza" → Interactive pizza maker with drag-and-drop ingredients, oven timer, customer orders
- "A typing game with falling words" → Words fall from sky, player types to destroy them, increasing speed and difficulty
- "A memory game with colors and sounds" → Simon-says style with audio feedback and visual patterns
- "A tower defense with magical creatures" → Place towers, upgrade them, waves of fantasy enemies with special abilities
- "A fishing game in space" → Cast line into space, catch alien fish, upgrade equipment, manage oxygen
- "A puzzle game with physics" → Objects fall and interact realistically, player manipulates gravity or obstacles

IMPORTANT: Create a game that is:
- Completely different from any template
- Specifically matches the user's description
- Has unique mechanics and gameplay
- Is immediately playable and engaging
- Looks professional and polished

Respond with ONLY the JSON object, no other text or explanation."""

    def _create_improvement_prompt(self, description, improvement_request, existing_game_id):
        """Create prompt for improving existing games"""
        existing_game = self.games_db.get(existing_game_id, {})
        existing_html = existing_game.get('html', '')
        
        return f"""You are an expert game developer. Improve an existing game based on user feedback.

ORIGINAL GAME DESCRIPTION: "{description}"
IMPROVEMENT REQUEST: "{improvement_request}"

EXISTING GAME CODE:
{existing_html[:2000]}...

TASK: Create an improved version that addresses the user's feedback while maintaining the core game concept.

Respond with ONLY a JSON object in this EXACT format:
{{
    "title": "Improved Game Title",
    "description": "Updated description reflecting improvements",
    "genre": "game genre",
    "html": "complete improved HTML game code"
}}

IMPROVEMENT GUIDELINES:
1. Keep the core game concept but enhance based on feedback
2. If user wants "more difficulty" → add levels, faster speed, more obstacles
3. If user wants "better graphics" → improve CSS, add animations, better colors
4. If user wants "new features" → add power-ups, special abilities, bonus rounds
5. If user wants "different mechanics" → modify gameplay while keeping theme
6. Always maintain mobile and desktop compatibility
7. Ensure the improved game is more engaging than the original

Make meaningful improvements that directly address the user's request."""

    def _parse_ai_response(self, content, game_id):
        """Parse AI response and extract game data"""
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
            required_fields = ['title', 'description', 'html']
            for field in required_fields:
                if field not in game_data or not game_data[field]:
                    print(f"❌ Missing required field: {field}")
                    return None
            
            # Enhance HTML if needed
            html = game_data['html']
            if not html.startswith('<!DOCTYPE html>'):
                html = self._wrap_html(html, game_data['title'], game_data['description'])
            
            # Ensure mobile optimization
            html = self._ensure_mobile_optimization(html)
            
            return {
                'title': self._clean_text(game_data['title'], 50),
                'description': self._clean_text(game_data['description'], 200),
                'genre': game_data.get('genre', 'custom'),
                'html': html
            }
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parse error: {e}")
            print(f"Content: {content[:500]}...")
            return None
        except Exception as e:
            print(f"❌ Parse error: {e}")
            return None
    
    def _ensure_mobile_optimization(self, html):
        """Ensure HTML includes mobile optimization"""
        mobile_optimizations = """
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
        <style>
            * { touch-action: manipulation; }
            body { -webkit-user-select: none; -moz-user-select: none; -ms-user-select: none; user-select: none; }
            canvas { touch-action: none; }
        </style>
        <script>
            // Prevent zoom on double tap
            document.addEventListener('touchstart', function(e) {
                if (e.touches.length > 1) {
                    e.preventDefault();
                }
            });
            
            let lastTouchEnd = 0;
            document.addEventListener('touchend', function(e) {
                const now = (new Date()).getTime();
                if (now - lastTouchEnd <= 300) {
                    e.preventDefault();
                }
                lastTouchEnd = now;
            }, false);
        </script>
        """
        
        if '<head>' in html and mobile_optimizations not in html:
            html = html.replace('<head>', f'<head>{mobile_optimizations}')
        
        return html
    
    def _wrap_html(self, html_content, title, description):
        """Wrap HTML content with proper structure"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>{title}</title>
    <style>
        * {{ touch-action: manipulation; }}
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
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
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
    
    <script>
        // Prevent zoom on double tap
        document.addEventListener('touchstart', function(e) {{
            if (e.touches.length > 1) {{
                e.preventDefault();
            }}
        }});
        
        let lastTouchEnd = 0;
        document.addEventListener('touchend', function(e) {{
            const now = (new Date()).getTime();
            if (now - lastTouchEnd <= 300) {{
                e.preventDefault();
            }}
            lastTouchEnd = now;
        }}, false);
    </script>
</body>
</html>"""

    def _clean_text(self, text, max_length):
        """Clean and limit text length"""
        text = str(text).strip()
        # Remove any HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        if len(text) > max_length:
            text = text[:max_length-3] + "..."
        return text
    
    def _generate_advanced_game(self, description, game_id):
        """Generate advanced games using intelligent templates"""
        description_lower = description.lower()
        
        # Advanced game type detection
        if any(word in description_lower for word in ['cook', 'pizza', 'recipe', 'ingredient', 'bake', 'chef']):
            return self._create_cooking_game(description, game_id)
        elif any(word in description_lower for word in ['type', 'word', 'letter', 'spell', 'keyboard']):
            return self._create_typing_game(description, game_id)
        elif any(word in description_lower for word in ['memory', 'remember', 'match', 'pair', 'simon']):
            return self._create_memory_game(description, game_id)
        elif any(word in description_lower for word in ['tower', 'defense', 'defend', 'enemy', 'wave']):
            return self._create_tower_defense_game(description, game_id)
        elif any(word in description_lower for word in ['fish', 'fishing', 'catch', 'rod', 'ocean', 'lake']):
            return self._create_fishing_game(description, game_id)
        elif any(word in description_lower for word in ['collect', 'gather', 'pick', 'find', 'treasure']):
            return self._create_collection_game(description, game_id)
        elif any(word in description_lower for word in ['avoid', 'dodge', 'escape', 'run', 'survive']):
            return self._create_avoidance_game(description, game_id)
        elif any(word in description_lower for word in ['shoot', 'fire', 'blast', 'destroy', 'gun']):
            return self._create_shooter_game(description, game_id)
        elif any(word in description_lower for word in ['jump', 'platform', 'climb', 'leap', 'run']):
            return self._create_platformer_game(description, game_id)
        elif any(word in description_lower for word in ['race', 'drive', 'speed', 'fast', 'car']):
            return self._create_racing_game(description, game_id)
        else:
            return self._create_adventure_game(description, game_id)
    
    def _create_cooking_game(self, description, game_id):
        """Create an interactive cooking game"""
        title = "Pizza Master Chef"
        desc = "Create delicious pizzas by dragging ingredients onto the dough and baking them to perfection!"
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>{title}</title>
    <style>
        * {{ touch-action: manipulation; }}
        body {{
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%);
            color: white;
            font-family: 'Arial', sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
            -webkit-user-select: none;
            user-select: none;
        }}
        .game-header {{
            text-align: center;
            margin-bottom: 20px;
        }}
        .game-title {{
            font-size: 2.5em;
            margin: 0;
            background: linear-gradient(45deg, #ff9ff3, #f368e0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }}
        .game-area {{
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
            max-width: 800px;
        }}
        .pizza-base {{
            width: 200px;
            height: 200px;
            background: radial-gradient(circle, #deb887 0%, #cd853f 100%);
            border-radius: 50%;
            border: 5px solid #8b4513;
            position: relative;
            cursor: pointer;
        }}
        .ingredients {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
        }}
        .ingredient {{
            width: 60px;
            height: 60px;
            border-radius: 10px;
            cursor: grab;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2em;
            border: 2px solid white;
            transition: transform 0.2s;
        }}
        .ingredient:hover {{
            transform: scale(1.1);
        }}
        .ingredient:active {{
            cursor: grabbing;
            transform: scale(0.9);
        }}
        .cheese {{ background: #ffeb3b; }}
        .pepperoni {{ background: #f44336; }}
        .mushroom {{ background: #8bc34a; }}
        .olive {{ background: #4caf50; }}
        .tomato {{ background: #ff5722; }}
        .oven {{
            width: 250px;
            height: 150px;
            background: linear-gradient(135deg, #424242 0%, #212121 100%);
            border-radius: 15px;
            border: 3px solid #757575;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s;
        }}
        .oven:hover {{
            background: linear-gradient(135deg, #ff6b6b 0%, #ff5722 100%);
        }}
        .score {{
            font-size: 1.5em;
            margin: 20px 0;
        }}
        .topping {{
            position: absolute;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            pointer-events: none;
        }}
        .controls {{
            margin-top: 20px;
            text-align: center;
        }}
        .btn {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            color: white;
            padding: 15px 30px;
            border-radius: 25px;
            font-size: 1.1em;
            cursor: pointer;
            margin: 5px;
            transition: all 0.3s;
        }}
        .btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }}
    </style>
</head>
<body>
    <div class="game-header">
        <h1 class="game-title">{title}</h1>
        <p>{desc}</p>
    </div>
    
    <div class="score">Score: <span id="score">0</span> | Pizzas Made: <span id="pizzas">0</span></div>
    
    <div class="game-area">
        <div class="pizza-base" id="pizzaBase"></div>
        
        <div class="ingredients">
            <div class="ingredient cheese" draggable="true" data-ingredient="cheese">🧀</div>
            <div class="ingredient pepperoni" draggable="true" data-ingredient="pepperoni">🍕</div>
            <div class="ingredient mushroom" draggable="true" data-ingredient="mushroom">🍄</div>
            <div class="ingredient olive" draggable="true" data-ingredient="olive">🫒</div>
            <div class="ingredient tomato" draggable="true" data-ingredient="tomato">🍅</div>
        </div>
        
        <div class="oven" id="oven">
            <span>🔥 OVEN - Click to Bake! 🔥</span>
        </div>
    </div>
    
    <div class="controls">
        <button class="btn" onclick="clearPizza()">🗑️ Clear Pizza</button>
        <button class="btn" onclick="newOrder()">📋 New Order</button>
    </div>

    <script>
        let score = 0;
        let pizzasMade = 0;
        let toppings = [];
        let currentOrder = [];
        
        const pizzaBase = document.getElementById('pizzaBase');
        const oven = document.getElementById('oven');
        const ingredients = document.querySelectorAll('.ingredient');
        
        // Generate random order
        function newOrder() {{
            const availableIngredients = ['cheese', 'pepperoni', 'mushroom', 'olive', 'tomato'];
            currentOrder = [];
            const orderSize = Math.floor(Math.random() * 3) + 2; // 2-4 ingredients
            
            for (let i = 0; i < orderSize; i++) {{
                const ingredient = availableIngredients[Math.floor(Math.random() * availableIngredients.length)];
                if (!currentOrder.includes(ingredient)) {{
                    currentOrder.push(ingredient);
                }}
            }}
            
            alert(`New Order: ${{currentOrder.join(', ').toUpperCase()}}!`);
        }}
        
        // Drag and drop for desktop
        ingredients.forEach(ingredient => {{
            ingredient.addEventListener('dragstart', (e) => {{
                e.dataTransfer.setData('text/plain', e.target.dataset.ingredient);
            }});
        }});
        
        pizzaBase.addEventListener('dragover', (e) => {{
            e.preventDefault();
        }});
        
        pizzaBase.addEventListener('drop', (e) => {{
            e.preventDefault();
            const ingredient = e.dataTransfer.getData('text/plain');
            addTopping(ingredient, e.offsetX, e.offsetY);
        }});
        
        // Touch support for mobile
        let draggedElement = null;
        
        ingredients.forEach(ingredient => {{
            ingredient.addEventListener('touchstart', (e) => {{
                draggedElement = e.target.dataset.ingredient;
                e.target.style.opacity = '0.5';
            }});
            
            ingredient.addEventListener('touchend', (e) => {{
                e.target.style.opacity = '1';
                draggedElement = null;
            }});
        }});
        
        pizzaBase.addEventListener('touchstart', (e) => {{
            if (draggedElement) {{
                e.preventDefault();
                const rect = pizzaBase.getBoundingClientRect();
                const x = e.touches[0].clientX - rect.left;
                const y = e.touches[0].clientY - rect.top;
                addTopping(draggedElement, x, y);
                draggedElement = null;
            }}
        }});
        
        // Click to add toppings (fallback)
        pizzaBase.addEventListener('click', (e) => {{
            const ingredients = ['cheese', 'pepperoni', 'mushroom', 'olive', 'tomato'];
            const randomIngredient = ingredients[Math.floor(Math.random() * ingredients.length)];
            addTopping(randomIngredient, e.offsetX, e.offsetY);
        }});
        
        function addTopping(ingredient, x, y) {{
            const topping = document.createElement('div');
            topping.className = 'topping';
            topping.style.left = (x - 10) + 'px';
            topping.style.top = (y - 10) + 'px';
            
            // Set topping appearance
            const toppingStyles = {{
                cheese: {{ background: '#ffeb3b', content: '🧀' }},
                pepperoni: {{ background: '#f44336', content: '🍕' }},
                mushroom: {{ background: '#8bc34a', content: '🍄' }},
                olive: {{ background: '#4caf50', content: '🫒' }},
                tomato: {{ background: '#ff5722', content: '🍅' }}
            }};
            
            const style = toppingStyles[ingredient];
            topping.style.background = style.background;
            topping.textContent = style.content;
            topping.style.fontSize = '12px';
            
            pizzaBase.appendChild(topping);
            toppings.push(ingredient);
            
            // Haptic feedback
            if (navigator.vibrate) {{
                navigator.vibrate(50);
            }}
        }}
        
        function clearPizza() {{
            pizzaBase.innerHTML = '';
            toppings = [];
        }}
        
        function bakePizza() {{
            if (toppings.length === 0) {{
                alert('Add some toppings first!');
                return;
            }}
            
            // Check if order matches
            let orderScore = 0;
            if (currentOrder.length > 0) {{
                const orderMatches = currentOrder.every(ingredient => toppings.includes(ingredient));
                if (orderMatches) {{
                    orderScore = currentOrder.length * 50;
                    alert(`Perfect! Order completed! Bonus: +${{orderScore}} points!`);
                }} else {{
                    orderScore = 10;
                    alert('Pizza made, but not quite the order. Try again!');
                }}
            }} else {{
                orderScore = toppings.length * 10;
            }}
            
            score += orderScore;
            pizzasMade++;
            
            document.getElementById('score').textContent = score;
            document.getElementById('pizzas').textContent = pizzasMade;
            
            // Baking animation
            pizzaBase.style.background = 'radial-gradient(circle, #8b4513 0%, #654321 100%)';
            setTimeout(() => {{
                pizzaBase.style.background = 'radial-gradient(circle, #deb887 0%, #cd853f 100%)';
                clearPizza();
                if (currentOrder.length > 0) {{
                    newOrder();
                }}
            }}, 1000);
            
            // Haptic feedback
            if (navigator.vibrate) {{
                navigator.vibrate([100, 50, 100]);
            }}
        }}
        
        oven.addEventListener('click', bakePizza);
        
        // Start with first order
        newOrder();
        
        // Prevent scrolling
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
            "genre": "cooking",
            "html": html,
            "ai_generated": False,
            "created_at": datetime.now().isoformat()
        }
    
    def _generate_simple_fallback(self, description, game_id):
        """Simple fallback when everything else fails"""
        return {
            "success": True,
            "game_id": game_id,
            "title": "Custom Game",
            "description": f"A custom game inspired by: {description[:50]}...",
            "genre": "custom",
            "html": f"""<!DOCTYPE html>
<html><head><title>Custom Game</title><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-align: center; padding: 50px; font-family: Arial;">
<h1>🎮 Custom Game</h1>
<p>Inspired by: {description}</p>
<button onclick="playGame()" style="padding: 20px; font-size: 20px; background: #f093fb; color: white; border: none; border-radius: 10px; cursor: pointer; margin: 10px;">🎮 Play Game</button>
<div id="score" style="font-size: 24px; margin: 20px;">Score: 0</div>
<script>
let score = 0;
function playGame() {{
    score += Math.floor(Math.random() * 50) + 10;
    document.getElementById('score').textContent = 'Score: ' + score;
    if (navigator.vibrate) navigator.vibrate(50);
    if (score >= 200) alert('🎉 You won! Final score: ' + score);
}}
</script>
</body></html>""",
            "ai_generated": False,
            "created_at": datetime.now().isoformat()
        }

# Create global instance
game_engine = UltimateGameEngine()

def generate_game(description, improvement_request=None, existing_game_id=None):
    """Main function for external use"""
    return game_engine.generate_game(description, improvement_request, existing_game_id)

def improve_game(game_id, improvement_request):
    """Function to improve existing games"""
    return game_engine.improve_game(game_id, improvement_request)

# Export functions
__all__ = ['generate_game', 'improve_game']
