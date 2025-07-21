#!/usr/bin/env python3
"""
🎮 GAME SHOWCASE - FIXED VERSION
Displays and manages created games without syntax errors
"""

import json
import os
from datetime import datetime
from flask import Blueprint, render_template_string, request, jsonify

# Create blueprint
showcase = Blueprint('showcase', __name__)

# Simple file-based storage
GAMES_FILE = 'games_data.json'

def load_games():
    """Load games from JSON file"""
    try:
        if os.path.exists(GAMES_FILE):
            with open(GAMES_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading games: {e}")
    return []

def save_games(games):
    """Save games to JSON file"""
    try:
        with open(GAMES_FILE, 'w') as f:
            json.dump(games, f, indent=2)
    except Exception as e:
        print(f"Error saving games: {e}")

def add_game(title, description, genre, game_code, creator_ip="unknown"):
    """Add a new game to the showcase"""
    games = load_games()
    
    # Generate unique ID
    game_id = f"game_{int(datetime.now().timestamp())}_{len(games)}"
    
    new_game = {
        'id': game_id,
        'title': title,
        'description': description,
        'genre': genre,
        'code': game_code,
        'created_at': datetime.now().isoformat(),
        'creator_ip': creator_ip,
        'plays': 0,
        'likes': 0,
        'featured': False
    }
    
    games.append(new_game)
    save_games(games)
    return game_id

@showcase.route('/games/showcase')
def show_showcase():
    """Display the game showcase"""
    games = load_games()
    
    # Sort by featured first, then by creation date
    games.sort(key=lambda x: (not x.get('featured', False), x.get('created_at', '')), reverse=True)
    
    showcase_html = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎮 Game Showcase - AI Created Games</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: white;
        }}
        
        .header {{
            text-align: center;
            padding: 40px 20px;
            background: rgba(0,0,0,0.2);
        }}
        
        .header h1 {{
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }}
        
        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .create-section {{
            max-width: 800px;
            margin: 0 auto 40px;
            padding: 0 20px;
        }}
        
        .create-form {{
            background: rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }}
        
        .form-group {{
            margin-bottom: 20px;
        }}
        
        .form-group label {{
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
        }}
        
        .form-group input, .form-group textarea {{
            width: 100%;
            padding: 12px;
            border: none;
            border-radius: 8px;
            background: rgba(255,255,255,0.9);
            color: #333;
            font-size: 16px;
        }}
        
        .form-group textarea {{
            height: 100px;
            resize: vertical;
        }}
        
        .create-btn {{
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 25px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
        }}
        
        .create-btn:hover {{
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }}
        
        .games-grid {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px 40px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
        }}
        
        .game-card {{
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 25px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
            position: relative;
        }}
        
        .game-card:hover {{
            transform: translateY(-10px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.4);
        }}
        
        .game-card.featured {{
            border: 3px solid #FFD700;
            background: rgba(255,215,0,0.1);
        }}
        
        .featured-badge {{
            position: absolute;
            top: -10px;
            right: -10px;
            background: #FFD700;
            color: #333;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
        }}
        
        .game-title {{
            font-size: 1.5em;
            margin-bottom: 10px;
            color: #FFD700;
        }}
        
        .game-genre {{
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            margin-bottom: 15px;
        }}
        
        .game-description {{
            margin-bottom: 20px;
            line-height: 1.6;
            opacity: 0.9;
        }}
        
        .game-stats {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 20px;
            font-size: 0.9em;
        }}
        
        .game-actions {{
            display: flex;
            gap: 10px;
        }}
        
        .action-btn {{
            flex: 1;
            padding: 12px;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            text-align: center;
            display: block;
        }}
        
        .play-btn {{
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white;
        }}
        
        .share-btn {{
            background: linear-gradient(45deg, #2196F3, #1976D2);
            color: white;
        }}
        
        .like-btn {{
            background: linear-gradient(45deg, #FF5722, #D84315);
            color: white;
        }}
        
        .action-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }}
        
        .no-games {{
            text-align: center;
            padding: 60px 20px;
            opacity: 0.7;
        }}
        
        .loading {{
            text-align: center;
            padding: 40px;
            font-size: 18px;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2em;
            }}
            
            .games-grid {{
                grid-template-columns: 1fr;
                gap: 20px;
            }}
            
            .game-actions {{
                flex-direction: column;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎮 Game Showcase</h1>
        <p>Discover amazing games created by AI • Play, Share, and Enjoy!</p>
    </div>
    
    <div class="create-section">
        <div class="create-form">
            <h2>🚀 Create Your Game</h2>
            <form id="gameForm">
                <div class="form-group">
                    <label for="gamePrompt">Describe your game:</label>
                    <textarea id="gamePrompt" placeholder="A space shooter where you defend Earth from alien invaders..." required></textarea>
                </div>
                <button type="submit" class="create-btn">✨ Create Game</button>
            </form>
        </div>
    </div>
    
    <div class="games-grid" id="gamesGrid">
        {generate_games_html(games)}
    </div>
    
    <script>
        document.getElementById('gameForm').addEventListener('submit', async (e) => {{
            e.preventDefault();
            
            const prompt = document.getElementById('gamePrompt').value;
            const button = e.target.querySelector('.create-btn');
            
            if (!prompt.trim()) {{
                alert('Please describe your game!');
                return;
            }}
            
            // Show loading
            button.textContent = '🎮 Creating Game...';
            button.disabled = true;
            
            try {{
                const response = await fetch('/api/games/create', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json',
                    }},
                    body: JSON.stringify({{ description: prompt }})
                }});
                
                const result = await response.json();
                
                if (result.success) {{
                    // Redirect to the new game
                    window.location.href = `/games/play/${{result.game_id}}`;
                }} else {{
                    alert('Error creating game: ' + result.error);
                }}
            }} catch (error) {{
                alert('Error creating game: ' + error.message);
            }} finally {{
                button.textContent = '✨ Create Game';
                button.disabled = false;
            }}
        }});
        
        async function playGame(gameId) {{
            // Track play
            try {{
                await fetch(`/api/games/${{gameId}}/play`, {{ method: 'POST' }});
            }} catch (e) {{
                console.log('Play tracking failed:', e);
            }}
            
            // Open game
            window.open(`/games/play/${{gameId}}`, '_blank');
        }}
        
        async function likeGame(gameId) {{
            try {{
                const response = await fetch(`/api/games/${{gameId}}/like`, {{ method: 'POST' }});
                const result = await response.json();
                
                if (result.success) {{
                    // Update like count in UI
                    const likeBtn = document.querySelector(`[onclick="likeGame('${{gameId}}')"]`);
                    if (likeBtn) {{
                        likeBtn.textContent = `❤️ ${{result.likes}}`;
                    }}
                }} else {{
                    alert(result.message || 'Already liked!');
                }}
            }} catch (error) {{
                console.log('Like failed:', error);
            }}
        }}
        
        function shareGame(gameId, title) {{
            const url = `${{window.location.origin}}/games/play/${{gameId}}`;
            
            if (navigator.share) {{
                navigator.share({{
                    title: `Check out this AI-created game: ${{title}}`,
                    url: url
                }});
            }} else {{
                // Fallback to clipboard
                navigator.clipboard.writeText(url).then(() => {{
                    alert('Game link copied to clipboard!');
                }}).catch(() => {{
                    prompt('Copy this link to share:', url);
                }});
            }}
        }}
    </script>
</body>
</html>
'''
    
    return showcase_html

def generate_games_html(games):
    """Generate HTML for games grid"""
    if not games:
        return '''
        <div class="no-games">
            <h2>🎮 No games yet!</h2>
            <p>Be the first to create an amazing AI-generated game!</p>
        </div>
        '''
    
    games_html = ""
    for game in games:
        featured_class = "featured" if game.get('featured', False) else ""
        featured_badge = '<div class="featured-badge">⭐ FEATURED</div>' if game.get('featured', False) else ""
        
        games_html += f'''
        <div class="game-card {featured_class}">
            {featured_badge}
            <div class="game-title">{game['title']}</div>
            <div class="game-genre">{game['genre'].upper()}</div>
            <div class="game-description">{game['description']}</div>
            <div class="game-stats">
                <span>🎮 {game['plays']} plays</span>
                <span>❤️ {game['likes']} likes</span>
                <span>📅 {game['created_at'][:10]}</span>
            </div>
            <div class="game-actions">
                <button class="action-btn play-btn" onclick="playGame('{game['id']}')">
                    ▶️ Play
                </button>
                <button class="action-btn like-btn" onclick="likeGame('{game['id']}')">
                    ❤️ {game['likes']}
                </button>
                <button class="action-btn share-btn" onclick="shareGame('{game['id']}', '{game['title']}')">
                    📤 Share
                </button>
            </div>
        </div>
        '''
    
    return games_html

@showcase.route('/games/play/<game_id>')
def play_game(game_id):
    """Display a specific game"""
    games = load_games()
    game = next((g for g in games if g['id'] == game_id), None)
    
    if not game:
        return "Game not found", 404
    
    return game['code']

@showcase.route('/api/games/<game_id>/play', methods=['POST'])
def track_play(game_id):
    """Track game play"""
    games = load_games()
    
    for game in games:
        if game['id'] == game_id:
            game['plays'] = game.get('plays', 0) + 1
            save_games(games)
            return jsonify({'success': True, 'plays': game['plays']})
    
    return jsonify({'success': False, 'error': 'Game not found'}), 404

@showcase.route('/api/games/<game_id>/like', methods=['POST'])
def like_game(game_id):
    """Like a game"""
    games = load_games()
    client_ip = request.remote_addr
    
    for game in games:
        if game['id'] == game_id:
            # Simple like tracking (one per IP)
            likes_key = f"likes_{game_id}"
            liked_ips = game.get('liked_ips', [])
            
            if client_ip in liked_ips:
                return jsonify({'success': False, 'message': 'Already liked!'})
            
            liked_ips.append(client_ip)
            game['liked_ips'] = liked_ips
            game['likes'] = len(liked_ips)
            save_games(games)
            
            return jsonify({'success': True, 'likes': game['likes']})
    
    return jsonify({'success': False, 'error': 'Game not found'}), 404

@showcase.route('/api/games/demo')
def demo_games():
    """Demo endpoint for testing"""
    return jsonify({
        'status': 'success',
        'message': 'Game showcase is working!',
        'games_count': len(load_games())
    })
