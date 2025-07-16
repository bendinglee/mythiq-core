from flask import Blueprint, request, jsonify

merge_bp = Blueprint("merge_bp", __name__)

@merge_bp.route("/merge", methods=["POST"])
def merge_agents():
    agents = request.json.get("agents", [])
    node = f"SuperNode_{len(agents)}"

    return jsonify({
        "merged_agents": agents,
        "new_node": node,
        "status": "agent fusion complete"
    })
