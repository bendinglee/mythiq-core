from flask import Blueprint, request, jsonify

train_bp_rlstudio = Blueprint("train_bp_rlstudio", __name__)

@train_bp_rlstudio.route("/loop", methods=["POST"])
def loop_feedback():
    loop_data = request.json.get("cycle", [])
    return jsonify({
        "loops": len(loop_data),
        "status": "reinforcement cycle tracked"
    })
