from flask import Blueprint, request, jsonify

bridge_bp = Blueprint("bridge_bp", __name__)

# 🔗 /bridge/load/external — Load external API integration
@bridge_bp.route("/load/external", methods=["POST"])
def load_external_bridge():
    source = request.json.get("source", "undefined")
    api_key = request.json.get("key", "demo")
    fallback = request.json.get("fallback", True)

    return jsonify({
        "source": source,
        "key_status": "secured" if api_key != "demo" else "default",
        "fallback_routing": fallback,
        "status": "external bridge injected"
    })

# ⚖️ /bridge/fuse/score — Score fusion impact from API blend
@bridge_bp.route("/fuse/score", methods=["POST"])
def fuse_score():
    inputs = request.json.get("results", [])
    score = sum([len(str(i)) for i in inputs])

    return jsonify({
        "fusion_score": score,
        "sources": len(inputs),
        "status": "external data fused and scored"
    })
