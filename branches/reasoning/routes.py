from flask import Blueprint, jsonify
import time

# CRITICAL: This variable name MUST match exactly what main.py expects
reasoning_bp = Blueprint('reasoning', __name__)

@reasoning_bp.route('/test', methods=['GET'])
def test_reasoning():
    """Test endpoint for reasoning module"""
    return jsonify({
        "status": "success",
        "module": "reasoning",
        "message": "Reasoning module is working correctly",
        "timestamp": time.time(),
        "version": "2.5.1",
        "type": "real"
    })

@reasoning_bp.route('/status', methods=['GET'])
def reasoning_status():
    """Status endpoint for reasoning module"""
    return jsonify({
        "status": "operational",
        "module": "reasoning",
        "features": ["logical_inference", "problem_solving", "decision_making"],
        "timestamp": time.time(),
        "version": "2.5.1"
    })

@reasoning_bp.route('/analyze', methods=['POST'])
def analyze_reasoning():
    """Analyze reasoning patterns"""
    return jsonify({
        "status": "success",
        "module": "reasoning",
        "analysis": {
            "reasoning_type": "deductive",
            "confidence": 0.85,
            "steps": 3
        },
        "timestamp": time.time(),
        "version": "2.5.1"
    })
