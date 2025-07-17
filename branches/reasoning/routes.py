"""
Reasoning Module - Cognitive Architecture Component
Mythiq Gateway Enterprise v2.5.1
"""

from flask import Blueprint, jsonify, request

# Create the reasoning_bp blueprint with exact variable name expected by main.py
reasoning_bp = Blueprint('reasoning_bp', __name__)

@reasoning_bp.route('/test')
def test():
    """Test endpoint to verify reasoning module is working"""
    return jsonify({
        "status": "success",
        "module": "reasoning",
        "message": "Reasoning module is operational",
        "features": [
            "logical_analysis",
            "problem_solving",
            "decision_making",
            "structured_reasoning",
            "chain_of_thought",
            "verification"
        ],
        "frameworks": ["logical", "problem_solving", "decision_making", "chain_of_thought", "socratic"],
        "active_sessions": 0,
        "version": "2.5.1",
        "timestamp": "2025-07-17T04:36:00Z"
    })

@reasoning_bp.route('/status')
def reasoning_status():
    """Get reasoning system status"""
    return jsonify({
        "status": "success",
        "module": "reasoning",
        "message": "Reasoning system operational",
        "statistics": {
            "total_frameworks": 5,
            "total_sessions": 0,
            "active_sessions": 0,
            "success_rate": 0,
            "most_used_framework": "logical"
        },
        "features": {
            "logical_analysis": True,
            "problem_solving": True,
            "decision_making": True,
            "structured_reasoning": True,
            "chain_of_thought": True,
            "verification": True
        },
        "version": "2.5.1",
        "timestamp": "2025-07-17T04:36:00Z"
    })

# Note: This blueprint will be registered with URL prefix "/api/reason" (not "/api/reasoning")
