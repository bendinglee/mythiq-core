from flask import Blueprint, jsonify

explore_api = Blueprint("explore_api", __name__)

@explore_api.route("/scan", methods=["GET"])
def exploration_status():
    return jsonify({
        "exploration_api": "online",
        "message": "Exploration node ready to probe unknowns"
    })
