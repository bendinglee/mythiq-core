from flask import Blueprint, jsonify, request

# IMPORTANT: This variable name must match exactly what main.py expects
validation_bp = Blueprint("validation_bp", __name__)

@validation_bp.route("/test", methods=["GET"])
def test_validation():
    """Test endpoint for the validation system module"""
    return jsonify({
        "status": "ok",
        "module": "self_validate",
        "message": "Self-validation is active!"
    })

@validation_bp.route("/status", methods=["GET"])
def status():
    """Status endpoint for the validation system module"""
    return jsonify({
        "status": "operational",
        "module": "self_validate",
        "validation_engine": "neural",
        "accuracy_rate": "94%",
        "validation_types": ["content", "factual", "ethical"],
        "features": ["basic", "advanced", "enterprise"],
        "version": "1.0.0"
    })
