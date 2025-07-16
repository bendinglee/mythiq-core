from flask import Blueprint, request, jsonify

heal_bp = Blueprint("heal_bp", __name__)

# 🛡 /self/fallback — Fallback logic runner
@heal_bp.route("/fallback", methods=["POST"])
def fallback_logic():
    module = request.json.get("module", "unspecified")
    action = f"{module} rerouted to default pathway"
    return jsonify({
        "module": module,
        "fallback": action,
        "status": "fallback triggered"
    })

# 🔁 /self/recover — Trace and recover logic
@heal_bp.route("/recover", methods=["POST"])
def recover_logic():
    trace = request.json.get("trace", [])
    recovered = f"{len(trace)} operations restored"
    return jsonify({
        "trace": trace,
        "recovery": recovered,
        "status": "system state regenerated"
    })
