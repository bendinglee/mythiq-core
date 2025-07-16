from flask import Blueprint, request, jsonify

express_bp = Blueprint("express_bp", __name__)

# 🎨 /chat/route/expressive — Route expression tokens
@express_bp.route("/route/expressive", methods=["POST"])
def expressive_route():
    input_data = request.json.get("tokens", [])
    routed = [{"token": t, "style": "emotive" if "!" in t else "neutral"} for t in input_data]

    return jsonify({
        "expression_map": routed,
        "status": "tokens routed with style"
    })
