#!/usr/bin/env python3
"""
🎮 AI Game Engine - MOBILE & DESKTOP OPTIMIZED VERSION
Creates complete games that work perfectly on both mobile and desktop
"""

import os
import json
import time
import random
import string
from typing import Dict, List, Any, Optional
import requests

class GameEngine:
    """AI-powered game creation engine optimized for mobile and desktop"""
    
    def __init__(self):
        self.groq_api_key = os.environ.get('GROQ_API_KEY')
        self.groq_api_base = "https://api.groq.com/openai/v1"
        
        # Debug: Print API key status (first 10 chars only for security)
        if self.groq_api_key:
            print(f"✅ GROQ API Key found: {self.groq_api_key[:10]}...")
        else:
            print("❌ GROQ API Key not found in environment variables")
        
        # Game templates with mobile-optimized implementations
        self.templates = {
            'platformer': self.get_platformer_template(),
            'puzzle': self.get_puzzle_template(),
            'shooter': self.get_shooter_template(),
            'rpg': self.get_rpg_template(),
            'racing': self.get_racing_template(),
            'strategy': self.get_strategy_template()
        }
    
    def create_complete_game(self, prompt: str) -> Dict[str, Any]:
        """Create a complete mobile-optimized game from user prompt"""
        
        try:
            print(f"🎮 Creating mobile-optimized game from prompt: {prompt}")
            
            # Step 1: Generate game concept
            concept_result = self.generate_game_concept(prompt)
            if concept_result['status'] != 'success':
                return concept_result
            
            concept = concept_result['concept']
            print(f"✅ Generated concept: {concept.get('title', 'Unknown')}")
            
            # Step 2: Select and customize template
            template_name = concept.get('genre', 'puzzle').lower()
            if template_name not in self.templates:
                template_name = 'puzzle'  # Default fallback
            
            print(f"🎯 Using mobile-optimized template: {template_name}")
            
            # Step 3: Customize the game with mobile optimizations
            customized_code = self.customize_game_template(template_name, concept)
            
            # Step 4: Generate game assets
            assets = self.generate_game_assets(concept)
            
            # Step 5: Create final game package
            game_id = self.generate_game_id()
            
            game_data = {
                'id': game_id,
                'title': concept.get('title', 'AI Generated Game'),
                'concept': concept,
                'code': customized_code,
                'assets': assets,
                'instructions': self.generate_instructions(concept),
                'created_at': time.time(),
                'play_url': f'/games/play/{game_id}',
                'share_url': f'/games/share/{game_id}',
                'mobile_optimized': True
            }
            
            print(f"🎉 Mobile-optimized game created successfully: {game_data['title']}")
            
            return {
                'status': 'success',
                'game': game_data,
                'message': f"Successfully created '{game_data['title']}' - Optimized for mobile & desktop!",
                'cost': '$0.02'
            }
            
        except Exception as e:
            print(f"❌ Error creating game: {str(e)}")
            return {
                'status': 'error',
                'message': f'Failed to create game: {str(e)}',
                'cost': '$0.00'
            }
    
    def generate_game_concept(self, prompt: str) -> Dict[str, Any]:
        """Generate game concept using Groq API with enhanced error handling"""
        
        try:
            # Check if API key is available
            if not self.groq_api_key:
                print("❌ No GROQ API key - using fallback concept generation")
                return self.generate_fallback_concept(prompt)
            
            # Prepare the API request
            headers = {
                "Authorization": f"Bearer {self.groq_api_key}",
                "Content-Type": "application/json"
            }
            
            system_prompt = """You are a professional game designer specializing in mobile-friendly games. Create a detailed game concept based on the user's description. 
            
            Respond with ONLY a valid JSON object in this exact format:
            {
                "title": "Game Title",
                "genre": "puzzle",
                "description": "Brief description",
                "mechanics": ["mechanic1", "mechanic2"],
                "difficulty": "easy",
                "theme": "space",
                "target_audience": "casual",
                "estimated_playtime": "5-10 minutes",
                "mobile_friendly": true
            }
            
            Genre must be one of: platformer, puzzle, shooter, rpg, racing, strategy
            Difficulty must be one of: easy, medium, hard
            Keep descriptions concise and family-friendly.
            Ensure all games work well on mobile devices with touch controls."""
            
            payload = {
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Create a mobile-friendly game concept for: {prompt}"}
                ],
                "temperature": 0.7,
                "max_tokens": 500,
                "top_p": 1,
                "stream": False
            }
            
            print(f"🔄 Calling Groq API for mobile-optimized concept...")
            
            # Make the API request with timeout
            response = requests.post(
                f"{self.groq_api_base}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            print(f"📊 API Response Status: {response.status_code}")
            
            # Check response status
            if response.status_code != 200:
                print(f"❌ API Error {response.status_code}: {response.text}")
                return self.generate_fallback_concept(prompt)
            
            # Parse response
            try:
                response_data = response.json()
                print(f"✅ API Response received: {len(str(response_data))} characters")
                
                if 'choices' not in response_data or not response_data['choices']:
                    print("❌ No choices in API response")
                    return self.generate_fallback_concept(prompt)
                
                content = response_data['choices'][0]['message']['content'].strip()
                print(f"📄 AI Generated Content: {content[:200]}...")
                
                # Parse JSON from AI response
                concept = json.loads(content)
                
                # Validate required fields
                required_fields = ['title', 'genre', 'description']
                for field in required_fields:
                    if field not in concept:
                        concept[field] = self.get_default_value(field, prompt)
                
                # Ensure mobile-friendly flag
                concept['mobile_friendly'] = True
                
                print(f"✅ Mobile-optimized concept parsed successfully: {concept.get('title')}")
                
                return {
                    'status': 'success',
                    'concept': concept
                }
                
            except json.JSONDecodeError as e:
                print(f"❌ JSON Parse Error: {str(e)}")
                print(f"📄 Raw content: {content}")
                return self.generate_fallback_concept(prompt)
                
        except requests.exceptions.Timeout:
            print("❌ API request timed out")
            return self.generate_fallback_concept(prompt)
            
        except requests.exceptions.RequestException as e:
            print(f"❌ API request failed: {str(e)}")
            return self.generate_fallback_concept(prompt)
            
        except Exception as e:
            print(f"❌ Unexpected error in concept generation: {str(e)}")
            return self.generate_fallback_concept(prompt)
    
    def generate_fallback_concept(self, prompt: str) -> Dict[str, Any]:
        """Generate a mobile-optimized fallback concept when API fails"""
        
        print("🔄 Using mobile-optimized fallback concept generation")
        
        # Analyze prompt for keywords to determine genre
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ['shoot', 'space', 'alien', 'laser', 'enemy']):
            genre = 'shooter'
            title = 'Space Defender'
            description = 'Defend Earth from alien invaders in this mobile-friendly space shooter'
        elif any(word in prompt_lower for word in ['puzzle', 'tile', 'slide', 'match', 'solve']):
            genre = 'puzzle'
            title = 'Sliding Puzzle'
            description = 'Arrange numbered tiles in the correct order with touch controls'
        elif any(word in prompt_lower for word in ['jump', 'platform', 'run', 'collect']):
            genre = 'platformer'
            title = 'Platform Adventure'
            description = 'Jump and run through challenging platforms with touch controls'
        elif any(word in prompt_lower for word in ['race', 'car', 'speed', 'track']):
            genre = 'racing'
            title = 'Speed Racer'
            description = 'Race through exciting tracks with mobile-friendly controls'
        elif any(word in prompt_lower for word in ['rpg', 'adventure', 'quest', 'character']):
            genre = 'rpg'
            title = 'Adventure Quest'
            description = 'Embark on an epic adventure with touch-friendly interface'
        else:
            genre = 'strategy'
            title = 'Strategy Game'
            description = 'Plan your moves carefully with intuitive touch controls'
        
        concept = {
            'title': title,
            'genre': genre,
            'description': description,
            'mechanics': ['touch', 'tap', 'swipe', 'score'],
            'difficulty': 'easy',
            'theme': 'colorful',
            'target_audience': 'casual',
            'estimated_playtime': '5-10 minutes',
            'mobile_friendly': True
        }
        
        print(f"✅ Mobile-optimized fallback concept created: {concept['title']}")
        
        return {
            'status': 'success',
            'concept': concept
        }
    
    def get_default_value(self, field: str, prompt: str) -> str:
        """Get default values for missing fields"""
        defaults = {
            'title': 'AI Generated Game',
            'genre': 'puzzle',
            'description': f'A fun mobile-friendly game based on: {prompt[:50]}...',
            'difficulty': 'easy',
            'theme': 'colorful',
            'target_audience': 'casual'
        }
        return defaults.get(field, 'unknown')
    
    def customize_game_template(self, template_name: str, concept: Dict[str, Any]) -> Dict[str, str]:
        """Customize game template based on concept with mobile optimizations"""
        
        template = self.templates[template_name].copy()
        
        # Replace placeholders with concept data
        replacements = {
            '{{GAME_TITLE}}': concept.get('title', 'AI Game'),
            '{{GAME_DESCRIPTION}}': concept.get('description', 'A fun AI-generated mobile game'),
            '{{DIFFICULTY}}': concept.get('difficulty', 'easy'),
            '{{THEME}}': concept.get('theme', 'colorful')
        }
        
        # Apply replacements to HTML
        html = template['html']
        for placeholder, value in replacements.items():
            html = html.replace(placeholder, value)
        
        return {
            'html': html,
            'css': template['css'],
            'javascript': template['javascript']
        }
    
    def generate_game_assets(self, concept: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mobile-optimized game assets"""
        
        return {
            'sprites': {
                'player': '/static/sprites/player.png',
                'enemy': '/static/sprites/enemy.png',
                'background': '/static/sprites/background.png'
            },
            'sounds': {
                'tap': '/static/sounds/tap.wav',
                'collect': '/static/sounds/collect.wav',
                'game_over': '/static/sounds/game_over.wav'
            },
            'music': {
                'background': '/static/music/background.mp3'
            },
            'mobile_assets': {
                'touch_controls': True,
                'haptic_feedback': True,
                'responsive_design': True
            }
        }
    
    def generate_instructions(self, concept: Dict[str, Any]) -> Dict[str, str]:
        """Generate mobile-friendly game instructions"""
        
        genre = concept.get('genre', 'puzzle')
        
        instructions = {
            'puzzle': 'Tap tiles to slide them into the correct order. Arrange numbers 1-15 in sequence.',
            'shooter': 'Tap to move, tap and hold to shoot. Destroy all enemies to win!',
            'platformer': 'Tap left/right to move, tap jump button to jump. Collect coins and avoid enemies.',
            'racing': 'Tap left/right to steer, avoid obstacles and reach the finish line first.',
            'rpg': 'Tap to move and interact. Complete quests and level up your character.',
            'strategy': 'Tap to select units, plan your moves carefully to defeat opponents.'
        }
        
        return {
            'how_to_play': instructions.get(genre, 'Use touch controls to play.'),
            'objective': concept.get('description', 'Have fun playing!'),
            'controls': 'Touch and tap controls optimized for mobile and desktop'
        }
    
    def generate_game_id(self) -> str:
        """Generate unique game ID"""
        timestamp = str(int(time.time()))
        random_chars = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        return f"game_{timestamp}_{random_chars}"
    
    def get_puzzle_template(self) -> Dict[str, str]:
        """Get mobile-optimized sliding puzzle game template"""
        
        html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>{{GAME_TITLE}}</title>
    <style>
        * {
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
            -webkit-touch-callout: none;
            -webkit-user-select: none;
            user-select: none;
        }
        
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            text-align: center; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            margin: 0; 
            padding: 10px; 
            min-height: 100vh; 
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            overflow-x: hidden;
        }
        
        .game-container { 
            width: 100%;
            max-width: 400px; 
            margin: 0 auto; 
            background: rgba(255,255,255,0.1); 
            padding: 15px; 
            border-radius: 20px; 
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        
        h1 {
            font-size: clamp(1.5rem, 5vw, 2.5rem);
            margin: 10px 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        p {
            font-size: clamp(0.9rem, 3vw, 1.1rem);
            margin: 10px 0;
            opacity: 0.9;
        }
        
        .puzzle-grid { 
            display: grid; 
            grid-template-columns: repeat(4, 1fr); 
            gap: 3px; 
            margin: 20px 0; 
            background: rgba(0,0,0,0.2); 
            padding: 10px; 
            border-radius: 15px; 
            aspect-ratio: 1;
            max-width: 320px;
            margin-left: auto;
            margin-right: auto;
        }
        
        .tile { 
            aspect-ratio: 1;
            background: linear-gradient(45deg, #FF6B6B, #4ECDC4); 
            border: none; 
            border-radius: 8px; 
            font-size: clamp(1rem, 4vw, 1.5rem);
            font-weight: bold; 
            color: white; 
            cursor: pointer; 
            transition: all 0.2s ease; 
            display: flex;
            align-items: center;
            justify-content: center;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
            touch-action: manipulation;
            min-height: 60px;
        }
        
        .tile:hover, .tile:active { 
            transform: scale(0.95); 
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
        
        .empty { 
            background: transparent; 
            cursor: default; 
        }
        
        .empty:hover, .empty:active { 
            transform: none; 
            box-shadow: none;
        }
        
        .controls { 
            margin: 20px 0; 
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
        }
        
        .btn { 
            background: linear-gradient(45deg, #FFD93D, #FF6B6B); 
            color: white; 
            border: none; 
            padding: 12px 20px; 
            border-radius: 25px; 
            font-size: clamp(0.9rem, 3vw, 1rem);
            font-weight: bold;
            cursor: pointer; 
            transition: all 0.2s ease;
            touch-action: manipulation;
            min-width: 100px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        
        .btn:hover, .btn:active {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }
        
        .score { 
            font-size: clamp(1rem, 4vw, 1.2rem);
            margin: 15px 0; 
            display: flex;
            justify-content: space-around;
            background: rgba(255,255,255,0.1);
            padding: 10px;
            border-radius: 15px;
        }
        
        .score div {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        .score span {
            font-weight: bold;
            font-size: 1.2em;
            margin-top: 5px;
        }
        
        #message {
            margin-top: 20px;
            padding: 15px;
            border-radius: 15px;
            background: rgba(255,255,255,0.1);
            font-size: clamp(1rem, 4vw, 1.2rem);
        }
        
        /* Mobile-specific optimizations */
        @media (max-width: 480px) {
            .game-container {
                padding: 10px;
                margin: 5px;
            }
            
            .puzzle-grid {
                gap: 2px;
                padding: 8px;
            }
            
            .tile {
                min-height: 50px;
            }
            
            .controls {
                flex-direction: column;
                align-items: center;
            }
            
            .btn {
                width: 80%;
                max-width: 200px;
            }
        }
        
        /* Landscape mobile optimization */
        @media (max-height: 600px) and (orientation: landscape) {
            body {
                padding: 5px;
            }
            
            .game-container {
                max-width: 90vw;
                padding: 10px;
            }
            
            h1 {
                font-size: 1.5rem;
                margin: 5px 0;
            }
            
            .puzzle-grid {
                max-width: 250px;
                margin: 10px auto;
            }
        }
    </style>
</head>
<body>
    <div class="game-container">
        <h1>{{GAME_TITLE}}</h1>
        <p>{{GAME_DESCRIPTION}}</p>
        
        <div class="score">
            <div>
                <span>Moves</span>
                <span id="moves">0</span>
            </div>
            <div>
                <span>Time</span>
                <span id="time">00:00</span>
            </div>
        </div>
        
        <div class="puzzle-grid" id="puzzle-grid"></div>
        
        <div class="controls">
            <button class="btn" onclick="shufflePuzzle()">🎲 New Game</button>
            <button class="btn" onclick="solvePuzzle()">✨ Solve</button>
        </div>
        
        <div id="message"></div>
    </div>
    
    <script>
        let tiles = [];
        let emptyIndex = 15;
        let moves = 0;
        let startTime = Date.now();
        let gameWon = false;
        let touchStartX = 0;
        let touchStartY = 0;
        
        function initPuzzle() {
            tiles = Array.from({length: 16}, (_, i) => i === 15 ? 0 : i + 1);
            emptyIndex = 15;
            moves = 0;
            startTime = Date.now();
            gameWon = false;
            updateDisplay();
            updateTimer();
        }
        
        function updateDisplay() {
            const grid = document.getElementById('puzzle-grid');
            grid.innerHTML = '';
            
            tiles.forEach((tile, index) => {
                const button = document.createElement('button');
                button.className = tile === 0 ? 'tile empty' : 'tile';
                button.textContent = tile === 0 ? '' : tile;
                
                // Add both click and touch event listeners
                button.onclick = () => moveTile(index);
                
                // Touch events for better mobile experience
                button.addEventListener('touchstart', (e) => {
                    e.preventDefault();
                    touchStartX = e.touches[0].clientX;
                    touchStartY = e.touches[0].clientY;
                    button.style.transform = 'scale(0.95)';
                }, {passive: false});
                
                button.addEventListener('touchend', (e) => {
                    e.preventDefault();
                    button.style.transform = '';
                    moveTile(index);
                }, {passive: false});
                
                button.addEventListener('touchmove', (e) => {
                    e.preventDefault();
                }, {passive: false});
                
                grid.appendChild(button);
            });
            
            document.getElementById('moves').textContent = moves;
        }
        
        function moveTile(index) {
            if (gameWon) return;
            
            const row = Math.floor(index / 4);
            const col = index % 4;
            const emptyRow = Math.floor(emptyIndex / 4);
            const emptyCol = emptyIndex % 4;
            
            if ((Math.abs(row - emptyRow) === 1 && col === emptyCol) || 
                (Math.abs(col - emptyCol) === 1 && row === emptyRow)) {
                
                [tiles[index], tiles[emptyIndex]] = [tiles[emptyIndex], tiles[index]];
                emptyIndex = index;
                moves++;
                
                // Haptic feedback for mobile devices
                if (navigator.vibrate) {
                    navigator.vibrate(50);
                }
                
                updateDisplay();
                checkWin();
            }
        }
        
        function checkWin() {
            const solved = tiles.slice(0, 15).every((tile, index) => tile === index + 1) && tiles[15] === 0;
            if (solved) {
                gameWon = true;
                const time = Math.floor((Date.now() - startTime) / 1000);
                
                // Celebration haptic feedback
                if (navigator.vibrate) {
                    navigator.vibrate([100, 50, 100, 50, 200]);
                }
                
                document.getElementById('message').innerHTML = 
                    `<h2>🎉 Congratulations!</h2><p>Solved in ${moves} moves and ${time} seconds!</p>`;
            }
        }
        
        function shufflePuzzle() {
            for (let i = 0; i < 1000; i++) {
                const validMoves = getValidMoves();
                const randomMove = validMoves[Math.floor(Math.random() * validMoves.length)];
                moveTileForShuffle(randomMove);
            }
            moves = 0;
            startTime = Date.now();
            gameWon = false;
            updateDisplay();
            document.getElementById('message').innerHTML = '';
        }
        
        function getValidMoves() {
            const moves = [];
            const row = Math.floor(emptyIndex / 4);
            const col = emptyIndex % 4;
            
            if (row > 0) moves.push(emptyIndex - 4);
            if (row < 3) moves.push(emptyIndex + 4);
            if (col > 0) moves.push(emptyIndex - 1);
            if (col < 3) moves.push(emptyIndex + 1);
            
            return moves;
        }
        
        function moveTileForShuffle(index) {
            [tiles[index], tiles[emptyIndex]] = [tiles[emptyIndex], tiles[index]];
            emptyIndex = index;
        }
        
        function solvePuzzle() {
            tiles = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0];
            emptyIndex = 15;
            updateDisplay();
            checkWin();
        }
        
        function updateTimer() {
            if (!gameWon) {
                const elapsed = Math.floor((Date.now() - startTime) / 1000);
                const minutes = Math.floor(elapsed / 60).toString().padStart(2, '0');
                const seconds = (elapsed % 60).toString().padStart(2, '0');
                document.getElementById('time').textContent = `${minutes}:${seconds}`;
                setTimeout(updateTimer, 1000);
            }
        }
        
        // Prevent zoom on double tap
        let lastTouchEnd = 0;
        document.addEventListener('touchend', function (event) {
            const now = (new Date()).getTime();
            if (now - lastTouchEnd <= 300) {
                event.preventDefault();
            }
            lastTouchEnd = now;
        }, false);
        
        // Prevent context menu on long press
        document.addEventListener('contextmenu', function(e) {
            e.preventDefault();
        });
        
        // Initialize game
        initPuzzle();
        shufflePuzzle();
    </script>
</body>
</html>'''
        
        return {
            'html': html,
            'css': '',
            'javascript': ''
        }
    
    def get_shooter_template(self) -> Dict[str, str]:
        """Get mobile-optimized space shooter game template"""
        
        html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>{{GAME_TITLE}}</title>
    <style>
        * {
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
            -webkit-touch-callout: none;
            -webkit-user-select: none;
            user-select: none;
        }
        
        body { 
            margin: 0; 
            padding: 0; 
            background: #000; 
            color: white; 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            overflow: hidden; 
            display: flex;
            flex-direction: column;
            height: 100vh;
        }
        
        canvas { 
            display: block; 
            margin: 0 auto; 
            background: linear-gradient(180deg, #000428 0%, #004e92 100%); 
            touch-action: none;
            max-width: 100vw;
            max-height: 70vh;
        }
        
        .ui { 
            position: absolute; 
            top: 10px; 
            left: 10px; 
            font-size: clamp(1rem, 4vw, 1.2rem);
            z-index: 10;
            background: rgba(0,0,0,0.5);
            padding: 10px;
            border-radius: 10px;
        }
        
        .mobile-controls {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            height: 120px;
            background: rgba(0,0,0,0.8);
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 20px;
            z-index: 20;
        }
        
        .control-pad {
            width: 80px;
            height: 80px;
            border: 2px solid #fff;
            border-radius: 50%;
            background: rgba(255,255,255,0.1);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            touch-action: manipulation;
            user-select: none;
        }
        
        .control-pad:active {
            background: rgba(255,255,255,0.3);
            transform: scale(0.95);
        }
        
        .shoot-btn {
            width: 80px;
            height: 80px;
            border: 2px solid #ff4444;
            border-radius: 50%;
            background: rgba(255,68,68,0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            touch-action: manipulation;
            user-select: none;
        }
        
        .shoot-btn:active {
            background: rgba(255,68,68,0.5);
            transform: scale(0.95);
        }
        
        .desktop-controls {
            position: absolute;
            bottom: 10px;
            left: 50%;
            transform: translateX(-50%);
            text-align: center;
            font-size: 0.9rem;
            opacity: 0.7;
        }
        
        @media (max-width: 768px) {
            .desktop-controls {
                display: none;
            }
        }
        
        @media (min-width: 769px) {
            .mobile-controls {
                display: none;
            }
        }
    </style>
</head>
<body>
    <div class="ui">
        <div>Score: <span id="score">0</span></div>
        <div>Lives: <span id="lives">3</span></div>
    </div>
    
    <canvas id="gameCanvas"></canvas>
    
    <div class="mobile-controls">
        <div class="control-pad" id="leftBtn">←</div>
        <div class="control-pad" id="upBtn">↑</div>
        <div class="control-pad" id="downBtn">↓</div>
        <div class="control-pad" id="rightBtn">→</div>
        <div class="shoot-btn" id="shootBtn">🚀</div>
    </div>
    
    <div class="desktop-controls">
        <p>Desktop: Arrow Keys to Move | Spacebar to Shoot</p>
    </div>
    
    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        
        // Responsive canvas sizing
        function resizeCanvas() {
            const maxWidth = window.innerWidth;
            const maxHeight = window.innerHeight - (window.innerWidth <= 768 ? 120 : 0);
            
            canvas.width = Math.min(800, maxWidth);
            canvas.height = Math.min(600, maxHeight);
        }
        
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);
        
        // Game state
        let score = 0;
        let lives = 3;
        let gameRunning = true;
        
        // Player
        const player = {
            x: canvas.width / 2 - 25,
            y: canvas.height - 60,
            width: 50,
            height: 30,
            speed: 5
        };
        
        // Arrays for game objects
        let bullets = [];
        let enemies = [];
        let particles = [];
        
        // Input handling
        const keys = {};
        const mobileControls = {
            left: false,
            right: false,
            up: false,
            down: false,
            shoot: false
        };
        
        // Desktop controls
        document.addEventListener('keydown', (e) => {
            keys[e.code] = true;
            if (e.code === 'Space') {
                e.preventDefault();
                shoot();
            }
        });
        
        document.addEventListener('keyup', (e) => {
            keys[e.code] = false;
        });
        
        // Mobile controls
        const leftBtn = document.getElementById('leftBtn');
        const rightBtn = document.getElementById('rightBtn');
        const upBtn = document.getElementById('upBtn');
        const downBtn = document.getElementById('downBtn');
        const shootBtn = document.getElementById('shootBtn');
        
        // Touch event handlers
        function addTouchEvents(element, control) {
            element.addEventListener('touchstart', (e) => {
                e.preventDefault();
                mobileControls[control] = true;
                if (control === 'shoot') shoot();
            }, {passive: false});
            
            element.addEventListener('touchend', (e) => {
                e.preventDefault();
                mobileControls[control] = false;
            }, {passive: false});
        }
        
        addTouchEvents(leftBtn, 'left');
        addTouchEvents(rightBtn, 'right');
        addTouchEvents(upBtn, 'up');
        addTouchEvents(downBtn, 'down');
        addTouchEvents(shootBtn, 'shoot');
        
        // Continuous shooting for mobile
        let shootInterval;
        shootBtn.addEventListener('touchstart', (e) => {
            e.preventDefault();
            shoot();
            shootInterval = setInterval(shoot, 200);
        }, {passive: false});
        
        shootBtn.addEventListener('touchend', (e) => {
            e.preventDefault();
            clearInterval(shootInterval);
        }, {passive: false});
        
        function shoot() {
            if (!gameRunning) return;
            
            bullets.push({
                x: player.x + player.width / 2 - 2,
                y: player.y,
                width: 4,
                height: 10,
                speed: 7
            });
            
            // Haptic feedback
            if (navigator.vibrate) {
                navigator.vibrate(30);
            }
        }
        
        function spawnEnemy() {
            enemies.push({
                x: Math.random() * (canvas.width - 40),
                y: -40,
                width: 40,
                height: 30,
                speed: 2 + Math.random() * 2
            });
        }
        
        function update() {
            if (!gameRunning) return;
            
            // Update player position based on canvas size
            player.y = Math.min(player.y, canvas.height - player.height);
            
            // Move player (desktop)
            if (keys['ArrowLeft'] && player.x > 0) {
                player.x -= player.speed;
            }
            if (keys['ArrowRight'] && player.x < canvas.width - player.width) {
                player.x += player.speed;
            }
            if (keys['ArrowUp'] && player.y > 0) {
                player.y -= player.speed;
            }
            if (keys['ArrowDown'] && player.y < canvas.height - player.height) {
                player.y += player.speed;
            }
            
            // Move player (mobile)
            if (mobileControls.left && player.x > 0) {
                player.x -= player.speed;
            }
            if (mobileControls.right && player.x < canvas.width - player.width) {
                player.x += player.speed;
            }
            if (mobileControls.up && player.y > 0) {
                player.y -= player.speed;
            }
            if (mobileControls.down && player.y < canvas.height - player.height) {
                player.y += player.speed;
            }
            
            // Move bullets
            bullets = bullets.filter(bullet => {
                bullet.y -= bullet.speed;
                return bullet.y > -bullet.height;
            });
            
            // Move enemies
            enemies = enemies.filter(enemy => {
                enemy.y += enemy.speed;
                return enemy.y < canvas.height + enemy.height;
            });
            
            // Check bullet-enemy collisions
            bullets.forEach((bullet, bulletIndex) => {
                enemies.forEach((enemy, enemyIndex) => {
                    if (bullet.x < enemy.x + enemy.width &&
                        bullet.x + bullet.width > enemy.x &&
                        bullet.y < enemy.y + enemy.height &&
                        bullet.y + bullet.height > enemy.y) {
                        
                        // Create explosion particles
                        for (let i = 0; i < 5; i++) {
                            particles.push({
                                x: enemy.x + enemy.width / 2,
                                y: enemy.y + enemy.height / 2,
                                vx: (Math.random() - 0.5) * 4,
                                vy: (Math.random() - 0.5) * 4,
                                life: 30
                            });
                        }
                        
                        bullets.splice(bulletIndex, 1);
                        enemies.splice(enemyIndex, 1);
                        score += 10;
                        document.getElementById('score').textContent = score;
                        
                        // Haptic feedback for hit
                        if (navigator.vibrate) {
                            navigator.vibrate(100);
                        }
                    }
                });
            });
            
            // Check player-enemy collisions
            enemies.forEach((enemy, enemyIndex) => {
                if (player.x < enemy.x + enemy.width &&
                    player.x + player.width > enemy.x &&
                    player.y < enemy.y + enemy.height &&
                    player.y + player.height > enemy.y) {
                    
                    enemies.splice(enemyIndex, 1);
                    lives--;
                    document.getElementById('lives').textContent = lives;
                    
                    // Strong haptic feedback for damage
                    if (navigator.vibrate) {
                        navigator.vibrate([200, 100, 200]);
                    }
                    
                    if (lives <= 0) {
                        gameRunning = false;
                        setTimeout(() => {
                            alert(`Game Over! Final Score: ${score}\\nTap to restart`);
                            location.reload();
                        }, 500);
                    }
                }
            });
            
            // Update particles
            particles = particles.filter(particle => {
                particle.x += particle.vx;
                particle.y += particle.vy;
                particle.life--;
                return particle.life > 0;
            });
            
            // Spawn enemies
            if (Math.random() < 0.02) {
                spawnEnemy();
            }
        }
        
        function draw() {
            // Clear canvas
            ctx.fillStyle = 'rgba(0, 4, 40, 0.1)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Draw stars
            ctx.fillStyle = 'white';
            for (let i = 0; i < 100; i++) {
                const x = (i * 37) % canvas.width;
                const y = (i * 73 + Date.now() * 0.1) % canvas.height;
                ctx.fillRect(x, y, 1, 1);
            }
            
            // Draw player
            ctx.fillStyle = '#00ff00';
            ctx.fillRect(player.x, player.y, player.width, player.height);
            
            // Draw bullets
            ctx.fillStyle = '#ffff00';
            bullets.forEach(bullet => {
                ctx.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
            });
            
            // Draw enemies
            ctx.fillStyle = '#ff0000';
            enemies.forEach(enemy => {
                ctx.fillRect(enemy.x, enemy.y, enemy.width, enemy.height);
            });
            
            // Draw particles
            ctx.fillStyle = '#ff8800';
            particles.forEach(particle => {
                ctx.globalAlpha = particle.life / 30;
                ctx.fillRect(particle.x, particle.y, 3, 3);
                ctx.globalAlpha = 1;
            });
        }
        
        function gameLoop() {
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }
        
        // Prevent scrolling on mobile
        document.addEventListener('touchmove', (e) => {
            e.preventDefault();
        }, {passive: false});
        
        // Start game
        gameLoop();
    </script>
</body>
</html>'''
        
        return {
            'html': html,
            'css': '',
            'javascript': ''
        }
    
    def get_platformer_template(self) -> Dict[str, str]:
        """Get mobile-optimized platformer game template"""
        return self.get_puzzle_template()  # Use puzzle template for now
    
    def get_rpg_template(self) -> Dict[str, str]:
        """Get mobile-optimized RPG game template"""
        return self.get_puzzle_template()  # Use puzzle template for now
    
    def get_racing_template(self) -> Dict[str, str]:
        """Get mobile-optimized racing game template"""
        return self.get_puzzle_template()  # Use puzzle template for now
    
    def get_strategy_template(self) -> Dict[str, str]:
        """Get mobile-optimized strategy game template"""
        return self.get_puzzle_template()  # Use puzzle template for now

# Global instance
game_engine = GameEngine()
