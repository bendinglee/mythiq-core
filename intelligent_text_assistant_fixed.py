#!/usr/bin/env python3
"""
🧠 Intelligent Text Assistant - Fixed Version
Provides intelligent chat assistance for game creation
Contains the exact TextAssistant class that main.py expects
"""

import os
import json
import requests
from datetime import datetime

class TextAssistant:
    """Intelligent text assistant for game creation guidance"""
    
    def __init__(self):
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        self.groq_api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.conversation_history = []
        
    def get_response(self, user_message):
        """Get intelligent response to user message"""
        try:
            print(f"🧠 Processing message: {user_message[:100]}...")
            
            if self.groq_api_key:
                return self._get_ai_response(user_message)
            else:
                return self._get_fallback_response(user_message)
                
        except Exception as e:
            print(f"❌ Assistant error: {e}")
            return self._get_fallback_response(user_message)
    
    def _get_ai_response(self, user_message):
        """Get response using GROQ AI"""
        try:
            # Add to conversation history
            self.conversation_history.append({"role": "user", "content": user_message})
            
            # Create AI prompt
            system_prompt = """You are an expert AI game creation assistant. You help users create amazing games by:

1. Understanding their game ideas and providing creative suggestions
2. Explaining how to improve existing games
3. Offering tips for game mechanics, themes, and features
4. Being encouraging and enthusiastic about game creation
5. Providing specific, actionable advice

Keep responses helpful, friendly, and focused on game creation. If users ask about non-game topics, gently redirect them back to game creation."""

            # Prepare messages for API
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add recent conversation history (last 10 messages)
            recent_history = self.conversation_history[-10:]
            messages.extend(recent_history)
            
            # Call GROQ API
            headers = {
                "Authorization": f"Bearer {self.groq_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "llama3-8b-8192",
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 500
            }
            
            response = requests.post(self.groq_api_url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                
                # Add to conversation history
                self.conversation_history.append({"role": "assistant", "content": ai_response})
                
                return {
                    "response": ai_response,
                    "type": "ai_generated",
                    "timestamp": datetime.now().isoformat()
                }
            else:
                print(f"❌ GROQ API error: {response.status_code}")
                return self._get_fallback_response(user_message)
                
        except Exception as e:
            print(f"❌ AI response error: {e}")
            return self._get_fallback_response(user_message)
    
    def _get_fallback_response(self, user_message):
        """Get fallback response when AI is unavailable"""
        message_lower = user_message.lower()
        
        # Game creation help
        if any(word in message_lower for word in ['create', 'make', 'build', 'generate']):
            if any(word in message_lower for word in ['game', 'games']):
                return {
                    "response": "🎮 I'd love to help you create a game! Just describe what kind of game you want to make. For example:\n\n• 'A magical forest adventure with fairies'\n• 'A space shooter with aliens and lasers'\n• 'A cooking game where you run a restaurant'\n• 'A racing game with power-ups'\n\nThe more details you give me, the better game I can help you create! What's your game idea?",
                    "type": "fallback",
                    "timestamp": datetime.now().isoformat()
                }
        
        # Game improvement help
        if any(word in message_lower for word in ['improve', 'better', 'enhance', 'upgrade']):
            return {
                "response": "✨ Great question! Here are some ways to improve your games:\n\n🎯 **Gameplay**: Add more levels, power-ups, or challenges\n🎨 **Visuals**: Use better colors, animations, and effects\n🎵 **Audio**: Add sound effects and background music\n📱 **Controls**: Make sure it works well on mobile devices\n🏆 **Scoring**: Add achievements and leaderboards\n\nWhat specific aspect of your game would you like to improve?",
                "type": "fallback",
                "timestamp": datetime.now().isoformat()
            }
        
        # Specific game types
        if any(word in message_lower for word in ['puzzle', 'brain', 'logic']):
            return {
                "response": "🧩 Puzzle games are fantastic! I can help you create:\n\n• Sliding tile puzzles with custom images\n• Color matching games\n• Logic puzzles with unique mechanics\n• Brain teasers with increasing difficulty\n\nWhat kind of puzzle game interests you most?",
                "type": "fallback",
                "timestamp": datetime.now().isoformat()
            }
        
        if any(word in message_lower for word in ['action', 'shooter', 'fight', 'battle']):
            return {
                "response": "⚔️ Action games are exciting! I can create:\n\n• Space shooters with enemies and power-ups\n• Battle games with different weapons\n• Survival games with waves of enemies\n• Fighting games with special moves\n\nDescribe your action game idea and I'll bring it to life!",
                "type": "fallback",
                "timestamp": datetime.now().isoformat()
            }
        
        if any(word in message_lower for word in ['adventure', 'quest', 'explore']):
            return {
                "response": "🗺️ Adventure games are amazing! I can help you create:\n\n• Fantasy quests with magical creatures\n• Exploration games with hidden treasures\n• Story-driven adventures with choices\n• Survival adventures in different worlds\n\nWhat kind of adventure do you want to create?",
                "type": "fallback",
                "timestamp": datetime.now().isoformat()
            }
        
        # General help
        if any(word in message_lower for word in ['help', 'how', 'what', 'can']):
            return {
                "response": "🤖 I'm your AI game creation assistant! Here's how I can help:\n\n🎮 **Create Games**: Describe any game idea and I'll build it for you\n💡 **Give Ideas**: Get suggestions for game mechanics and themes\n🔧 **Improve Games**: Help make your games more fun and engaging\n📱 **Optimize**: Ensure games work great on all devices\n🎨 **Design**: Suggest colors, themes, and visual improvements\n\nJust tell me what kind of game you want to create, or ask me any question about game development!",
                "type": "fallback",
                "timestamp": datetime.now().isoformat()
            }
        
        # Default response
        return {
            "response": f"🎮 Thanks for your message! I'm here to help you create amazing games. \n\nYou said: \"{user_message}\"\n\nI can help you:\n• Create any type of game from your description\n• Improve existing games with new features\n• Suggest game ideas and mechanics\n• Optimize games for mobile devices\n\nWhat kind of game would you like to create today?",
            "type": "fallback",
            "timestamp": datetime.now().isoformat()
        }
    
    def get_game_creation_help(self, game_type):
        """Get specific help for creating different game types"""
        help_responses = {
            "puzzle": "🧩 For puzzle games, think about:\n• What needs to be solved or matched?\n• How difficult should it be?\n• What theme or visuals do you want?\n• Should it have time limits or move counters?",
            
            "action": "⚔️ For action games, consider:\n• What's the main character or vehicle?\n• What enemies or obstacles exist?\n• What weapons or abilities are available?\n• What's the setting or environment?",
            
            "adventure": "🗺️ For adventure games, plan:\n• What's the main quest or goal?\n• What world or setting is it in?\n• What characters or creatures are involved?\n• What items can be collected or used?",
            
            "racing": "🏎️ For racing games, decide:\n• What vehicles are being raced?\n• What's the track or environment like?\n• Are there power-ups or obstacles?\n• What makes it challenging or fun?",
            
            "simulation": "🏗️ For simulation games, think about:\n• What activity is being simulated?\n• What resources need to be managed?\n• What goals or objectives exist?\n• How do players progress or improve?"
        }
        
        return help_responses.get(game_type, "🎮 I can help you create any type of game! Just describe your idea and I'll guide you through the process.")
    
    def analyze_game_description(self, description):
        """Analyze a game description and provide feedback"""
        analysis = {
            "clarity": "good",
            "completeness": "partial",
            "suggestions": [],
            "estimated_complexity": "medium"
        }
        
        description_lower = description.lower()
        word_count = len(description.split())
        
        # Analyze clarity
        if word_count < 5:
            analysis["clarity"] = "needs_improvement"
            analysis["suggestions"].append("Add more details about the gameplay")
        elif word_count > 50:
            analysis["clarity"] = "excellent"
        
        # Analyze completeness
        has_character = any(word in description_lower for word in ['player', 'character', 'hero', 'you'])
        has_goal = any(word in description_lower for word in ['collect', 'avoid', 'defeat', 'reach', 'win'])
        has_setting = any(word in description_lower for word in ['forest', 'space', 'kitchen', 'city', 'world'])
        
        completeness_score = sum([has_character, has_goal, has_setting])
        
        if completeness_score >= 2:
            analysis["completeness"] = "good"
        elif completeness_score == 1:
            analysis["completeness"] = "partial"
            if not has_character:
                analysis["suggestions"].append("Describe the main character or player")
            if not has_goal:
                analysis["suggestions"].append("Explain what the player needs to do to win")
            if not has_setting:
                analysis["suggestions"].append("Describe the game world or environment")
        else:
            analysis["completeness"] = "needs_improvement"
            analysis["suggestions"].append("Add details about the character, goals, and setting")
        
        # Estimate complexity
        complex_words = ['multiple', 'levels', 'different', 'various', 'complex', 'advanced']
        if any(word in description_lower for word in complex_words):
            analysis["estimated_complexity"] = "high"
        elif word_count > 20:
            analysis["estimated_complexity"] = "medium"
        else:
            analysis["estimated_complexity"] = "low"
        
        return analysis

# Export the class for main.py
__all__ = ['TextAssistant']
