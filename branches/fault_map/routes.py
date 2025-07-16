from flask import Blueprint, request, jsonify

fault_bp = Blueprint("fault_bp", __name__)

@fault_bp.route("/reason", methods=["POST"])
def error_reason():
    context = request.json.get("context", "unspecified")
    reason = "Missing payload or misrouted intent" if not context else "Trigger conflict within dispatcher tree"

    return jsonify({
        "context": context,
        "reason": reason,
        "status": "diagnostic complete"
    })
