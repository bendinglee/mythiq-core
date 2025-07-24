"""
Game Showcase System - Revolutionary Game Sharing and Discovery Platform
Advanced system for showcasing, sharing, and discovering AI-generated games

This module provides:
- Game gallery with filtering and search
- Social sharing and community features
- Mobile-optimized game viewing
- Game analytics and statistics
- User ratings and reviews
- Game collections and playlists
- Viral sharing mechanisms
"""

import json
import random
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta

@dataclass
class GameEntry:
    """Represents a game in the showcase system"""
    game_id: str
    title: str
    description: str
    genre: str
    theme: str
    creator: str
    created_date: str
    play_count: int
    like_count: int
    share_count: int
    rating: float
    tags: List[str]
    thumbnail_url: str
    game_url: str
    mobile_compatible: bool
    estimated_playtime: str
    difficulty: str
    featured: bool
    trending_score: float

@dataclass
class GameStats:
    """Game statistics and analytics"""
    total_plays: int
    unique_players: int
    average_session_time: float
    completion_rate: float
    user_ratings: List[int]
    popular_times: List[str]
    device_breakdown: Dict[str, int]
    geographic_data: Dict[str, int]

@dataclass
class UserInteraction:
    """User interaction with games"""
    user_id: str
    game_id: str
    action: str  # 'play', 'like', 'share', 'rate', 'comment'
    timestamp: str
    metadata: Dict[str, Any]

class GameShowcaseSystem:
    """
    Advanced game showcase and sharing system
    Manages game discovery, social features, and analytics
    """
    
    def __init__(self):
        self.games_database = {}
        self.user_interactions = []
        self.featured_games = []
        self.trending_games = []
        self.game_collections = {}
        
        # Initialize with some sample games for demonstration
        self._initialize_sample_games()
    
    def add_game(self, game_data: Dict[str, Any]) -> str:
        """Add a new game to the showcase system"""
        game_id = self._generate_game_id()
        
        game_entry = GameEntry(
            game_id=game_id,
            title=game_data.get('title', 'Untitled Game'),
            description=game_data.get('description', 'An exciting AI-generated game'),
            genre=game_data.get('genre', 'adventure'),
            theme=game_data.get('theme', 'fantasy'),
            creator=game_data.get('creator', 'AI Creator'),
            created_date=datetime.now().isoformat(),
            play_count=0,
            like_count=0,
            share_count=0,
            rating=0.0,
            tags=game_data.get('tags', []),
            thumbnail_url=f"/api/games/{game_id}/thumbnail",
            game_url=f"/play/{game_id}",
            mobile_compatible=game_data.get('mobile_compatible', True),
            estimated_playtime=game_data.get('estimated_playtime', '5-15 minutes'),
            difficulty=game_data.get('difficulty', 'medium'),
            featured=False,
            trending_score=0.0
        )
        
        self.games_database[game_id] = game_entry
        return game_id
    
    def get_game(self, game_id: str) -> Optional[GameEntry]:
        """Get a specific game by ID"""
        return self.games_database.get(game_id)
    
    def get_all_games(self, limit: int = 50, offset: int = 0) -> List[GameEntry]:
        """Get all games with pagination"""
        games = list(self.games_database.values())
        return games[offset:offset + limit]
    
    def get_featured_games(self, limit: int = 10) -> List[GameEntry]:
        """Get featured games"""
        featured = [game for game in self.games_database.values() if game.featured]
        return sorted(featured, key=lambda x: x.trending_score, reverse=True)[:limit]
    
    def get_trending_games(self, limit: int = 10) -> List[GameEntry]:
        """Get trending games based on recent activity"""
        games = list(self.games_database.values())
        # Sort by trending score (combination of recent plays, likes, and shares)
        trending = sorted(games, key=lambda x: x.trending_score, reverse=True)
        return trending[:limit]
    
    def get_games_by_genre(self, genre: str, limit: int = 20) -> List[GameEntry]:
        """Get games filtered by genre"""
        games = [game for game in self.games_database.values() if game.genre.lower() == genre.lower()]
        return sorted(games, key=lambda x: x.play_count, reverse=True)[:limit]
    
    def get_games_by_theme(self, theme: str, limit: int = 20) -> List[GameEntry]:
        """Get games filtered by theme"""
        games = [game for game in self.games_database.values() if theme.lower() in game.theme.lower()]
        return sorted(games, key=lambda x: x.rating, reverse=True)[:limit]
    
    def search_games(self, query: str, limit: int = 20) -> List[GameEntry]:
        """Search games by title, description, or tags"""
        query_lower = query.lower()
        matching_games = []
        
        for game in self.games_database.values():
            if (query_lower in game.title.lower() or 
                query_lower in game.description.lower() or
                any(query_lower in tag.lower() for tag in game.tags)):
                matching_games.append(game)
        
        return sorted(matching_games, key=lambda x: x.play_count, reverse=True)[:limit]
    
    def record_play(self, game_id: str, user_id: str = None, session_data: Dict[str, Any] = None) -> bool:
        """Record a game play event"""
        if game_id not in self.games_database:
            return False
        
        game = self.games_database[game_id]
        game.play_count += 1
        
        # Update trending score
        self._update_trending_score(game_id, 'play')
        
        # Record user interaction
        interaction = UserInteraction(
            user_id=user_id or f"anonymous_{random.randint(1000, 9999)}",
            game_id=game_id,
            action='play',
            timestamp=datetime.now().isoformat(),
            metadata=session_data or {}
        )
        self.user_interactions.append(interaction)
        
        return True
    
    def record_like(self, game_id: str, user_id: str) -> bool:
        """Record a game like"""
        if game_id not in self.games_database:
            return False
        
        game = self.games_database[game_id]
        game.like_count += 1
        
        # Update trending score
        self._update_trending_score(game_id, 'like')
        
        # Record user interaction
        interaction = UserInteraction(
            user_id=user_id,
            game_id=game_id,
            action='like',
            timestamp=datetime.now().isoformat(),
            metadata={}
        )
        self.user_interactions.append(interaction)
        
        return True
    
    def record_share(self, game_id: str, user_id: str, platform: str = 'general') -> bool:
        """Record a game share"""
        if game_id not in self.games_database:
            return False
        
        game = self.games_database[game_id]
        game.share_count += 1
        
        # Update trending score (shares have high impact)
        self._update_trending_score(game_id, 'share')
        
        # Record user interaction
        interaction = UserInteraction(
            user_id=user_id,
            game_id=game_id,
            action='share',
            timestamp=datetime.now().isoformat(),
            metadata={'platform': platform}
        )
        self.user_interactions.append(interaction)
        
        return True
    
    def rate_game(self, game_id: str, user_id: str, rating: int) -> bool:
        """Rate a game (1-5 stars)"""
        if game_id not in self.games_database or not (1 <= rating <= 5):
            return False
        
        game = self.games_database[game_id]
        
        # Simple rating calculation (in real implementation, you'd track individual ratings)
        current_total = game.rating * max(1, game.like_count)
        new_total = current_total + rating
        new_count = max(1, game.like_count) + 1
        game.rating = new_total / new_count
        
        # Record user interaction
        interaction = UserInteraction(
            user_id=user_id,
            game_id=game_id,
            action='rate',
            timestamp=datetime.now().isoformat(),
            metadata={'rating': rating}
        )
        self.user_interactions.append(interaction)
        
        return True
    
    def get_game_stats(self, game_id: str) -> Optional[GameStats]:
        """Get detailed statistics for a game"""
        if game_id not in self.games_database:
            return None
        
        game = self.games_database[game_id]
        game_interactions = [i for i in self.user_interactions if i.game_id == game_id]
        
        # Calculate statistics
        total_plays = len([i for i in game_interactions if i.action == 'play'])
        unique_players = len(set(i.user_id for i in game_interactions if i.action == 'play'))
        
        # Mock some additional stats
        stats = GameStats(
            total_plays=total_plays,
            unique_players=unique_players,
            average_session_time=random.uniform(2.0, 8.0),  # minutes
            completion_rate=random.uniform(0.6, 0.9),
            user_ratings=[random.randint(3, 5) for _ in range(min(10, total_plays))],
            popular_times=['evening', 'weekend'],
            device_breakdown={'mobile': 60, 'desktop': 35, 'tablet': 5},
            geographic_data={'US': 40, 'EU': 30, 'Asia': 20, 'Other': 10}
        )
        
        return stats
    
    def create_collection(self, collection_name: str, game_ids: List[str], creator: str) -> str:
        """Create a game collection/playlist"""
        collection_id = f"collection_{int(time.time())}_{random.randint(100, 999)}"
        
        self.game_collections[collection_id] = {
            'id': collection_id,
            'name': collection_name,
            'game_ids': game_ids,
            'creator': creator,
            'created_date': datetime.now().isoformat(),
            'play_count': 0,
            'like_count': 0
        }
        
        return collection_id
    
    def get_collection(self, collection_id: str) -> Optional[Dict[str, Any]]:
        """Get a game collection"""
        return self.game_collections.get(collection_id)
    
    def get_popular_collections(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get popular game collections"""
        collections = list(self.game_collections.values())
        return sorted(collections, key=lambda x: x['play_count'], reverse=True)[:limit]
    
    def generate_share_url(self, game_id: str, platform: str = 'general') -> str:
        """Generate shareable URL for a game"""
        base_url = "https://mythiq-games.com"  # Your domain
        game_url = f"{base_url}/play/{game_id}"
        
        if platform == 'twitter':
            game = self.get_game(game_id)
            text = f"Check out this amazing AI-generated game: {game.title}!"
            return f"https://twitter.com/intent/tweet?text={text}&url={game_url}"
        elif platform == 'facebook':
            return f"https://www.facebook.com/sharer/sharer.php?u={game_url}"
        elif platform == 'reddit':
            game = self.get_game(game_id)
            title = f"Amazing AI-generated {game.genre} game: {game.title}"
            return f"https://reddit.com/submit?url={game_url}&title={title}"
        else:
            return game_url
    
    def get_recommendations(self, user_id: str = None, game_id: str = None, limit: int = 5) -> List[GameEntry]:
        """Get game recommendations based on user activity or similar games"""
        if game_id:
            # Recommend similar games
            base_game = self.get_game(game_id)
            if base_game:
                similar_games = [
                    game for game in self.games_database.values()
                    if game.game_id != game_id and (
                        game.genre == base_game.genre or 
                        game.theme == base_game.theme
                    )
                ]
                return sorted(similar_games, key=lambda x: x.rating, reverse=True)[:limit]
        
        # Default recommendations: trending games
        return self.get_trending_games(limit)
    
    def generate_showcase_html(self, featured_only: bool = False) -> str:
        """Generate HTML for the game showcase"""
        games = self.get_featured_games(12) if featured_only else self.get_all_games(24)
        
        html = """
        <div class="game-showcase">
            <div class="showcase-header">
                <h2>🎮 AI Game Showcase</h2>
                <p>Discover amazing games created by AI from simple prompts!</p>
            </div>
            
            <div class="showcase-filters">
                <button class="filter-btn active" data-filter="all">All Games</button>
                <button class="filter-btn" data-filter="platformer">Platformer</button>
                <button class="filter-btn" data-filter="shooter">Shooter</button>
                <button class="filter-btn" data-filter="puzzle">Puzzle</button>
                <button class="filter-btn" data-filter="racing">Racing</button>
            </div>
            
            <div class="games-grid">
        """
        
        for game in games:
            html += self._generate_game_card_html(game)
        
        html += """
            </div>
            
            <div class="showcase-footer">
                <button class="load-more-btn">Load More Games</button>
            </div>
        </div>
        """
        
        return html
    
    def generate_showcase_css(self) -> str:
        """Generate CSS for the game showcase"""
        return """
        .game-showcase {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .showcase-header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .showcase-header h2 {
            font-size: 2.5em;
            color: #333;
            margin-bottom: 10px;
        }
        
        .showcase-header p {
            font-size: 1.2em;
            color: #666;
        }
        
        .showcase-filters {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }
        
        .filter-btn {
            padding: 10px 20px;
            border: 2px solid #ddd;
            background: white;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
        }
        
        .filter-btn:hover, .filter-btn.active {
            background: #007bff;
            color: white;
            border-color: #007bff;
        }
        
        .games-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }
        
        .game-card {
            background: white;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            cursor: pointer;
        }
        
        .game-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }
        
        .game-thumbnail {
            width: 100%;
            height: 180px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 3em;
            position: relative;
        }
        
        .game-info {
            padding: 20px;
        }
        
        .game-title {
            font-size: 1.3em;
            font-weight: bold;
            color: #333;
            margin-bottom: 8px;
        }
        
        .game-description {
            color: #666;
            font-size: 0.9em;
            line-height: 1.4;
            margin-bottom: 15px;
        }
        
        .game-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .game-genre {
            background: #e3f2fd;
            color: #1976d2;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.8em;
            font-weight: 500;
        }
        
        .game-rating {
            display: flex;
            align-items: center;
            gap: 5px;
            color: #ff9800;
        }
        
        .game-stats {
            display: flex;
            justify-content: space-between;
            color: #999;
            font-size: 0.8em;
            margin-bottom: 15px;
        }
        
        .game-actions {
            display: flex;
            gap: 10px;
        }
        
        .play-btn {
            flex: 1;
            background: #4caf50;
            color: white;
            border: none;
            padding: 12px;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        
        .play-btn:hover {
            background: #45a049;
        }
        
        .like-btn, .share-btn {
            background: #f5f5f5;
            border: none;
            padding: 12px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .like-btn:hover {
            background: #ff5722;
            color: white;
        }
        
        .share-btn:hover {
            background: #2196f3;
            color: white;
        }
        
        .mobile-badge {
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(76, 175, 80, 0.9);
            color: white;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.7em;
            font-weight: bold;
        }
        
        .featured-badge {
            position: absolute;
            top: 10px;
            left: 10px;
            background: rgba(255, 193, 7, 0.9);
            color: #333;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.7em;
            font-weight: bold;
        }
        
        .load-more-btn {
            display: block;
            margin: 0 auto;
            padding: 15px 30px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 25px;
            font-size: 1.1em;
            font-weight: bold;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        
        .load-more-btn:hover {
            background: #0056b3;
        }
        
        /* Mobile Responsive */
        @media (max-width: 768px) {
            .games-grid {
                grid-template-columns: 1fr;
                gap: 20px;
            }
            
            .showcase-filters {
                gap: 8px;
            }
            
            .filter-btn {
                padding: 8px 16px;
                font-size: 0.9em;
            }
            
            .game-card {
                margin: 0 10px;
            }
        }
        """
    
    def generate_showcase_javascript(self) -> str:
        """Generate JavaScript for interactive showcase features"""
        return """
        // Game Showcase Interactive Features
        document.addEventListener('DOMContentLoaded', function() {
            // Filter functionality
            const filterBtns = document.querySelectorAll('.filter-btn');
            const gameCards = document.querySelectorAll('.game-card');
            
            filterBtns.forEach(btn => {
                btn.addEventListener('click', function() {
                    // Update active filter
                    filterBtns.forEach(b => b.classList.remove('active'));
                    this.classList.add('active');
                    
                    const filter = this.dataset.filter;
                    
                    // Filter games
                    gameCards.forEach(card => {
                        if (filter === 'all' || card.dataset.genre === filter) {
                            card.style.display = 'block';
                        } else {
                            card.style.display = 'none';
                        }
                    });
                });
            });
            
            // Game card interactions
            gameCards.forEach(card => {
                const playBtn = card.querySelector('.play-btn');
                const likeBtn = card.querySelector('.like-btn');
                const shareBtn = card.querySelector('.share-btn');
                
                if (playBtn) {
                    playBtn.addEventListener('click', function(e) {
                        e.stopPropagation();
                        const gameId = card.dataset.gameId;
                        playGame(gameId);
                    });
                }
                
                if (likeBtn) {
                    likeBtn.addEventListener('click', function(e) {
                        e.stopPropagation();
                        const gameId = card.dataset.gameId;
                        likeGame(gameId, this);
                    });
                }
                
                if (shareBtn) {
                    shareBtn.addEventListener('click', function(e) {
                        e.stopPropagation();
                        const gameId = card.dataset.gameId;
                        shareGame(gameId);
                    });
                }
                
                // Click to play
                card.addEventListener('click', function() {
                    const gameId = this.dataset.gameId;
                    playGame(gameId);
                });
            });
            
            // Load more functionality
            const loadMoreBtn = document.querySelector('.load-more-btn');
            if (loadMoreBtn) {
                loadMoreBtn.addEventListener('click', function() {
                    loadMoreGames();
                });
            }
        });
        
        function playGame(gameId) {
            // Record play event
            fetch(`/api/games/${gameId}/play`, { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    // Open game in new window/tab
                    window.open(`/play/${gameId}`, '_blank');
                })
                .catch(error => console.error('Error recording play:', error));
        }
        
        function likeGame(gameId, button) {
            fetch(`/api/games/${gameId}/like`, { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        button.style.background = '#ff5722';
                        button.style.color = 'white';
                        button.innerHTML = '❤️';
                        
                        // Update like count
                        const likeCount = button.parentElement.parentElement.querySelector('.like-count');
                        if (likeCount) {
                            likeCount.textContent = parseInt(likeCount.textContent) + 1;
                        }
                    }
                })
                .catch(error => console.error('Error liking game:', error));
        }
        
        function shareGame(gameId) {
            // Get share URL
            fetch(`/api/games/${gameId}/share-url`)
                .then(response => response.json())
                .then(data => {
                    if (navigator.share) {
                        // Use native sharing if available
                        navigator.share({
                            title: data.title,
                            text: data.description,
                            url: data.url
                        });
                    } else {
                        // Fallback: copy to clipboard
                        navigator.clipboard.writeText(data.url).then(() => {
                            alert('Game link copied to clipboard!');
                        });
                    }
                    
                    // Record share event
                    fetch(`/api/games/${gameId}/share`, { method: 'POST' });
                })
                .catch(error => console.error('Error sharing game:', error));
        }
        
        function loadMoreGames() {
            const currentCount = document.querySelectorAll('.game-card').length;
            
            fetch(`/api/games?offset=${currentCount}&limit=12`)
                .then(response => response.json())
                .then(data => {
                    const gamesGrid = document.querySelector('.games-grid');
                    data.games.forEach(game => {
                        const gameCard = createGameCard(game);
                        gamesGrid.appendChild(gameCard);
                    });
                    
                    if (data.games.length < 12) {
                        document.querySelector('.load-more-btn').style.display = 'none';
                    }
                })
                .catch(error => console.error('Error loading more games:', error));
        }
        
        function createGameCard(game) {
            const card = document.createElement('div');
            card.className = 'game-card';
            card.dataset.gameId = game.game_id;
            card.dataset.genre = game.genre;
            
            card.innerHTML = `
                <div class="game-thumbnail">
                    🎮
                    ${game.mobile_compatible ? '<div class="mobile-badge">📱 Mobile</div>' : ''}
                    ${game.featured ? '<div class="featured-badge">⭐ Featured</div>' : ''}
                </div>
                <div class="game-info">
                    <div class="game-title">${game.title}</div>
                    <div class="game-description">${game.description}</div>
                    <div class="game-meta">
                        <span class="game-genre">${game.genre}</span>
                        <div class="game-rating">
                            ⭐ ${game.rating.toFixed(1)}
                        </div>
                    </div>
                    <div class="game-stats">
                        <span>👥 <span class="play-count">${game.play_count}</span> plays</span>
                        <span>❤️ <span class="like-count">${game.like_count}</span> likes</span>
                        <span>📤 ${game.share_count} shares</span>
                    </div>
                    <div class="game-actions">
                        <button class="play-btn">▶️ Play</button>
                        <button class="like-btn">👍</button>
                        <button class="share-btn">📤</button>
                    </div>
                </div>
            `;
            
            return card;
        }
        """
    
    def _generate_game_id(self) -> str:
        """Generate unique game ID"""
        timestamp = int(time.time())
        random_suffix = random.randint(1000, 9999)
        return f"game_{timestamp}_{random_suffix}"
    
    def _generate_game_card_html(self, game: GameEntry) -> str:
        """Generate HTML for a single game card"""
        return f"""
        <div class="game-card" data-game-id="{game.game_id}" data-genre="{game.genre}">
            <div class="game-thumbnail">
                🎮
                {f'<div class="mobile-badge">📱 Mobile</div>' if game.mobile_compatible else ''}
                {f'<div class="featured-badge">⭐ Featured</div>' if game.featured else ''}
            </div>
            <div class="game-info">
                <div class="game-title">{game.title}</div>
                <div class="game-description">{game.description}</div>
                <div class="game-meta">
                    <span class="game-genre">{game.genre}</span>
                    <div class="game-rating">
                        ⭐ {game.rating:.1f}
                    </div>
                </div>
                <div class="game-stats">
                    <span>👥 <span class="play-count">{game.play_count}</span> plays</span>
                    <span>❤️ <span class="like-count">{game.like_count}</span> likes</span>
                    <span>📤 {game.share_count} shares</span>
                </div>
                <div class="game-actions">
                    <button class="play-btn">▶️ Play</button>
                    <button class="like-btn">👍</button>
                    <button class="share-btn">📤</button>
                </div>
            </div>
        </div>
        """
    
    def _update_trending_score(self, game_id: str, action: str):
        """Update trending score based on user actions"""
        if game_id not in self.games_database:
            return
        
        game = self.games_database[game_id]
        
        # Weight different actions
        action_weights = {
            'play': 1.0,
            'like': 2.0,
            'share': 3.0,
            'rate': 1.5
        }
        
        weight = action_weights.get(action, 1.0)
        
        # Time decay factor (recent actions have more weight)
        time_factor = 1.0  # In real implementation, you'd calculate based on time
        
        game.trending_score += weight * time_factor
    
    def _initialize_sample_games(self):
        """Initialize with sample games for demonstration"""
        sample_games = [
            {
                'title': 'Mystic Forest Adventure',
                'description': 'A magical platformer where a brave cat explores an enchanted forest filled with mysteries and treasures.',
                'genre': 'platformer',
                'theme': 'fantasy',
                'creator': 'AI Creator',
                'tags': ['magic', 'adventure', 'cat', 'forest'],
                'mobile_compatible': True,
                'estimated_playtime': '10-20 minutes',
                'difficulty': 'medium'
            },
            {
                'title': 'Neon Speed Circuit',
                'description': 'A high-speed cyberpunk racing game through neon-lit city streets with futuristic vehicles.',
                'genre': 'racing',
                'theme': 'cyberpunk',
                'creator': 'AI Creator',
                'tags': ['racing', 'cyberpunk', 'neon', 'speed'],
                'mobile_compatible': True,
                'estimated_playtime': '5-15 minutes',
                'difficulty': 'hard'
            },
            {
                'title': 'Cosmic Defender',
                'description': 'An intense space shooter where you defend Earth from waves of alien invaders.',
                'genre': 'shooter',
                'theme': 'sci-fi',
                'creator': 'AI Creator',
                'tags': ['space', 'shooter', 'aliens', 'defense'],
                'mobile_compatible': True,
                'estimated_playtime': '15-30 minutes',
                'difficulty': 'medium'
            },
            {
                'title': 'Ocean Puzzle Quest',
                'description': 'A relaxing underwater puzzle game featuring beautiful marine life and challenging brain teasers.',
                'genre': 'puzzle',
                'theme': 'underwater',
                'creator': 'AI Creator',
                'tags': ['puzzle', 'underwater', 'relaxing', 'brain'],
                'mobile_compatible': True,
                'estimated_playtime': '20-40 minutes',
                'difficulty': 'easy'
            }
        ]
        
        for game_data in sample_games:
            game_id = self.add_game(game_data)
            game = self.games_database[game_id]
            
            # Add some sample stats
            game.play_count = random.randint(50, 500)
            game.like_count = random.randint(10, 100)
            game.share_count = random.randint(5, 50)
            game.rating = random.uniform(3.5, 5.0)
            game.trending_score = random.uniform(10, 100)
            
            # Mark some as featured
            if random.random() < 0.5:
                game.featured = True

# Example usage and testing
if __name__ == "__main__":
    showcase = GameShowcaseSystem()
    
    # Test adding a new game
    new_game = {
        'title': 'Dream Walker',
        'description': 'A surreal adventure through the world of dreams',
        'genre': 'adventure',
        'theme': 'fantasy',
        'creator': 'Dream AI',
        'tags': ['dreams', 'surreal', 'adventure'],
        'mobile_compatible': True,
        'estimated_playtime': '30-60 minutes',
        'difficulty': 'medium'
    }
    
    game_id = showcase.add_game(new_game)
    print(f"Added game with ID: {game_id}")
    
    # Test getting games
    featured_games = showcase.get_featured_games(3)
    print(f"Featured games: {[g.title for g in featured_games]}")
    
    # Test search
    search_results = showcase.search_games("space")
    print(f"Search results for 'space': {[g.title for g in search_results]}")
    
    # Test recording interactions
    showcase.record_play(game_id, "user123")
    showcase.record_like(game_id, "user123")
    showcase.rate_game(game_id, "user123", 5)
    
    print("Game showcase system initialized and tested successfully!")
