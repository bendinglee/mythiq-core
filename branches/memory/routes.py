from flask import Blueprint, jsonify, request
from datetime import datetime

# IMPORTANT: This variable name must match exactly what main.py expects
memory_bp = Blueprint("memory_bp", __name__)

@memory_bp.route("/test", methods=["GET"])
def test_memory():
    """Test endpoint for the memory system module"""
    return jsonify({
        "status": "ok",
        "module": "memory",
        "message": "Memory service is online!"
    })

@memory_bp.route("/status", methods=["GET"])
def status():
    """Status endpoint for the memory system module"""
    return jsonify({
        "status": "operational",
        "module": "memory",
        "memory_usage": "45%",
        "entries": 128,
        "retention_policy": "adaptive",
        "features": ["basic", "advanced", "enterprise"],
        "version": "1.0.0"
    })
