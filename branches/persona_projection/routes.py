from flask import Blueprint, request, jsonify

modecast_bp = Blueprint("modecast_bp", __name__)

@modecast_bp.route("/modecast", methods=["POST"])
def modecast():
    layers = request.json.get("layers", [])
    fused = " → ".join(layers)

    return jsonify({
        "projection": fused,
        "status": "persona modecast rendered"
    })
