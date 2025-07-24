"""
AI Stylist & Assistant - Revolutionary Game Enhancement System
Intelligent assistant that provides real-time game improvements and creative suggestions

This module provides:
- Creative brainstorming for game concepts
- Real-time game analysis and improvement suggestions
- Dynamic feedback processing and implementation
- Style and aesthetic recommendations
- Gameplay balance optimization
- User interaction enhancement
"""

import json
import random
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from advanced_prompt_interpreter import GameConfig

@dataclass
class Enhancement:
    """Represents a specific game enhancement suggestion"""
    category: str
    title: str
    description: str
    implementation: str
    priority: int  # 1-10, 10 being highest priority
    difficulty: str  # 'easy', 'medium', 'hard'
    impact: str  # 'low', 'medium', 'high'

@dataclass
class GameAnalysis:
    """Comprehensive analysis of a generated game"""
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[Enhancement]
    overall_score: int  # 1-100
    target_audience_fit: str
    engagement_potential: str
    technical_quality: str

class AIStylistAssistant:
    """
    Advanced AI assistant for game enhancement and creative guidance
    Provides intelligent suggestions for improving generated games
    """
    
    def __init__(self):
        self.enhancement_categories = {
            'gameplay': 'Core game mechanics and player interaction',
            'visuals': 'Graphics, animations, and visual effects',
            'audio': 'Sound effects, music, and audio feedback',
            'ui_ux': 'User interface and user experience',
            'story': 'Narrative elements and storytelling',
            'difficulty': 'Game balance and challenge progression',
            'mobile': 'Mobile-specific optimizations',
            'accessibility': 'Features for inclusive gaming',
            'social': 'Multiplayer and sharing features',
            'monetization': 'Revenue and engagement strategies'
        }
        
        self.style_suggestions = {
            'pixel': {
                'colors': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'],
                'effects': ['pixelated borders', 'retro animations', '8-bit sound effects'],
                'fonts': ['monospace', 'pixel fonts', 'retro typefaces']
            },
            'neon': {
                'colors': ['#FF0080', '#00FFFF', '#FFFF00', '#FF4000', '#8000FF'],
                'effects': ['glowing outlines', 'pulsing animations', 'electric particles'],
                'fonts': ['futuristic', 'bold sans-serif', 'tech-inspired']
            },
            'cartoon': {
                'colors': ['#FF6B9D', '#C44569', '#F8B500', '#6C5CE7', '#00B894'],
                'effects': ['bouncy animations', 'rounded corners', 'playful transitions'],
                'fonts': ['rounded', 'friendly', 'comic-style']
            },
            'minimalist': {
                'colors': ['#2D3436', '#636E72', '#DDD', '#0984E3', '#00B894'],
                'effects': ['clean lines', 'subtle shadows', 'smooth transitions'],
                'fonts': ['clean sans-serif', 'geometric', 'modern']
            }
        }
        
        self.gameplay_patterns = {
            'platformer': {
                'core_mechanics': ['jumping', 'collecting', 'avoiding obstacles'],
                'enhancements': ['double jump', 'wall jumping', 'power-ups', 'moving platforms'],
                'progression': ['new abilities', 'harder levels', 'boss fights']
            },
            'shooter': {
                'core_mechanics': ['shooting', 'dodging', 'aiming'],
                'enhancements': ['weapon upgrades', 'special abilities', 'combo system'],
                'progression': ['stronger enemies', 'new weapons', 'boss battles']
            },
            'puzzle': {
                'core_mechanics': ['problem solving', 'pattern recognition', 'logic'],
                'enhancements': ['hint system', 'time challenges', 'multiple solutions'],
                'progression': ['complex puzzles', 'new mechanics', 'puzzle variations']
            },
            'racing': {
                'core_mechanics': ['steering', 'acceleration', 'avoiding obstacles'],
                'enhancements': ['boost system', 'car upgrades', 'track variations'],
                'progression': ['faster speeds', 'more obstacles', 'championship mode']
            }
        }
        
        self.feedback_responses = {
            'too_easy': {
                'suggestions': ['increase enemy speed', 'add more obstacles', 'reduce power-up frequency'],
                'implementations': ['multiply enemy speed by 1.5', 'spawn obstacles more frequently', 'increase challenge rating']
            },
            'too_hard': {
                'suggestions': ['decrease enemy speed', 'add more power-ups', 'increase player health'],
                'implementations': ['multiply enemy speed by 0.8', 'spawn power-ups more frequently', 'add invincibility frames']
            },
            'boring': {
                'suggestions': ['add visual effects', 'increase game speed', 'add new mechanics'],
                'implementations': ['add particle effects', 'increase base speed', 'introduce combo system']
            },
            'confusing': {
                'suggestions': ['improve instructions', 'add visual cues', 'simplify controls'],
                'implementations': ['show control hints', 'highlight interactive elements', 'reduce control complexity']
            },
            'laggy': {
                'suggestions': ['optimize rendering', 'reduce particle count', 'simplify graphics'],
                'implementations': ['limit frame rate', 'reduce visual effects', 'optimize collision detection']
            }
        }

    def analyze_game(self, config: GameConfig, game_assets: Dict[str, Any]) -> GameAnalysis:
        """
        Perform comprehensive analysis of a generated game
        
        Args:
            config: Game configuration used to generate the game
            game_assets: Generated game assets and metadata
            
        Returns:
            GameAnalysis with detailed feedback and suggestions
        """
        strengths = self._identify_strengths(config, game_assets)
        weaknesses = self._identify_weaknesses(config, game_assets)
        suggestions = self._generate_enhancement_suggestions(config, weaknesses)
        overall_score = self._calculate_overall_score(config, strengths, weaknesses)
        target_audience_fit = self._assess_target_audience_fit(config)
        engagement_potential = self._assess_engagement_potential(config, overall_score)
        technical_quality = self._assess_technical_quality(config, game_assets)
        
        return GameAnalysis(
            strengths=strengths,
            weaknesses=weaknesses,
            suggestions=suggestions,
            overall_score=overall_score,
            target_audience_fit=target_audience_fit,
            engagement_potential=engagement_potential,
            technical_quality=technical_quality
        )

    def brainstorm_game_ideas(self, theme: str, genre: str = None, constraints: List[str] = None) -> List[Dict[str, Any]]:
        """
        Generate creative game ideas based on theme and optional constraints
        
        Args:
            theme: Main theme or setting for the game
            genre: Optional preferred genre
            constraints: Optional list of constraints or requirements
            
        Returns:
            List of creative game concept dictionaries
        """
        ideas = []
        
        # Generate 5 unique game concepts
        for i in range(5):
            idea = self._generate_creative_concept(theme, genre, constraints)
            ideas.append(idea)
        
        return ideas

    def process_feedback(self, feedback: str, config: GameConfig) -> List[Enhancement]:
        """
        Process user feedback and generate specific improvement suggestions
        
        Args:
            feedback: Natural language feedback from the user
            config: Current game configuration
            
        Returns:
            List of specific enhancement suggestions
        """
        feedback_lower = feedback.lower()
        enhancements = []
        
        # Analyze feedback sentiment and keywords
        feedback_type = self._classify_feedback(feedback_lower)
        
        if feedback_type in self.feedback_responses:
            responses = self.feedback_responses[feedback_type]
            
            for i, suggestion in enumerate(responses['suggestions']):
                enhancement = Enhancement(
                    category='gameplay',
                    title=f"Address: {feedback_type.replace('_', ' ').title()}",
                    description=suggestion,
                    implementation=responses['implementations'][i],
                    priority=8,
                    difficulty='medium',
                    impact='high'
                )
                enhancements.append(enhancement)
        
        # Add general improvements based on feedback content
        enhancements.extend(self._generate_contextual_enhancements(feedback_lower, config))
        
        return enhancements

    def suggest_visual_improvements(self, config: GameConfig) -> List[Enhancement]:
        """Generate visual enhancement suggestions based on theme and style"""
        enhancements = []
        
        style = config.visual_style
        theme = config.theme
        
        if style in self.style_suggestions:
            style_data = self.style_suggestions[style]
            
            # Color palette enhancement
            enhancement = Enhancement(
                category='visuals',
                title='Enhanced Color Palette',
                description=f'Implement {style}-specific color scheme with {", ".join(style_data["colors"][:3])}',
                implementation=f'Update CSS color variables to use {style} palette',
                priority=7,
                difficulty='easy',
                impact='medium'
            )
            enhancements.append(enhancement)
            
            # Visual effects enhancement
            enhancement = Enhancement(
                category='visuals',
                title='Style-Specific Effects',
                description=f'Add {style} visual effects: {", ".join(style_data["effects"])}',
                implementation=f'Implement {style} CSS animations and effects',
                priority=6,
                difficulty='medium',
                impact='medium'
            )
            enhancements.append(enhancement)
        
        # Theme-specific visual suggestions
        theme_visuals = self._get_theme_visual_suggestions(theme)
        enhancements.extend(theme_visuals)
        
        return enhancements

    def suggest_gameplay_improvements(self, config: GameConfig) -> List[Enhancement]:
        """Generate gameplay enhancement suggestions based on genre"""
        enhancements = []
        
        genre = config.genre
        
        if genre in self.gameplay_patterns:
            pattern = self.gameplay_patterns[genre]
            
            # Core mechanic enhancements
            for enhancement_idea in pattern['enhancements']:
                enhancement = Enhancement(
                    category='gameplay',
                    title=f'Add {enhancement_idea.title()}',
                    description=f'Implement {enhancement_idea} to enhance {genre} gameplay',
                    implementation=f'Add {enhancement_idea} mechanic to game logic',
                    priority=random.randint(5, 8),
                    difficulty='medium',
                    impact='high'
                )
                enhancements.append(enhancement)
            
            # Progression suggestions
            for progression_idea in pattern['progression']:
                enhancement = Enhancement(
                    category='gameplay',
                    title=f'Progression: {progression_idea.title()}',
                    description=f'Add {progression_idea} for better game progression',
                    implementation=f'Implement {progression_idea} system',
                    priority=random.randint(4, 7),
                    difficulty='hard',
                    impact='high'
                )
                enhancements.append(enhancement)
        
        return enhancements

    def suggest_mobile_optimizations(self, config: GameConfig) -> List[Enhancement]:
        """Generate mobile-specific optimization suggestions"""
        enhancements = [
            Enhancement(
                category='mobile',
                title='Touch Gesture Support',
                description='Add swipe gestures for enhanced mobile interaction',
                implementation='Implement touch gesture recognition for mobile controls',
                priority=8,
                difficulty='medium',
                impact='high'
            ),
            Enhancement(
                category='mobile',
                title='Haptic Feedback',
                description='Add vibration feedback for mobile devices',
                implementation='Implement navigator.vibrate() for game events',
                priority=6,
                difficulty='easy',
                impact='medium'
            ),
            Enhancement(
                category='mobile',
                title='Adaptive UI Scaling',
                description='Improve UI scaling for different screen sizes',
                implementation='Add responsive CSS for various mobile screen sizes',
                priority=7,
                difficulty='medium',
                impact='high'
            ),
            Enhancement(
                category='mobile',
                title='Battery Optimization',
                description='Optimize game performance for mobile battery life',
                implementation='Implement frame rate limiting and efficient rendering',
                priority=5,
                difficulty='hard',
                impact='medium'
            )
        ]
        
        return enhancements

    def generate_creative_prompt_variations(self, original_prompt: str) -> List[str]:
        """Generate creative variations of the original prompt"""
        variations = []
        
        # Extract key elements from the original prompt
        elements = self._extract_prompt_elements(original_prompt)
        
        # Generate variations by modifying elements
        variation_templates = [
            "A {mood} {genre} where {protagonist} {action} in a {setting}",
            "An {adjective} {theme} {genre} featuring {protagonist} and {antagonist}",
            "{protagonist} must {objective} through {setting} while {challenge}",
            "A {visual_style} {genre} about {protagonist} discovering {mystery}",
            "An epic {theme} adventure where {protagonist} {quest} to save {target}"
        ]
        
        for template in variation_templates:
            try:
                variation = template.format(**elements)
                variations.append(variation)
            except KeyError:
                # Skip if template requires elements not found
                continue
        
        return variations[:3]  # Return top 3 variations

    def get_style_recommendations(self, config: GameConfig) -> Dict[str, Any]:
        """Get comprehensive style recommendations for the game"""
        recommendations = {
            'color_palette': self._recommend_color_palette(config),
            'typography': self._recommend_typography(config),
            'visual_effects': self._recommend_visual_effects(config),
            'audio_style': self._recommend_audio_style(config),
            'ui_layout': self._recommend_ui_layout(config)
        }
        
        return recommendations

    def _identify_strengths(self, config: GameConfig, game_assets: Dict[str, Any]) -> List[str]:
        """Identify strengths of the generated game"""
        strengths = []
        
        # Genre-specific strengths
        if config.genre == 'platformer':
            strengths.append("Classic platformer mechanics with jumping and collecting")
        elif config.genre == 'shooter':
            strengths.append("Fast-paced action with shooting mechanics")
        elif config.genre == 'puzzle':
            strengths.append("Engaging puzzle mechanics that challenge the mind")
        elif config.genre == 'racing':
            strengths.append("Exciting racing gameplay with speed and obstacles")
        
        # Theme-specific strengths
        if config.theme in ['fantasy', 'sci-fi', 'cyberpunk']:
            strengths.append(f"Immersive {config.theme} theme with appropriate atmosphere")
        
        # Technical strengths
        strengths.append("Mobile-compatible design with touch controls")
        strengths.append("Responsive layout that works on all devices")
        
        # Visual strengths
        if config.visual_style:
            strengths.append(f"Consistent {config.visual_style} visual style")
        
        return strengths

    def _identify_weaknesses(self, config: GameConfig, game_assets: Dict[str, Any]) -> List[str]:
        """Identify potential weaknesses or areas for improvement"""
        weaknesses = []
        
        # Complexity assessment
        if config.complexity < 4:
            weaknesses.append("Game may be too simple for extended engagement")
        elif config.complexity > 8:
            weaknesses.append("Game complexity might overwhelm casual players")
        
        # Genre-specific weaknesses
        if config.genre == 'platformer' and 'jumping' not in config.mechanics:
            weaknesses.append("Missing core jumping mechanics for platformer genre")
        
        # Difficulty assessment
        if config.difficulty == 'easy':
            weaknesses.append("May lack challenge for experienced players")
        elif config.difficulty == 'hard':
            weaknesses.append("Might be too difficult for casual players")
        
        # Feature gaps
        if not config.special_features:
            weaknesses.append("Lacks unique features to differentiate from similar games")
        
        if not config.narrative_elements:
            weaknesses.append("Missing story elements that could enhance engagement")
        
        return weaknesses

    def _generate_enhancement_suggestions(self, config: GameConfig, weaknesses: List[str]) -> List[Enhancement]:
        """Generate specific enhancement suggestions based on identified weaknesses"""
        suggestions = []
        
        for weakness in weaknesses:
            if "too simple" in weakness:
                suggestions.append(Enhancement(
                    category='gameplay',
                    title='Add Complexity Layers',
                    description='Introduce additional mechanics like power-ups, combos, or special abilities',
                    implementation='Add secondary objectives and advanced mechanics',
                    priority=8,
                    difficulty='medium',
                    impact='high'
                ))
            
            elif "too difficult" in weakness:
                suggestions.append(Enhancement(
                    category='difficulty',
                    title='Implement Difficulty Scaling',
                    description='Add adaptive difficulty that adjusts to player performance',
                    implementation='Monitor player success rate and adjust game parameters',
                    priority=7,
                    difficulty='hard',
                    impact='high'
                ))
            
            elif "unique features" in weakness:
                suggestions.append(Enhancement(
                    category='gameplay',
                    title='Add Signature Feature',
                    description='Implement a unique mechanic that sets this game apart',
                    implementation='Design and add a genre-specific innovative feature',
                    priority=9,
                    difficulty='hard',
                    impact='high'
                ))
        
        return suggestions

    def _calculate_overall_score(self, config: GameConfig, strengths: List[str], weaknesses: List[str]) -> int:
        """Calculate overall game quality score (1-100)"""
        base_score = 60  # Starting point
        
        # Add points for strengths
        base_score += len(strengths) * 5
        
        # Subtract points for weaknesses
        base_score -= len(weaknesses) * 3
        
        # Bonus for complexity
        base_score += config.complexity * 2
        
        # Bonus for special features
        base_score += len(config.special_features) * 3
        
        # Bonus for narrative elements
        base_score += len(config.narrative_elements) * 2
        
        return max(1, min(100, base_score))

    def _assess_target_audience_fit(self, config: GameConfig) -> str:
        """Assess how well the game fits its target audience"""
        if config.target_audience == 'children':
            if config.difficulty in ['easy', 'medium'] and config.mood in ['cheerful', 'whimsical']:
                return 'Excellent fit for children with appropriate difficulty and mood'
            else:
                return 'May need adjustment for child-friendly content'
        
        elif config.target_audience == 'adults':
            if config.complexity >= 6:
                return 'Good complexity level for adult engagement'
            else:
                return 'Could benefit from increased complexity for adult players'
        
        else:
            return 'Well-balanced for general audience appeal'

    def _assess_engagement_potential(self, config: GameConfig, overall_score: int) -> str:
        """Assess the game's potential for player engagement"""
        if overall_score >= 80:
            return 'High engagement potential with strong replay value'
        elif overall_score >= 60:
            return 'Good engagement potential with room for improvement'
        else:
            return 'Moderate engagement potential, needs significant enhancements'

    def _assess_technical_quality(self, config: GameConfig, game_assets: Dict[str, Any]) -> str:
        """Assess the technical quality of the generated game"""
        quality_factors = []
        
        # Mobile compatibility
        if game_assets.get('mobile_compatible', False):
            quality_factors.append('mobile-compatible')
        
        # Visual consistency
        if config.visual_style and config.color_palette:
            quality_factors.append('consistent visual design')
        
        # Code structure (assumed good for generated games)
        quality_factors.append('clean code structure')
        
        if len(quality_factors) >= 3:
            return f'High technical quality: {", ".join(quality_factors)}'
        else:
            return 'Good technical foundation with room for optimization'

    def _generate_creative_concept(self, theme: str, genre: str = None, constraints: List[str] = None) -> Dict[str, Any]:
        """Generate a single creative game concept"""
        # Random genre if not specified
        if not genre:
            genres = ['platformer', 'shooter', 'puzzle', 'racing', 'rpg', 'action']
            genre = random.choice(genres)
        
        # Creative elements
        protagonists = ['robot', 'cat', 'wizard', 'alien', 'ninja', 'detective', 'pirate']
        objectives = ['save the world', 'find treasure', 'solve mysteries', 'escape danger', 'collect artifacts']
        settings = ['floating islands', 'underground caves', 'space stations', 'magical forests', 'cyber cities']
        
        concept = {
            'title': f"{random.choice(['Epic', 'Mystical', 'Cosmic', 'Secret', 'Lost'])} {theme.title()} {genre.title()}",
            'genre': genre,
            'theme': theme,
            'protagonist': random.choice(protagonists),
            'objective': random.choice(objectives),
            'setting': random.choice(settings),
            'unique_mechanic': self._generate_unique_mechanic(genre),
            'description': f"A {genre} game where a {random.choice(protagonists)} must {random.choice(objectives)} in {random.choice(settings)}"
        }
        
        return concept

    def _generate_unique_mechanic(self, genre: str) -> str:
        """Generate a unique mechanic for the specified genre"""
        mechanics = {
            'platformer': ['time manipulation', 'gravity switching', 'shadow cloning', 'size changing'],
            'shooter': ['bullet time', 'ricochet shots', 'enemy conversion', 'shield absorption'],
            'puzzle': ['reality shifting', 'mind reading', 'time loops', 'dimension swapping'],
            'racing': ['track building', 'vehicle morphing', 'weather control', 'teleportation'],
            'rpg': ['soul swapping', 'memory manipulation', 'dream walking', 'emotion control']
        }
        
        return random.choice(mechanics.get(genre, ['special ability']))

    def _classify_feedback(self, feedback: str) -> str:
        """Classify user feedback into predefined categories"""
        feedback_keywords = {
            'too_easy': ['easy', 'simple', 'boring', 'no challenge', 'too simple'],
            'too_hard': ['hard', 'difficult', 'impossible', 'frustrating', 'too tough'],
            'boring': ['boring', 'dull', 'repetitive', 'monotonous', 'uninteresting'],
            'confusing': ['confusing', 'unclear', 'complicated', 'hard to understand'],
            'laggy': ['slow', 'laggy', 'choppy', 'performance', 'frame rate']
        }
        
        for category, keywords in feedback_keywords.items():
            if any(keyword in feedback for keyword in keywords):
                return category
        
        return 'general'

    def _generate_contextual_enhancements(self, feedback: str, config: GameConfig) -> List[Enhancement]:
        """Generate enhancements based on specific feedback content"""
        enhancements = []
        
        # Look for specific improvement requests
        if 'visual' in feedback or 'graphics' in feedback:
            enhancements.append(Enhancement(
                category='visuals',
                title='Visual Enhancement',
                description='Improve visual quality based on user feedback',
                implementation='Enhance graphics, animations, and visual effects',
                priority=7,
                difficulty='medium',
                impact='medium'
            ))
        
        if 'sound' in feedback or 'audio' in feedback:
            enhancements.append(Enhancement(
                category='audio',
                title='Audio Enhancement',
                description='Improve audio quality and sound effects',
                implementation='Add better sound effects and background music',
                priority=6,
                difficulty='easy',
                impact='medium'
            ))
        
        if 'control' in feedback or 'input' in feedback:
            enhancements.append(Enhancement(
                category='ui_ux',
                title='Control Improvement',
                description='Enhance game controls and input responsiveness',
                implementation='Optimize input handling and control feedback',
                priority=8,
                difficulty='medium',
                impact='high'
            ))
        
        return enhancements

    def _extract_prompt_elements(self, prompt: str) -> Dict[str, str]:
        """Extract key elements from a prompt for variation generation"""
        # This is a simplified extraction - in a real implementation,
        # you'd use more sophisticated NLP
        elements = {
            'mood': random.choice(['epic', 'mysterious', 'exciting', 'magical']),
            'genre': 'adventure',
            'protagonist': 'hero',
            'action': 'explores',
            'setting': 'unknown world',
            'adjective': random.choice(['incredible', 'amazing', 'fantastic']),
            'theme': 'fantasy',
            'antagonist': 'enemies',
            'objective': 'complete the quest',
            'challenge': 'facing dangers',
            'mystery': 'ancient secrets',
            'quest': 'journeys',
            'target': 'the realm'
        }
        
        return elements

    def _recommend_color_palette(self, config: GameConfig) -> Dict[str, str]:
        """Recommend color palette based on theme and mood"""
        palettes = {
            'fantasy': {'primary': '#4A148C', 'secondary': '#7B1FA2', 'accent': '#FFD700'},
            'sci-fi': {'primary': '#0D47A1', 'secondary': '#1976D2', 'accent': '#00E5FF'},
            'cyberpunk': {'primary': '#000000', 'secondary': '#1A1A1A', 'accent': '#00FFFF'}
        }
        
        return palettes.get(config.theme, palettes['fantasy'])

    def _recommend_typography(self, config: GameConfig) -> Dict[str, str]:
        """Recommend typography based on visual style"""
        typography = {
            'pixel': {'font_family': 'monospace', 'style': 'retro'},
            'cartoon': {'font_family': 'rounded sans-serif', 'style': 'playful'},
            'minimalist': {'font_family': 'clean sans-serif', 'style': 'modern'}
        }
        
        return typography.get(config.visual_style, typography['cartoon'])

    def _recommend_visual_effects(self, config: GameConfig) -> List[str]:
        """Recommend visual effects based on theme and style"""
        effects = {
            'cyberpunk': ['neon glows', 'digital glitches', 'holographic elements'],
            'fantasy': ['magical sparkles', 'mystical auras', 'enchanted animations'],
            'sci-fi': ['energy beams', 'tech interfaces', 'futuristic transitions']
        }
        
        return effects.get(config.theme, ['smooth animations', 'subtle effects'])

    def _recommend_audio_style(self, config: GameConfig) -> str:
        """Recommend audio style based on theme and mood"""
        audio_styles = {
            'fantasy': 'orchestral with mystical elements',
            'sci-fi': 'electronic ambient with tech sounds',
            'cyberpunk': 'synthwave with digital effects',
            'underwater': 'ambient with water sounds'
        }
        
        return audio_styles.get(config.theme, 'upbeat electronic music')

    def _recommend_ui_layout(self, config: GameConfig) -> Dict[str, str]:
        """Recommend UI layout based on genre and target audience"""
        layouts = {
            'children': {'style': 'large buttons', 'colors': 'bright and friendly'},
            'adults': {'style': 'sleek interface', 'colors': 'sophisticated palette'},
            'general': {'style': 'balanced design', 'colors': 'accessible colors'}
        }
        
        return layouts.get(config.target_audience, layouts['general'])

    def _get_theme_visual_suggestions(self, theme: str) -> List[Enhancement]:
        """Get theme-specific visual enhancement suggestions"""
        theme_suggestions = {
            'cyberpunk': [
                Enhancement(
                    category='visuals',
                    title='Neon Glow Effects',
                    description='Add cyberpunk-style neon glowing effects to UI elements',
                    implementation='Implement CSS neon glow animations and effects',
                    priority=8,
                    difficulty='medium',
                    impact='high'
                )
            ],
            'fantasy': [
                Enhancement(
                    category='visuals',
                    title='Magical Particle Effects',
                    description='Add magical sparkles and mystical particle effects',
                    implementation='Create CSS/JS particle system for magical effects',
                    priority=7,
                    difficulty='medium',
                    impact='medium'
                )
            ],
            'underwater': [
                Enhancement(
                    category='visuals',
                    title='Underwater Ambiance',
                    description='Add flowing water effects and bubble animations',
                    implementation='Implement underwater CSS animations and effects',
                    priority=6,
                    difficulty='medium',
                    impact='medium'
                )
            ]
        }
        
        return theme_suggestions.get(theme, [])

# Example usage and testing
if __name__ == "__main__":
    from advanced_prompt_interpreter import AdvancedPromptInterpreter
    
    interpreter = AdvancedPromptInterpreter()
    assistant = AIStylistAssistant()
    
    # Test game analysis
    test_config = interpreter.interpret_prompt("a cyberpunk racing game with neon lights")
    test_assets = {'mobile_compatible': True, 'title': 'Neon Speed'}
    
    analysis = assistant.analyze_game(test_config, test_assets)
    print("Game Analysis:")
    print(f"Overall Score: {analysis.overall_score}/100")
    print(f"Strengths: {analysis.strengths}")
    print(f"Suggestions: {[s.title for s in analysis.suggestions]}")
    
    # Test brainstorming
    ideas = assistant.brainstorm_game_ideas("space", "shooter")
    print(f"\nBrainstormed Ideas: {[idea['title'] for idea in ideas]}")
    
    # Test feedback processing
    feedback = "The game is too easy and boring"
    enhancements = assistant.process_feedback(feedback, test_config)
    print(f"\nFeedback Enhancements: {[e.title for e in enhancements]}")
