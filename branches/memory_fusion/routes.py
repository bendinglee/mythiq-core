from flask import Blueprint, request, jsonify

fuse_bp = Blueprint("fuse_bp", __name__)

@fuse_bp.route("/fuse", methods=["POST"])
def fuse_memory():
    branches = request.json.get("branches", [])
    fused_context = "_".join(branches) if branches else "core_only"

    return jsonify({
        "branches": branches,
        "fusion_result": f"Memory branches fused into → {fused_context}",
        "status": "fusion complete"
    })
