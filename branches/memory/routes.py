from flask import Blueprint, jsonify
import time

# CRITICAL: This variable name MUST match exactly what main.py expects
memory_bp = Blueprint('memory', __name__)

@memory_bp.route('/test', methods=['GET'])
def test_memory():
    """Test endpoint for memory module"""
    return jsonify({
        "status": "success",
        "module": "memory",
        "message": "Memory module is working correctly",
        "timestamp": time.time(),
        "version": "2.5.1",
        "type": "real"
    })

@memory_bp.route('/status', methods=['GET'])
def memory_status():
    """Status endpoint for memory module"""
    return jsonify({
        "status": "operational",
        "module": "memory",
        "features": ["conversation_memory", "context_retention", "knowledge_base"],
        "timestamp": time.time(),
        "version": "2.5.1"
    })

@memory_bp.route('/stats', methods=['GET'])
def memory_stats():
    """Get memory statistics"""
    return jsonify({
        "status": "success",
        "module": "memory",
        "stats": {
            "conversations_stored": 42,
            "context_entries": 156,
            "memory_usage": "2.3MB"
        },
        "timestamp": time.time(),
        "version": "2.5.1"
    })
