"""
Main Application - 100% Unique AI Game Creator
Revolutionary platform that generates completely unique games from user prompts

This application provides:
- Web interface for users to enter game descriptions
- Integration with the Dynamic AI Game Generator
- API endpoints for game creation and retrieval
- Game showcase for displaying unique creations
- Real-time AI-powered game generation
"""

import os
import json
from flask import Flask, request, jsonify, render_template_string, redirect, url_for
from dynamic_ai_game_generator import dynamic_game_generator

app = Flask(__name__)

# In-memory database for storing created games
games_db = {}

# --- HTML Templates ---

HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>100% Unique AI Game Creator</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            color: #ffffff;
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        #container {
            width: 100%;
            max-width: 800px;
            background: rgba(0, 0, 0, 0.3);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.18);
            text-align: center;
        }
        h1 {
            font-size: 3em;
            color: #00ffff;
            margin-bottom: 20px;
            text-shadow: 0 0 15px #00ffff;
        }
        textarea {
            width: 95%;
            height: 150px;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #00ffff;
            background: rgba(255, 255, 255, 0.1);
            color: #ffffff;
            font-size: 1.1em;
            margin-bottom: 20px;
            resize: vertical;
        }
        button {
            padding: 15px 30px;
            font-size: 1.2em;
            border: none;
            border-radius: 10px;
            background: #00ffff;
            color: #1a1a2e;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: bold;
        }
        button:hover {
            background: #ff00ff;
            box-shadow: 0 0 20px #ff00ff;
            transform: translateY(-3px);
        }
        #showcase-link {
            display: block;
            margin-top: 30px;
            color: #ffff00;
            font-size: 1.1em;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div id="container">
        <h1>100% Unique AI Game Creator</h1>
        <p>Describe any game you can imagine, and our revolutionary AI will create it for you from scratch!</p>
        <form action="/create" method="post">
            <textarea name="prompt" placeholder="e.g., A cyberpunk racing game where you drive a flying car through neon city streets, dodging traffic and collecting power-ups..."></textarea>
            <button type="submit">✨ Generate My Unique Game</button>
        </form>
        <a id="showcase-link" href="/showcase">View Previously Generated Games</a>
    </div>
</body>
</html>
"""

SHOWCASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Unique Game Showcase</title>
    <style>
        body { font-family: sans-serif; background: #1a1a2e; color: white; padding: 20px; }
        h1 { color: #00ffff; text-align: center; }
        #game-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
        .game-card {
            background: rgba(0,0,0,0.3); padding: 20px; border-radius: 10px;
            border: 1px solid #00ffff; text-align: center;
        }
        .game-card h2 { color: #ff00ff; }
        .game-card a { color: #ffff00; text-decoration: none; font-weight: bold; }
    </style>
</head>
<body>
    <h1>Unique Game Showcase</h1>
    <div id="game-list">
        {% for game_id, game in games.items() %}
            <div class="game-card">
                <h2>{{ game.title }}</h2>
                <p>{{ game.description }}</p>
                <a href="/play/{{ game_id }}">Play Game</a>
            </div>
        {% endfor %}
        {% if not games %}
            <p>No games have been generated yet. <a href="/">Create one!</a></p>
        {% endif %}
    </div>
    <p style="text-align:center; margin-top: 20px;"><a href="/">← Back to Creator</a></p>
</body>
</html>
"""

PLAY_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Playing: {{ game.title }}</title>
    <style>
        body { margin: 0; background: #000; }
        iframe { display: block; width: 100%; height: 100vh; border: none; }
    </style>
</head>
<body>
    <iframe srcdoc="{{ game.html_content|e }}"></iframe>
</body>
</html>
"""

# --- API Endpoints ---

@app.route('/')
def home():
    return render_template_string(HOME_TEMPLATE)

@app.route('/create', methods=['POST'])
def create_game_route():
    prompt = request.form.get('prompt')
    if not prompt:
        return "Prompt is required", 400
    
    try:
        # Generate the unique game
        game_data = dynamic_game_generator.generate_unique_game(prompt)
        
        # Combine HTML, CSS, and JS for the final game file
        full_html = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>{game_data['title']}</title>
    <style>{game_data['css_styles']}</style>
</head>
<body>
    {game_data['html_content']}
    <script>{game_data['javascript_code']}</script>
</body>
</html>"""
        
        game_data['html_content'] = full_html
        
        # Store game in our 'database'
        game_id = game_data['game_id']
        games_db[game_id] = game_data
        
        return redirect(url_for('play_game_route', game_id=game_id))
    
    except Exception as e:
        return f"Error generating game: {e}", 500

@app.route('/showcase')
def showcase_route():
    return render_template_string(SHOWCASE_TEMPLATE, games=games_db)

@app.route('/play/<game_id>')
def play_game_route(game_id):
    game = games_db.get(game_id)
    if not game:
        return "Game not found", 404
    
    # The HTML content is already a full document, so we can render it directly
    return render_template_string(game['html_content'])

@app.route('/api/games/<game_id>')
def get_game_api(game_id):
    game = games_db.get(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404
    return jsonify(game)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)

"""
This is a simplified main application. In a real-world scenario, you would:
- Use a proper database (like SQLite, PostgreSQL) instead of an in-memory dictionary.
- Have more robust error handling and logging.
- Implement user authentication to manage who can create and view games.
- Use a more sophisticated template engine like Jinja2 with separate files.
- Add more features to the showcase, like sorting, searching, and rating games.
"""
