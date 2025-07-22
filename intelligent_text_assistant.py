#!/usr/bin/env python3
"""
🧠 Intelligent Text Assistant - Final Version
Provides intelligent chat assistance for game creation
Contains the exact TextAssistant class that main.py expects
"""

import os
import json
import requests
from datetime import datetime


class TextAssistant:
    """Intelligent text assistant for game creation help"""
    
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.groq_api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.conversation_history = []
        
    def get_response(self, user_message):
        """Get intelligent response to user message"""
        try:
            print(f"🧠 Processing message: {user_message[:50]}...")
            
            # Add user message to history
            self.conversation_history.append({
                "role": "user", 
                "content": user_message,
                "timestamp": datetime.now().isoformat()
            })
            
            if self.groq_api_key:
                response = self._get_ai_response(user_message)
            else:
                response = self._get_fallback_response(user_message)
                
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": response["response"],
                "timestamp": datetime.now().isoformat()
            })
            
            return response
            
        except Exception as e:
            print(f"❌ Text assistant error: {e}")
            return self._get_fallback_response(user_message)
    
    def _get_ai_response(self, user_message):
        """Get response using GROQ AI"""
        try:
            headers = {
                "Authorization": f"Bearer {self.groq_api_key}",
                "Content-Type": "application/json",
            }
            
            # Create context-aware prompt
            system_prompt = self._create_system_prompt()
            
            data = {
                "model": "llama3-8b-8192",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                "temperature": 0.7,
                "max_tokens": 500,
            }
            
            response = requests.post(
                self.groq_api_url, headers=headers, json=data, timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result["choices"][0]["message"]["content"]
                
                return {
                    "response": ai_response,
                    "type": "ai_assistant",
                    "timestamp": datetime.now().isoformat(),
                    "source": "groq_ai"
                }
            else:
                print(f"❌ GROQ API error: {response.status_code}")
                return self._get_fallback_response(user_message)
                
        except Exception as e:
            print(f"❌ AI response error: {e}")
            return self._get_fallback_response(user_message)
    
    def _create_system_prompt(self):
        """Create system prompt for AI assistant"""
        return """You are an expert AI game creation assistant for the Mythiq Gateway platform. You help users create amazing games by:

1. **Game Creation Guidance**: Help users describe their game ideas clearly and suggest improvements
2. **Creative Suggestions**: Provide creative ideas for game mechanics, themes, and features
3. **Technical Help**: Explain how the AI game generation works and what's possible
4. **Encouragement**: Be enthusiastic and supportive about their game ideas

Key capabilities of the platform:
- Creates unique HTML5 games from any description
- Supports multiple genres: adventure, puzzle, racing, cooking, space, fantasy
- Games work on mobile and desktop
- Each game is completely unique and matches the user's description

Guidelines:
- Be helpful, friendly, and encouraging
- Ask clarifying questions to improve their game ideas
- Suggest specific game mechanics and features
- Explain what makes a good game description
- Keep responses concise but informative
- Use emojis to make responses engaging

Examples of great game descriptions:
- "A magical fairy collecting glowing mushrooms while avoiding dark spirits in an enchanted forest"
- "A space adventure where you pilot a ship through asteroid fields collecting energy crystals"
- "A cooking game where you race against time to prepare recipes for demanding customers"

Always encourage creativity and help users refine their ideas into amazing games!"""

    def _get_fallback_response(self, user_message):
        """Get fallback response when AI is unavailable"""
        message_lower = user_message.lower()
        
        # Game creation help
        if any(word in message_lower for word in ["create", "make", "game", "how"]):
            if any(word in message_lower for word in ["fairy", "magic", "fantasy"]):
                response = "🧚‍♀️ Great choice! For a magical fairy game, try describing: 'A fairy adventure where you collect glowing mushrooms while avoiding dark spirits in an enchanted forest.' The more details you add about the character, objectives, and obstacles, the more unique your game will be!"
            elif any(word in message_lower for word in ["space", "alien", "rocket"]):
                response = "🚀 Awesome! For a space game, try: 'A space adventure where you pilot a ship through asteroid fields, collecting energy crystals while avoiding alien enemies.' Add details about your spaceship, the challenges you face, and what you're trying to achieve!"
            elif any(word in message_lower for word in ["cook", "food", "recipe"]):
                response = "👨‍🍳 Perfect! For a cooking game, describe: 'A cooking challenge where you prepare recipes under time pressure, selecting the right ingredients and following cooking steps.' Mention specific dishes, time limits, and cooking techniques!"
            elif any(word in message_lower for word in ["race", "car", "speed"]):
                response = "🏎️ Exciting! For a racing game, try: 'A high-speed racing game where you drive through traffic, collect power-ups, and avoid obstacles on a busy highway.' Describe the environment, challenges, and special features!"
            else:
                response = "🎮 I'd love to help you create an amazing game! To get started, describe your game idea with details like:\n\n• What's the main character or player?\n• What's the objective or goal?\n• What challenges or obstacles are there?\n• What's the setting or theme?\n\nFor example: 'A magical fairy collecting glowing mushrooms while avoiding dark spirits in an enchanted forest.' The more creative details you add, the more unique your game will be!"
        
        # Platform capabilities
        elif any(word in message_lower for word in ["what", "can", "do", "capable"]):
            response = "✨ I can help you create incredible games! Here's what our AI can do:\n\n🎮 **Generate Unique Games**: Create completely custom games from your descriptions\n🎨 **Multiple Genres**: Fantasy, space, cooking, racing, puzzles, and more\n📱 **Mobile & Desktop**: Games work perfectly on all devices\n🧠 **Smart AI**: Uses advanced AI to match your exact vision\n💡 **Creative Help**: I'll help you refine ideas and suggest improvements\n\nJust describe any game idea and watch the magic happen!"
        
        # Encouragement and tips
        elif any(word in message_lower for word in ["help", "stuck", "idea", "suggest"]):
            response = "💡 Here are some creative game ideas to inspire you:\n\n🧚‍♀️ **Fantasy**: 'A wizard's apprentice collecting spell ingredients while avoiding magical traps'\n🚀 **Space**: 'An astronaut exploring alien planets and discovering mysterious artifacts'\n🍳 **Cooking**: 'A chef competing in a cooking tournament with exotic ingredients'\n🏎️ **Racing**: 'A futuristic racer speeding through neon-lit cyberpunk cities'\n🧩 **Puzzle**: 'A detective solving mysteries by connecting clues and evidence'\n\nPick one that excites you and add your own creative twist!"
        
        # General encouragement
        else:
            response = f"Thanks for your message! 🎮 I'm here to help you create amazing games. Whether you want to build a magical adventure, space exploration, cooking challenge, or any other type of game, I can guide you through the process.\n\nWhat kind of game would you like to create today? Just describe your idea and I'll help you make it even better!"
        
        return {
            "response": response,
            "type": "fallback_assistant",
            "timestamp": datetime.now().isoformat(),
            "source": "fallback_system"
        }
    
    def get_conversation_history(self):
        """Get the conversation history"""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        return {"status": "cleared", "message": "Conversation history cleared"}
    
    def get_game_creation_tips(self):
        """Get tips for creating better games"""
        return {
            "tips": [
                "🎯 Be specific about your game's objective",
                "🎨 Describe the visual style and theme",
                "⚡ Mention the main challenges or obstacles",
                "🎮 Include details about player actions",
                "🌟 Add unique elements that make it special",
                "📱 Consider how it will work on mobile devices"
            ],
            "examples": [
                "Instead of 'a racing game', try 'a futuristic racing game through neon-lit cities with gravity-defying tracks'",
                "Instead of 'a puzzle game', try 'a magical puzzle where you rotate crystal formations to create light patterns'",
                "Instead of 'a cooking game', try 'a time-pressure cooking game where you prepare alien cuisine for intergalactic customers'"
            ]
        }


# Export the TextAssistant class for main.py
__all__ = ["TextAssistant"]
