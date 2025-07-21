#!/usr/bin/env python3
"""
🏆 Enhanced Game Showcase - Database-Powered Game Gallery
Manages game display, storage, and user interactions with persistent database
"""

from flask import Blueprint, request, jsonify, render_template_string
import time
import json
from typing import Dict, List, Any
from database_manager import db_manager

# Create blueprint
showcase_bp = Blueprint('showcase', __name__)

class GameShowcase:
    """Enhanced game showcase with database integration"""
    
    def __init__(self):
        self.db = db_manager
        print("✅ Game Showcase initialized with database integration")
    
    def add_game(self, game_data: Dict[str, Any], creator_ip: str = None) -> Dict[str, Any]:
        """Add a new game to the showcase"""
        try:
            # Save to database
            success = self.db.save_game(game_data, creator_ip)
            
            if success:
                return {
                    'status': 'success',
                    'message': f'Game "{game_data["title"]}" added to showcase!',
                    'game_id': game_data['id']
                }
            else:
                return {
                    'status': 'error',
                    'message': 'Failed to save game to database'
                }
                
        except Exception as e:
            print(f"❌ Error adding game to showcase: {str(e)}")
            return {
                'status': 'error',
                'message': f'Error adding game: {str(e)}'
            }
    
    def get_all_games(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get all games from the showcase"""
        return self.db.get_all_games(limit)
    
    def get_game(self, game_id: str) -> Dict[str, Any]:
        """Get a specific game by ID"""
        game = self.db.get_game_by_id(game_id)
        if game:
            return {
                'status': 'success',
                'game': game
            }
        else:
            return {
                'status': 'error',
                'message': 'Game not found'
            }
    
    def play_game(self, game_id: str, user_ip: str = None) -> Dict[str, Any]:
        """Record a game play and return game data"""
        game = self.db.get_game_by_id(game_id)
        if not game:
            return {
                'status': 'error',
                'message': 'Game not found'
            }
        
        # Increment play count
        self.db.increment_plays(game_id, user_ip)
        
        return {
            'status': 'success',
            'game': game
        }
    
    def like_game(self, game_id: str, user_ip: str = None) -> Dict[str, Any]:
        """Like a game"""
        success = self.db.increment_likes(game_id, user_ip)
        
        if success:
            return {
                'status': 'success',
                'message': 'Game liked!'
            }
        else:
            return {
                'status': 'error',
                'message': 'Already liked or game not found'
            }
    
    def delete_game(self, game_id: str) -> Dict[str, Any]:
        """Delete a game (admin function)"""
        success = self.db.delete_game(game_id)
        
        if success:
            return {
                'status': 'success',
                'message': 'Game deleted successfully'
            }
        else:
            return {
                'status': 'error',
                'message': 'Failed to delete game'
            }
    
    def set_featured(self, game_id: str, featured: bool = True) -> Dict[str, Any]:
        """Set game as featured (admin function)"""
        success = self.db.set_featured(game_id, featured)
        
        if success:
            return {
                'status': 'success',
                'message': f'Game {"featured" if featured else "unfeatured"} successfully'
            }
        else:
            return {
                'status': 'error',
                'message': 'Failed to update featured status'
            }
    
    def get_analytics(self) -> Dict[str, Any]:
        """Get showcase analytics"""
        return self.db.get_analytics()
    
    def generate_showcase_html(self, games: List[Dict[str, Any]]) -> str:
        """Generate HTML for the game showcase"""
        
        games_html = ""
        for game in games:
            concept = game.get('concept', {})
            genre = concept.get('genre', 'puzzle')
            
            games_html += f'''
            <div class="game-card">
                <div class="game-header">
                    <h3>{game['title']}</h3>
                    <span class="genre-tag {genre}">{genre}</span>
                </div>
                <p class="game-description">{game.get('description', concept.get('description', 'A fun AI-generated game'))}</p>
                <div class="game-stats">
                    <span>🎮 {game['plays']} plays</span>
                    <span>❤️ {game['likes']} likes</span>
                    {f'<span class="featured">⭐ Featured</span>' if game.get('featured') else ''}
                </div>
                <div class="game-actions">
                    <a href="/games/play/{game['id']}" class="btn play-btn">🎮 Play</a>
                    <a href="/games/share/{game['id']}" class="btn share-btn">📤 Share</a>
                    <button onclick="likeGame('{game['id']}')" class="btn like-btn">❤️ Like</button>
                </div>
            </div>
            '''
        
        return f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>🎮 AI Game Showcase</title>
            <style>
                * {{
                    box-sizing: border-box;
                    margin: 0;
                    padding: 0;
                }}
                
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    min-height: 100vh;
                    padding: 20px;
                }}
                
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                }}
                
                .header {{
                    text-align: center;
                    margin-bottom: 40px;
                    background: rgba(255,255,255,0.1);
                    padding: 30px;
                    border-radius: 20px;
                    backdrop-filter: blur(10px);
                }}
                
                .header h1 {{
                    font-size: 2.5rem;
                    margin-bottom: 10px;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                }}
                
                .header p {{
                    font-size: 1.2rem;
                    opacity: 0.9;
                }}
                
                .create-section {{
                    background: rgba(255,255,255,0.1);
                    padding: 30px;
                    border-radius: 20px;
                    margin-bottom: 40px;
                    text-align: center;
                    backdrop-filter: blur(10px);
                }}
                
                .create-section h2 {{
                    margin-bottom: 20px;
                    font-size: 1.8rem;
                }}
                
                .game-input {{
                    width: 100%;
                    max-width: 600px;
                    padding: 15px;
                    border: none;
                    border-radius: 15px;
                    font-size: 1.1rem;
                    margin-bottom: 20px;
                    background: rgba(255,255,255,0.9);
                    color: #333;
                }}
                
                .create-btn {{
                    background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
                    color: white;
                    border: none;
                    padding: 15px 30px;
                    border-radius: 25px;
                    font-size: 1.1rem;
                    font-weight: bold;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                }}
                
                .create-btn:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 6px 20px rgba(0,0,0,0.3);
                }}
                
                .games-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
                    gap: 25px;
                    margin-top: 40px;
                }}
                
                .game-card {{
                    background: rgba(255,255,255,0.1);
                    border-radius: 20px;
                    padding: 25px;
                    backdrop-filter: blur(10px);
                    transition: all 0.3s ease;
                    border: 1px solid rgba(255,255,255,0.2);
                }}
                
                .game-card:hover {{
                    transform: translateY(-5px);
                    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                }}
                
                .game-header {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 15px;
                }}
                
                .game-header h3 {{
                    font-size: 1.4rem;
                    margin: 0;
                }}
                
                .genre-tag {{
                    padding: 5px 12px;
                    border-radius: 15px;
                    font-size: 0.8rem;
                    font-weight: bold;
                    text-transform: uppercase;
                }}
                
                .genre-tag.puzzle {{ background: #9b59b6; }}
                .genre-tag.shooter {{ background: #e74c3c; }}
                .genre-tag.platformer {{ background: #f39c12; }}
                .genre-tag.racing {{ background: #2ecc71; }}
                .genre-tag.rpg {{ background: #3498db; }}
                .genre-tag.strategy {{ background: #34495e; }}
                
                .game-description {{
                    margin-bottom: 15px;
                    line-height: 1.5;
                    opacity: 0.9;
                }}
                
                .game-stats {{
                    display: flex;
                    gap: 15px;
                    margin-bottom: 20px;
                    font-size: 0.9rem;
                }}
                
                .featured {{
                    color: #f1c40f;
                    font-weight: bold;
                }}
                
                .game-actions {{
                    display: flex;
                    gap: 10px;
                    flex-wrap: wrap;
                }}
                
                .btn {{
                    padding: 10px 15px;
                    border: none;
                    border-radius: 20px;
                    text-decoration: none;
                    font-weight: bold;
                    cursor: pointer;
                    transition: all 0.2s ease;
                    font-size: 0.9rem;
                    display: inline-flex;
                    align-items: center;
                    gap: 5px;
                }}
                
                .play-btn {{
                    background: linear-gradient(45deg, #2ecc71, #27ae60);
                    color: white;
                }}
                
                .share-btn {{
                    background: linear-gradient(45deg, #3498db, #2980b9);
                    color: white;
                }}
                
                .like-btn {{
                    background: linear-gradient(45deg, #e74c3c, #c0392b);
                    color: white;
                }}
                
                .btn:hover {{
                    transform: scale(1.05);
                }}
                
                .success-message {{
                    background: rgba(46, 204, 113, 0.2);
                    border: 1px solid #2ecc71;
                    color: #2ecc71;
                    padding: 15px;
                    border-radius: 10px;
                    margin: 20px 0;
                    text-align: center;
                }}
                
                @media (max-width: 768px) {{
                    .games-grid {{
                        grid-template-columns: 1fr;
                    }}
                    
                    .header h1 {{
                        font-size: 2rem;
                    }}
                    
                    .game-actions {{
                        justify-content: center;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎮 AI Game Showcase</h1>
                    <p>Discover amazing games created by AI in minutes!</p>
                </div>
                
                <div class="create-section">
                    <h2>🚀 Create Your Own Game</h2>
                    <p>Describe your dream game and watch AI bring it to life!</p>
                    <form id="gameForm" onsubmit="createGame(event)">
                        <input type="text" id="gameIdea" class="game-input" 
                               placeholder="Describe your game idea... (e.g., 'A space shooter where you defend Earth from alien invaders')" 
                               required>
                        <br>
                        <button type="submit" class="create-btn">🎮 Create Game</button>
                    </form>
                    <div id="message"></div>
                </div>
                
                <div class="games-section">
                    <h2 style="text-align: center; margin-bottom: 30px; font-size: 2rem;">🏆 Featured Games</h2>
                    <div class="games-grid">
                        {games_html}
                    </div>
                </div>
            </div>
            
            <script>
                async function createGame(event) {{
                    event.preventDefault();
                    
                    const gameIdea = document.getElementById('gameIdea').value;
                    const messageDiv = document.getElementById('message');
                    const submitBtn = event.target.querySelector('button');
                    
                    // Show loading state
                    submitBtn.textContent = '🎮 Creating Game...';
                    submitBtn.disabled = true;
                    messageDiv.innerHTML = '';
                    
                    try {{
                        const response = await fetch('/api/games/create', {{
                            method: 'POST',
                            headers: {{
                                'Content-Type': 'application/json'
                            }},
                            body: JSON.stringify({{ prompt: gameIdea }})
                        }});
                        
                        const result = await response.json();
                        
                        if (result.status === 'success') {{
                            messageDiv.innerHTML = `
                                <div class="success-message">
                                    <h3>🎉 Game Created Successfully!</h3>
                                    <p><strong>${{result.game.title}}</strong></p>
                                    <p>${{result.game.concept.description || 'A fun AI-generated game'}}</p>
                                    <div style="margin-top: 15px;">
                                        <a href="/games/play/${{result.game.id}}" class="btn play-btn">🎮 Play Now</a>
                                        <a href="/games/share/${{result.game.id}}" class="btn share-btn">📤 Share</a>
                                    </div>
                                </div>
                            `;
                            
                            // Clear form
                            document.getElementById('gameIdea').value = '';
                            
                            // Refresh page after 3 seconds to show new game
                            setTimeout(() => {{
                                window.location.reload();
                            }}, 3000);
                        }} else {{
                            messageDiv.innerHTML = `
                                <div style="background: rgba(231, 76, 60, 0.2); border: 1px solid #e74c3c; color: #e74c3c; padding: 15px; border-radius: 10px;">
                                    <strong>Error:</strong> ${{result.message}}
                                </div>
                            `;
                        }}
                    }} catch (error) {{
                        messageDiv.innerHTML = `
                            <div style="background: rgba(231, 76, 60, 0.2); border: 1px solid #e74c3c; color: #e74c3c; padding: 15px; border-radius: 10px;">
                                <strong>Error:</strong> Failed to create game. Please try again.
                            </div>
                        `;
                    }}
                    
                    // Reset button
                    submitBtn.textContent = '🎮 Create Game';
                    submitBtn.disabled = false;
                }}
                
                async function likeGame(gameId) {{
                    try {{
                        const response = await fetch(`/api/games/${{gameId}}/like`, {{
                            method: 'POST'
                        }});
                        
                        const result = await response.json();
                        
                        if (result.status === 'success') {{
                            // Refresh page to show updated like count
                            window.location.reload();
                        }} else {{
                            alert(result.message);
                        }}
                    }} catch (error) {{
                        alert('Failed to like game. Please try again.');
                    }}
                }}
            </script>
        </body>
        </html>
        '''

# Global showcase instance
game_showcase = GameShowcase()

# Flask routes
@showcase_bp.route('/games/showcase')
def showcase():
    """Display the game showcase"""
    games = game_showcase.get_all_games()
    return game_showcase.generate_showcase_html(games)

@showcase_bp.route('/api/games/create', methods=['POST'])
def create_game():
    """API endpoint to create a new game"""
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({
                'status': 'error',
                'message': 'Game prompt is required'
            })
        
        # Import game engine
        from game_engine import game_engine
        
        # Create the game
        result = game_engine.create_complete_game(prompt)
        
        if result['status'] == 'success':
            # Add to showcase
            creator_ip = request.remote_addr
            showcase_result = game_showcase.add_game(result['game'], creator_ip)
            
            if showcase_result['status'] == 'success':
                return jsonify(result)
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'Game created but failed to add to showcase'
                })
        else:
            return jsonify(result)
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to create game: {str(e)}'
        })

@showcase_bp.route('/games/play/<game_id>')
def play_game(game_id):
    """Play a specific game"""
    user_ip = request.remote_addr
    result = game_showcase.play_game(game_id, user_ip)
    
    if result['status'] == 'success':
        game = result['game']
        return game['code']['html']
    else:
        return f"<h1>Game Not Found</h1><p>{result['message']}</p>", 404

@showcase_bp.route('/api/games/<game_id>/like', methods=['POST'])
def like_game(game_id):
    """Like a game"""
    user_ip = request.remote_addr
    result = game_showcase.like_game(game_id, user_ip)
    return jsonify(result)

@showcase_bp.route('/api/games/analytics')
def get_analytics():
    """Get analytics data"""
    analytics = game_showcase.get_analytics()
    return jsonify(analytics)

@showcase_bp.route('/games/admin')
def admin_panel():
    """Simple admin panel for game management"""
    # This would typically require authentication
    games = game_showcase.get_all_games()
    analytics = game_showcase.get_analytics()
    
    admin_html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Game Admin Panel</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .stats {{ display: flex; gap: 20px; margin-bottom: 30px; }}
            .stat-card {{ background: #f0f0f0; padding: 20px; border-radius: 10px; }}
            .games-table {{ width: 100%; border-collapse: collapse; }}
            .games-table th, .games-table td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
            .games-table th {{ background: #f0f0f0; }}
            .btn {{ padding: 5px 10px; margin: 2px; border: none; border-radius: 5px; cursor: pointer; }}
            .btn-danger {{ background: #e74c3c; color: white; }}
            .btn-warning {{ background: #f39c12; color: white; }}
        </style>
    </head>
    <body>
        <h1>🎮 Game Admin Panel</h1>
        
        <div class="stats">
            <div class="stat-card">
                <h3>Total Games</h3>
                <p>{analytics.get('total_games', 0)}</p>
            </div>
            <div class="stat-card">
                <h3>Total Plays</h3>
                <p>{analytics.get('total_plays', 0)}</p>
            </div>
            <div class="stat-card">
                <h3>Total Likes</h3>
                <p>{analytics.get('total_likes', 0)}</p>
            </div>
        </div>
        
        <h2>Games Management</h2>
        <table class="games-table">
            <thead>
                <tr>
                    <th>Title</th>
                    <th>Genre</th>
                    <th>Plays</th>
                    <th>Likes</th>
                    <th>Featured</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {''.join([f'''
                <tr>
                    <td>{game['title']}</td>
                    <td>{game.get('genre', 'N/A')}</td>
                    <td>{game['plays']}</td>
                    <td>{game['likes']}</td>
                    <td>{'Yes' if game.get('featured') else 'No'}</td>
                    <td>
                        <button class="btn btn-warning" onclick="toggleFeatured('{game['id']}', {not game.get('featured', False)})">
                            {'Unfeature' if game.get('featured') else 'Feature'}
                        </button>
                        <button class="btn btn-danger" onclick="deleteGame('{game['id']}')">Delete</button>
                    </td>
                </tr>
                ''' for game in games])}
            </tbody>
        </table>
        
        <script>
            async function toggleFeatured(gameId, featured) {{
                const response = await fetch(`/api/games/${{gameId}}/featured`, {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ featured: featured }})
                }});
                
                if (response.ok) {{
                    location.reload();
                }}
            }}
            
            async function deleteGame(gameId) {{
                if (confirm('Are you sure you want to delete this game?')) {{
                    const response = await fetch(`/api/games/${{gameId}}`, {{
                        method: 'DELETE'
                    }});
                    
                    if (response.ok) {{
                        location.reload();
                    }}
                }}
            }}
        </script>
    </body>
    </html>
    '''
    
    return admin_html

@showcase_bp.route('/api/games/<game_id>/featured', methods=['POST'])
def set_featured(game_id):
    """Set game featured status"""
    data = request.get_json()
    featured = data.get('featured', True)
    result = game_showcase.set_featured(game_id, featured)
    return jsonify(result)

@showcase_bp.route('/api/games/<game_id>', methods=['DELETE'])
def delete_game(game_id):
    """Delete a game"""
    result = game_showcase.delete_game(game_id)
    return jsonify(result)
