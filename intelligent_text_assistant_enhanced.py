"""
Intelligent Text Assistant - Enhanced Edition
Advanced AI assistant for game creation, improvement, and guidance

Features:
- Natural language game creation guidance
- Real-time game analysis and improvement suggestions
- Creative brainstorming and idea enhancement
- Technical game development advice
- User-friendly explanations and tutorials
"""

import json
import re
import random
from datetime import datetime
import os

class GameAnalyzer:
    """Analyzes games and provides improvement suggestions"""
    
    def __init__(self):
        self.improvement_categories = {
            'gameplay': ['mechanics', 'difficulty', 'progression', 'balance', 'objectives'],
            'visual': ['graphics', 'colors', 'animations', 'effects', 'ui'],
            'audio': ['music', 'sound effects', 'ambient', 'feedback'],
            'story': ['narrative', 'characters', 'dialogue', 'world building'],
            'technical': ['performance', 'controls', 'responsiveness', 'compatibility']
        }
        
        self.enhancement_suggestions = {
            'gameplay': [
                "Add power-ups that temporarily boost player abilities",
                "Implement a combo system for skilled players",
                "Create multiple difficulty levels for different skill levels",
                "Add boss battles at the end of each level",
                "Include hidden secrets and easter eggs to discover",
                "Implement a scoring system with multipliers",
                "Add time-based challenges for extra excitement",
                "Create unlockable content as rewards for progression"
            ],
            'visual': [
                "Add particle effects for more visual impact",
                "Implement smooth animations for character movements",
                "Use color gradients to create depth and atmosphere",
                "Add visual feedback for player actions",
                "Create themed backgrounds that match the game world",
                "Implement screen shake effects for impactful moments",
                "Add glowing effects for important game elements",
                "Use contrasting colors to highlight interactive objects"
            ],
            'audio': [
                "Add background music that matches the game theme",
                "Include sound effects for player actions and feedback",
                "Create ambient sounds to enhance the game atmosphere",
                "Add audio cues for important game events",
                "Implement dynamic music that changes with gameplay",
                "Include victory and defeat sound effects",
                "Add subtle audio feedback for UI interactions",
                "Create themed sound effects that match the game world"
            ],
            'story': [
                "Develop a compelling backstory for the main character",
                "Create an engaging narrative that drives player motivation",
                "Add dialogue or text that explains the game world",
                "Implement character development and growth",
                "Create meaningful choices that affect the story",
                "Add lore and world-building elements",
                "Develop interesting antagonists and conflicts",
                "Include emotional moments that connect with players"
            ],
            'technical': [
                "Optimize game performance for smooth gameplay",
                "Implement responsive controls for better player experience",
                "Add mobile touch controls for accessibility",
                "Ensure consistent frame rate across different devices",
                "Implement proper collision detection",
                "Add keyboard shortcuts for power users",
                "Optimize loading times and resource usage",
                "Ensure cross-platform compatibility"
            ]
        }
    
    def analyze_game_concept(self, description):
        """Analyze a game concept and provide detailed feedback"""
        analysis = {
            'strengths': [],
            'improvements': [],
            'suggestions': [],
            'theme_analysis': {},
            'complexity_score': 0
        }
        
        description_lower = description.lower()
        
        # Identify strengths
        if any(word in description_lower for word in ['unique', 'original', 'creative', 'innovative']):
            analysis['strengths'].append("Creative and original concept")
        
        if any(word in description_lower for word in ['collect', 'gather', 'find']):
            analysis['strengths'].append("Clear collection-based objective")
        
        if any(word in description_lower for word in ['avoid', 'dodge', 'escape']):
            analysis['strengths'].append("Engaging challenge mechanics")
        
        if any(word in description_lower for word in ['magical', 'mystical', 'enchanted', 'fantasy']):
            analysis['strengths'].append("Rich fantasy theming")
        
        # Suggest improvements
        if 'story' not in description_lower and 'narrative' not in description_lower:
            analysis['improvements'].append("Consider adding a backstory or narrative element")
        
        if 'level' not in description_lower and 'stage' not in description_lower:
            analysis['improvements'].append("Think about level progression and difficulty scaling")
        
        if 'power' not in description_lower and 'ability' not in description_lower:
            analysis['improvements'].append("Consider adding special abilities or power-ups")
        
        # Generate specific suggestions
        for category, suggestions in self.enhancement_suggestions.items():
            analysis['suggestions'].extend(random.sample(suggestions, min(2, len(suggestions))))
        
        # Calculate complexity score
        complexity_factors = [
            len(re.findall(r'\b(character|enemy|obstacle|collectible|power|ability)\w*\b', description_lower)),
            len(re.findall(r'\b(level|stage|world|area|zone)\w*\b', description_lower)),
            len(re.findall(r'\b(mechanic|system|feature|element)\w*\b', description_lower))
        ]
        analysis['complexity_score'] = min(10, sum(complexity_factors) * 2)
        
        return analysis

class CreativeAssistant:
    """Provides creative guidance and brainstorming support"""
    
    def __init__(self):
        self.game_genres = {
            'action': ['platformer', 'shooter', 'fighting', 'beat-em-up'],
            'adventure': ['exploration', 'quest', 'puzzle-adventure', 'story-driven'],
            'puzzle': ['logic', 'matching', 'physics', 'word'],
            'strategy': ['real-time', 'turn-based', 'tower-defense', 'resource-management'],
            'simulation': ['life-sim', 'building', 'management', 'sandbox'],
            'racing': ['arcade', 'simulation', 'kart', 'futuristic'],
            'rpg': ['fantasy', 'sci-fi', 'modern', 'historical'],
            'casual': ['match-3', 'endless-runner', 'clicker', 'time-management']
        }
        
        self.theme_elements = {
            'fantasy': {
                'characters': ['wizard', 'knight', 'fairy', 'dragon', 'elf', 'dwarf'],
                'settings': ['castle', 'forest', 'dungeon', 'tower', 'village', 'mountain'],
                'objects': ['sword', 'magic', 'potion', 'treasure', 'crystal', 'scroll'],
                'enemies': ['goblin', 'orc', 'skeleton', 'demon', 'witch', 'monster']
            },
            'sci-fi': {
                'characters': ['astronaut', 'alien', 'robot', 'cyborg', 'scientist', 'pilot'],
                'settings': ['spaceship', 'planet', 'station', 'laboratory', 'colony', 'nebula'],
                'objects': ['laser', 'crystal', 'technology', 'energy', 'data', 'artifact'],
                'enemies': ['alien', 'robot', 'mutant', 'virus', 'ai', 'invader']
            },
            'modern': {
                'characters': ['hero', 'detective', 'agent', 'soldier', 'civilian', 'expert'],
                'settings': ['city', 'building', 'street', 'office', 'warehouse', 'rooftop'],
                'objects': ['weapon', 'vehicle', 'gadget', 'document', 'key', 'phone'],
                'enemies': ['criminal', 'terrorist', 'spy', 'gang', 'corrupt', 'villain']
            }
        }
    
    def generate_game_ideas(self, user_input):
        """Generate creative game ideas based on user input"""
        ideas = []
        user_lower = user_input.lower()
        
        # Identify themes and genres from input
        detected_themes = []
        for theme, elements in self.theme_elements.items():
            if any(element in user_lower for element_list in elements.values() for element in element_list):
                detected_themes.append(theme)
        
        if not detected_themes:
            detected_themes = ['fantasy']  # Default theme
        
        # Generate ideas for each detected theme
        for theme in detected_themes[:2]:  # Limit to 2 themes
            elements = self.theme_elements[theme]
            
            for i in range(3):  # Generate 3 ideas per theme
                character = random.choice(elements['characters'])
                setting = random.choice(elements['settings'])
                object_item = random.choice(elements['objects'])
                enemy = random.choice(elements['enemies'])
                
                idea = f"A {character} exploring a {setting}, collecting {object_item}s while avoiding {enemy}s"
                ideas.append(idea)
        
        return ideas
    
    def enhance_game_concept(self, concept):
        """Enhance a basic game concept with additional details"""
        enhancements = {
            'mechanics': [],
            'story': [],
            'features': [],
            'progression': []
        }
        
        concept_lower = concept.lower()
        
        # Suggest mechanics based on concept
        if 'collect' in concept_lower:
            enhancements['mechanics'].extend([
                "Add a combo system for collecting multiple items quickly",
                "Include rare collectibles that provide bonus points",
                "Implement a collection meter that unlocks special abilities"
            ])
        
        if 'avoid' in concept_lower:
            enhancements['mechanics'].extend([
                "Add temporary invincibility power-ups",
                "Include slow-motion abilities for precise dodging",
                "Implement a shield system for protection"
            ])
        
        # Suggest story elements
        enhancements['story'].extend([
            "Create a compelling reason why the character needs to collect these items",
            "Develop a backstory that explains the world and its dangers",
            "Add a final boss or ultimate challenge to overcome"
        ])
        
        # Suggest features
        enhancements['features'].extend([
            "Add multiple levels with increasing difficulty",
            "Include different environments and themes",
            "Implement a scoring system with leaderboards",
            "Add achievements and unlockable content"
        ])
        
        # Suggest progression
        enhancements['progression'].extend([
            "Start with simple mechanics and gradually introduce complexity",
            "Unlock new abilities as the player progresses",
            "Increase the number and speed of obstacles over time",
            "Add boss battles at key progression points"
        ])
        
        return enhancements

class TextAssistant:
    """Main text assistant class that provides comprehensive game creation support"""
    
    def __init__(self):
        self.game_analyzer = GameAnalyzer()
        self.creative_assistant = CreativeAssistant()
        self.conversation_history = []
        
        self.response_templates = {
            'greeting': [
                "Hello! I'm your AI game creation assistant. I'm here to help you create amazing games!",
                "Welcome to the ultimate game creation studio! What kind of game would you like to create today?",
                "Hi there! I'm excited to help you bring your game ideas to life. What's your vision?"
            ],
            'game_creation': [
                "That sounds like an fantastic game concept! Let me help you develop it further.",
                "I love that idea! Here's how we can make it even more engaging:",
                "Great concept! I can see a lot of potential. Let's enhance it together."
            ],
            'improvement': [
                "I've analyzed your game and have some exciting suggestions to make it even better!",
                "Here are some ways we can enhance your game to make it more engaging:",
                "I see several opportunities to take your game to the next level:"
            ],
            'technical': [
                "Let me help you with the technical aspects of your game:",
                "Here's how we can implement that feature:",
                "From a technical standpoint, here's what I recommend:"
            ]
        }
    
    def get_response(self, user_message):
        """Generate an intelligent response to user messages"""
        try:
            user_message_lower = user_message.lower()
            
            # Store conversation history
            self.conversation_history.append({
                'user': user_message,
                'timestamp': datetime.now().isoformat()
            })
            
            response_data = {
                'response': '',
                'type': 'assistant',
                'timestamp': datetime.now().isoformat(),
                'suggestions': [],
                'analysis': None
            }
            
            # Determine response type and generate appropriate response
            if any(greeting in user_message_lower for greeting in ['hello', 'hi', 'hey', 'start']):
                response_data['response'] = self._generate_greeting_response()
                response_data['type'] = 'greeting'
            
            elif any(word in user_message_lower for word in ['create', 'make', 'build', 'generate']):
                response_data = self._handle_game_creation_request(user_message)
            
            elif any(word in user_message_lower for word in ['improve', 'enhance', 'better', 'upgrade']):
                response_data = self._handle_improvement_request(user_message)
            
            elif any(word in user_message_lower for word in ['help', 'how', 'what', 'explain']):
                response_data = self._handle_help_request(user_message)
            
            elif any(word in user_message_lower for word in ['idea', 'suggest', 'brainstorm']):
                response_data = self._handle_brainstorming_request(user_message)
            
            else:
                response_data = self._handle_general_conversation(user_message)
            
            # Add conversation to history
            self.conversation_history.append({
                'assistant': response_data['response'],
                'timestamp': response_data['timestamp']
            })
            
            return response_data
            
        except Exception as e:
            return {
                'response': f"I'm here to help you create amazing games! What would you like to work on today?",
                'type': 'fallback',
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def _generate_greeting_response(self):
        """Generate a friendly greeting response"""
        greeting = random.choice(self.response_templates['greeting'])
        
        tips = [
            "💡 Try describing a game idea like: 'A magical fairy collecting glowing mushrooms'",
            "🎮 I can help you create games in any theme: fantasy, sci-fi, adventure, and more!",
            "✨ Ask me to improve existing games or brainstorm new ideas",
            "🚀 I can provide technical advice and creative suggestions"
        ]
        
        tip = random.choice(tips)
        
        return f"{greeting}\n\n{tip}\n\nWhat would you like to create today?"
    
    def _handle_game_creation_request(self, user_message):
        """Handle requests to create games"""
        response_intro = random.choice(self.response_templates['game_creation'])
        
        # Analyze the game concept
        analysis = self.game_analyzer.analyze_game_concept(user_message)
        
        # Generate creative suggestions
        ideas = self.creative_assistant.generate_game_ideas(user_message)
        enhancements = self.creative_assistant.enhance_game_concept(user_message)
        
        response = f"{response_intro}\n\n"
        
        if analysis['strengths']:
            response += "🌟 **Strengths of your concept:**\n"
            for strength in analysis['strengths']:
                response += f"• {strength}\n"
            response += "\n"
        
        if analysis['improvements']:
            response += "🎯 **Areas to consider:**\n"
            for improvement in analysis['improvements']:
                response += f"• {improvement}\n"
            response += "\n"
        
        response += "💡 **Enhancement suggestions:**\n"
        for category, suggestions in enhancements.items():
            if suggestions:
                response += f"**{category.title()}:** {suggestions[0]}\n"
        
        response += "\n🎮 Ready to create your game? Just click the 'Create Game' button!"
        
        return {
            'response': response,
            'type': 'game_creation',
            'timestamp': datetime.now().isoformat(),
            'suggestions': ideas[:3],
            'analysis': analysis
        }
    
    def _handle_improvement_request(self, user_message):
        """Handle requests to improve games"""
        response_intro = random.choice(self.response_templates['improvement'])
        
        # Analyze for improvement opportunities
        analysis = self.game_analyzer.analyze_game_concept(user_message)
        
        response = f"{response_intro}\n\n"
        
        # Provide specific improvement suggestions
        improvements = []
        for category, suggestion_list in self.game_analyzer.enhancement_suggestions.items():
            improvements.extend(random.sample(suggestion_list, min(2, len(suggestion_list))))
        
        response += "🚀 **Improvement suggestions:**\n"
        for i, improvement in enumerate(improvements[:6], 1):
            response += f"{i}. {improvement}\n"
        
        response += "\n💬 Tell me more about your game and I can provide more specific suggestions!"
        
        return {
            'response': response,
            'type': 'improvement',
            'timestamp': datetime.now().isoformat(),
            'suggestions': improvements[:6],
            'analysis': analysis
        }
    
    def _handle_help_request(self, user_message):
        """Handle help and how-to requests"""
        help_topics = {
            'create': "To create a game, simply describe your idea in detail. For example: 'A space adventure where you collect energy crystals while avoiding alien ships.' The more details you provide, the better I can help!",
            'improve': "To improve a game, tell me about the current game and what aspects you'd like to enhance. I can suggest improvements for gameplay, visuals, story, and technical aspects.",
            'ideas': "For game ideas, tell me what themes or genres interest you. I can brainstorm creative concepts based on your preferences!",
            'technical': "For technical help, ask specific questions about game mechanics, controls, or implementation. I can provide guidance on making your games more engaging and polished."
        }
        
        user_lower = user_message.lower()
        
        if 'create' in user_lower or 'make' in user_lower:
            help_text = help_topics['create']
        elif 'improve' in user_lower or 'better' in user_lower:
            help_text = help_topics['improve']
        elif 'idea' in user_lower or 'suggest' in user_lower:
            help_text = help_topics['ideas']
        elif 'technical' in user_lower or 'how' in user_lower:
            help_text = help_topics['technical']
        else:
            help_text = "I'm here to help you create amazing games! Here's what I can do:\n\n🎮 **Create Games:** Describe your idea and I'll help develop it\n🚀 **Improve Games:** Get suggestions to enhance existing games\n💡 **Brainstorm Ideas:** Generate creative game concepts\n🔧 **Technical Advice:** Get help with game mechanics and features"
        
        return {
            'response': help_text,
            'type': 'help',
            'timestamp': datetime.now().isoformat(),
            'suggestions': [],
            'analysis': None
        }
    
    def _handle_brainstorming_request(self, user_message):
        """Handle brainstorming and idea generation requests"""
        ideas = self.creative_assistant.generate_game_ideas(user_message)
        
        response = "🧠 **Creative brainstorming time!** Here are some game ideas based on your interests:\n\n"
        
        for i, idea in enumerate(ideas[:5], 1):
            response += f"{i}. {idea}\n"
        
        response += "\n💡 **Want to develop any of these ideas further?** Just tell me which one interests you and I'll help you flesh it out with more details, mechanics, and features!"
        
        return {
            'response': response,
            'type': 'brainstorming',
            'timestamp': datetime.now().isoformat(),
            'suggestions': ideas,
            'analysis': None
        }
    
    def _handle_general_conversation(self, user_message):
        """Handle general conversation and provide helpful responses"""
        responses = [
            "That's interesting! How can I help you turn that into an amazing game concept?",
            "I love your creativity! Let's work together to develop this into a fantastic game.",
            "Great thinking! What kind of game mechanics would you like to explore?",
            "Fascinating idea! Tell me more about what you envision for the gameplay.",
            "I can see the potential in that concept! What would make it fun and engaging?"
        ]
        
        response = random.choice(responses)
        response += "\n\n🎮 **Some ways I can help:**\n"
        response += "• Develop your ideas into complete game concepts\n"
        response += "• Suggest improvements and enhancements\n"
        response += "• Provide technical guidance and best practices\n"
        response += "• Brainstorm creative solutions to design challenges"
        
        return {
            'response': response,
            'type': 'general',
            'timestamp': datetime.now().isoformat(),
            'suggestions': [],
            'analysis': None
        }

# Test the enhanced assistant
if __name__ == "__main__":
    assistant = TextAssistant()
    
    test_messages = [
        "Hello!",
        "I want to create a magical fairy game",
        "How can I improve my space shooter?",
        "Give me some creative game ideas",
        "Help me make my game better"
    ]
    
    for message in test_messages:
        print(f"\nUser: {message}")
        response = assistant.get_response(message)
        print(f"Assistant: {response['response'][:200]}...")
        if response['suggestions']:
            print(f"Suggestions: {len(response['suggestions'])} provided")
