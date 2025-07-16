from flask import Blueprint, request, jsonify
import random

predictor_bp = Blueprint("predictor_bp", __name__)

# ⚠️ /self/simulate/failure — Simulated error trace
@predictor_bp.route("/simulate/failure", methods=["POST"])
def simulate_failure():
    module = request.json.get("module", "dialogue_engine")
    fault = random.choice(["timeout", "null_ref", "bad_route"])

    return jsonify({
        "module": module,
        "simulated_fault": fault,
        "status": "error scenario generated"
    })
