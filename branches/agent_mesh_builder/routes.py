from flask import Blueprint, request, jsonify

cluster_bp = Blueprint("cluster_bp", __name__)

@cluster_bp.route("/cluster", methods=["POST"])
def cluster_agents():
    count = request.json.get("count", 3)
    style = request.json.get("style", "cognitive")

    agents = [f"Agent_{i+1}" for i in range(count)]

    return jsonify({
        "cluster": agents,
        "mode": style,
        "status": "cluster spawned"
    })
