from flask import Blueprint, request, jsonify
import time

bond_bp = Blueprint("bond_bp", __name__)

@bond_bp.route("/bonding", methods=["POST"])
def bonding():
    user_id = request.json.get("user", "anonymous")
    agent = request.json.get("agent", "Mythiq")
    strength = request.json.get("score", 0.5)

    relationship = {
        "user": user_id,
        "agent": agent,
        "bond_level": strength,
        "timestamp": int(time.time())
    }

    return jsonify({
        "relationship": relationship,
        "message": "Bonding state updated"
    })
