#!/usr/bin/env python3
"""
🧠 INTELLIGENT TEXT ASSISTANT
Advanced AI assistant that can help with game creation and improvement
Integrates with the Ultimate Game Engine for real-time game modifications
"""

import json
import os
import requests
import time
from datetime import datetime
import re

class IntelligentTextAssistant:
    def __init__(self, game_engine=None):
        self.api_key = os.getenv('GROQ_API_KEY')
        self.game_engine = game_engine
        self.conversation_history = []
        self.current_game_context = None
        
    def chat(self, user_message, game_context=None):
        """
        Main chat function that handles all user interactions
        """
        try:
            user_message = user_message.strip()
            if not user_message:
                return self._create_response("Hello! How can I help you create or improve games today?")
            
            print(f"🧠 Processing message: {user_message[:50]}...")
            
            # Update game context if provided
            if game_context:
                self.current_game_context = game_context
            
            # Add to conversation history
            self.conversation_history.append({
                "role": "user",
                "content": user_message,
                "timestamp": datetime.now().isoformat()
            })
            
            # Determine intent and respond accordingly
            intent = self._analyze_intent(user_message)
            
            if intent == "game_creation":
                return self._handle_game_creation(user_message)
            elif intent == "game_improvement":
                return self._handle_game_improvement(user_message)
            elif intent == "game_help":
                return self._handle_game_help(user_message)
            elif intent == "general_chat":
                return self._handle_general_chat(user_message)
            else:
                return self._handle_ai_chat(user_message)
                
        except Exception as e:
            print(f"❌ Chat error: {e}")
            return self._create_response("I'm having trouble processing that. Could you try rephrasing your request?")
    
    def _analyze_intent(self, message):
        """Analyze user intent from message"""
        message_lower = message.lower()
        
        # Game creation intents
        creation_keywords = ['create', 'make', 'build', 'generate', 'new game', 'game about', 'game where']
        if any(keyword in message_lower for keyword in creation_keywords):
            return "game_creation"
        
        # Game improvement intents
        improvement_keywords = ['improve', 'better', 'enhance', 'modify', 'change', 'add', 'fix', 'update']
        if any(keyword in message_lower for keyword in improvement_keywords) and ('game' in message_lower or self.current_game_context):
            return "game_improvement"
        
        # Game help intents
        help_keywords = ['how to', 'help', 'explain', 'what is', 'tutorial', 'guide']
        if any(keyword in message_lower for keyword in help_keywords):
            return "game_help"
        
        # General chat
        general_keywords = ['hello', 'hi', 'thanks', 'thank you', 'bye', 'goodbye']
        if any(keyword in message_lower for keyword in general_keywords):
            return "general_chat"
        
        return "ai_chat"
    
    def _handle_game_creation(self, message):
        """Handle game creation requests"""
        try:
            # Extract game description from message
            game_description = self._extract_game_description(message)
            
            if not game_description:
                return self._create_response(
                    "I'd love to help you create a game! Could you describe what kind of game you want? For example: 'Create a space shooter where you defend Earth from aliens' or 'Make a puzzle game with falling blocks'."
                )
            
            # Create the game using the game engine
            if self.game_engine:
                print(f"🎮 Creating game: {game_description}")
                game_result = self.game_engine.generate_game(game_description)
                
                if game_result and game_result.get('success'):
                    self.current_game_context = game_result
                    
                    response_text = f"""🎉 **Game Created Successfully!**

**{game_result['title']}**
{game_result['description']}

Your game is ready to play! Here are some things you can do:

🎮 **Play your game** - Click the play button to test it out
✨ **Improve it** - Tell me what you'd like to change (e.g., "make it harder", "add more colors", "change the controls")
🎯 **Create another** - Describe a different game you'd like to make
📱 **Share it** - Your game works on both mobile and desktop

What would you like to do next?"""
                    
                    return self._create_response(response_text, game_result)
                else:
                    return self._create_response(
                        "I had trouble creating that game. Could you try describing it differently? For example, mention the main gameplay mechanics or what the player does."
                    )
            else:
                return self._create_response(
                    "The game creation system isn't available right now. Please try again in a moment."
                )
                
        except Exception as e:
            print(f"❌ Game creation error: {e}")
            return self._create_response(
                "I encountered an issue while creating your game. Could you try describing it again with more details?"
            )
    
    def _handle_game_improvement(self, message):
        """Handle game improvement requests"""
        try:
            if not self.current_game_context:
                return self._create_response(
                    "I don't see a current game to improve. Could you create a game first, or tell me which game you'd like to modify?"
                )
            
            # Extract improvement request
            improvement_request = self._extract_improvement_request(message)
            
            if not improvement_request:
                return self._create_response(
                    "I'd be happy to improve your game! What would you like to change? For example: 'make it faster', 'add more enemies', 'change the colors', or 'make it easier'."
                )
            
            # Improve the game using the game engine
            if self.game_engine:
                print(f"🔧 Improving game: {improvement_request}")
                game_id = self.current_game_context.get('game_id')
                improved_game = self.game_engine.improve_game(game_id, improvement_request)
                
                if improved_game and improved_game.get('success'):
                    self.current_game_context = improved_game
                    
                    response_text = f"""✨ **Game Improved!**

**{improved_game['title']}**
{improved_game['description']}

I've updated your game based on your request: "{improvement_request}"

🎮 **Try it out** - Play the improved version
🔧 **More changes?** - Tell me what else you'd like to adjust
🎯 **New game?** - Describe a completely different game to create

What do you think of the improvements?"""
                    
                    return self._create_response(response_text, improved_game)
                else:
                    return self._create_response(
                        "I had trouble making those improvements. Could you try describing the changes differently?"
                    )
            else:
                return self._create_response(
                    "The game improvement system isn't available right now. Please try again in a moment."
                )
                
        except Exception as e:
            print(f"❌ Game improvement error: {e}")
            return self._create_response(
                "I encountered an issue while improving your game. Could you try describing the changes again?"
            )
    
    def _handle_game_help(self, message):
        """Handle help and tutorial requests"""
        message_lower = message.lower()
        
        if 'create' in message_lower or 'make' in message_lower:
            return self._create_response("""🎮 **How to Create Games**

Creating games with me is super easy! Just describe what you want:

**Examples:**
• "Create a space shooter where you defend Earth"
• "Make a puzzle game with falling blocks"
• "Build a racing game on the moon"
• "Create a cooking game where you make pizza"

**Tips:**
• Be specific about what the player does
• Mention the theme or setting
• Describe the main challenge or goal

**I can create:**
• Puzzle games • Shooter games • Racing games
• Cooking games • Memory games • Adventure games
• And many more unique types!

What kind of game would you like to create?""")
        
        elif 'improve' in message_lower or 'modify' in message_lower:
            return self._create_response("""✨ **How to Improve Games**

After creating a game, you can ask me to improve it:

**Examples:**
• "Make it harder" → I'll add more challenges
• "Change the colors" → I'll update the visual style
• "Add more enemies" → I'll increase the difficulty
• "Make it faster" → I'll speed up the gameplay
• "Add sound effects" → I'll include audio feedback

**Types of improvements:**
• Difficulty adjustments • Visual enhancements
• New features • Control changes
• Performance optimizations • Mobile improvements

Just tell me what you'd like to change and I'll update your game!""")
        
        else:
            return self._create_response("""🧠 **AI Game Assistant Help**

I'm your intelligent game creation assistant! Here's what I can do:

**🎮 Create Games**
Describe any game idea and I'll build it for you with full HTML5 code, mobile controls, and professional styling.

**✨ Improve Games**
Tell me how to make your games better - I can modify difficulty, graphics, features, and more.

**💬 Chat & Help**
Ask me questions about game development, get suggestions, or just chat about games!

**🎯 Examples to try:**
• "Create a tower defense game with magical creatures"
• "Make the game more challenging"
• "How do I create a memory game?"
• "Add more visual effects to my game"

What would you like to do first?""")
    
    def _handle_general_chat(self, message):
        """Handle general conversation"""
        message_lower = message.lower()
        
        if any(greeting in message_lower for greeting in ['hello', 'hi', 'hey']):
            return self._create_response("""👋 **Hello! Welcome to the AI Game Studio!**

I'm your intelligent game creation assistant. I can help you:

🎮 **Create unique games** from any description
✨ **Improve existing games** with your feedback  
💬 **Answer questions** about game development
🎯 **Provide suggestions** for game ideas

Ready to create something amazing? Just describe a game you'd like to make!

**Popular requests:**
• "Create a space adventure game"
• "Make a puzzle game with colors"
• "Build a racing game with power-ups"

What sounds fun to you?""")
        
        elif any(thanks in message_lower for thanks in ['thank', 'thanks']):
            return self._create_response("""😊 **You're very welcome!**

I'm glad I could help! Creating games should be fun and accessible for everyone.

🎮 **Want to create another game?** Just describe what you have in mind!
✨ **Need improvements?** Tell me how to make your current game better!
💡 **Looking for ideas?** I can suggest popular game types to try!

I'm here whenever you need help with game creation!""")
        
        elif any(bye in message_lower for bye in ['bye', 'goodbye', 'see you']):
            return self._create_response("""👋 **Goodbye! Thanks for using the AI Game Studio!**

🎮 Your games will be saved and ready when you return
✨ Come back anytime to create more amazing games
💡 Don't forget to share your creations with friends!

Happy gaming! 🎯""")
        
        else:
            return self._handle_ai_chat(message)
    
    def _handle_ai_chat(self, message):
        """Handle general AI conversation using GROQ"""
        try:
            if not self.api_key:
                return self._create_response(
                    "I'd love to chat, but I'm focused on helping you create amazing games! What kind of game would you like to make?"
                )
            
            # Create context-aware prompt
            system_prompt = """You are an intelligent game creation assistant. You help users create and improve games through natural conversation. 

Key capabilities:
- Create unique HTML5 games from any description
- Improve existing games based on user feedback
- Provide game development advice and suggestions
- Maintain a friendly, encouraging tone

Always try to steer conversations toward game creation while being helpful and engaging."""
            
            # Prepare conversation for AI
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add recent conversation history (last 5 messages)
            recent_history = self.conversation_history[-5:] if len(self.conversation_history) > 5 else self.conversation_history
            for msg in recent_history:
                messages.append({"role": msg["role"], "content": msg["content"]})
            
            # Add current message
            messages.append({"role": "user", "content": message})
            
            # Call GROQ API
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                "messages": messages,
                "model": "llama3-8b-8192",
                "temperature": 0.7,
                "max_tokens": 500
            }
            
            response = requests.post(
                'https://api.groq.com/openai/v1/chat/completions',
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content'].strip()
                
                # Add AI response to history
                self.conversation_history.append({
                    "role": "assistant",
                    "content": ai_response,
                    "timestamp": datetime.now().isoformat()
                })
                
                return self._create_response(ai_response)
            else:
                print(f"❌ GROQ API error: {response.status_code}")
                return self._create_response(
                    "I'm having trouble with my AI systems right now. But I can still help you create games! What kind of game would you like to make?"
                )
                
        except Exception as e:
            print(f"❌ AI chat error: {e}")
            return self._create_response(
                "I'm having some technical difficulties. Let's focus on creating an amazing game! What would you like to build?"
            )
    
    def _extract_game_description(self, message):
        """Extract game description from user message"""
        message = message.strip()
        
        # Remove common prefixes
        prefixes = [
            'create a game', 'make a game', 'build a game', 'generate a game',
            'create', 'make', 'build', 'generate', 'i want', 'can you',
            'please', 'could you'
        ]
        
        message_lower = message.lower()
        for prefix in prefixes:
            if message_lower.startswith(prefix):
                message = message[len(prefix):].strip()
                break
        
        # Clean up common words
        cleanup_words = ['about', 'where', 'that', 'with']
        words = message.split()
        if words and words[0].lower() in cleanup_words:
            message = ' '.join(words[1:])
        
        return message.strip() if len(message.strip()) > 3 else None
    
    def _extract_improvement_request(self, message):
        """Extract improvement request from user message"""
        message = message.strip()
        
        # Remove common prefixes
        prefixes = [
            'improve the game', 'make the game', 'change the game',
            'improve it', 'make it', 'change it', 'modify it',
            'can you', 'please', 'could you'
        ]
        
        message_lower = message.lower()
        for prefix in prefixes:
            if message_lower.startswith(prefix):
                message = message[len(prefix):].strip()
                break
        
        return message.strip() if len(message.strip()) > 2 else None
    
    def _create_response(self, text, game_data=None):
        """Create standardized response format"""
        response = {
            "success": True,
            "message": text,
            "timestamp": datetime.now().isoformat(),
            "has_game": bool(game_data)
        }
        
        if game_data:
            response["game"] = game_data
        
        return response
    
    def get_conversation_history(self):
        """Get conversation history"""
        return self.conversation_history
    
    def clear_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
        self.current_game_context = None
    
    def set_game_context(self, game_data):
        """Set current game context"""
        self.current_game_context = game_data

# Create global instance
text_assistant = IntelligentTextAssistant()

def chat_with_assistant(message, game_context=None):
    """Main function for external use"""
    return text_assistant.chat(message, game_context)

def set_game_engine(game_engine):
    """Set the game engine for the assistant"""
    text_assistant.game_engine = game_engine

# Export functions
__all__ = ['chat_with_assistant', 'set_game_engine']
