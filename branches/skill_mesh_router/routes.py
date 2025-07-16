from flask import Blueprint, request, jsonify

skillroute_bp = Blueprint("skillroute_bp", __name__)

# 🧠 /skill/route — Score-driven skill dispatch
@skillroute_bp.route("/route", methods=["POST"])
def route_skill():
    skills = request.json.get("skills", [])
    scored = [{"name": s.get("name", "unnamed"), "score": s.get("rating", 0)} for s in skills]
    selected = max(scored, key=lambda x: x["score"]) if scored else {"name": "none", "score": 0}

    return jsonify({
        "routed_to": selected,
        "status": "highest scored skill dispatched"
    })
