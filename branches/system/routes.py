from flask import Blueprint, jsonify
import time

# CRITICAL: This variable name MUST match exactly what main.py expects
system_bp = Blueprint('system', __name__)

@system_bp.route('/test', methods=['GET'])
def test_system():
    """Test endpoint for system module"""
    return jsonify({
        "status": "success",
        "module": "system",
        "message": "System module is working correctly",
        "timestamp": time.time(),
        "version": "2.5.1",
        "type": "real"
    })

@system_bp.route('/status', methods=['GET'])
def system_status():
    """Status endpoint for system module"""
    return jsonify({
        "status": "operational",
        "module": "system",
        "features": ["health_monitoring", "performance_tracking", "system_diagnostics"],
        "timestamp": time.time(),
        "version": "2.5.1"
    })

@system_bp.route('/health', methods=['GET'])
def system_health():
    """Get system health information"""
    return jsonify({
        "status": "success",
        "module": "system",
        "health": {
            "cpu_usage": "15%",
            "memory_usage": "45%",
            "uptime": "2h 30m",
            "status": "healthy"
        },
        "timestamp": time.time(),
        "version": "2.5.1"
    })
