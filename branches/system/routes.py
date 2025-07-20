from flask import Blueprint, jsonify, request
import os
import platform
from datetime import datetime

# IMPORTANT: This variable name must match exactly what main.py expects
system_bp = Blueprint("system_bp", __name__)

@system_bp.route("/test", methods=["GET"])
def test_system():
    """Test endpoint for the system module"""
    return jsonify({
        "status": "ok",
        "module": "system",
        "message": "System module is operational!"
    })

@system_bp.route("/status", methods=["GET"])
def status():
    """Status endpoint for the system module"""
    # System information
    system_info = {
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "processor": platform.processor(),
        "hostname": platform.node()
    }
    
    return jsonify({
        "status": "operational",
        "module": "system",
        "system_info": system_info,
        "uptime": "12h 34m 56s",
        "features": ["basic", "advanced", "enterprise"],
        "version": "1.0.0"
    })
