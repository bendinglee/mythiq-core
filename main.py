#!/usr/bin/env python3
"""
🚀 MYTHIQ GATEWAY - FIXED VERSION
AI-Powered Game Creation Platform with Working Integration
"""

import os
import json
import requests
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify, redirect, url_for
from flask_cors import CORS

# Import blueprints
try:
    from branches.auth_gate.routes import auth_bp
    from branches.pro_router.routes import pro_router_bp
    from branches.quota.routes import quota_bp
    from branches.memory.routes import memory_bp
    from branches.reasoning.routes import reasoning_bp
    from branches.self_validate.routes import validation_bp
    from branches.system.routes import system_bp
    print("✅ All blueprint imports successful")
except ImportError as e:
    print(f"❌ Blueprint import error: {e}")

# Import game systems
try:
    from game_engine import generate_game
    from game_showcase import showcase, add_game
    print("✅ Game systems imported successfully")
except ImportError as e:
    print(f"❌ Game system import error: {e}")

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mythiq-gateway-secret-key')

# Register blueprints
blueprints = [
    (auth_bp, 'auth_bp'),
    (pro_router_bp, 'pro_router_bp'), 
    (quota_bp, 'quota_bp'),
    (memory_bp, 'memory_bp'),
    (reasoning_bp, 'reasoning_bp'),
    (validation_bp, 'validation_bp'),
    (system_bp, 'system_bp')
]

registered_blueprints = []
for blueprint, name in blueprints:
    try:
        app.register_blueprint(blueprint)
        registered_blueprints.append(name)
        print(f"✅ Registered {name} successfully")
    except Exception as e:
        print(f"❌ Failed to register {name}: {e}")

print(f"🎉 Successfully registered {len(registered_blueprints)} blueprints: {registered_blueprints}")

# Register game showcase blueprint
app.register_blueprint(showcase)

# GROQ API Configuration
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
if GROQ_API_KEY:
    print(f"✅ GROQ API Key found: {GROQ_API_KEY[:10]}...")
else:
    print("❌ GROQ API Key not found")

@app.route('/')
def home():
    """Main dashboard"""
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Mythiq Gateway - AI Game Creation Platform</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: white;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            padding: 60px 0;
        }
        
        .header h1 {
            font-size: 4em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        
        .header p {
            font-size: 1.3em;
            opacity: 0.9;
            max-width: 600px;
            margin: 0 auto;
            line-height: 1.6;
        }
        
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin: 60px 0;
        }
        
        .feature-card {
            background: rgba(255,255,255,0.1);
            padding: 40px;
            border-radius: 15px;
            text-align: center;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.4);
        }
        
        .feature-icon {
            font-size: 3em;
            margin-bottom: 20px;
        }
        
        .feature-title {
            font-size: 1.5em;
            margin-bottom: 15px;
            color: #FFD700;
        }
        
        .feature-description {
            opacity: 0.9;
            line-height: 1.6;
        }
        
        .cta-section {
            text-align: center;
            padding: 60px 0;
        }
        
        .cta-button {
            display: inline-block;
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white;
            padding: 20px 40px;
            border-radius: 30px;
            text-decoration: none;
            font-size: 1.2em;
            font-weight: bold;
            margin: 10px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        
        .cta-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }
        
        .cta-button.secondary {
            background: linear-gradient(45deg, #2196F3, #1976D2);
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 40px 0;
        }
        
        .stat-card {
            background: rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 10px;
            text-align: center;
        }
        
        .stat-number {
            font-size: 2.5em;
            font-weight: bold;
            color: #FFD700;
        }
        
        .stat-label {
            opacity: 0.9;
            margin-top: 10px;
        }
        
        @media (max-width: 768px) {
            .header h1 {
                font-size: 2.5em;
            }
            
            .features {
                grid-template-columns: 1fr;
                gap: 20px;
            }
            
            .cta-button {
                display: block;
                margin: 10px 0;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Mythiq Gateway</h1>
            <p>The world's most advanced AI-powered game creation platform. Create professional games instantly with just a description!</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">∞</div>
                <div class="stat-label">Game Types</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">100%</div>
                <div class="stat-label">AI Powered</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">0</div>
                <div class="stat-label">Coding Required</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">⚡</div>
                <div class="stat-label">Instant Creation</div>
            </div>
        </div>
        
        <div class="features">
            <div class="feature-card">
                <div class="feature-icon">🎮</div>
                <div class="feature-title">AI Game Creation</div>
                <div class="feature-description">
                    Describe any game in natural language and watch our AI create a fully functional, playable game instantly.
                </div>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">🏆</div>
                <div class="feature-title">Game Showcase</div>
                <div class="feature-description">
                    Discover amazing games created by our community. Play, share, and get inspired by endless creativity.
                </div>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">📱</div>
                <div class="feature-title">Mobile Optimized</div>
                <div class="feature-description">
                    All games work perfectly on desktop, tablet, and mobile devices with touch controls and responsive design.
                </div>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">🚀</div>
                <div class="feature-title">Enterprise Ready</div>
                <div class="feature-description">
                    Professional-grade platform with advanced AI modules, analytics, and scalable architecture.
                </div>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">🎨</div>
                <div class="feature-title">Multiple Genres</div>
                <div class="feature-description">
                    Create platformers, shooters, puzzles, RPGs, racing games, strategy games, and more!
                </div>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <div class="feature-title">Instant Play</div>
                <div class="feature-description">
                    Games are created and ready to play in seconds. No downloads, no installations required.
                </div>
            </div>
        </div>
        
        <div class="cta-section">
            <h2>Ready to Create Amazing Games?</h2>
            <a href="/games/showcase" class="cta-button">🎮 Start Creating Games</a>
            <a href="/api/health" class="cta-button secondary">📊 System Status</a>
        </div>
    </div>
</body>
</html>
    ''')

@app.route('/api/games/create', methods=['POST'])
def create_game():
    """Create a new game"""
    try:
        data = request.get_json()
        description = data.get('description', '')
        
        if not description:
            return jsonify({'success': False, 'error': 'Description required'})
        
        # Generate game using AI
        result = generate_game(description)
        
        if result['success']:
            # Add to showcase
            game_id = add_game(
                title=result['title'],
                description=result['description'], 
                genre=result['genre'],
                game_code=result['code'],
                creator_ip=request.remote_addr
            )
            
            return jsonify({
                'success': True,
                'game_id': game_id,
                'title': result['title'],
                'description': result['description'],
                'genre': result['genre']
            })
        else:
            return jsonify({'success': False, 'error': result['error']})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/health')
def health_check():
    """System health check"""
    return jsonify({
        'status': 'healthy',
        'version': 'Mythiq Gateway Enterprise v3.1.0 - Fixed Edition',
        'timestamp': datetime.now().isoformat(),
        'features': {
            'ai_game_creation': True,
            'game_showcase': True,
            'mobile_optimized': True,
            'enterprise_modules': len(registered_blueprints),
            'groq_api': bool(GROQ_API_KEY)
        },
        'modules': {
            'registered_blueprints': len(registered_blueprints),
            'blueprint_names': registered_blueprints,
            'game_engine': 'active',
            'showcase': 'active'
        }
    })

@app.route('/api/test')
def test_endpoint():
    """Test endpoint"""
    return jsonify({
        'message': 'Mythiq Gateway is working!',
        'timestamp': datetime.now().isoformat(),
        'blueprints': registered_blueprints
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
