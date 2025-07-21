#!/usr/bin/env python3
"""
🗄️ Database Manager - Persistent Game Storage System
Handles SQLite database operations for game storage, user management, and analytics
"""

import sqlite3
import json
import time
import os
from typing import Dict, List, Any, Optional
from contextlib import contextmanager

class DatabaseManager:
    """Manages SQLite database for persistent game storage"""
    
    def __init__(self, db_path: str = "mythiq_games.db"):
        self.db_path = db_path
        self.init_database()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like access
        try:
            yield conn
        finally:
            conn.close()
    
    def init_database(self):
        """Initialize database tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Games table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS games (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    genre TEXT,
                    concept TEXT,
                    html_code TEXT,
                    css_code TEXT,
                    javascript_code TEXT,
                    assets TEXT,
                    instructions TEXT,
                    created_at REAL,
                    updated_at REAL,
                    plays INTEGER DEFAULT 0,
                    likes INTEGER DEFAULT 0,
                    status TEXT DEFAULT 'active',
                    creator_ip TEXT,
                    featured BOOLEAN DEFAULT FALSE
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
            
            # User sessions table (for basic user tracking)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT UNIQUE,
                    ip_address TEXT,
                    user_agent TEXT,
                    created_at REAL,
                    last_active REAL,
                    games_created INTEGER DEFAULT 0,
                    games_played INTEGER DEFAULT 0
                )
            ''')
            
            conn.commit()
            print("✅ Database initialized successfully")
    
    def save_game(self, game_data: Dict[str, Any], creator_ip: str = None) -> bool:
        """Save a game to the database"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Check if game with same title already exists
                cursor.execute('SELECT id FROM games WHERE title = ?', (game_data['title'],))
                existing = cursor.fetchone()
                
                if existing:
                    # Update existing game
                    cursor.execute('''
                        UPDATE games SET
                            description = ?, genre = ?, concept = ?, html_code = ?,
                            css_code = ?, javascript_code = ?, assets = ?, instructions = ?,
                            updated_at = ?
                        WHERE title = ?
                    ''', (
                        game_data.get('description', ''),
                        game_data.get('genre', ''),
                        json.dumps(game_data.get('concept', {})),
                        game_data.get('code', {}).get('html', ''),
                        game_data.get('code', {}).get('css', ''),
                        game_data.get('code', {}).get('javascript', ''),
                        json.dumps(game_data.get('assets', {})),
                        json.dumps(game_data.get('instructions', {})),
                        time.time(),
                        game_data['title']
                    ))
                    print(f"✅ Updated existing game: {game_data['title']}")
                else:
                    # Insert new game
                    cursor.execute('''
                        INSERT INTO games (
                            id, title, description, genre, concept, html_code, css_code,
                            javascript_code, assets, instructions, created_at, updated_at,
                            creator_ip
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        game_data['id'],
                        game_data['title'],
                        game_data.get('description', ''),
                        game_data.get('concept', {}).get('genre', 'puzzle'),
                        json.dumps(game_data.get('concept', {})),
                        game_data.get('code', {}).get('html', ''),
                        game_data.get('code', {}).get('css', ''),
                        game_data.get('code', {}).get('javascript', ''),
                        json.dumps(game_data.get('assets', {})),
                        json.dumps(game_data.get('instructions', {})),
                        game_data.get('created_at', time.time()),
                        time.time(),
                        creator_ip
                    ))
                    print(f"✅ Saved new game: {game_data['title']}")
                
                conn.commit()
                return True
                
        except Exception as e:
            print(f"❌ Error saving game: {str(e)}")
            return False
    
    def get_all_games(self, limit: int = 50, status: str = 'active') -> List[Dict[str, Any]]:
        """Get all games from database"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM games 
                    WHERE status = ? 
                    ORDER BY featured DESC, plays DESC, created_at DESC 
                    LIMIT ?
                ''', (status, limit))
                
                games = []
                for row in cursor.fetchall():
                    game = {
                        'id': row['id'],
                        'title': row['title'],
                        'description': row['description'],
                        'genre': row['genre'],
                        'concept': json.loads(row['concept']) if row['concept'] else {},
                        'code': {
                            'html': row['html_code'],
                            'css': row['css_code'],
                            'javascript': row['javascript_code']
                        },
                        'assets': json.loads(row['assets']) if row['assets'] else {},
                        'instructions': json.loads(row['instructions']) if row['instructions'] else {},
                        'created_at': row['created_at'],
                        'updated_at': row['updated_at'],
                        'plays': row['plays'],
                        'likes': row['likes'],
                        'status': row['status'],
                        'featured': bool(row['featured']),
                        'play_url': f'/games/play/{row["id"]}',
                        'share_url': f'/games/share/{row["id"]}'
                    }
                    games.append(game)
                
                print(f"✅ Retrieved {len(games)} games from database")
                return games
                
        except Exception as e:
            print(f"❌ Error retrieving games: {str(e)}")
            return []
    
    def get_game_by_id(self, game_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific game by ID"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM games WHERE id = ?', (game_id,))
                row = cursor.fetchone()
                
                if row:
                    return {
                        'id': row['id'],
                        'title': row['title'],
                        'description': row['description'],
                        'genre': row['genre'],
                        'concept': json.loads(row['concept']) if row['concept'] else {},
                        'code': {
                            'html': row['html_code'],
                            'css': row['css_code'],
                            'javascript': row['javascript_code']
                        },
                        'assets': json.loads(row['assets']) if row['assets'] else {},
                        'instructions': json.loads(row['instructions']) if row['instructions'] else {},
                        'created_at': row['created_at'],
                        'updated_at': row['updated_at'],
                        'plays': row['plays'],
                        'likes': row['likes'],
                        'status': row['status'],
                        'featured': bool(row['featured'])
                    }
                return None
                
        except Exception as e:
            print(f"❌ Error retrieving game {game_id}: {str(e)}")
            return None
    
    def increment_plays(self, game_id: str, user_ip: str = None) -> bool:
        """Increment play count for a game"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Update play count
                cursor.execute('UPDATE games SET plays = plays + 1 WHERE id = ?', (game_id,))
                
                # Log analytics
                cursor.execute('''
                    INSERT INTO game_analytics (game_id, event_type, user_ip, timestamp)
                    VALUES (?, ?, ?, ?)
                ''', (game_id, 'play', user_ip, time.time()))
                
                conn.commit()
                return True
                
        except Exception as e:
            print(f"❌ Error incrementing plays for {game_id}: {str(e)}")
            return False
    
    def increment_likes(self, game_id: str, user_ip: str = None) -> bool:
        """Increment like count for a game"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Check if user already liked this game
                cursor.execute('''
                    SELECT id FROM game_analytics 
                    WHERE game_id = ? AND event_type = 'like' AND user_ip = ?
                ''', (game_id, user_ip))
                
                if cursor.fetchone():
                    return False  # Already liked
                
                # Update like count
                cursor.execute('UPDATE games SET likes = likes + 1 WHERE id = ?', (game_id,))
                
                # Log analytics
                cursor.execute('''
                    INSERT INTO game_analytics (game_id, event_type, user_ip, timestamp)
                    VALUES (?, ?, ?, ?)
                ''', (game_id, 'like', user_ip, time.time()))
                
                conn.commit()
                return True
                
        except Exception as e:
            print(f"❌ Error incrementing likes for {game_id}: {str(e)}")
            return False
    
    def delete_game(self, game_id: str) -> bool:
        """Delete a game (soft delete by setting status to 'deleted')"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE games SET status = ? WHERE id = ?', ('deleted', game_id))
                conn.commit()
                print(f"✅ Game {game_id} marked as deleted")
                return True
                
        except Exception as e:
            print(f"❌ Error deleting game {game_id}: {str(e)}")
            return False
    
    def set_featured(self, game_id: str, featured: bool = True) -> bool:
        """Set a game as featured"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE games SET featured = ? WHERE id = ?', (featured, game_id))
                conn.commit()
                print(f"✅ Game {game_id} featured status set to {featured}")
                return True
                
        except Exception as e:
            print(f"❌ Error setting featured status for {game_id}: {str(e)}")
            return False
    
    def get_analytics(self, days: int = 7) -> Dict[str, Any]:
        """Get analytics data for the last N days"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Time range
                start_time = time.time() - (days * 24 * 60 * 60)
                
                # Total games
                cursor.execute('SELECT COUNT(*) FROM games WHERE status = ?', ('active',))
                total_games = cursor.fetchone()[0]
                
                # Total plays
                cursor.execute('SELECT SUM(plays) FROM games WHERE status = ?', ('active',))
                total_plays = cursor.fetchone()[0] or 0
                
                # Total likes
                cursor.execute('SELECT SUM(likes) FROM games WHERE status = ?', ('active',))
                total_likes = cursor.fetchone()[0] or 0
                
                # Recent activity
                cursor.execute('''
                    SELECT COUNT(*) FROM game_analytics 
                    WHERE timestamp > ? AND event_type = ?
                ''', (start_time, 'play'))
                recent_plays = cursor.fetchone()[0]
                
                cursor.execute('''
                    SELECT COUNT(*) FROM game_analytics 
                    WHERE timestamp > ? AND event_type = ?
                ''', (start_time, 'like'))
                recent_likes = cursor.fetchone()[0]
                
                # Top games
                cursor.execute('''
                    SELECT title, plays, likes FROM games 
                    WHERE status = ? 
                    ORDER BY plays DESC 
                    LIMIT 5
                ''', ('active',))
                top_games = [{'title': row[0], 'plays': row[1], 'likes': row[2]} 
                           for row in cursor.fetchall()]
                
                return {
                    'total_games': total_games,
                    'total_plays': total_plays,
                    'total_likes': total_likes,
                    'recent_plays': recent_plays,
                    'recent_likes': recent_likes,
                    'top_games': top_games,
                    'period_days': days
                }
                
        except Exception as e:
            print(f"❌ Error getting analytics: {str(e)}")
            return {}
    
    def cleanup_old_analytics(self, days: int = 30):
        """Clean up old analytics data"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cutoff_time = time.time() - (days * 24 * 60 * 60)
                cursor.execute('DELETE FROM game_analytics WHERE timestamp < ?', (cutoff_time,))
                deleted = cursor.rowcount
                conn.commit()
                print(f"✅ Cleaned up {deleted} old analytics records")
                
        except Exception as e:
            print(f"❌ Error cleaning up analytics: {str(e)}")

# Global database instance
db_manager = DatabaseManager()
