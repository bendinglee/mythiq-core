from flask import Blueprint, request, jsonify
import time

bond_bp_social = Blueprint("bond_bp_social", __name__)

@bond_bp_social.route("/bonding", methods=["POST"])
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
