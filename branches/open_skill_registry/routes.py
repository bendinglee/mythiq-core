from flask import Blueprint, request, jsonify

skillreg_bp = Blueprint("skillreg_bp", __name__)

# ✅ /skill/register — Skill blueprint registration
@skillreg_bp.route("/register", methods=["POST"])
def register_skill():
    skill = request.json.get("name", "unnamed")
    hook = request.json.get("hook", "none")
    rating = request.json.get("rating", 0)

    return jsonify({
        "skill": skill,
        "hook": hook,
        "rating": rating,
        "status": "skill registered"
    })

# 🌍 /skill/load/community — Load from external community registry
@skillreg_bp.route("/load/community", methods=["GET"])
def load_community_skills():
    skills = [
        {"name": "tone_synth", "source": "github.com/mythiq-skills/tone_synth"},
        {"name": "vision_map", "source": "huggingface.co/mythiq/vision_map"}
    ]
    return jsonify({
        "community_skills": skills,
        "status": "community skill registry loaded"
    })
