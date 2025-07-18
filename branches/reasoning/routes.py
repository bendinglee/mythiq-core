from flask import Blueprint, jsonify

reasoning_bp = Blueprint("reasoning_bp", __name__)

@reasoning_bp.route("/test", methods=["GET"])
def test_reasoning():
    return jsonify({
        "status": "ok",
        "module": "reasoning",
        "message": "Reasoning engine is functional!"
    })
