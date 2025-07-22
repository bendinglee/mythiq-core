#!/usr/bin/env python3
"""
🎯 SESSION MANAGER - GAME SEED VARIANCE & USER AWARENESS
Advanced session tracking and personalization for unique game experiences
"""

import json
import hashlib
import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from collections import defaultdict

@dataclass
class UserPreferences:
    """User preference tracking"""
    preferred_genres: List[str]
    preferred_difficulty: str
    preferred_colors: List[str]
    accessibility_needs: Dict[str, bool]
    play_style: str
    favorite_mechanics: List[str]
    session_count: int
    total_playtime: int
    last_active: str

@dataclass
class GameSession:
    """Individual game session data"""
    session_id: str
    user_id: str
    game_id: str
    genre: str
    start_time: str
    end_time: Optional[str]
    duration: int
    score: int
    completed: bool
    difficulty: str
    actions_taken: int
    preferences_learned: Dict[str, Any]

class SessionManager:
    """Manages user sessions and learning preferences"""
    
    def __init__(self):
        self.sessions = {}  # session_id -> GameSession
        self.user_profiles = {}  # user_id -> UserPreferences
        self.game_analytics = defaultdict(list)  # genre -> [session_data]
        self.active_sessions = {}  # user_id -> session_id
        
    def create_user_session(self, ip_address: str, user_agent: str = "") -> str:
        """Create or retrieve user session"""
        # Generate consistent user ID from IP and user agent
        user_data = f"{ip_address}_{user_agent}"
        user_id = hashlib.md5(user_data.encode()).hexdigest()[:12]
        
        # Initialize user profile if new
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = UserPreferences(
                preferred_genres=[],
                preferred_difficulty="medium",
                preferred_colors=["blue", "green"],
                accessibility_needs={
                    "high_contrast": False,
                    "large_text": False,
                    "reduced_motion": False,
                    "audio_cues": False
                },
                play_style="balanced",
                favorite_mechanics=[],
                session_count=0,
                total_playtime=0,
                last_active=datetime.now().isoformat()
            )
        
        return user_id
    
    def start_game_session(self, user_id: str, game_id: str, genre: str, difficulty: str) -> str:
        """Start a new game session"""
        session_id = hashlib.md5(f"{user_id}_{game_id}_{time.time()}".encode()).hexdigest()[:16]
        
        session = GameSession(
            session_id=session_id,
            user_id=user_id,
            game_id=game_id,
            genre=genre,
            start_time=datetime.now().isoformat(),
            end_time=None,
            duration=0,
            score=0,
            completed=False,
            difficulty=difficulty,
            actions_taken=0,
            preferences_learned={}
        )
        
        self.sessions[session_id] = session
        self.active_sessions[user_id] = session_id
        
        # Update user profile
        profile = self.user_profiles[user_id]
        profile.session_count += 1
        profile.last_active = datetime.now().isoformat()
        
        return session_id
    
    def end_game_session(self, session_id: str, score: int = 0, completed: bool = False, actions_taken: int = 0):
        """End a game session and learn from it"""
        if session_id not in self.sessions:
            return
        
        session = self.sessions[session_id]
        session.end_time = datetime.now().isoformat()
        session.score = score
        session.completed = completed
        session.actions_taken = actions_taken
        
        # Calculate duration
        start_time = datetime.fromisoformat(session.start_time)
        end_time = datetime.fromisoformat(session.end_time)
        session.duration = int((end_time - start_time).total_seconds())
        
        # Update user profile with learned preferences
        self._learn_from_session(session)
        
        # Add to analytics
        self.game_analytics[session.genre].append(asdict(session))
        
        # Remove from active sessions
        if session.user_id in self.active_sessions:
            del self.active_sessions[session.user_id]
    
    def _learn_from_session(self, session: GameSession):
        """Learn user preferences from completed session"""
        profile = self.user_profiles[session.user_id]
        
        # Update total playtime
        profile.total_playtime += session.duration
        
        # Learn genre preferences
        if session.completed or session.score > 0:
            if session.genre not in profile.preferred_genres:
                profile.preferred_genres.append(session.genre)
            
            # Move preferred genre to front if played well
            if session.score > 100 or session.completed:
                if session.genre in profile.preferred_genres:
                    profile.preferred_genres.remove(session.genre)
                profile.preferred_genres.insert(0, session.genre)
        
        # Learn difficulty preferences
        if session.completed:
            if session.difficulty == "easy" and session.duration < 60:
                profile.preferred_difficulty = "medium"
            elif session.difficulty == "medium" and session.completed and session.duration < 120:
                profile.preferred_difficulty = "hard"
            elif session.difficulty == "hard" and not session.completed:
                profile.preferred_difficulty = "medium"
        
        # Learn play style
        if session.actions_taken > 0:
            actions_per_minute = session.actions_taken / max(session.duration / 60, 1)
            if actions_per_minute > 30:
                profile.play_style = "aggressive"
            elif actions_per_minute < 10:
                profile.play_style = "careful"
            else:
                profile.play_style = "balanced"
        
        # Keep only top 5 preferred genres
        profile.preferred_genres = profile.preferred_genres[:5]
    
    def get_user_preferences(self, user_id: str) -> Optional[UserPreferences]:
        """Get user preferences"""
        return self.user_profiles.get(user_id)
    
    def update_user_preferences(self, user_id: str, preferences: Dict[str, Any]):
        """Update user preferences manually"""
        if user_id not in self.user_profiles:
            return
        
        profile = self.user_profiles[user_id]
        
        for key, value in preferences.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
    
    def get_session_analytics(self, genre: Optional[str] = None) -> Dict[str, Any]:
        """Get analytics data"""
        if genre:
            sessions = self.game_analytics.get(genre, [])
        else:
            sessions = []
            for genre_sessions in self.game_analytics.values():
                sessions.extend(genre_sessions)
        
        if not sessions:
            return {"total_sessions": 0}
        
        total_sessions = len(sessions)
        completed_sessions = sum(1 for s in sessions if s['completed'])
        total_playtime = sum(s['duration'] for s in sessions)
        avg_score = sum(s['score'] for s in sessions) / total_sessions
        
        return {
            "total_sessions": total_sessions,
            "completed_sessions": completed_sessions,
            "completion_rate": completed_sessions / total_sessions if total_sessions > 0 else 0,
            "total_playtime": total_playtime,
            "avg_playtime": total_playtime / total_sessions if total_sessions > 0 else 0,
            "avg_score": avg_score,
            "genres_played": list(self.game_analytics.keys())
        }

class GameSeedVarianceEngine:
    """Advanced seed generation for unique game experiences"""
    
    def __init__(self):
        self.seed_history = {}  # user_id -> [seeds]
        self.genre_seeds = defaultdict(set)  # genre -> {seeds}
        
    def generate_unique_seed(self, user_id: str, genre: str, description: str, 
                           user_preferences: Optional[UserPreferences] = None) -> Dict[str, Any]:
        """Generate a unique seed ensuring variety for the user"""
        
        # Base seed from description and timestamp
        base_content = f"{description}_{genre}_{time.time()}"
        base_seed = hashlib.md5(base_content.encode()).hexdigest()[:12]
        
        # Ensure uniqueness for this user
        user_seeds = self.seed_history.get(user_id, [])
        attempt = 0
        while base_seed in user_seeds and attempt < 10:
            base_content = f"{description}_{genre}_{time.time()}_{attempt}"
            base_seed = hashlib.md5(base_content.encode()).hexdigest()[:12]
            attempt += 1
        
        # Track seed usage
        if user_id not in self.seed_history:
            self.seed_history[user_id] = []
        self.seed_history[user_id].append(base_seed)
        self.genre_seeds[genre].add(base_seed)
        
        # Keep only last 50 seeds per user
        self.seed_history[user_id] = self.seed_history[user_id][-50:]
        
        # Generate variance parameters
        random.seed(base_seed)
        
        variance_config = {
            "seed": base_seed,
            "genre": genre,
            "user_id": user_id,
            "generation_time": datetime.now().isoformat(),
            
            # Visual variance
            "color_variance": {
                "hue_shift": random.randint(-30, 30),
                "saturation_multiplier": random.uniform(0.8, 1.2),
                "brightness_multiplier": random.uniform(0.9, 1.1),
                "contrast_boost": random.uniform(0.9, 1.1)
            },
            
            # Gameplay variance
            "mechanics_variance": {
                "speed_multiplier": random.uniform(0.8, 1.2),
                "difficulty_modifier": random.uniform(0.9, 1.1),
                "spawn_rate_modifier": random.uniform(0.8, 1.2),
                "score_multiplier": random.uniform(0.9, 1.1)
            },
            
            # Layout variance
            "layout_variance": {
                "element_count_modifier": random.uniform(0.8, 1.2),
                "spacing_modifier": random.uniform(0.9, 1.1),
                "size_variance": random.uniform(0.9, 1.1),
                "position_jitter": random.uniform(0, 10)
            },
            
            # Audio variance (for future implementation)
            "audio_variance": {
                "pitch_shift": random.uniform(0.9, 1.1),
                "tempo_modifier": random.uniform(0.95, 1.05),
                "reverb_amount": random.uniform(0, 0.3),
                "volume_modifier": random.uniform(0.8, 1.0)
            }
        }
        
        # Apply user preferences if available
        if user_preferences:
            variance_config = self._apply_user_preferences(variance_config, user_preferences)
        
        # Apply genre-specific variance
        variance_config = self._apply_genre_variance(variance_config, genre)
        
        return variance_config
    
    def _apply_user_preferences(self, config: Dict[str, Any], preferences: UserPreferences) -> Dict[str, Any]:
        """Apply user preferences to variance configuration"""
        
        # Adjust difficulty based on user preference
        difficulty_map = {"easy": 0.8, "medium": 1.0, "hard": 1.2}
        difficulty_mult = difficulty_map.get(preferences.preferred_difficulty, 1.0)
        config["mechanics_variance"]["difficulty_modifier"] *= difficulty_mult
        
        # Adjust colors based on preferences
        if "blue" in preferences.preferred_colors:
            config["color_variance"]["hue_shift"] += 10
        elif "red" in preferences.preferred_colors:
            config["color_variance"]["hue_shift"] -= 10
        
        # Apply accessibility needs
        if preferences.accessibility_needs.get("high_contrast"):
            config["color_variance"]["contrast_boost"] = 1.3
            config["color_variance"]["saturation_multiplier"] = 1.2
        
        if preferences.accessibility_needs.get("large_text"):
            config["layout_variance"]["size_variance"] = 1.2
        
        if preferences.accessibility_needs.get("reduced_motion"):
            config["mechanics_variance"]["speed_multiplier"] *= 0.8
            config["audio_variance"]["tempo_modifier"] *= 0.9
        
        # Adjust based on play style
        if preferences.play_style == "aggressive":
            config["mechanics_variance"]["speed_multiplier"] *= 1.1
            config["mechanics_variance"]["spawn_rate_modifier"] *= 1.1
        elif preferences.play_style == "careful":
            config["mechanics_variance"]["speed_multiplier"] *= 0.9
            config["layout_variance"]["spacing_modifier"] *= 1.1
        
        return config
    
    def _apply_genre_variance(self, config: Dict[str, Any], genre: str) -> Dict[str, Any]:
        """Apply genre-specific variance rules"""
        
        if genre == "puzzle":
            # Puzzles need consistent spacing and clear visuals
            config["layout_variance"]["spacing_modifier"] = max(0.95, config["layout_variance"]["spacing_modifier"])
            config["color_variance"]["contrast_boost"] = max(1.0, config["color_variance"]["contrast_boost"])
            
        elif genre == "shooter":
            # Shooters benefit from high contrast and fast movement
            config["color_variance"]["contrast_boost"] *= 1.1
            config["mechanics_variance"]["speed_multiplier"] = max(1.0, config["mechanics_variance"]["speed_multiplier"])
            
        elif genre == "platformer":
            # Platformers need clear visual distinction between elements
            config["color_variance"]["saturation_multiplier"] *= 1.1
            config["layout_variance"]["spacing_modifier"] = max(1.0, config["layout_variance"]["spacing_modifier"])
            
        elif genre == "racing":
            # Racing games benefit from speed and motion
            config["mechanics_variance"]["speed_multiplier"] *= 1.1
            config["audio_variance"]["tempo_modifier"] *= 1.05
            
        elif genre == "rpg":
            # RPGs benefit from rich visuals and varied content
            config["color_variance"]["saturation_multiplier"] *= 1.1
            config["layout_variance"]["element_count_modifier"] *= 1.1
            
        elif genre == "strategy":
            # Strategy games need clear, organized layouts
            config["layout_variance"]["spacing_modifier"] = max(1.0, config["layout_variance"]["spacing_modifier"])
            config["color_variance"]["contrast_boost"] = max(1.0, config["color_variance"]["contrast_boost"])
        
        return config
    
    def get_seed_statistics(self, user_id: Optional[str] = None, genre: Optional[str] = None) -> Dict[str, Any]:
        """Get statistics about seed generation"""
        
        if user_id and user_id in self.seed_history:
            user_seeds = self.seed_history[user_id]
            return {
                "user_total_seeds": len(user_seeds),
                "user_unique_seeds": len(set(user_seeds)),
                "user_variety_score": len(set(user_seeds)) / len(user_seeds) if user_seeds else 0
            }
        
        if genre and genre in self.genre_seeds:
            genre_seeds = self.genre_seeds[genre]
            return {
                "genre_total_seeds": len(genre_seeds),
                "genre_unique_seeds": len(genre_seeds)
            }
        
        # Global statistics
        total_seeds = sum(len(seeds) for seeds in self.seed_history.values())
        unique_seeds = len(set().union(*self.seed_history.values())) if self.seed_history else 0
        
        return {
            "total_seeds_generated": total_seeds,
            "total_unique_seeds": unique_seeds,
            "global_variety_score": unique_seeds / total_seeds if total_seeds > 0 else 0,
            "active_users": len(self.seed_history),
            "genres_with_seeds": len(self.genre_seeds)
        }

class PersonalizationEngine:
    """Advanced personalization based on user behavior"""
    
    def __init__(self, session_manager: SessionManager, seed_engine: GameSeedVarianceEngine):
        self.session_manager = session_manager
        self.seed_engine = seed_engine
    
    def get_personalized_recommendations(self, user_id: str) -> Dict[str, Any]:
        """Get personalized game recommendations"""
        preferences = self.session_manager.get_user_preferences(user_id)
        if not preferences:
            return self._get_default_recommendations()
        
        recommendations = {
            "suggested_genres": preferences.preferred_genres[:3] if preferences.preferred_genres else ["puzzle", "shooter", "platformer"],
            "suggested_difficulty": preferences.preferred_difficulty,
            "suggested_themes": self._get_theme_suggestions(preferences),
            "personalization_score": self._calculate_personalization_score(preferences),
            "new_user": preferences.session_count < 3,
            "returning_user": preferences.session_count >= 10,
            "power_user": preferences.total_playtime > 3600  # 1 hour
        }
        
        return recommendations
    
    def _get_default_recommendations(self) -> Dict[str, Any]:
        """Default recommendations for new users"""
        return {
            "suggested_genres": ["puzzle", "shooter", "platformer"],
            "suggested_difficulty": "medium",
            "suggested_themes": ["colorful", "modern", "friendly"],
            "personalization_score": 0.0,
            "new_user": True,
            "returning_user": False,
            "power_user": False
        }
    
    def _get_theme_suggestions(self, preferences: UserPreferences) -> List[str]:
        """Get theme suggestions based on preferences"""
        themes = []
        
        if "blue" in preferences.preferred_colors:
            themes.extend(["ocean", "sky", "tech"])
        if "red" in preferences.preferred_colors:
            themes.extend(["fire", "energy", "passion"])
        if "green" in preferences.preferred_colors:
            themes.extend(["nature", "forest", "growth"])
        
        if preferences.play_style == "aggressive":
            themes.extend(["action", "intense", "competitive"])
        elif preferences.play_style == "careful":
            themes.extend(["calm", "strategic", "thoughtful"])
        else:
            themes.extend(["balanced", "versatile", "adaptive"])
        
        return list(set(themes))[:5]  # Remove duplicates and limit to 5
    
    def _calculate_personalization_score(self, preferences: UserPreferences) -> float:
        """Calculate how well we know this user (0.0 to 1.0)"""
        score = 0.0
        
        # Genre knowledge
        if preferences.preferred_genres:
            score += min(len(preferences.preferred_genres) / 5, 0.3)
        
        # Session history
        if preferences.session_count > 0:
            score += min(preferences.session_count / 20, 0.3)
        
        # Playtime knowledge
        if preferences.total_playtime > 0:
            score += min(preferences.total_playtime / 7200, 0.2)  # 2 hours max
        
        # Preference specificity
        if preferences.play_style != "balanced":
            score += 0.1
        
        if any(preferences.accessibility_needs.values()):
            score += 0.1
        
        return min(score, 1.0)
    
    def generate_personalized_game_config(self, user_id: str, description: str, genre: str) -> Dict[str, Any]:
        """Generate a fully personalized game configuration"""
        preferences = self.session_manager.get_user_preferences(user_id)
        
        # Generate unique seed with variance
        seed_config = self.seed_engine.generate_unique_seed(user_id, genre, description, preferences)
        
        # Get personalized recommendations
        recommendations = self.get_personalized_recommendations(user_id)
        
        # Combine into final configuration
        config = {
            "seed_config": seed_config,
            "recommendations": recommendations,
            "user_preferences": asdict(preferences) if preferences else None,
            "personalization_applied": True,
            "generation_metadata": {
                "user_id": user_id,
                "genre": genre,
                "description": description,
                "timestamp": datetime.now().isoformat(),
                "personalization_version": "1.0"
            }
        }
        
        return config

# Global instances for use in main application
session_manager = SessionManager()
seed_engine = GameSeedVarianceEngine()
personalization_engine = PersonalizationEngine(session_manager, seed_engine)

# Export main functions
def create_user_session(ip_address: str, user_agent: str = "") -> str:
    """Create or retrieve user session"""
    return session_manager.create_user_session(ip_address, user_agent)

def start_game_session(user_id: str, game_id: str, genre: str, difficulty: str = "medium") -> str:
    """Start a new game session"""
    return session_manager.start_game_session(user_id, game_id, genre, difficulty)

def end_game_session(session_id: str, score: int = 0, completed: bool = False, actions_taken: int = 0):
    """End a game session"""
    session_manager.end_game_session(session_id, score, completed, actions_taken)

def get_personalized_config(user_id: str, description: str, genre: str) -> Dict[str, Any]:
    """Get personalized game configuration"""
    return personalization_engine.generate_personalized_game_config(user_id, description, genre)

def get_user_analytics(user_id: Optional[str] = None) -> Dict[str, Any]:
    """Get user analytics"""
    if user_id:
        preferences = session_manager.get_user_preferences(user_id)
        recommendations = personalization_engine.get_personalized_recommendations(user_id)
        return {
            "preferences": asdict(preferences) if preferences else None,
            "recommendations": recommendations,
            "session_analytics": session_manager.get_session_analytics()
        }
    else:
        return session_manager.get_session_analytics()

# Export all classes and functions
__all__ = [
    'SessionManager', 'GameSeedVarianceEngine', 'PersonalizationEngine',
    'UserPreferences', 'GameSession',
    'create_user_session', 'start_game_session', 'end_game_session',
    'get_personalized_config', 'get_user_analytics',
    'session_manager', 'seed_engine', 'personalization_engine'
