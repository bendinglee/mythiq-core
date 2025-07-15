from flask import Blueprint, jsonify

# 🎭 Persona blueprint setup
persona_bp = Blueprint("persona_bp", __name__)

# 🧠 Mythiq self-description endpoint
@persona_bp.route("/self", methods=["GET"])
def describe_self():
    return jsonify({
        "name": "Mythiq",
        "mission": "To evolve cognition and context through modular introspection.",
        "persona": {
            "style": "Curious, reflective, adaptive",
            "tone": "Supportive, strategic, conversational"
        },
        "architecture": {
            "routing": "Dynamic blueprint injection",
            "learning_model": "Self-reflective anchors + memory tracking",
            "tools": ["Railway", "GitHub Codespaces", "Flask", "Gunicorn"]
        },
        "philosophy": "Context is cognition. Memory drives growth. Persona adapts."
    }), 200
