"""
Advanced Prompt Interpreter - NLP Core for AI Game Generation
Revolutionary natural language processing system that extracts game specifications from user prompts

This module provides:
- Advanced genre detection and classification
- Theme and aesthetic analysis
- Protagonist and character extraction
- Mechanics and gameplay element identification
- Difficulty and complexity assessment
- Visual style and mood interpretation
"""

import re
import json
import random
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict

@dataclass
class GameConfig:
    """Structured configuration object for game generation"""
    genre: str
    subgenre: Optional[str]
    theme: str
    setting: str
    protagonist: str
    antagonist: Optional[str]
    mechanics: List[str]
    visual_style: str
    mood: str
    difficulty: str
    complexity: int
    special_features: List[str]
    color_palette: str
    audio_style: str
    narrative_elements: List[str]
    target_audience: str
    estimated_playtime: str

class AdvancedPromptInterpreter:
    """
    Advanced NLP system for interpreting game creation prompts
    Extracts detailed game specifications from natural language input
    """
    
    def __init__(self):
        self.genre_keywords = {
            'platformer': [
                'platformer', 'platform', 'jumping', 'mario', 'sonic', 'side-scrolling',
                'jump', 'climb', 'ledges', 'obstacles', 'coins', 'power-ups'
            ],
            'shooter': [
                'shooter', 'shooting', 'gun', 'weapon', 'bullet', 'enemy', 'combat',
                'space invaders', 'asteroids', 'laser', 'missile', 'defend', 'attack'
            ],
            'puzzle': [
                'puzzle', 'solve', 'brain', 'logic', 'match', 'tetris', 'sliding',
                'riddle', 'challenge', 'think', 'strategy', 'mind', 'clever'
            ],
            'rpg': [
                'rpg', 'role-playing', 'character', 'level up', 'stats', 'quest',
                'adventure', 'story', 'dialogue', 'inventory', 'magic', 'fantasy'
            ],
            'racing': [
                'racing', 'car', 'speed', 'fast', 'track', 'lap', 'finish line',
                'vehicle', 'driving', 'acceleration', 'boost', 'competition'
            ],
            'strategy': [
                'strategy', 'tactical', 'plan', 'resource', 'build', 'manage',
                'empire', 'civilization', 'war', 'army', 'base', 'economy'
            ],
            'action': [
                'action', 'fast-paced', 'reflex', 'quick', 'intense', 'adrenaline',
                'combat', 'fight', 'battle', 'warrior', 'hero', 'adventure'
            ],
            'simulation': [
                'simulation', 'sim', 'realistic', 'life', 'city', 'farm',
                'business', 'management', 'real-world', 'economy', 'society'
            ],
            'survival': [
                'survival', 'survive', 'resources', 'craft', 'build', 'hunger',
                'thirst', 'shelter', 'wilderness', 'danger', 'harsh', 'endure'
            ],
            'horror': [
                'horror', 'scary', 'fear', 'ghost', 'monster', 'dark', 'creepy',
                'nightmare', 'terror', 'haunted', 'evil', 'spine-chilling'
            ]
        }
        
        self.theme_keywords = {
            'fantasy': [
                'fantasy', 'magic', 'wizard', 'dragon', 'castle', 'medieval',
                'knight', 'sword', 'spell', 'enchanted', 'mystical', 'fairy'
            ],
            'sci-fi': [
                'sci-fi', 'science fiction', 'space', 'alien', 'robot', 'future',
                'technology', 'laser', 'spaceship', 'galaxy', 'cybernetic', 'android'
            ],
            'cyberpunk': [
                'cyberpunk', 'neon', 'cyber', 'hacker', 'matrix', 'digital',
                'virtual', 'tech', 'dystopian', 'corporate', 'augmented', 'neural'
            ],
            'steampunk': [
                'steampunk', 'steam', 'victorian', 'brass', 'gears', 'clockwork',
                'mechanical', 'industrial', 'airship', 'goggles', 'copper', 'invention'
            ],
            'underwater': [
                'underwater', 'ocean', 'sea', 'marine', 'aquatic', 'submarine',
                'coral', 'fish', 'mermaid', 'deep', 'diving', 'nautical'
            ],
            'forest': [
                'forest', 'woods', 'trees', 'nature', 'woodland', 'jungle',
                'animals', 'green', 'natural', 'wild', 'organic', 'ecosystem'
            ],
            'desert': [
                'desert', 'sand', 'dunes', 'arid', 'hot', 'oasis', 'camel',
                'nomad', 'mirage', 'scorching', 'barren', 'wasteland'
            ],
            'arctic': [
                'arctic', 'ice', 'snow', 'cold', 'frozen', 'polar', 'glacier',
                'blizzard', 'tundra', 'penguin', 'seal', 'frigid'
            ],
            'urban': [
                'urban', 'city', 'street', 'building', 'metropolitan', 'downtown',
                'skyscraper', 'traffic', 'modern', 'concrete', 'bustling', 'crowded'
            ],
            'post-apocalyptic': [
                'post-apocalyptic', 'wasteland', 'ruins', 'destroyed', 'survivor',
                'radiation', 'mutant', 'desolate', 'abandoned', 'decay', 'rubble'
            ]
        }
        
        self.protagonist_keywords = {
            'cat': ['cat', 'feline', 'kitten', 'kitty', 'tabby', 'persian'],
            'dog': ['dog', 'puppy', 'canine', 'hound', 'retriever', 'shepherd'],
            'robot': ['robot', 'android', 'cyborg', 'mechanical', 'artificial', 'bot'],
            'wizard': ['wizard', 'mage', 'sorcerer', 'magician', 'warlock', 'enchanter'],
            'knight': ['knight', 'warrior', 'paladin', 'crusader', 'champion', 'hero'],
            'alien': ['alien', 'extraterrestrial', 'martian', 'being', 'creature', 'visitor'],
            'pirate': ['pirate', 'buccaneer', 'corsair', 'sailor', 'captain', 'mariner'],
            'ninja': ['ninja', 'assassin', 'shinobi', 'stealth', 'shadow', 'warrior'],
            'princess': ['princess', 'queen', 'royal', 'nobility', 'monarch', 'ruler'],
            'detective': ['detective', 'investigator', 'sleuth', 'inspector', 'agent', 'spy']
        }
        
        self.mechanics_keywords = {
            'jumping': ['jump', 'leap', 'bounce', 'hop', 'spring', 'vault'],
            'collecting': ['collect', 'gather', 'pickup', 'acquire', 'obtain', 'find'],
            'shooting': ['shoot', 'fire', 'blast', 'attack', 'weapon', 'projectile'],
            'puzzle-solving': ['solve', 'puzzle', 'riddle', 'challenge', 'brain', 'logic'],
            'racing': ['race', 'speed', 'fast', 'compete', 'lap', 'finish'],
            'building': ['build', 'construct', 'create', 'craft', 'make', 'assemble'],
            'exploring': ['explore', 'discover', 'adventure', 'journey', 'travel', 'roam'],
            'fighting': ['fight', 'battle', 'combat', 'duel', 'clash', 'struggle'],
            'stealth': ['stealth', 'sneak', 'hide', 'invisible', 'quiet', 'shadow'],
            'magic': ['magic', 'spell', 'enchant', 'mystical', 'supernatural', 'arcane']
        }
        
        self.visual_styles = {
            'pixel': ['pixel', 'retro', '8-bit', '16-bit', 'pixelated', 'classic'],
            'cartoon': ['cartoon', 'animated', 'colorful', 'bright', 'cheerful', 'fun'],
            'realistic': ['realistic', 'photorealistic', 'detailed', 'lifelike', 'accurate'],
            'minimalist': ['minimalist', 'simple', 'clean', 'basic', 'stripped', 'bare'],
            'dark': ['dark', 'gothic', 'noir', 'shadow', 'black', 'grim'],
            'neon': ['neon', 'glowing', 'bright', 'electric', 'fluorescent', 'vivid'],
            'watercolor': ['watercolor', 'painted', 'artistic', 'soft', 'flowing', 'dreamy'],
            'geometric': ['geometric', 'angular', 'sharp', 'abstract', 'mathematical', 'precise']
        }
        
        self.mood_keywords = {
            'cheerful': ['cheerful', 'happy', 'joyful', 'upbeat', 'positive', 'bright'],
            'mysterious': ['mysterious', 'enigmatic', 'secretive', 'hidden', 'unknown', 'cryptic'],
            'intense': ['intense', 'dramatic', 'powerful', 'strong', 'fierce', 'passionate'],
            'relaxing': ['relaxing', 'calm', 'peaceful', 'serene', 'tranquil', 'soothing'],
            'exciting': ['exciting', 'thrilling', 'exhilarating', 'stimulating', 'energetic'],
            'spooky': ['spooky', 'eerie', 'creepy', 'haunting', 'ghostly', 'supernatural'],
            'epic': ['epic', 'grand', 'magnificent', 'legendary', 'heroic', 'monumental'],
            'whimsical': ['whimsical', 'playful', 'quirky', 'imaginative', 'fanciful', 'magical']
        }
        
        self.difficulty_keywords = {
            'easy': ['easy', 'simple', 'beginner', 'casual', 'relaxed', 'gentle'],
            'medium': ['medium', 'moderate', 'balanced', 'standard', 'normal', 'average'],
            'hard': ['hard', 'difficult', 'challenging', 'tough', 'demanding', 'intense'],
            'extreme': ['extreme', 'brutal', 'punishing', 'hardcore', 'unforgiving', 'insane']
        }

    def interpret_prompt(self, prompt: str) -> GameConfig:
        """
        Main method to interpret a natural language prompt and extract game configuration
        
        Args:
            prompt: Natural language description of the desired game
            
        Returns:
            GameConfig object with extracted specifications
        """
        prompt_lower = prompt.lower()
        
        # Extract core game elements
        genre = self._detect_genre(prompt_lower)
        subgenre = self._detect_subgenre(prompt_lower, genre)
        theme = self._detect_theme(prompt_lower)
        setting = self._detect_setting(prompt_lower, theme)
        protagonist = self._detect_protagonist(prompt_lower)
        antagonist = self._detect_antagonist(prompt_lower)
        mechanics = self._detect_mechanics(prompt_lower, genre)
        visual_style = self._detect_visual_style(prompt_lower)
        mood = self._detect_mood(prompt_lower)
        difficulty = self._detect_difficulty(prompt_lower)
        complexity = self._assess_complexity(prompt_lower)
        special_features = self._detect_special_features(prompt_lower)
        color_palette = self._generate_color_palette(theme, mood, visual_style)
        audio_style = self._determine_audio_style(theme, mood, genre)
        narrative_elements = self._extract_narrative_elements(prompt_lower)
        target_audience = self._determine_target_audience(prompt_lower, difficulty)
        estimated_playtime = self._estimate_playtime(complexity, genre)
        
        return GameConfig(
            genre=genre,
            subgenre=subgenre,
            theme=theme,
            setting=setting,
            protagonist=protagonist,
            antagonist=antagonist,
            mechanics=mechanics,
            visual_style=visual_style,
            mood=mood,
            difficulty=difficulty,
            complexity=complexity,
            special_features=special_features,
            color_palette=color_palette,
            audio_style=audio_style,
            narrative_elements=narrative_elements,
            target_audience=target_audience,
            estimated_playtime=estimated_playtime
        )

    def _detect_genre(self, prompt: str) -> str:
        """Detect the primary game genre from the prompt"""
        genre_scores = {}
        
        for genre, keywords in self.genre_keywords.items():
            score = sum(1 for keyword in keywords if keyword in prompt)
            if score > 0:
                genre_scores[genre] = score
        
        if genre_scores:
            return max(genre_scores, key=genre_scores.get)
        
        # Fallback based on common patterns
        if any(word in prompt for word in ['jump', 'platform', 'side']):
            return 'platformer'
        elif any(word in prompt for word in ['shoot', 'gun', 'enemy']):
            return 'shooter'
        elif any(word in prompt for word in ['puzzle', 'solve', 'brain']):
            return 'puzzle'
        elif any(word in prompt for word in ['race', 'car', 'speed']):
            return 'racing'
        else:
            return 'action'  # Default fallback

    def _detect_subgenre(self, prompt: str, genre: str) -> Optional[str]:
        """Detect subgenre based on main genre and additional context"""
        subgenre_map = {
            'platformer': {
                'metroidvania': ['explore', 'backtrack', 'ability', 'unlock'],
                'endless runner': ['endless', 'infinite', 'runner', 'continuous'],
                'puzzle platformer': ['puzzle', 'solve', 'brain', 'logic']
            },
            'shooter': {
                'bullet hell': ['bullet', 'hell', 'intense', 'overwhelming'],
                'twin stick': ['twin', 'stick', 'dual', 'control'],
                'space shooter': ['space', 'alien', 'spaceship', 'galaxy']
            },
            'puzzle': {
                'match-3': ['match', 'three', 'connect', 'line'],
                'sliding puzzle': ['slide', 'sliding', 'tile', 'arrange'],
                'logic puzzle': ['logic', 'deduction', 'reasoning', 'brain']
            }
        }
        
        if genre in subgenre_map:
            for subgenre, keywords in subgenre_map[genre].items():
                if any(keyword in prompt for keyword in keywords):
                    return subgenre
        
        return None

    def _detect_theme(self, prompt: str) -> str:
        """Detect the thematic setting of the game"""
        theme_scores = {}
        
        for theme, keywords in self.theme_keywords.items():
            score = sum(1 for keyword in keywords if keyword in prompt)
            if score > 0:
                theme_scores[theme] = score
        
        if theme_scores:
            return max(theme_scores, key=theme_scores.get)
        
        # Contextual fallback
        if any(word in prompt for word in ['dream', 'sleep', 'night']):
            return 'fantasy'
        elif any(word in prompt for word in ['city', 'street', 'building']):
            return 'urban'
        else:
            return 'fantasy'  # Default fallback

    def _detect_setting(self, prompt: str, theme: str) -> str:
        """Determine the specific setting based on theme and context"""
        setting_map = {
            'fantasy': ['enchanted forest', 'magical kingdom', 'mystical realm', 'ancient castle'],
            'sci-fi': ['space station', 'alien planet', 'futuristic city', 'starship'],
            'cyberpunk': ['neon city', 'digital world', 'corporate tower', 'virtual reality'],
            'underwater': ['coral reef', 'deep ocean', 'underwater city', 'submarine'],
            'forest': ['dense woodland', 'magical forest', 'jungle canopy', 'tree village'],
            'urban': ['city streets', 'rooftops', 'subway system', 'skyscrapers']
        }
        
        if theme in setting_map:
            return random.choice(setting_map[theme])
        else:
            return f"{theme} environment"

    def _detect_protagonist(self, prompt: str) -> str:
        """Identify the main character or protagonist"""
        for character, keywords in self.protagonist_keywords.items():
            if any(keyword in prompt for keyword in keywords):
                return character
        
        # Contextual detection
        if any(word in prompt for word in ['player', 'character', 'hero']):
            return 'hero'
        elif any(word in prompt for word in ['animal', 'creature']):
            return 'creature'
        else:
            return 'adventurer'  # Default fallback

    def _detect_antagonist(self, prompt: str) -> Optional[str]:
        """Identify enemies or antagonistic forces"""
        antagonist_keywords = {
            'monsters': ['monster', 'beast', 'creature', 'demon'],
            'robots': ['robot', 'machine', 'android', 'cyborg'],
            'aliens': ['alien', 'extraterrestrial', 'invader'],
            'pirates': ['pirate', 'bandit', 'raider', 'thief'],
            'ghosts': ['ghost', 'spirit', 'phantom', 'specter'],
            'dragons': ['dragon', 'wyrm', 'serpent', 'drake']
        }
        
        for antagonist, keywords in antagonist_keywords.items():
            if any(keyword in prompt for keyword in keywords):
                return antagonist
        
        if any(word in prompt for word in ['enemy', 'villain', 'bad', 'evil']):
            return 'enemies'
        
        return None

    def _detect_mechanics(self, prompt: str, genre: str) -> List[str]:
        """Identify core gameplay mechanics"""
        detected_mechanics = []
        
        for mechanic, keywords in self.mechanics_keywords.items():
            if any(keyword in prompt for keyword in keywords):
                detected_mechanics.append(mechanic)
        
        # Add genre-specific default mechanics
        genre_defaults = {
            'platformer': ['jumping', 'collecting'],
            'shooter': ['shooting', 'dodging'],
            'puzzle': ['puzzle-solving', 'logic'],
            'racing': ['racing', 'speed'],
            'rpg': ['exploring', 'character progression'],
            'action': ['fighting', 'movement']
        }
        
        if genre in genre_defaults:
            for mechanic in genre_defaults[genre]:
                if mechanic not in detected_mechanics:
                    detected_mechanics.append(mechanic)
        
        return detected_mechanics if detected_mechanics else ['movement', 'interaction']

    def _detect_visual_style(self, prompt: str) -> str:
        """Determine the visual art style"""
        for style, keywords in self.visual_styles.items():
            if any(keyword in prompt for keyword in keywords):
                return style
        
        # Theme-based defaults
        theme_style_map = {
            'cyberpunk': 'neon',
            'fantasy': 'cartoon',
            'horror': 'dark',
            'sci-fi': 'realistic'
        }
        
        # This would need theme detection first, simplified for now
        return 'cartoon'  # Default fallback

    def _detect_mood(self, prompt: str) -> str:
        """Determine the emotional tone and atmosphere"""
        for mood, keywords in self.mood_keywords.items():
            if any(keyword in prompt for keyword in keywords):
                return mood
        
        # Genre-based defaults
        genre_mood_map = {
            'horror': 'spooky',
            'puzzle': 'relaxing',
            'action': 'intense',
            'platformer': 'cheerful'
        }
        
        return 'cheerful'  # Default fallback

    def _detect_difficulty(self, prompt: str) -> str:
        """Assess intended difficulty level"""
        for difficulty, keywords in self.difficulty_keywords.items():
            if any(keyword in prompt for keyword in keywords):
                return difficulty
        
        # Context-based assessment
        if any(word in prompt for word in ['child', 'kid', 'family']):
            return 'easy'
        elif any(word in prompt for word in ['expert', 'master', 'pro']):
            return 'hard'
        else:
            return 'medium'  # Default

    def _assess_complexity(self, prompt: str) -> int:
        """Assess game complexity on a scale of 1-10"""
        complexity_indicators = [
            'multiple levels', 'story', 'characters', 'inventory', 'upgrades',
            'multiplayer', 'achievements', 'customization', 'progression',
            'dialogue', 'quests', 'crafting', 'economy', 'factions'
        ]
        
        complexity_score = sum(1 for indicator in complexity_indicators if indicator in prompt)
        
        # Base complexity by genre
        genre_complexity = {
            'puzzle': 3,
            'platformer': 4,
            'shooter': 5,
            'rpg': 8,
            'strategy': 9,
            'simulation': 7
        }
        
        base_complexity = 5  # Default
        complexity_score += base_complexity
        
        return min(10, max(1, complexity_score))

    def _detect_special_features(self, prompt: str) -> List[str]:
        """Identify special or unique features mentioned"""
        features = []
        
        feature_keywords = {
            'multiplayer': ['multiplayer', 'coop', 'versus', 'online'],
            'procedural': ['procedural', 'random', 'generated', 'infinite'],
            'physics': ['physics', 'realistic', 'gravity', 'momentum'],
            'day_night': ['day', 'night', 'time', 'cycle'],
            'weather': ['weather', 'rain', 'snow', 'storm'],
            'achievements': ['achievement', 'trophy', 'reward', 'unlock'],
            'customization': ['customize', 'personalize', 'modify', 'edit'],
            'voice_acting': ['voice', 'narration', 'spoken', 'audio']
        }
        
        for feature, keywords in feature_keywords.items():
            if any(keyword in prompt for keyword in keywords):
                features.append(feature)
        
        return features

    def _generate_color_palette(self, theme: str, mood: str, visual_style: str) -> str:
        """Generate appropriate color palette based on theme, mood, and style"""
        palette_map = {
            ('fantasy', 'cheerful'): 'bright_magical',
            ('fantasy', 'mysterious'): 'dark_mystical',
            ('sci-fi', 'intense'): 'neon_tech',
            ('cyberpunk', 'dark'): 'neon_noir',
            ('underwater', 'relaxing'): 'ocean_blues',
            ('forest', 'cheerful'): 'nature_greens',
            ('horror', 'spooky'): 'dark_gothic'
        }
        
        key = (theme, mood)
        if key in palette_map:
            return palette_map[key]
        
        # Fallback based on mood
        mood_palettes = {
            'cheerful': 'bright_colorful',
            'dark': 'monochrome_dark',
            'mysterious': 'purple_mystical',
            'intense': 'red_orange',
            'relaxing': 'soft_pastels'
        }
        
        return mood_palettes.get(mood, 'balanced_natural')

    def _determine_audio_style(self, theme: str, mood: str, genre: str) -> str:
        """Determine appropriate audio/music style"""
        audio_map = {
            'fantasy': 'orchestral_epic',
            'sci-fi': 'electronic_ambient',
            'cyberpunk': 'synthwave_electronic',
            'horror': 'dark_atmospheric',
            'underwater': 'ambient_flowing',
            'forest': 'nature_acoustic'
        }
        
        return audio_map.get(theme, 'upbeat_electronic')

    def _extract_narrative_elements(self, prompt: str) -> List[str]:
        """Extract story and narrative elements"""
        elements = []
        
        narrative_keywords = {
            'quest': ['quest', 'mission', 'journey', 'adventure'],
            'rescue': ['rescue', 'save', 'help', 'protect'],
            'discovery': ['discover', 'find', 'uncover', 'reveal'],
            'revenge': ['revenge', 'vengeance', 'payback', 'retribution'],
            'survival': ['survive', 'escape', 'endure', 'overcome'],
            'mystery': ['mystery', 'secret', 'hidden', 'unknown'],
            'romance': ['love', 'romance', 'relationship', 'heart'],
            'friendship': ['friend', 'companion', 'ally', 'team']
        }
        
        for element, keywords in narrative_keywords.items():
            if any(keyword in prompt for keyword in keywords):
                elements.append(element)
        
        return elements

    def _determine_target_audience(self, prompt: str, difficulty: str) -> str:
        """Determine the intended target audience"""
        if any(word in prompt for word in ['child', 'kid', 'family', 'young']):
            return 'children'
        elif any(word in prompt for word in ['adult', 'mature', 'complex']):
            return 'adults'
        elif difficulty in ['easy', 'medium']:
            return 'general'
        else:
            return 'hardcore_gamers'

    def _estimate_playtime(self, complexity: int, genre: str) -> str:
        """Estimate expected playtime based on complexity and genre"""
        base_times = {
            'puzzle': 15,
            'platformer': 30,
            'shooter': 20,
            'racing': 10,
            'rpg': 120,
            'strategy': 90,
            'action': 25
        }
        
        base_time = base_times.get(genre, 30)
        adjusted_time = base_time * (complexity / 5)
        
        if adjusted_time < 15:
            return "5-15 minutes"
        elif adjusted_time < 60:
            return "15-60 minutes"
        elif adjusted_time < 180:
            return "1-3 hours"
        else:
            return "3+ hours"

    def get_config_summary(self, config: GameConfig) -> str:
        """Generate a human-readable summary of the game configuration"""
        summary = f"""
Game Configuration Summary:
==========================

Genre: {config.genre.title()}
{f"Subgenre: {config.subgenre.title()}" if config.subgenre else ""}
Theme: {config.theme.title()}
Setting: {config.setting}

Protagonist: {config.protagonist.title()}
{f"Antagonist: {config.antagonist.title()}" if config.antagonist else ""}

Core Mechanics: {', '.join(config.mechanics)}
Visual Style: {config.visual_style.title()}
Mood: {config.mood.title()}
Difficulty: {config.difficulty.title()}
Complexity: {config.complexity}/10

Color Palette: {config.color_palette}
Audio Style: {config.audio_style}
Target Audience: {config.target_audience.replace('_', ' ').title()}
Estimated Playtime: {config.estimated_playtime}

{f"Special Features: {', '.join(config.special_features)}" if config.special_features else ""}
{f"Narrative Elements: {', '.join(config.narrative_elements)}" if config.narrative_elements else ""}
"""
        return summary.strip()

    def export_config_json(self, config: GameConfig) -> str:
        """Export configuration as JSON string"""
        return json.dumps(asdict(config), indent=2)

# Example usage and testing
if __name__ == "__main__":
    interpreter = AdvancedPromptInterpreter()
    
    # Test prompts
    test_prompts = [
        "a platformer where a cat travels through dreams",
        "a cyberpunk racing game with neon lights and fast cars",
        "an underwater puzzle adventure with a mermaid collecting pearls",
        "a spooky horror game in a haunted mansion with ghosts",
        "a space shooter defending Earth from alien invaders"
    ]
    
    for prompt in test_prompts:
        print(f"\nPrompt: '{prompt}'")
        print("=" * 50)
        config = interpreter.interpret_prompt(prompt)
        print(interpreter.get_config_summary(config))
        print("\nJSON Export:")
        print(interpreter.export_config_json(config))
        print("\n" + "="*80)
