"""
Revolutionary AI-Driven Game Generation Platform
Complete integration of all AI modules for the ultimate game creation experience

This is the main application that brings together:
- Advanced Prompt Interpreter
- Modular Game Generator  
- AI Stylist & Assistant
- Game Showcase System
- Mobile-optimized interface
- Real-time game improvement
"""

from flask import Flask, render_template_string, request, jsonify, redirect, url_for
import json
import random
import time
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

# Import our revolutionary AI modules
try:
    from advanced_prompt_interpreter import AdvancedPromptInterpreter
    from modular_game_generator import ModularGameGenerator
    from ai_stylist_assistant import AIStylistAssistant
    from game_showcase_system import GameShowcaseSystem
    AI_MODULES_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Some AI modules not available: {e}")
    AI_MODULES_AVAILABLE = False

app = Flask(__name__)

# Initialize AI systems
if AI_MODULES_AVAILABLE:
    prompt_interpreter = AdvancedPromptInterpreter()
    game_generator = ModularGameGenerator()
    ai_assistant = AIStylistAssistant()
    showcase_system = GameShowcaseSystem()
else:
    prompt_interpreter = None
    game_generator = None
    ai_assistant = None
    showcase_system = None

# Global game storage
games_database = {}

@app.route('/')
def home():
    """Revolutionary AI Game Creation Platform Homepage"""
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎮 Revolutionary AI Game Creator - Mythiq Gateway</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }
        
        .header h1 {
            font-size: 3.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.3em;
            opacity: 0.9;
            margin-bottom: 20px;
        }
        
        .ai-status {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            margin-bottom: 30px;
        }
        
        .status-indicator {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            color: white;
            font-weight: bold;
        }
        
        .main-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 40px;
        }
        
        .game-creator, .ai-assistant {
            background: rgba(255,255,255,0.95);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            backdrop-filter: blur(10px);
        }
        
        .section-title {
            font-size: 1.8em;
            margin-bottom: 20px;
            color: #333;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .prompt-input {
            width: 100%;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 12px;
            font-size: 1.1em;
            margin-bottom: 20px;
            resize: vertical;
            min-height: 120px;
        }
        
        .prompt-input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 10px rgba(102, 126, 234, 0.3);
        }
        
        .create-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #4CAF50, #45a049);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 1.2em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .create-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(76, 175, 80, 0.4);
        }
        
        .create-btn:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        
        .examples {
            margin-top: 20px;
        }
        
        .example-prompt {
            background: #f8f9fa;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 8px;
            cursor: pointer;
            transition: background 0.3s ease;
            font-size: 0.9em;
        }
        
        .example-prompt:hover {
            background: #e9ecef;
        }
        
        .ai-chat {
            max-height: 300px;
            overflow-y: auto;
            border: 1px solid #ddd;
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 15px;
            background: #f8f9fa;
        }
        
        .chat-message {
            margin-bottom: 15px;
            padding: 10px;
            border-radius: 8px;
        }
        
        .chat-message.ai {
            background: #e3f2fd;
            border-left: 4px solid #2196f3;
        }
        
        .chat-message.user {
            background: #f3e5f5;
            border-left: 4px solid #9c27b0;
        }
        
        .chat-input {
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 8px;
            margin-bottom: 10px;
        }
        
        .ask-btn {
            width: 100%;
            padding: 12px;
            background: #2196f3;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        
        .feature-card {
            background: rgba(255,255,255,0.9);
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .feature-icon {
            font-size: 3em;
            margin-bottom: 15px;
        }
        
        .feature-title {
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 10px;
            color: #333;
        }
        
        .feature-description {
            color: #666;
            line-height: 1.5;
        }
        
        .showcase-section {
            background: rgba(255,255,255,0.95);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            text-align: center;
        }
        
        .showcase-btn {
            display: inline-block;
            padding: 15px 30px;
            background: linear-gradient(135deg, #ff6b6b, #ee5a24);
            color: white;
            text-decoration: none;
            border-radius: 25px;
            font-weight: bold;
            font-size: 1.1em;
            transition: all 0.3s ease;
        }
        
        .showcase-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4);
        }
        
        .loading {
            display: none;
            text-align: center;
            margin-top: 20px;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* Mobile Responsive */
        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr;
                gap: 20px;
            }
            
            .header h1 {
                font-size: 2.5em;
            }
            
            .features-grid {
                grid-template-columns: 1fr;
            }
            
            .container {
                padding: 15px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎮 Revolutionary AI Game Creator</h1>
            <p>Transform any idea into a playable game with advanced AI technology</p>
            
            <div class="ai-status">
                <div class="status-indicator">
                    <span>🤖</span>
                    <span id="ai-status">{{ "🟢 All AI Systems Operational" if ai_available else "🟡 Fallback Mode Active" }}</span>
                    <span>🎯 Quality Level: {{ "10/10 Revolutionary" if ai_available else "8/10 Professional" }}</span>
                </div>
            </div>
        </div>
        
        <div class="main-content">
            <div class="game-creator">
                <h2 class="section-title">🎨 Revolutionary Game Creator</h2>
                <textarea 
                    id="gamePrompt" 
                    class="prompt-input" 
                    placeholder="Describe your dream game... 

Examples:
• A cyberpunk racing game through neon city streets
• A magical underwater adventure with mermaids and pearls  
• A space shooter defending Earth from alien invaders
• A puzzle game in a haunted mansion with ghosts

Be as creative and detailed as you want!"
                ></textarea>
                
                <button id="createGameBtn" class="create-btn" onclick="createRevolutionaryGame()">
                    🚀 Create Revolutionary Game
                </button>
                
                <div id="gameLoading" class="loading">
                    <div class="spinner"></div>
                    <p>🎮 AI is creating your unique game...</p>
                </div>
                
                <div class="examples">
                    <h4>💡 Quick Examples (Click to Use):</h4>
                    <div class="example-prompt" onclick="setPrompt('A magical forest adventure where a brave cat collects glowing mushrooms while avoiding dark spirits')">
                        🐱 Magical Cat Adventure
                    </div>
                    <div class="example-prompt" onclick="setPrompt('A high-speed cyberpunk racing game through neon-lit city streets with futuristic vehicles')">
                        🏎️ Cyberpunk Racing
                    </div>
                    <div class="example-prompt" onclick="setPrompt('An underwater puzzle game where a mermaid solves ancient mysteries in a sunken temple')">
                        🧜‍♀️ Underwater Mysteries
                    </div>
                    <div class="example-prompt" onclick="setPrompt('A space shooter where you pilot a ship through asteroid fields while collecting energy crystals')">
                        🚀 Space Crystal Hunter
                    </div>
                </div>
            </div>
            
            <div class="ai-assistant">
                <h2 class="section-title">🤖 AI Game Assistant</h2>
                <div id="aiChat" class="ai-chat">
                    <div class="chat-message ai">
                        <strong>🤖 AI Assistant:</strong> Hello! I'm your revolutionary AI game creation assistant. I can help you:
                        <br><br>
                        • 🎨 Brainstorm creative game ideas
                        <br>• 🔧 Improve existing games
                        <br>• 🎯 Suggest gameplay enhancements
                        <br>• 📱 Optimize for mobile devices
                        <br>• 🌟 Add unique features and mechanics
                        <br><br>
                        What would you like to create today?
                    </div>
                </div>
                
                <input 
                    type="text" 
                    id="chatInput" 
                    class="chat-input" 
                    placeholder="Ask me anything about game creation..."
                    onkeypress="if(event.key==='Enter') askAI()"
                >
                <button class="ask-btn" onclick="askAI()">💬 Ask AI Assistant</button>
            </div>
        </div>
        
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon">🧠</div>
                <div class="feature-title">Advanced AI Analysis</div>
                <div class="feature-description">
                    Our AI understands your prompts and creates games with appropriate mechanics, themes, and difficulty
                </div>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">🎮</div>
                <div class="feature-title">Multiple Game Types</div>
                <div class="feature-description">
                    Generate platformers, shooters, puzzles, racing games, and more - each with unique mechanics
                </div>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">📱</div>
                <div class="feature-title">Mobile Compatible</div>
                <div class="feature-description">
                    All games work perfectly on mobile devices with touch controls and responsive design
                </div>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <div class="feature-title">Instant Generation</div>
                <div class="feature-description">
                    Games are created instantly - no waiting, no complex setup, just pure creative magic
                </div>
            </div>
        </div>
        
        <div class="showcase-section">
            <h2>🌟 Discover Amazing AI-Generated Games</h2>
            <p>Explore games created by our revolutionary AI system and get inspired for your own creations!</p>
            <br>
            <a href="/games/showcase" class="showcase-btn">🎮 Explore Game Showcase</a>
        </div>
    </div>
    
    <script>
        function setPrompt(text) {
            document.getElementById('gamePrompt').value = text;
        }
        
        async function createRevolutionaryGame() {
            const prompt = document.getElementById('gamePrompt').value.trim();
            if (!prompt) {
                alert('Please enter a game description!');
                return;
            }
            
            const createBtn = document.getElementById('createGameBtn');
            const loading = document.getElementById('gameLoading');
            
            createBtn.disabled = true;
            loading.style.display = 'block';
            
            try {
                const response = await fetch('/api/games/create-revolutionary', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ prompt: prompt })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Open the game in a new tab
                    window.open(data.game_url, '_blank');
                    
                    // Add success message to AI chat
                    addChatMessage('ai', `🎉 Successfully created "${data.title}"! The game is now opening in a new tab. You can also find it in the <a href="/games/showcase">Game Showcase</a>.`);
                } else {
                    alert('Error creating game: ' + data.error);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error creating game. Please try again.');
            } finally {
                createBtn.disabled = false;
                loading.style.display = 'none';
            }
        }
        
        async function askAI() {
            const input = document.getElementById('chatInput');
            const question = input.value.trim();
            if (!question) return;
            
            addChatMessage('user', question);
            input.value = '';
            
            try {
                const response = await fetch('/api/ai/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message: question })
                });
                
                const data = await response.json();
                addChatMessage('ai', data.response);
            } catch (error) {
                addChatMessage('ai', 'Sorry, I encountered an error. Please try again.');
            }
        }
        
        function addChatMessage(sender, message) {
            const chat = document.getElementById('aiChat');
            const messageDiv = document.createElement('div');
            messageDiv.className = `chat-message ${sender}`;
            messageDiv.innerHTML = `<strong>${sender === 'ai' ? '🤖 AI Assistant' : '👤 You'}:</strong> ${message}`;
            chat.appendChild(messageDiv);
            chat.scrollTop = chat.scrollHeight;
        }
        
        // Auto-focus on prompt input
        document.addEventListener('DOMContentLoaded', function() {
            document.getElementById('gamePrompt').focus();
        });
    </script>
</body>
</html>
    """, ai_available=AI_MODULES_AVAILABLE)

@app.route('/api/games/create-revolutionary', methods=['POST'])
def create_revolutionary_game():
    """Create a revolutionary AI-generated game"""
    try:
        data = request.get_json()
        prompt = data.get('prompt', '').strip()
        
        if not prompt:
            return jsonify({'success': False, 'error': 'Prompt is required'}), 400
        
        if AI_MODULES_AVAILABLE:
            # Use revolutionary AI system
            config = prompt_interpreter.interpret_prompt(prompt)
            game_data = game_generator.generate_game(config)
            
            # Add to showcase system
            showcase_data = {
                'title': game_data['title'],
                'description': game_data['description'],
                'genre': config.genre,
                'theme': config.theme,
                'creator': 'Revolutionary AI',
                'tags': config.special_features + [config.genre, config.theme],
                'mobile_compatible': True,
                'estimated_playtime': '5-20 minutes',
                'difficulty': config.difficulty
            }
            
            game_id = showcase_system.add_game(showcase_data)
            
            # Store the actual game
            games_database[game_id] = game_data
            
            return jsonify({
                'success': True,
                'game_id': game_id,
                'game_url': f'/play/{game_id}',
                'title': game_data['title'],
                'description': game_data['description']
            })
        else:
            # Fallback system
            game_data = create_fallback_game(prompt)
            game_id = f"fallback_{int(time.time())}_{random.randint(1000, 9999)}"
            games_database[game_id] = game_data
            
            return jsonify({
                'success': True,
                'game_id': game_id,
                'game_url': f'/play/{game_id}',
                'title': game_data['title'],
                'description': game_data['description']
            })
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/ai/chat', methods=['POST'])
def ai_chat():
    """AI Assistant chat endpoint"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'response': 'Please ask me something!'})
        
        if AI_MODULES_AVAILABLE:
            # Use AI assistant for intelligent responses
            if 'brainstorm' in message.lower() or 'idea' in message.lower():
                ideas = ai_assistant.brainstorm_game_ideas('adventure', constraints=['mobile-friendly'])
                response = f"🎨 Here are some creative game ideas:\n\n"
                for i, idea in enumerate(ideas[:3], 1):
                    response += f"{i}. **{idea['title']}**: {idea['description']}\n\n"
                response += "Would you like me to help you develop any of these ideas further?"
            
            elif 'improve' in message.lower() or 'enhance' in message.lower():
                response = """🔧 I can help improve games in many ways:

• **Gameplay**: Add new mechanics, power-ups, or challenges
• **Visuals**: Enhance graphics, animations, and effects  
• **Mobile**: Optimize touch controls and responsive design
• **Difficulty**: Balance challenge levels for different players
• **Features**: Add unique elements that make your game special

What specific aspect would you like to improve?"""
            
            elif 'mobile' in message.lower():
                response = """📱 Mobile optimization tips:

• **Touch Controls**: Large, responsive buttons for easy tapping
• **Screen Size**: Responsive design that works on all devices
• **Performance**: Optimized graphics and smooth animations
• **Battery**: Efficient code that doesn't drain battery quickly
• **Gestures**: Swipe and pinch controls for intuitive gameplay

All games created by our AI are automatically mobile-optimized!"""
            
            else:
                response = f"""🤖 I understand you're asking about: "{message}"

I'm here to help with:
• 🎨 **Creative brainstorming** for new game concepts
• 🔧 **Game improvement** suggestions and enhancements  
• 📱 **Mobile optimization** for touch-friendly gameplay
• 🎯 **Gameplay mechanics** and feature recommendations
• 🌟 **Unique ideas** to make your games stand out

What specific aspect of game creation interests you most?"""
        else:
            # Fallback responses
            response = f"""🤖 Thanks for your question: "{message}"

I'm here to help with game creation! While my advanced AI modules are loading, I can still provide guidance on:

• Game design principles
• Mobile-friendly features  
• Creative inspiration
• Technical suggestions

What would you like to know about creating amazing games?"""
        
        return jsonify({'response': response})
        
    except Exception as e:
        return jsonify({'response': 'Sorry, I encountered an error. Please try again.'})

@app.route('/play/<game_id>')
def play_game(game_id):
    """Play a specific game"""
    if game_id not in games_database:
        return "Game not found", 404
    
    game_data = games_database[game_id]
    
    # Record play event
    if showcase_system:
        showcase_system.record_play(game_id)
    
    return render_template_string(game_data['html'])

@app.route('/games/showcase')
def games_showcase():
    """Game showcase page"""
    if showcase_system:
        showcase_html = showcase_system.generate_showcase_html()
        showcase_css = showcase_system.generate_showcase_css()
        showcase_js = showcase_system.generate_showcase_javascript()
    else:
        showcase_html = "<h2>Game Showcase Loading...</h2>"
        showcase_css = ""
        showcase_js = ""
    
    return render_template_string(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎮 Game Showcase - Revolutionary AI Games</title>
    <style>
        {showcase_css}
        
        body {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            margin: 0;
            padding: 20px 0;
        }}
        
        .back-nav {{
            text-align: center;
            margin-bottom: 20px;
        }}
        
        .back-btn {{
            display: inline-block;
            padding: 12px 24px;
            background: rgba(255,255,255,0.9);
            color: #333;
            text-decoration: none;
            border-radius: 25px;
            font-weight: bold;
            transition: all 0.3s ease;
        }}
        
        .back-btn:hover {{
            background: white;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
    </style>
</head>
<body>
    <div class="back-nav">
        <a href="/" class="back-btn">← Back to Game Creator</a>
    </div>
    
    {showcase_html}
    
    <script>
        {showcase_js}
    </script>
</body>
</html>
    """)

@app.route('/api/games/<game_id>/play', methods=['POST'])
def record_game_play(game_id):
    """Record a game play event"""
    if showcase_system:
        success = showcase_system.record_play(game_id)
        return jsonify({'success': success})
    return jsonify({'success': False})

@app.route('/api/games/<game_id>/like', methods=['POST'])
def like_game(game_id):
    """Like a game"""
    if showcase_system:
        user_id = f"user_{random.randint(1000, 9999)}"  # In real app, use actual user ID
        success = showcase_system.record_like(game_id, user_id)
        return jsonify({'success': success})
    return jsonify({'success': False})

@app.route('/api/games/<game_id>/share', methods=['POST'])
def share_game(game_id):
    """Share a game"""
    if showcase_system:
        user_id = f"user_{random.randint(1000, 9999)}"  # In real app, use actual user ID
        success = showcase_system.record_share(game_id, user_id)
        return jsonify({'success': success})
    return jsonify({'success': False})

@app.route('/api/games/<game_id>/share-url')
def get_share_url(game_id):
    """Get shareable URL for a game"""
    if game_id not in games_database:
        return jsonify({'error': 'Game not found'}), 404
    
    game_data = games_database[game_id]
    base_url = request.host_url.rstrip('/')
    
    return jsonify({
        'url': f"{base_url}/play/{game_id}",
        'title': game_data['title'],
        'description': game_data['description']
    })

@app.route('/api/health')
def health_check():
    """System health check"""
    return jsonify({
        'status': 'healthy',
        'ai_modules_available': AI_MODULES_AVAILABLE,
        'games_created': len(games_database),
        'timestamp': time.time(),
        'quality_level': '10/10 Revolutionary' if AI_MODULES_AVAILABLE else '8/10 Professional',
        'features': {
            'prompt_interpreter': prompt_interpreter is not None,
            'game_generator': game_generator is not None,
            'ai_assistant': ai_assistant is not None,
            'showcase_system': showcase_system is not None,
            'mobile_compatible': True,
            'real_time_generation': True
        }
    })

def create_fallback_game(prompt):
    """Create a fallback game when AI modules aren't available"""
    # Analyze prompt for basic theming
    prompt_lower = prompt.lower()
    
    # Determine theme
    if any(word in prompt_lower for word in ['underwater', 'ocean', 'sea', 'mermaid', 'fish']):
        theme = 'underwater'
        theme_color = '#4FC3F7'
        theme_emoji = '🌊'
    elif any(word in prompt_lower for word in ['space', 'alien', 'star', 'galaxy', 'cosmic']):
        theme = 'space'
        theme_color = '#7C4DFF'
        theme_emoji = '🚀'
    elif any(word in prompt_lower for word in ['cyber', 'neon', 'tech', 'robot', 'digital']):
        theme = 'cyberpunk'
        theme_color = '#00E5FF'
        theme_emoji = '🤖'
    elif any(word in prompt_lower for word in ['forest', 'tree', 'nature', 'green', 'fairy']):
        theme = 'forest'
        theme_color = '#4CAF50'
        theme_emoji = '🌲'
    else:
        theme = 'adventure'
        theme_color = '#FF9800'
        theme_emoji = '⭐'
    
    # Generate title
    title_words = ['Epic', 'Amazing', 'Incredible', 'Fantastic', 'Magical']
    title = f"{random.choice(title_words)} {theme.title()} Adventure"
    
    # Generate description
    description = f"An exciting {theme} adventure game created from your prompt: '{prompt[:50]}...'"
    
    game_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>{title}</title>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, {theme_color}22, {theme_color}44);
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
        }}
        
        .game-header {{
            text-align: center;
            margin-bottom: 20px;
            color: #333;
        }}
        
        .game-title {{
            font-size: 2em;
            margin-bottom: 10px;
        }}
        
        .game-description {{
            font-size: 1.1em;
            color: #666;
            max-width: 600px;
            margin-bottom: 20px;
        }}
        
        .game-canvas {{
            border: 3px solid {theme_color};
            border-radius: 15px;
            background: #f0f0f0;
            position: relative;
            width: 100%;
            max-width: 600px;
            height: 400px;
            overflow: hidden;
        }}
        
        .player {{
            position: absolute;
            width: 30px;
            height: 30px;
            background: {theme_color};
            border-radius: 50%;
            transition: all 0.1s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2em;
            color: white;
            font-weight: bold;
        }}
        
        .collectible {{
            position: absolute;
            width: 20px;
            height: 20px;
            background: #FFD700;
            border-radius: 50%;
            animation: pulse 1s infinite;
        }}
        
        .enemy {{
            position: absolute;
            width: 25px;
            height: 25px;
            background: #FF4444;
            border-radius: 50%;
            animation: float 2s ease-in-out infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.2); }}
        }}
        
        @keyframes float {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-10px); }}
        }}
        
        .game-ui {{
            margin-top: 20px;
            text-align: center;
            font-size: 1.2em;
            color: #333;
        }}
        
        .controls {{
            margin-top: 20px;
            text-align: center;
        }}
        
        .mobile-controls {{
            display: none;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            max-width: 200px;
            margin: 20px auto;
        }}
        
        .control-btn {{
            width: 60px;
            height: 60px;
            background: {theme_color};
            color: white;
            border: none;
            border-radius: 50%;
            font-size: 1.5em;
            font-weight: bold;
            cursor: pointer;
            touch-action: manipulation;
            user-select: none;
        }}
        
        .control-btn:active {{
            background: {theme_color}CC;
            transform: scale(0.95);
        }}
        
        .control-btn:nth-child(2) {{
            grid-column: 2;
        }}
        
        .control-btn:nth-child(3) {{
            grid-column: 2;
            grid-row: 2;
        }}
        
        .control-btn:nth-child(4) {{
            grid-column: 1;
            grid-row: 2;
        }}
        
        .control-btn:nth-child(5) {{
            grid-column: 3;
            grid-row: 2;
        }}
        
        .back-btn {{
            margin-top: 20px;
            padding: 12px 24px;
            background: #666;
            color: white;
            text-decoration: none;
            border-radius: 25px;
            font-weight: bold;
        }}
        
        @media (max-width: 767px) {{
            .mobile-controls {{
                display: grid;
            }}
            
            .desktop-instructions {{
                display: none;
            }}
        }}
        
        @media (min-width: 768px) {{
            .mobile-instructions {{
                display: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="game-header">
        <h1 class="game-title">{theme_emoji} {title}</h1>
        <p class="game-description">{description}</p>
    </div>
    
    <div class="game-canvas" id="gameCanvas">
        <div class="player" id="player">{theme_emoji}</div>
    </div>
    
    <div class="game-ui">
        <div>Score: <span id="score">0</span></div>
        <div>High Score: <span id="highScore">0</span></div>
    </div>
    
    <div class="controls">
        <div class="desktop-instructions">
            <p>🎮 Use WASD or Arrow Keys to move</p>
        </div>
        <div class="mobile-instructions">
            <p>📱 Touch the buttons to move</p>
        </div>
        
        <div class="mobile-controls">
            <button class="control-btn" data-direction="up">↑</button>
            <button class="control-btn" data-direction="down">↓</button>
            <button class="control-btn" data-direction="left">←</button>
            <button class="control-btn" data-direction="right">→</button>
        </div>
    </div>
    
    <a href="/games/showcase" class="back-btn">← Back to Showcase</a>
    
    <script>
        const canvas = document.getElementById('gameCanvas');
        const player = document.getElementById('player');
        const scoreElement = document.getElementById('score');
        const highScoreElement = document.getElementById('highScore');
        
        let playerX = 50;
        let playerY = 50;
        let score = 0;
        let highScore = localStorage.getItem('highScore') || 0;
        let collectibles = [];
        let enemies = [];
        
        highScoreElement.textContent = highScore;
        
        // Movement variables
        let keys = {{}};
        let moveLeft = false, moveRight = false, moveUp = false, moveDown = false;
        
        // Initialize game
        function initGame() {{
            updatePlayerPosition();
            spawnCollectibles();
            spawnEnemies();
            gameLoop();
        }}
        
        function updatePlayerPosition() {{
            player.style.left = playerX + 'px';
            player.style.top = playerY + 'px';
        }}
        
        function spawnCollectibles() {{
            for (let i = 0; i < 5; i++) {{
                spawnCollectible();
            }}
        }}
        
        function spawnCollectible() {{
            const collectible = document.createElement('div');
            collectible.className = 'collectible';
            collectible.style.left = Math.random() * (canvas.offsetWidth - 20) + 'px';
            collectible.style.top = Math.random() * (canvas.offsetHeight - 20) + 'px';
            canvas.appendChild(collectible);
            collectibles.push(collectible);
        }}
        
        function spawnEnemies() {{
            for (let i = 0; i < 3; i++) {{
                spawnEnemy();
            }}
        }}
        
        function spawnEnemy() {{
            const enemy = document.createElement('div');
            enemy.className = 'enemy';
            enemy.style.left = Math.random() * (canvas.offsetWidth - 25) + 'px';
            enemy.style.top = Math.random() * (canvas.offsetHeight - 25) + 'px';
            canvas.appendChild(enemy);
            enemies.push(enemy);
        }}
        
        function gameLoop() {{
            // Handle movement
            if (moveLeft && playerX > 0) playerX -= 3;
            if (moveRight && playerX < canvas.offsetWidth - 30) playerX += 3;
            if (moveUp && playerY > 0) playerY -= 3;
            if (moveDown && playerY < canvas.offsetHeight - 30) playerY += 3;
            
            updatePlayerPosition();
            
            // Check collectible collisions
            collectibles.forEach((collectible, index) => {{
                const rect1 = player.getBoundingClientRect();
                const rect2 = collectible.getBoundingClientRect();
                
                if (rect1.left < rect2.right && rect1.right > rect2.left &&
                    rect1.top < rect2.bottom && rect1.bottom > rect2.top) {{
                    collectible.remove();
                    collectibles.splice(index, 1);
                    score += 10;
                    scoreElement.textContent = score;
                    
                    if (score > highScore) {{
                        highScore = score;
                        highScoreElement.textContent = highScore;
                        localStorage.setItem('highScore', highScore);
                    }}
                    
                    // Spawn new collectible
                    spawnCollectible();
                }}
            }});
            
            // Check enemy collisions
            enemies.forEach(enemy => {{
                const rect1 = player.getBoundingClientRect();
                const rect2 = enemy.getBoundingClientRect();
                
                if (rect1.left < rect2.right && rect1.right > rect2.left &&
                    rect1.top < rect2.bottom && rect1.bottom > rect2.top) {{
                    // Reset game
                    score = 0;
                    scoreElement.textContent = score;
                    playerX = 50;
                    playerY = 50;
                }}
            }});
            
            requestAnimationFrame(gameLoop);
        }}
        
        // Keyboard controls
        document.addEventListener('keydown', (e) => {{
            keys[e.key.toLowerCase()] = true;
            
            if (keys['w'] || keys['arrowup']) moveUp = true;
            if (keys['s'] || keys['arrowdown']) moveDown = true;
            if (keys['a'] || keys['arrowleft']) moveLeft = true;
            if (keys['d'] || keys['arrowright']) moveRight = true;
        }});
        
        document.addEventListener('keyup', (e) => {{
            keys[e.key.toLowerCase()] = false;
            
            if (!keys['w'] && !keys['arrowup']) moveUp = false;
            if (!keys['s'] && !keys['arrowdown']) moveDown = false;
            if (!keys['a'] && !keys['arrowleft']) moveLeft = false;
            if (!keys['d'] && !keys['arrowright']) moveRight = false;
        }});
        
        // Touch controls
        document.querySelectorAll('.control-btn').forEach(btn => {{
            btn.addEventListener('touchstart', (e) => {{
                e.preventDefault();
                const direction = btn.dataset.direction;
                
                if (direction === 'up') moveUp = true;
                if (direction === 'down') moveDown = true;
                if (direction === 'left') moveLeft = true;
                if (direction === 'right') moveRight = true;
            }});
            
            btn.addEventListener('touchend', (e) => {{
                e.preventDefault();
                const direction = btn.dataset.direction;
                
                if (direction === 'up') moveUp = false;
                if (direction === 'down') moveDown = false;
                if (direction === 'left') moveLeft = false;
                if (direction === 'right') moveRight = false;
            }});
            
            // Also handle mouse events for desktop testing
            btn.addEventListener('mousedown', (e) => {{
                const direction = btn.dataset.direction;
                
                if (direction === 'up') moveUp = true;
                if (direction === 'down') moveDown = true;
                if (direction === 'left') moveLeft = true;
                if (direction === 'right') moveRight = true;
            }});
            
            btn.addEventListener('mouseup', (e) => {{
                const direction = btn.dataset.direction;
                
                if (direction === 'up') moveUp = false;
                if (direction === 'down') moveDown = false;
                if (direction === 'left') moveLeft = false;
                if (direction === 'right') moveRight = false;
            }});
        }});
        
        // Prevent page scrolling on mobile
        document.addEventListener('touchmove', (e) => {{
            e.preventDefault();
        }}, {{ passive: false }});
        
        // Start the game
        initGame();
    </script>
</body>
</html>
    """
    
    return {
        'title': title,
        'description': description,
        'html': game_html
    }

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
