from flask import Blueprint, request, jsonify

growth_bp = Blueprint("growth_bp", __name__)

@growth_bp.route("/grow", methods=["POST"])
def grow_persona():
    current = request.json.get("persona", {})
    influence = request.json.get("influence", "none")

    updated = {
        "name": current.get("name", "Mythiq"),
        "tone": "adaptive",
        "growth": f"Shaped by: {influence}"
    }

    return jsonify({
        "persona": updated,
        "status": "persona evolved"
    })
