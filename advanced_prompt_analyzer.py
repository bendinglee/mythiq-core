"""
Advanced Prompt Analyzer - Intelligent Game Mechanics Detection
Revolutionary AI that analyzes user prompts to determine specific game types and mechanics

This module provides:
- Deep analysis of user prompts to extract game mechanics
- Intelligent detection of game types (racing, puzzle, combat, etc.)
- Entity extraction (characters, objects, environments)
- Theme and visual style detection
- Complexity scoring for appropriate game generation
"""

import re
import json
from typing import Dict, List, Any

class AdvancedPromptAnalyzer:
    """Advanced AI system for analyzing user prompts and extracting game mechanics"""
    
    def __init__(self):
        # Game type keywords and patterns
        self.game_type_patterns = {
            'racing': [
                'racing', 'race', 'car', 'vehicle', 'speed', 'track', 'lap', 'driving',
                'motorcycle', 'bike', 'formula', 'circuit', 'speedway', 'drift',
                'acceleration', 'finish line', 'pit stop', 'turbo', 'nitro'
            ],
            'puzzle': [
                'puzzle', 'solve', 'logic', 'brain', 'riddle', 'mystery', 'clue',
                'match', 'pattern', 'sequence', 'sliding', 'jigsaw', 'sudoku',
                'crossword', 'word', 'number', 'tile', 'block', 'piece'
            ],
            'combat': [
                'fight', 'battle', 'combat', 'war', 'attack', 'weapon', 'sword',
                'gun', 'shoot', 'enemy', 'boss', 'health', 'damage', 'armor',
                'shield', 'magic', 'spell', 'warrior', 'knight', 'soldier'
            ],
            'cooking': [
                'cook', 'chef', 'recipe', 'ingredient', 'kitchen', 'restaurant',
                'food', 'meal', 'dish', 'bake', 'fry', 'boil', 'chop', 'mix',
                'serve', 'customer', 'order', 'timer', 'oven', 'stove'
            ],
            'platformer': [
                'jump', 'platform', 'climb', 'run', 'level', 'stage', 'obstacle',
                'coin', 'power-up', 'mario', 'sonic', 'side-scroll', 'gravity',
                'fall', 'ledge', 'gap', 'bounce', 'wall', 'ground'
            ],
            'strategy': [
                'strategy', 'build', 'manage', 'resource', 'army', 'base', 'city',
                'empire', 'civilization', 'turn', 'plan', 'tactical', 'command',
                'troops', 'economy', 'research', 'upgrade', 'territory', 'conquest'
            ],
            'survival': [
                'survive', 'survival', 'craft', 'build', 'hunger', 'thirst', 'health',
                'shelter', 'wilderness', 'island', 'zombie', 'apocalypse', 'resource',
                'gather', 'hunt', 'fish', 'fire', 'tool', 'weapon', 'danger'
            ],
            'adventure': [
                'adventure', 'explore', 'quest', 'journey', 'story', 'character',
                'dialogue', 'choice', 'decision', 'world', 'map', 'treasure',
                'secret', 'discovery', 'travel', 'mission', 'objective', 'rpg'
            ]
        }
        
        # Theme detection patterns
        self.theme_patterns = {
            'fantasy': [
                'magic', 'wizard', 'dragon', 'fairy', 'elf', 'dwarf', 'castle',
                'kingdom', 'enchanted', 'mystical', 'spell', 'potion', 'sword',
                'knight', 'princess', 'forest', 'dungeon', 'crystal', 'rune'
            ],
            'space': [
                'space', 'galaxy', 'planet', 'star', 'alien', 'spaceship', 'rocket',
                'astronaut', 'cosmic', 'universe', 'nebula', 'asteroid', 'laser',
                'robot', 'android', 'station', 'colony', 'mars', 'moon'
            ],
            'underwater': [
                'underwater', 'ocean', 'sea', 'mermaid', 'fish', 'coral', 'reef',
                'submarine', 'deep', 'whale', 'shark', 'treasure', 'pearl',
                'seaweed', 'bubble', 'current', 'tide', 'abyss', 'aquatic'
            ],
            'cyberpunk': [
                'cyberpunk', 'cyber', 'neon', 'digital', 'hacker', 'matrix',
                'virtual', 'android', 'robot', 'ai', 'computer', 'code',
                'network', 'data', 'electric', 'circuit', 'tech', 'future'
            ],
            'steampunk': [
                'steampunk', 'steam', 'gear', 'clockwork', 'mechanical', 'brass',
                'copper', 'airship', 'dirigible', 'goggles', 'inventor', 'machine',
                'engine', 'boiler', 'pipe', 'valve', 'victorian', 'industrial'
            ],
            'horror': [
                'horror', 'scary', 'ghost', 'zombie', 'monster', 'demon', 'evil',
                'dark', 'shadow', 'nightmare', 'haunted', 'creepy', 'blood',
                'death', 'fear', 'terror', 'spine', 'chill', 'macabre'
            ],
            'western': [
                'western', 'cowboy', 'sheriff', 'outlaw', 'desert', 'saloon',
                'horse', 'gun', 'duel', 'frontier', 'ranch', 'cattle', 'gold',
                'mine', 'bandit', 'wagon', 'cactus', 'sunset', 'dust'
            ]
        }
        
        # Entity type patterns
        self.entity_patterns = {
            'characters': [
                'hero', 'player', 'character', 'protagonist', 'warrior', 'mage',
                'archer', 'thief', 'knight', 'princess', 'king', 'queen',
                'wizard', 'witch', 'elf', 'dwarf', 'human', 'alien'
            ],
            'enemies': [
                'enemy', 'monster', 'boss', 'villain', 'demon', 'dragon',
                'zombie', 'ghost', 'robot', 'alien', 'orc', 'goblin',
                'skeleton', 'spider', 'snake', 'wolf', 'bear', 'shark'
            ],
            'objects': [
                'treasure', 'coin', 'gem', 'crystal', 'key', 'sword', 'shield',
                'potion', 'scroll', 'book', 'chest', 'door', 'bridge',
                'ladder', 'rope', 'torch', 'lantern', 'map', 'compass'
            ],
            'environments': [
                'forest', 'castle', 'dungeon', 'cave', 'mountain', 'desert',
                'ocean', 'island', 'city', 'village', 'temple', 'tower',
                'bridge', 'river', 'lake', 'valley', 'hill', 'plain'
            ]
        }
        
        # Action patterns for mechanics detection
        self.action_patterns = {
            'movement': ['run', 'walk', 'jump', 'climb', 'swim', 'fly', 'drive', 'ride'],
            'collection': ['collect', 'gather', 'find', 'pick', 'grab', 'take', 'obtain'],
            'combat': ['fight', 'attack', 'defend', 'shoot', 'hit', 'strike', 'battle'],
            'interaction': ['talk', 'speak', 'use', 'activate', 'open', 'close', 'push'],
            'creation': ['build', 'craft', 'make', 'create', 'construct', 'assemble'],
            'solving': ['solve', 'figure', 'decode', 'unlock', 'discover', 'reveal']
        }
    
    def deep_analyze_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        Perform deep analysis of user prompt to extract all game-relevant information
        
        Args:
            prompt: User's game description
            
        Returns:
            Comprehensive analysis including game type, theme, entities, mechanics, etc.
        """
        prompt_lower = prompt.lower()
        
        analysis = {
            'original_prompt': prompt,
            'game_type': self._detect_game_type(prompt_lower),
            'theme': self._detect_theme(prompt_lower),
            'entities': self._extract_entities(prompt_lower),
            'actions': self._extract_actions(prompt_lower),
            'mechanics': self._determine_mechanics(prompt_lower),
            'complexity_score': self._calculate_complexity(prompt_lower),
            'visual_style': self._determine_visual_style(prompt_lower),
            'win_condition': self._extract_win_condition(prompt_lower),
            'challenge_type': self._determine_challenge_type(prompt_lower)
        }
        
        # Generate enhanced description based on analysis
        analysis['enhanced_description'] = self._generate_enhanced_description(analysis)
        analysis['suggested_title'] = self._generate_title(analysis)
        
        return analysis
    
    def _detect_game_type(self, prompt: str) -> str:
        """Detect the primary game type from the prompt"""
        type_scores = {}
        
        for game_type, keywords in self.game_type_patterns.items():
            score = 0
            for keyword in keywords:
                # Count occurrences with different weights
                if keyword in prompt:
                    score += prompt.count(keyword)
                    # Bonus for exact word matches
                    if f' {keyword} ' in f' {prompt} ':
                        score += 2
            type_scores[game_type] = score
        
        # Special logic for better detection
        if any(word in prompt for word in ['race', 'racing', 'car', 'speed', 'track']):
            type_scores['racing'] = type_scores.get('racing', 0) + 10
        
        if any(word in prompt for word in ['puzzle', 'solve', 'mystery', 'clue']):
            type_scores['puzzle'] = type_scores.get('puzzle', 0) + 10
        
        if any(word in prompt for word in ['fight', 'battle', 'combat', 'weapon']):
            type_scores['combat'] = type_scores.get('combat', 0) + 10
        
        if any(word in prompt for word in ['cook', 'chef', 'recipe', 'kitchen']):
            type_scores['cooking'] = type_scores.get('cooking', 0) + 10
        
        # Return the highest scoring type, default to collection
        if type_scores:
            best_type = max(type_scores, key=type_scores.get)
            if type_scores[best_type] > 0:
                return best_type
        
        return 'collection'  # Default fallback
    
    def _detect_theme(self, prompt: str) -> str:
        """Detect the visual/narrative theme from the prompt"""
        theme_scores = {}
        
        for theme, keywords in self.theme_patterns.items():
            score = 0
            for keyword in keywords:
                if keyword in prompt:
                    score += prompt.count(keyword) * 2
                    # Bonus for exact matches
                    if f' {keyword} ' in f' {prompt} ':
                        score += 3
            theme_scores[theme] = score
        
        # Return highest scoring theme, default to modern
        if theme_scores:
            best_theme = max(theme_scores, key=theme_scores.get)
            if theme_scores[best_theme] > 0:
                return best_theme
        
        return 'modern'
    
    def _extract_entities(self, prompt: str) -> Dict[str, List[str]]:
        """Extract different types of entities mentioned in the prompt"""
        entities = {
            'characters': [],
            'enemies': [],
            'objects': [],
            'environments': []
        }
        
        for entity_type, keywords in self.entity_patterns.items():
            for keyword in keywords:
                if keyword in prompt:
                    entities[entity_type].append(keyword)
        
        # Custom entity extraction based on context
        words = prompt.split()
        for i, word in enumerate(words):
            # Look for character descriptions
            if word in ['hero', 'player', 'character'] and i > 0:
                entities['characters'].append(f"{words[i-1]} {word}")
            
            # Look for object descriptions
            if word in ['crystal', 'gem', 'treasure'] and i > 0:
                entities['objects'].append(f"{words[i-1]} {word}")
        
        return entities
    
    def _extract_actions(self, prompt: str) -> List[str]:
        """Extract action verbs that indicate game mechanics"""
        actions = []
        
        for action_type, keywords in self.action_patterns.items():
            for keyword in keywords:
                if keyword in prompt:
                    actions.append(keyword)
        
        return list(set(actions))  # Remove duplicates
    
    def _determine_mechanics(self, prompt: str) -> List[str]:
        """Determine specific game mechanics based on prompt analysis"""
        mechanics = []
        
        # Movement mechanics
        if any(word in prompt for word in ['run', 'walk', 'move', 'navigate']):
            mechanics.append('movement')
        
        # Collection mechanics
        if any(word in prompt for word in ['collect', 'gather', 'find', 'pick']):
            mechanics.append('collection')
        
        # Combat mechanics
        if any(word in prompt for word in ['fight', 'battle', 'attack', 'defend']):
            mechanics.append('combat')
        
        # Puzzle mechanics
        if any(word in prompt for word in ['solve', 'puzzle', 'mystery', 'clue']):
            mechanics.append('puzzle_solving')
        
        # Racing mechanics
        if any(word in prompt for word in ['race', 'speed', 'fast', 'track']):
            mechanics.append('racing')
        
        # Timing mechanics
        if any(word in prompt for word in ['time', 'timer', 'quick', 'fast']):
            mechanics.append('timing')
        
        # Stealth mechanics
        if any(word in prompt for word in ['sneak', 'hide', 'stealth', 'avoid']):
            mechanics.append('stealth')
        
        return mechanics
    
    def _calculate_complexity(self, prompt: str) -> int:
        """Calculate complexity score (1-10) based on prompt analysis"""
        score = 1
        
        # Length bonus
        word_count = len(prompt.split())
        score += min(word_count // 10, 3)
        
        # Multiple mechanics bonus
        mechanics = self._determine_mechanics(prompt)
        score += len(mechanics)
        
        # Multiple entities bonus
        entities = self._extract_entities(prompt)
        total_entities = sum(len(entity_list) for entity_list in entities.values())
        score += min(total_entities // 3, 2)
        
        # Complex themes bonus
        theme = self._detect_theme(prompt)
        if theme in ['cyberpunk', 'steampunk', 'space']:
            score += 2
        
        return min(score, 10)
    
    def _determine_visual_style(self, prompt: str) -> Dict[str, str]:
        """Determine visual styling based on theme and content"""
        theme = self._detect_theme(prompt)
        
        style_mappings = {
            'fantasy': {
                'color_scheme': 'magical',
                'atmosphere': 'mystical',
                'lighting': 'warm_glow'
            },
            'space': {
                'color_scheme': 'cosmic',
                'atmosphere': 'vast',
                'lighting': 'stark_contrast'
            },
            'underwater': {
                'color_scheme': 'aquatic',
                'atmosphere': 'fluid',
                'lighting': 'filtered_light'
            },
            'cyberpunk': {
                'color_scheme': 'neon',
                'atmosphere': 'gritty',
                'lighting': 'harsh_neon'
            }
        }
        
        return style_mappings.get(theme, {
            'color_scheme': 'balanced',
            'atmosphere': 'neutral',
            'lighting': 'natural'
        })
    
    def _extract_win_condition(self, prompt: str) -> str:
        """Extract or infer the win condition from the prompt"""
        if any(word in prompt for word in ['complete', 'finish', 'win', 'victory']):
            return 'completion'
        elif any(word in prompt for word in ['collect', 'gather', 'find']):
            return 'collection'
        elif any(word in prompt for word in ['defeat', 'destroy', 'eliminate']):
            return 'elimination'
        elif any(word in prompt for word in ['reach', 'arrive', 'destination']):
            return 'destination'
        elif any(word in prompt for word in ['solve', 'figure', 'decode']):
            return 'puzzle_solution'
        else:
            return 'score_based'
    
    def _determine_challenge_type(self, prompt: str) -> str:
        """Determine the primary type of challenge"""
        if any(word in prompt for word in ['fast', 'quick', 'speed', 'time']):
            return 'speed'
        elif any(word in prompt for word in ['difficult', 'hard', 'challenge']):
            return 'skill'
        elif any(word in prompt for word in ['think', 'solve', 'logic']):
            return 'mental'
        elif any(word in prompt for word in ['precise', 'accurate', 'careful']):
            return 'precision'
        else:
            return 'balanced'
    
    def _generate_enhanced_description(self, analysis: Dict[str, Any]) -> str:
        """Generate an enhanced description based on analysis"""
        game_type = analysis['game_type']
        theme = analysis['theme']
        entities = analysis['entities']
        
        # Base description templates
        templates = {
            'racing': f"An exciting {theme} racing game where you speed through challenging tracks",
            'puzzle': f"A mind-bending {theme} puzzle game that tests your problem-solving skills",
            'combat': f"An intense {theme} combat game with strategic fighting mechanics",
            'cooking': f"A delicious {theme} cooking game where you master culinary arts",
            'collection': f"An engaging {theme} collection game with exploration elements"
        }
        
        base = templates.get(game_type, f"A unique {theme} {game_type} game")
        
        # Add entity details
        if entities['characters']:
            base += f" featuring {', '.join(entities['characters'][:2])}"
        
        if entities['objects']:
            base += f" with {', '.join(entities['objects'][:2])}"
        
        if entities['environments']:
            base += f" set in {', '.join(entities['environments'][:2])}"
        
        return base
    
    def _generate_title(self, analysis: Dict[str, Any]) -> str:
        """Generate a creative title based on analysis"""
        theme = analysis['theme']
        game_type = analysis['game_type']
        entities = analysis['entities']
        
        # Theme-based title prefixes
        theme_prefixes = {
            'fantasy': ['Mystical', 'Enchanted', 'Magical', 'Legendary'],
            'space': ['Cosmic', 'Galactic', 'Stellar', 'Nebula'],
            'underwater': ['Aquatic', 'Deep Sea', 'Ocean', 'Tidal'],
            'cyberpunk': ['Neon', 'Digital', 'Cyber', 'Matrix'],
            'steampunk': ['Steam', 'Clockwork', 'Brass', 'Mechanical']
        }
        
        # Game type suffixes
        type_suffixes = {
            'racing': ['Race', 'Grand Prix', 'Championship', 'Speed Trial'],
            'puzzle': ['Mystery', 'Enigma', 'Challenge', 'Quest'],
            'combat': ['Battle', 'War', 'Conflict', 'Arena'],
            'cooking': ['Kitchen', 'Chef', 'Cuisine', 'Recipe'],
            'collection': ['Quest', 'Hunt', 'Adventure', 'Journey']
        }
        
        # Select components
        prefix = random.choice(theme_prefixes.get(theme, ['Epic', 'Ultimate', 'Grand']))
        suffix = random.choice(type_suffixes.get(game_type, ['Adventure', 'Quest']))
        
        # Add entity-based middle part if available
        middle = ""
        if entities['objects']:
            middle = entities['objects'][0].title()
        elif entities['characters']:
            middle = entities['characters'][0].title()
        elif entities['environments']:
            middle = entities['environments'][0].title()
        
        if middle:
            return f"{prefix} {middle} {suffix}"
        else:
            return f"{prefix} {suffix}"

    def extract_game_mechanics(self, prompt: str) -> Dict[str, Any]:
        """
        Extract specific game mechanics that should be implemented
        
        Args:
            prompt: User's game description
            
        Returns:
            Dictionary of specific mechanics to implement
        """
        analysis = self.deep_analyze_prompt(prompt)
        
        mechanics = {
            'primary_mechanic': analysis['game_type'],
            'movement_type': self._determine_movement_type(prompt),
            'interaction_type': self._determine_interaction_type(prompt),
            'progression_type': self._determine_progression_type(prompt),
            'challenge_mechanics': self._extract_challenge_mechanics(prompt),
            'reward_system': self._determine_reward_system(prompt)
        }
        
        return mechanics
    
    def _determine_movement_type(self, prompt: str) -> str:
        """Determine how the player moves in the game"""
        if any(word in prompt for word in ['drive', 'car', 'vehicle', 'racing']):
            return 'vehicle_control'
        elif any(word in prompt for word in ['jump', 'platform', 'climb']):
            return 'platformer_movement'
        elif any(word in prompt for word in ['fly', 'flying', 'air', 'wings']):
            return 'flight_control'
        elif any(word in prompt for word in ['swim', 'underwater', 'dive']):
            return 'swimming_control'
        else:
            return 'standard_movement'
    
    def _determine_interaction_type(self, prompt: str) -> str:
        """Determine how the player interacts with the game world"""
        if any(word in prompt for word in ['click', 'tap', 'touch']):
            return 'click_interaction'
        elif any(word in prompt for word in ['drag', 'swipe', 'gesture']):
            return 'gesture_interaction'
        elif any(word in prompt for word in ['type', 'input', 'text']):
            return 'text_interaction'
        else:
            return 'key_interaction'
    
    def _determine_progression_type(self, prompt: str) -> str:
        """Determine how the player progresses through the game"""
        if any(word in prompt for word in ['level', 'stage', 'world']):
            return 'level_progression'
        elif any(word in prompt for word in ['score', 'points', 'high score']):
            return 'score_progression'
        elif any(word in prompt for word in ['time', 'timer', 'countdown']):
            return 'time_progression'
        elif any(word in prompt for word in ['unlock', 'upgrade', 'improve']):
            return 'unlock_progression'
        else:
            return 'continuous_progression'
    
    def _extract_challenge_mechanics(self, prompt: str) -> List[str]:
        """Extract specific challenge mechanics from the prompt"""
        challenges = []
        
        if any(word in prompt for word in ['avoid', 'dodge', 'escape']):
            challenges.append('avoidance')
        
        if any(word in prompt for word in ['time', 'timer', 'quick', 'fast']):
            challenges.append('time_pressure')
        
        if any(word in prompt for word in ['accurate', 'precise', 'aim']):
            challenges.append('precision')
        
        if any(word in prompt for word in ['memory', 'remember', 'recall']):
            challenges.append('memory')
        
        if any(word in prompt for word in ['pattern', 'sequence', 'order']):
            challenges.append('pattern_recognition')
        
        return challenges
    
    def _determine_reward_system(self, prompt: str) -> str:
        """Determine what rewards the player gets"""
        if any(word in prompt for word in ['coin', 'money', 'gold', 'currency']):
            return 'currency_rewards'
        elif any(word in prompt for word in ['power', 'upgrade', 'ability']):
            return 'power_rewards'
        elif any(word in prompt for word in ['unlock', 'new', 'access']):
            return 'unlock_rewards'
        elif any(word in prompt for word in ['score', 'points', 'rating']):
            return 'score_rewards'
        else:
            return 'completion_rewards'

# Global instance for easy importing
advanced_analyzer = AdvancedPromptAnalyzer()
