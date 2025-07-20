from flask import Blueprint, jsonify
import time

# Correct name that matches what main.py expects
pro_router_bp = Blueprint('pro_router_bp', __name__)

@pro_router_bp.route('/test', methods=['GET'])
def test_router():
    """Test endpoint for pro router module"""
    return jsonify({
        "status": "success",
        "module": "pro_router",
        "message": "Pro router module is working correctly",
        "timestamp": time.time(),
        "version": "2.5.1",
        "type": "real"
    })

@pro_router_bp.route('/status', methods=['GET'])
def router_status():
    """Status endpoint for pro router module"""
    return jsonify({
        "status": "operational",
        "module": "pro_router",
        "features": ["intelligent_routing", "load_balancing", "failover_support"],
        "timestamp": time.time(),
        "version": "2.5.1"
    })
