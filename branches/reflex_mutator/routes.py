from flask import Blueprint, request, jsonify

mutate_bp = Blueprint("mutate_bp", __name__)

@mutate_bp.route("/evolve", methods=["POST"])
def evolve_reflex():
    reflex = request.json.get("reflex", "default")
    success_rate = request.json.get("success_rate", 0.5)
    strength = "strong" if success_rate > 0.7 else "moderate"

    return jsonify({
        "reflex": reflex,
        "success_rate": success_rate,
        "adjusted_strength": strength,
        "status": "reflex evolution applied"
    })
