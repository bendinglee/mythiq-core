#!/usr/bin/env python3
"""
🎮 Game Showcase Platform
Manages created games, sharing, and user galleries
"""

import os
import json
import time
import sqlite3
from typing import Dict, List, Optional, Any
from flask import Flask, request, jsonify, render_template_string, send_from_directory

class GameShowcase:
    """Game showcase and management platform"""
    
    def __init__(self, db_path: str = "games.db"):
        self.db_path = db_path
        self.init_database()
        
        # Game storage directory
        self.games_dir = "generated_games"
        os.makedirs(self.games_dir, exist_ok=True)
    
    def init_database(self):
        """Initialize SQLite database for game storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Games table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS games (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                genre TEXT,
                creator_ip TEXT,
                created_at REAL,
                plays INTEGER DEFAULT 0,
                likes INTEGER DEFAULT 0,
                featured BOOLEAN DEFAULT FALSE,
                status TEXT DEFAULT 'active',
                concept_data TEXT,
                code_data TEXT,
                assets_data TEXT
            )
        ''')
        
        # Game ratings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_ratings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id TEXT,
                rating INTEGER,
                comment TEXT,
                user_ip TEXT,
                created_at REAL,
                FOREIGN KEY (game_id) REFERENCES games (id)
            )
        ''')
        
        # Game analytics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id TEXT,
                event_type TEXT,
                user_ip TEXT,
                timestamp REAL,
                data TEXT,
                FOREIGN KEY (game_id) REFERENCES games (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_game(self, game_data: Dict[str, Any], creator_ip: str = "unknown") -> Dict[str, Any]:
        """Save a generated game to the database and filesystem"""
        
        try:
            game_id = game_data['id']
            
            # Save to database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO games 
                (id, title, description, genre, creator_ip, created_at, concept_data, code_data, assets_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                game_id,
                game_data['title'],
                game_data['concept'].get('description', ''),
                game_data['concept'].get('genre', 'unknown'),
                creator_ip,
                game_data['created_at'],
                json.dumps(game_data['concept']),
                json.dumps(game_data['code']),
                json.dumps(game_data['assets'])
            ))
            
            conn.commit()
            conn.close()
            
            # Save game files to filesystem
            game_dir = os.path.join(self.games_dir, game_id)
            os.makedirs(game_dir, exist_ok=True)
            
            # Save HTML file
            with open(os.path.join(game_dir, 'index.html'), 'w') as f:
                f.write(game_data['code']['html'])
            
            # Save metadata
            with open(os.path.join(game_dir, 'metadata.json'), 'w') as f:
                json.dump({
                    'id': game_id,
                    'title': game_data['title'],
                    'concept': game_data['concept'],
                    'assets': game_data['assets'],
                    'instructions': game_data['instructions'],
                    'created_at': game_data['created_at']
                }, f, indent=2)
            
            return {
                'status': 'success',
                'message': f"Game '{game_data['title']}' saved successfully",
                'game_id': game_id,
                'play_url': f"/games/play/{game_id}",
                'share_url': f"/games/share/{game_id}"
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f"Failed to save game: {str(e)}"
            }
    
    def get_game(self, game_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a game by ID"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, description, genre, creator_ip, created_at, plays, likes, 
                   concept_data, code_data, assets_data
            FROM games WHERE id = ?
        ''', (game_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'genre': row[3],
                'creator_ip': row[4],
                'created_at': row[5],
                'plays': row[6],
                'likes': row[7],
                'concept': json.loads(row[8]),
                'code': json.loads(row[9]),
                'assets': json.loads(row[10])
            }
        
        return None
    
    def get_games_list(self, limit: int = 20, genre: str = None, featured: bool = None) -> List[Dict[str, Any]]:
        """Get list of games with optional filtering"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = '''
            SELECT id, title, description, genre, created_at, plays, likes, featured
            FROM games WHERE status = 'active'
        '''
        params = []
        
        if genre:
            query += ' AND genre = ?'
            params.append(genre)
        
        if featured is not None:
            query += ' AND featured = ?'
            params.append(featured)
        
        query += ' ORDER BY created_at DESC LIMIT ?'
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'genre': row[3],
                'created_at': row[4],
                'plays': row[5],
                'likes': row[6],
                'featured': bool(row[7]),
                'play_url': f"/games/play/{row[0]}",
                'share_url': f"/games/share/{row[0]}"
            }
            for row in rows
        ]
    
    def increment_plays(self, game_id: str, user_ip: str = "unknown"):
        """Increment play count for a game"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Update play count
        cursor.execute('UPDATE games SET plays = plays + 1 WHERE id = ?', (game_id,))
        
        # Log analytics
        cursor.execute('''
            INSERT INTO game_analytics (game_id, event_type, user_ip, timestamp, data)
            VALUES (?, ?, ?, ?, ?)
        ''', (game_id, 'play', user_ip, time.time(), '{}'))
        
        conn.commit()
        conn.close()
    
    def add_rating(self, game_id: str, rating: int, comment: str = "", user_ip: str = "unknown") -> Dict[str, Any]:
        """Add a rating to a game"""
        
        if not (1 <= rating <= 5):
            return {'status': 'error', 'message': 'Rating must be between 1 and 5'}
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Add rating
            cursor.execute('''
                INSERT INTO game_ratings (game_id, rating, comment, user_ip, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (game_id, rating, comment, user_ip, time.time()))
            
            # Update likes if rating is 4 or 5
            if rating >= 4:
                cursor.execute('UPDATE games SET likes = likes + 1 WHERE id = ?', (game_id,))
            
            conn.commit()
            conn.close()
            
            return {'status': 'success', 'message': 'Rating added successfully'}
            
        except Exception as e:
            return {'status': 'error', 'message': f'Failed to add rating: {str(e)}'}
    
    def get_game_stats(self, game_id: str) -> Dict[str, Any]:
        """Get statistics for a game"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get basic stats
        cursor.execute('''
            SELECT plays, likes FROM games WHERE id = ?
        ''', (game_id,))
        
        game_stats = cursor.fetchone()
        if not game_stats:
            conn.close()
            return {'status': 'error', 'message': 'Game not found'}
        
        # Get rating stats
        cursor.execute('''
            SELECT AVG(rating), COUNT(rating) FROM game_ratings WHERE game_id = ?
        ''', (game_id,))
        
        rating_stats = cursor.fetchone()
        
        # Get recent comments
        cursor.execute('''
            SELECT rating, comment, created_at FROM game_ratings 
            WHERE game_id = ? AND comment != '' 
            ORDER BY created_at DESC LIMIT 5
        ''', (game_id,))
        
        comments = cursor.fetchall()
        conn.close()
        
        return {
            'status': 'success',
            'plays': game_stats[0],
            'likes': game_stats[1],
            'average_rating': round(rating_stats[0], 1) if rating_stats[0] else 0,
            'total_ratings': rating_stats[1],
            'recent_comments': [
                {
                    'rating': comment[0],
                    'text': comment[1],
                    'created_at': comment[2]
                }
                for comment in comments
            ]
        }
    
    def get_showcase_html(self) -> str:
        """Generate HTML for the game showcase"""
        
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎮 AI Game Showcase</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            min-height: 100vh;
        }
        
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            padding: 20px; 
        }
        
        .header { 
            text-align: center; 
            margin-bottom: 40px; 
            background: rgba(255,255,255,0.1); 
            padding: 30px; 
            border-radius: 20px; 
            backdrop-filter: blur(10px); 
        }
        
        .games-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
            gap: 20px; 
            margin-bottom: 40px; 
        }
        
        .game-card { 
            background: rgba(255,255,255,0.1); 
            border-radius: 15px; 
            padding: 20px; 
            backdrop-filter: blur(10px); 
            transition: transform 0.3s ease; 
        }
        
        .game-card:hover { 
            transform: translateY(-5px); 
        }
        
        .game-title { 
            font-size: 20px; 
            font-weight: bold; 
            margin-bottom: 10px; 
            color: #FFD93D; 
        }
        
        .game-genre { 
            background: #4ECDC4; 
            color: #333; 
            padding: 4px 12px; 
            border-radius: 20px; 
            font-size: 12px; 
            display: inline-block; 
            margin-bottom: 10px; 
        }
        
        .game-description { 
            margin-bottom: 15px; 
            opacity: 0.9; 
        }
        
        .game-stats { 
            display: flex; 
            justify-content: space-between; 
            margin-bottom: 15px; 
            font-size: 14px; 
        }
        
        .game-actions { 
            display: flex; 
            gap: 10px; 
        }
        
        .btn { 
            padding: 8px 16px; 
            border: none; 
            border-radius: 8px; 
            cursor: pointer; 
            text-decoration: none; 
            display: inline-block; 
            text-align: center; 
            font-weight: bold; 
            transition: all 0.3s ease; 
        }
        
        .btn-play { 
            background: linear-gradient(45deg, #FF6B6B, #4ECDC4); 
            color: white; 
        }
        
        .btn-share { 
            background: linear-gradient(45deg, #A8E6CF, #88D8C0); 
            color: #333; 
        }
        
        .btn:hover { 
            transform: scale(1.05); 
        }
        
        .create-section { 
            text-align: center; 
            background: rgba(255,255,255,0.1); 
            padding: 30px; 
            border-radius: 20px; 
            backdrop-filter: blur(10px); 
        }
        
        .create-input { 
            width: 100%; 
            max-width: 600px; 
            padding: 15px; 
            border: none; 
            border-radius: 10px; 
            margin: 10px 0; 
            font-size: 16px; 
        }
        
        .create-btn { 
            background: linear-gradient(45deg, #FFD93D, #FF6B6B); 
            color: white; 
            padding: 15px 30px; 
            border: none; 
            border-radius: 10px; 
            font-size: 18px; 
            font-weight: bold; 
            cursor: pointer; 
            margin: 10px; 
        }
        
        .loading { 
            display: none; 
            margin: 20px 0; 
        }
        
        .spinner { 
            border: 4px solid rgba(255,255,255,0.3); 
            border-radius: 50%; 
            border-top: 4px solid #fff; 
            width: 40px; 
            height: 40px; 
            animation: spin 1s linear infinite; 
            margin: 0 auto; 
        }
        
        @keyframes spin { 
            0% { transform: rotate(0deg); } 
            100% { transform: rotate(360deg); } 
        }
        
        .result { 
            margin: 20px 0; 
            padding: 20px; 
            border-radius: 10px; 
            display: none; 
        }
        
        .result.success { 
            background: rgba(76, 175, 80, 0.2); 
            border: 2px solid #4CAF50; 
        }
        
        .result.error { 
            background: rgba(244, 67, 54, 0.2); 
            border: 2px solid #f44336; 
        }
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
            
            <input type="text" id="gamePrompt" class="create-input" 
                   placeholder="Describe your game idea... (e.g., 'A space shooter where you defend Earth from aliens')">
            
            <br>
            
            <button onclick="createGame()" class="create-btn">🎮 Create Game</button>
            
            <div id="loading" class="loading">
                <div class="spinner"></div>
                <p>AI is creating your game... This may take 30-60 seconds</p>
            </div>
            
            <div id="result" class="result">
                <div id="resultContent"></div>
            </div>
        </div>
        
        <h2 style="margin: 40px 0 20px 0; text-align: center;">🏆 Featured Games</h2>
        
        <div id="gamesGrid" class="games-grid">
            <!-- Games will be loaded here -->
        </div>
    </div>
    
    <script>
        async function createGame() {
            const prompt = document.getElementById('gamePrompt').value.trim();
            if (!prompt) {
                alert('Please describe your game idea!');
                return;
            }
            
            // Show loading
            document.getElementById('loading').style.display = 'block';
            document.getElementById('result').style.display = 'none';
            
            try {
                const response = await fetch('/api/games/create', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ prompt: prompt })
                });
                
                const data = await response.json();
                
                // Hide loading
                document.getElementById('loading').style.display = 'none';
                
                // Show result
                const resultDiv = document.getElementById('result');
                const resultContent = document.getElementById('resultContent');
                
                if (data.status === 'success') {
                    resultDiv.className = 'result success';
                    resultContent.innerHTML = `
                        <h3>🎉 Game Created Successfully!</h3>
                        <p><strong>${data.game.title}</strong></p>
                        <p>${data.game.concept.description}</p>
                        <div style="margin: 15px 0;">
                            <a href="${data.game.play_url}" class="btn btn-play" target="_blank">🎮 Play Now</a>
                            <a href="${data.game.share_url}" class="btn btn-share" target="_blank">📤 Share</a>
                        </div>
                    `;
                    
                    // Refresh games list
                    loadGames();
                } else {
                    resultDiv.className = 'result error';
                    resultContent.innerHTML = `
                        <h3>❌ Error</h3>
                        <p>${data.message}</p>
                    `;
                }
                
                resultDiv.style.display = 'block';
                
            } catch (error) {
                document.getElementById('loading').style.display = 'none';
                
                const resultDiv = document.getElementById('result');
                const resultContent = document.getElementById('resultContent');
                
                resultDiv.className = 'result error';
                resultContent.innerHTML = `
                    <h3>❌ Network Error</h3>
                    <p>Failed to create game. Please try again.</p>
                `;
                resultDiv.style.display = 'block';
            }
        }
        
        async function loadGames() {
            try {
                const response = await fetch('/api/games/list');
                const data = await response.json();
                
                const gamesGrid = document.getElementById('gamesGrid');
                
                if (data.status === 'success' && data.games.length > 0) {
                    gamesGrid.innerHTML = data.games.map(game => `
                        <div class="game-card">
                            <div class="game-title">${game.title}</div>
                            <div class="game-genre">${game.genre}</div>
                            <div class="game-description">${game.description}</div>
                            <div class="game-stats">
                                <span>🎮 ${game.plays} plays</span>
                                <span>❤️ ${game.likes} likes</span>
                            </div>
                            <div class="game-actions">
                                <a href="${game.play_url}" class="btn btn-play" target="_blank">🎮 Play</a>
                                <a href="${game.share_url}" class="btn btn-share" target="_blank">📤 Share</a>
                            </div>
                        </div>
                    `).join('');
                } else {
                    gamesGrid.innerHTML = `
                        <div style="grid-column: 1 / -1; text-align: center; padding: 40px;">
                            <h3>🎮 No games yet!</h3>
                            <p>Be the first to create an AI-generated game!</p>
                        </div>
                    `;
                }
                
            } catch (error) {
                console.error('Failed to load games:', error);
            }
        }
        
        // Load games on page load
        window.onload = loadGames;
        
        // Allow Enter key to create game
        document.getElementById('gamePrompt').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                createGame();
            }
        });
    </script>
</body>
</html>'''
    
    def get_game_player_html(self, game_id: str) -> str:
        """Generate HTML for playing a specific game"""
        
        game = self.get_game(game_id)
        if not game:
            return '<h1>Game not found</h1>'
        
        # Increment play count
        self.increment_plays(game_id)
        
        return game['code']['html']

# Global instance
showcase = GameShowcase()
