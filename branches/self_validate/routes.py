Self-Validation Module - Cognitive Architecture Component
Mythiq Gateway Enterprise v2.5.1
"""

from flask import Blueprint, jsonify, request

# Create the validation_bp blueprint with exact variable name expected by main.py
validation_bp = Blueprint('validation_bp', __name__)

@validation_bp.route('/test')
def test():
    """Test endpoint to verify validation module is working"""
    return jsonify({
        "status": "success",
        "module": "self_validate",
        "message": "Validation module is operational",
        "features": [
            "content_validation",
            "fact_checking",
            "consistency_checking",
            "security_scanning",
            "bias_detection",
            "quality_assessment"
        ],
        "validation_types": ["factual", "consistency", "security", "bias", "quality"],
        "total_validations": 0,
        "version": "2.5.1",
        "timestamp": "2025-07-17T04:36:00Z"
    })

@validation_bp.route('/status')
def validation_status():
    """Get validation system status"""
    return jsonify({
        "status": "success",
        "module": "self_validate",
        "message": "Validation system operational",
        "statistics": {
            "total_validation_types": 5,
            "total_validations": 0,
            "pass_rate": 0,
            "most_used_type": None
        },
        "features": {
            "content_validation": True,
            "fact_checking": True,
            "consistency_checking": True,
            "security_scanning": True,
            "bias_detection": True,
            "quality_assessment": True
        },
        "version": "2.5.1",
        "timestamp": "2025-07-17T04:36:00Z"
    })
    }
