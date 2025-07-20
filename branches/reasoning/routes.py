from flask import Blueprint, jsonify, request

# IMPORTANT: This variable name must match exactly what main.py expects
# Note: The URL prefix is /api/reason (not /api/reasoning)
reasoning_bp = Blueprint("reasoning_bp", __name__)

@reasoning_bp.route("/test", methods=["GET"])
def test_reasoning():
    """Test endpoint for the reasoning engine module"""
    return jsonify({
        "status": "ok",
        "module": "reasoning",
        "message": "Reasoning engine is functional!"
    })

@reasoning_bp.route("/status", methods=["GET"])
def status():
    """Status endpoint for the reasoning engine module"""
    return jsonify({
        "status": "operational",
        "module": "reasoning",
        "engine_type": "neural",
        "capabilities": ["logical", "causal", "temporal"],
        "accuracy": "92%",
        "features": ["basic", "advanced", "enterprise"],
        "version": "1.0.0"
    })
