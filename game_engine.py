#!/usr/bin/env python3
"""
🎮 MODULAR GAME ENGINE - GENRE EXPANSION SYSTEM
Advanced AI-Powered Game Generation with Unique Mechanics Per Genre
"""

import os
import json
import random
import hashlib
import requests
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any

class UnifiedPromptParser:
    """Centralized genre detection using keyword heuristics + LLM fallback"""
    
    def __init__(self, groq_api_key: Optional[str] = None):
        self.groq_api_key = groq_api_key
        
        # Genre keyword mappings with confidence scores
        self.genre_keywords = {
            'puzzle': {
                'primary': ['puzzle', 'solve', 'brain', 'logic', 'think', 'mind', 'challenge', 'riddle', 'match', 'connect'],
                'secondary': ['smart', 'clever', 'intellectual', 'problem', 'solution', 'strategy'],
                'weight': 1.0
            },
            'shooter': {
                'primary': ['shoot', 'gun', 'bullet', 'enemy', 'space', 'alien', 'laser', 'fire', 'combat', 'war'],
                'secondary': ['battle', 'fight', 'attack', 'defend', 'weapon', 'target', 'destroy'],
                'weight': 1.0
            },
            'platformer': {
                'primary': ['jump', 'platform', 'run', 'climb', 'collect', 'mario', 'side-scroll', 'adventure'],
                'secondary': ['hop', 'leap', 'move', 'explore', 'quest', 'journey', 'coins'],
                'weight': 1.0
            },
            'racing': {
                'primary': ['race', 'car', 'speed', 'fast', 'drive', 'racing', 'vehicle', 'track', 'lap'],
                'secondary': ['motor', 'engine', 'wheel', 'road', 'highway', 'finish', 'winner'],
                'weight': 1.0
            },
            'rpg': {
                'primary': ['rpg', 'adventure', 'quest', 'hero', 'magic', 'sword', 'level', 'character', 'story'],
                'secondary': ['fantasy', 'dragon', 'wizard', 'knight', 'dungeon', 'treasure', 'experience'],
                'weight': 1.0
            },
            'strategy': {
                'primary': ['strategy', 'build', 'manage', 'city', 'empire', 'resource', 'plan', 'tactical'],
                'secondary': ['construct', 'develop', 'economy', 'civilization', 'kingdom', 'army', 'base'],
                'weight': 1.0
            }
        }
    
    def analyze_prompt(self, description: str) -> Dict[str, Any]:
        """Analyze prompt and determine genre with confidence scores"""
        description_lower = description.lower()
        genre_scores = {}
        
        # Calculate keyword-based scores
        for genre, keywords in self.genre_keywords.items():
            score = 0
            
            # Primary keywords (higher weight)
            for keyword in keywords['primary']:
                if keyword in description_lower:
                    score += 2.0
            
            # Secondary keywords (lower weight)
            for keyword in keywords['secondary']:
                if keyword in description_lower:
                    score += 1.0
            
            # Apply genre weight
            score *= keywords['weight']
            genre_scores[genre] = score
        
        # Find best match
        best_genre = max(genre_scores, key=genre_scores.get) if genre_scores else 'puzzle'
        confidence = genre_scores.get(best_genre, 0) / 10.0  # Normalize to 0-1
        
        # Use LLM fallback for low confidence or ambiguous cases
        if confidence < 0.3 and self.groq_api_key:
            llm_result = self._llm_genre_detection(description)
            if llm_result:
                best_genre = llm_result.get('genre', best_genre)
                confidence = max(confidence, 0.7)  # Boost confidence for LLM results
        
        return {
            'genre': best_genre,
            'confidence': min(confidence, 1.0),
            'scores': genre_scores,
            'method': 'llm' if confidence >= 0.7 and self.groq_api_key else 'keywords'
        }
    
    def _llm_genre_detection(self, description: str) -> Optional[Dict[str, Any]]:
        """Use LLM for precise genre detection"""
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    'Authorization': f'Bearer {self.groq_api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'llama3-8b-8192',
                    'messages': [
                        {
                            'role': 'system',
                            'content': 'You are a game genre classifier. Respond with ONLY one word from: puzzle, shooter, platformer, racing, rpg, strategy. Choose the best fit for the game description.'
                        },
                        {
                            'role': 'user',
                            'content': f'Classify this game: {description}'
                        }
                    ],
                    'max_tokens': 10,
                    'temperature': 0.1
                },
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                genre = result['choices'][0]['message']['content'].strip().lower()
                
                # Validate genre
                if genre in self.genre_keywords:
                    return {'genre': genre}
            
        except Exception as e:
            print(f"LLM genre detection error: {e}")
        
        return None

class GameSeedGenerator:
    """Generate unique seeds and configurations for game variance"""
    
    @staticmethod
    def generate_seed(description: str, genre: str) -> str:
        """Generate unique seed based on description and timestamp"""
        timestamp = str(datetime.now().timestamp())
        content = f"{description}_{genre}_{timestamp}"
        return hashlib.md5(content.encode()).hexdigest()[:8]
    
    @staticmethod
    def generate_config(seed: str, genre: str) -> Dict[str, Any]:
        """Generate genre-specific configuration based on seed"""
        random.seed(seed)
        
        base_config = {
            'seed': seed,
            'genre': genre,
            'difficulty': random.choice(['easy', 'medium', 'hard']),
            'theme_variant': random.randint(1, 5),
            'color_scheme': random.choice(['blue', 'red', 'green', 'purple', 'orange']),
            'animation_speed': random.uniform(0.8, 1.2),
            'sound_theme': random.choice(['classic', 'modern', 'retro', 'ambient'])
        }
        
        # Genre-specific configurations
        if genre == 'puzzle':
            base_config.update({
                'grid_size': random.choice([3, 4, 5]),
                'tile_style': random.choice(['numbers', 'colors', 'patterns']),
                'shuffle_complexity': random.randint(50, 200)
            })
        elif genre == 'shooter':
            base_config.update({
                'enemy_types': random.randint(2, 4),
                'bullet_speed': random.uniform(5, 10),
                'spawn_rate': random.uniform(0.5, 2.0),
                'power_ups': random.choice([True, False])
            })
        elif genre == 'platformer':
            base_config.update({
                'platform_count': random.randint(5, 12),
                'jump_height': random.uniform(80, 120),
                'gravity': random.uniform(0.5, 1.0),
                'collectibles': random.randint(10, 30)
            })
        elif genre == 'racing':
            base_config.update({
                'track_length': random.randint(800, 1500),
                'opponent_count': random.randint(2, 5),
                'max_speed': random.uniform(8, 15),
                'track_complexity': random.choice(['simple', 'curves', 'obstacles'])
            })
        elif genre == 'rpg':
            base_config.update({
                'character_class': random.choice(['warrior', 'mage', 'rogue', 'archer']),
                'starting_level': random.randint(1, 3),
                'enemy_variety': random.randint(3, 6),
                'loot_rarity': random.choice(['common', 'rare', 'epic'])
            })
        elif genre == 'strategy':
            base_config.update({
                'map_size': random.choice(['small', 'medium', 'large']),
                'resource_types': random.randint(2, 4),
                'building_variety': random.randint(4, 8),
                'ai_difficulty': random.choice(['passive', 'normal', 'aggressive'])
            })
        
        return base_config

class GenreAssetThemer:
    """Generate genre-specific visual and audio themes"""
    
    @staticmethod
    def get_color_palette(genre: str, variant: int = 1) -> Dict[str, str]:
        """Get genre-specific color palettes"""
        palettes = {
            'puzzle': [
                {'primary': '#4A90E2', 'secondary': '#7ED321', 'accent': '#F5A623', 'background': '#F8F9FA'},
                {'primary': '#9013FE', 'secondary': '#E91E63', 'accent': '#FF9800', 'background': '#FAFAFA'},
                {'primary': '#00BCD4', 'secondary': '#4CAF50', 'accent': '#FFC107', 'background': '#F5F5F5'}
            ],
            'shooter': [
                {'primary': '#FF4444', 'secondary': '#000000', 'accent': '#FFFF00', 'background': '#0D1B2A'},
                {'primary': '#00FF00', 'secondary': '#333333', 'accent': '#FF6600', 'background': '#1A1A2E'},
                {'primary': '#FF0080', 'secondary': '#0080FF', 'accent': '#FFFFFF', 'background': '#16213E'}
            ],
            'platformer': [
                {'primary': '#4CAF50', 'secondary': '#2196F3', 'accent': '#FFC107', 'background': '#87CEEB'},
                {'primary': '#FF5722', 'secondary': '#795548', 'accent': '#FFEB3B', 'background': '#E3F2FD'},
                {'primary': '#9C27B0', 'secondary': '#3F51B5', 'accent': '#FF9800', 'background': '#F3E5F5'}
            ],
            'racing': [
                {'primary': '#F44336', 'secondary': '#212121', 'accent': '#FFEB3B', 'background': '#424242'},
                {'primary': '#2196F3', 'secondary': '#FFFFFF', 'accent': '#FF5722', 'background': '#ECEFF1'},
                {'primary': '#4CAF50', 'secondary': '#000000', 'accent': '#FFC107', 'background': '#1B5E20'}
            ],
            'rpg': [
                {'primary': '#8B4513', 'secondary': '#DAA520', 'accent': '#DC143C', 'background': '#2F4F4F'},
                {'primary': '#4B0082', 'secondary': '#FFD700', 'accent': '#FF69B4', 'background': '#191970'},
                {'primary': '#006400', 'secondary': '#8B4513', 'accent': '#FF4500', 'background': '#228B22'}
            ],
            'strategy': [
                {'primary': '#708090', 'secondary': '#4682B4', 'accent': '#DAA520', 'background': '#F5F5DC'},
                {'primary': '#8B0000', 'secondary': '#B8860B', 'accent': '#FFD700', 'background': '#FFFACD'},
                {'primary': '#2F4F4F', 'secondary': '#5F9EA0', 'accent': '#FF6347', 'background': '#F0F8FF'}
            ]
        }
        
        genre_palettes = palettes.get(genre, palettes['puzzle'])
        return genre_palettes[(variant - 1) % len(genre_palettes)]
    
    @staticmethod
    def get_font_theme(genre: str) -> Dict[str, str]:
        """Get genre-appropriate font styling"""
        themes = {
            'puzzle': {
                'family': 'Arial, sans-serif',
                'title_size': '24px',
                'body_size': '16px',
                'weight': 'normal',
                'style': 'clean'
            },
            'shooter': {
                'family': 'Impact, Arial Black, sans-serif',
                'title_size': '28px',
                'body_size': '14px',
                'weight': 'bold',
                'style': 'aggressive'
            },
            'platformer': {
                'family': 'Comic Sans MS, cursive',
                'title_size': '26px',
                'body_size': '15px',
                'weight': 'normal',
                'style': 'playful'
            },
            'racing': {
                'family': 'Tahoma, sans-serif',
                'title_size': '30px',
                'body_size': '16px',
                'weight': 'bold',
                'style': 'dynamic'
            },
            'rpg': {
                'family': 'Georgia, serif',
                'title_size': '25px',
                'body_size': '15px',
                'weight': 'normal',
                'style': 'fantasy'
            },
            'strategy': {
                'family': 'Verdana, sans-serif',
                'title_size': '22px',
                'body_size': '14px',
                'weight': 'normal',
                'style': 'professional'
            }
        }
        
        return themes.get(genre, themes['puzzle'])
    
    @staticmethod
    def get_visual_effects(genre: str) -> Dict[str, Any]:
        """Get genre-specific visual effects and animations"""
        effects = {
            'puzzle': {
                'transitions': 'smooth',
                'hover_effect': 'scale(1.05)',
                'particle_system': False,
                'glow_effects': False,
                'animation_style': 'ease-in-out'
            },
            'shooter': {
                'transitions': 'fast',
                'hover_effect': 'brightness(1.2)',
                'particle_system': True,
                'glow_effects': True,
                'animation_style': 'linear'
            },
            'platformer': {
                'transitions': 'bouncy',
                'hover_effect': 'translateY(-3px)',
                'particle_system': True,
                'glow_effects': False,
                'animation_style': 'ease-out'
            },
            'racing': {
                'transitions': 'fast',
                'hover_effect': 'skew(-5deg)',
                'particle_system': True,
                'glow_effects': True,
                'animation_style': 'ease-in'
            },
            'rpg': {
                'transitions': 'slow',
                'hover_effect': 'drop-shadow(0 0 10px gold)',
                'particle_system': True,
                'glow_effects': True,
                'animation_style': 'ease-in-out'
            },
            'strategy': {
                'transitions': 'precise',
                'hover_effect': 'border-glow',
                'particle_system': False,
                'glow_effects': False,
                'animation_style': 'linear'
            }
        }
        
        return effects.get(genre, effects['puzzle'])

class ModularGameEngine:
    """Main engine coordinating all game generation modules"""
    
    def __init__(self, groq_api_key: Optional[str] = None):
        self.parser = UnifiedPromptParser(groq_api_key)
        self.seed_generator = GameSeedGenerator()
        self.asset_themer = GenreAssetThemer()
        self.groq_api_key = groq_api_key
        
        # Import genre modules
        from .genres import (
            PuzzleModule, ShooterModule, PlatformerModule,
            RacingModule, RPGModule, StrategyModule
        )
        
        self.genre_modules = {
            'puzzle': PuzzleModule(),
            'shooter': ShooterModule(),
            'platformer': PlatformerModule(),
            'racing': RacingModule(),
            'rpg': RPGModule(),
            'strategy': StrategyModule()
        }
    
    def generate_game(self, description: str, session_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Main game generation pipeline"""
        try:
            # Step 1: Parse prompt and determine genre
            analysis = self.parser.analyze_prompt(description)
            genre = analysis['genre']
            
            # Step 2: Generate unique seed and configuration
            seed = self.seed_generator.generate_seed(description, genre)
            config = self.seed_generator.generate_config(seed, genre)
            
            # Step 3: Get genre-specific assets and themes
            color_palette = self.asset_themer.get_color_palette(genre, config['theme_variant'])
            font_theme = self.asset_themer.get_font_theme(genre)
            visual_effects = self.asset_themer.get_visual_effects(genre)
            
            # Step 4: Generate AI-powered title and description
            ai_content = self._generate_ai_content(description, genre, config)
            
            # Step 5: Apply session awareness (if available)
            if session_data:
                config = self._apply_session_preferences(config, session_data)
            
            # Step 6: Generate game using appropriate module
            game_module = self.genre_modules.get(genre)
            if not game_module:
                # Fallback with dynamic adaptation
                game_code = self._generate_adaptive_fallback(description, genre, config)
            else:
                game_code = game_module.generate(config, color_palette, font_theme, visual_effects)
            
            # Step 7: Compile final result
            return {
                'success': True,
                'title': ai_content['title'],
                'description': ai_content['description'],
                'genre': genre,
                'seed': seed,
                'config': config,
                'code': game_code,
                'analysis': analysis,
                'themes': {
                    'colors': color_palette,
                    'fonts': font_theme,
                    'effects': visual_effects
                }
            }
            
        except Exception as e:
            print(f"Game generation error: {e}")
            return {
                'success': False,
                'error': str(e),
                'fallback': self._generate_emergency_fallback(description)
            }
    
    def _generate_ai_content(self, description: str, genre: str, config: Dict) -> Dict[str, str]:
        """Generate AI-powered title and description"""
        if not self.groq_api_key:
            return self._generate_fallback_content(description, genre)
        
        try:
            # Generate title
            title_response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    'Authorization': f'Bearer {self.groq_api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'llama3-8b-8192',
                    'messages': [
                        {
                            'role': 'system',
                            'content': f'Create a catchy {genre} game title. Respond with ONLY the title, no quotes or extra text. Make it exciting and memorable.'
                        },
                        {
                            'role': 'user',
                            'content': f'Game concept: {description}'
                        }
                    ],
                    'max_tokens': 20,
                    'temperature': 0.8
                },
                timeout=5
            )
            
            # Generate description
            desc_response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    'Authorization': f'Bearer {self.groq_api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'llama3-8b-8192',
                    'messages': [
                        {
                            'role': 'system',
                            'content': f'Write a brief, exciting description for a {genre} game. Keep it under 100 characters. Make it sound fun and engaging.'
                        },
                        {
                            'role': 'user',
                            'content': f'Game concept: {description}'
                        }
                    ],
                    'max_tokens': 50,
                    'temperature': 0.7
                },
                timeout=5
            )
            
            title = "Untitled Game"
            description_text = "An exciting game experience!"
            
            if title_response.status_code == 200:
                title_result = title_response.json()
                title = self._clean_ai_response(title_result['choices'][0]['message']['content'])
            
            if desc_response.status_code == 200:
                desc_result = desc_response.json()
                description_text = self._clean_ai_response(desc_result['choices'][0]['message']['content'])
            
            return {
                'title': title,
                'description': description_text
            }
            
        except Exception as e:
            print(f"AI content generation error: {e}")
            return self._generate_fallback_content(description, genre)
    
    def _clean_ai_response(self, response: str) -> str:
        """Clean AI response text"""
        # Remove quotes, numbering, and extra formatting
        cleaned = response.strip()
        cleaned = cleaned.strip('"\'')
        cleaned = cleaned.split('\n')[0]  # Take first line only
        
        # Remove common prefixes
        prefixes = ['1. ', '2. ', '3. ', 'Title: ', 'Game: ', 'Here are', 'Option']
        for prefix in prefixes:
            if cleaned.startswith(prefix):
                cleaned = cleaned[len(prefix):].strip()
        
        # Ensure reasonable length
        if len(cleaned) > 50:
            cleaned = cleaned[:47] + "..."
        
        return cleaned if cleaned else "Untitled Game"
    
    def _generate_fallback_content(self, description: str, genre: str) -> Dict[str, str]:
        """Generate fallback content when AI is unavailable"""
        genre_titles = {
            'puzzle': ['Brain Teaser', 'Mind Bender', 'Logic Master', 'Puzzle Pro', 'Think Fast'],
            'shooter': ['Space Blaster', 'Alien Hunter', 'Cosmic War', 'Star Fighter', 'Galaxy Defender'],
            'platformer': ['Jump Quest', 'Platform Hero', 'Leap Adventure', 'Sky Runner', 'Coin Collector'],
            'racing': ['Speed Demon', 'Fast Track', 'Racing Thunder', 'Turbo Rush', 'Speed King'],
            'rpg': ['Epic Quest', 'Hero\'s Journey', 'Magic Adventure', 'Dragon Slayer', 'Fantasy World'],
            'strategy': ['Empire Builder', 'City Master', 'Strategic Mind', 'Kingdom Manager', 'Base Commander']
        }
        
        genre_descriptions = {
            'puzzle': 'Challenge your mind with this engaging puzzle game!',
            'shooter': 'Blast your way through waves of enemies in space!',
            'platformer': 'Jump and run through exciting platform adventures!',
            'racing': 'Race at high speeds and beat your opponents!',
            'rpg': 'Embark on an epic adventure in a fantasy world!',
            'strategy': 'Build and manage your empire to victory!'
        }
        
        titles = genre_titles.get(genre, genre_titles['puzzle'])
        descriptions = genre_descriptions.get(genre, genre_descriptions['puzzle'])
        
        return {
            'title': random.choice(titles),
            'description': descriptions
        }
    
    def _apply_session_preferences(self, config: Dict, session_data: Dict) -> Dict:
        """Apply user session preferences to game configuration"""
        # Apply preferred difficulty
        if 'preferred_difficulty' in session_data:
            config['difficulty'] = session_data['preferred_difficulty']
        
        # Apply preferred color scheme
        if 'preferred_colors' in session_data:
            config['color_scheme'] = session_data['preferred_colors']
        
        # Apply accessibility settings
        if 'accessibility' in session_data:
            accessibility = session_data['accessibility']
            if accessibility.get('high_contrast'):
                config['color_scheme'] = 'high_contrast'
            if accessibility.get('large_text'):
                config['font_size_multiplier'] = 1.5
        
        return config
    
    def _generate_adaptive_fallback(self, description: str, genre: str, config: Dict) -> str:
        """Generate adaptive fallback for unimplemented genres"""
        # This creates a basic game template that adapts to the requested genre
        # Instead of always showing a puzzle, it adapts layout and style
        
        color_palette = self.asset_themer.get_color_palette(genre, config['theme_variant'])
        font_theme = self.asset_themer.get_font_theme(genre)
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Adaptive {genre.title()} Game</title>
            <style>
                body {{
                    font-family: {font_theme['family']};
                    background: linear-gradient(135deg, {color_palette['primary']}, {color_palette['secondary']});
                    color: white;
                    margin: 0;
                    padding: 20px;
                    min-height: 100vh;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                }}
                .game-container {{
                    background: rgba(255,255,255,0.1);
                    padding: 30px;
                    border-radius: 15px;
                    text-align: center;
                    backdrop-filter: blur(10px);
                }}
                .genre-indicator {{
                    background: {color_palette['accent']};
                    color: black;
                    padding: 10px 20px;
                    border-radius: 25px;
                    font-weight: bold;
                    margin-bottom: 20px;
                    display: inline-block;
                }}
                .coming-soon {{
                    font-size: {font_theme['title_size']};
                    margin: 20px 0;
                }}
                .description {{
                    font-size: {font_theme['body_size']};
                    opacity: 0.9;
                    max-width: 400px;
                    line-height: 1.6;
                }}
            </style>
        </head>
        <body>
            <div class="game-container">
                <div class="genre-indicator">{genre.upper()} GAME</div>
                <div class="coming-soon">Coming Soon!</div>
                <div class="description">
                    This {genre} game is being generated with advanced AI. 
                    The full {genre} experience will be available soon with unique mechanics and gameplay!
                </div>
            </div>
        </body>
        </html>
        """
    
    def _generate_emergency_fallback(self, description: str) -> Dict[str, Any]:
        """Emergency fallback when everything fails"""
        return {
            'success': True,
            'title': 'Simple Game',
            'description': 'A basic game experience',
            'genre': 'puzzle',
            'code': '''
            <!DOCTYPE html>
            <html>
            <head><title>Simple Game</title></head>
            <body style="font-family: Arial; text-align: center; padding: 50px;">
                <h1>Game Created!</h1>
                <p>Your game is being processed. Please try again in a moment.</p>
            </body>
            </html>
            '''
        }

# Main function for external use
def generate_game(description: str, session_data: Optional[Dict] = None) -> Dict[str, Any]:
    """Main entry point for game generation"""
    groq_api_key = os.environ.get('GROQ_API_KEY')
    engine = ModularGameEngine(groq_api_key)
    return engine.generate_game(description, session_data)

# Export main function
__all__ = ['generate_game', 'ModularGameEngine', 'UnifiedPromptParser', 'GameSeedGenerator', 'GenreAssetThemer']
