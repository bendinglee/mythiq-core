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

@memory_bp.route("/store", methods=["POST"])
def store():
    """Store endpoint for the memory system module"""
    # This is a mock implementation - in a real system, you would store the memory
    content = request.json.get("content", "")
    memory_type = request.json.get("type", "conversation")
    
    # Generate a simple hash for the memory ID
    memory_id = f"mem-{hash(content) % 10000}"
    
    return jsonify({
        "status": "success",
        "message": "Memory stored successfully",
        "memory_id": memory_id,
        "type": memory_type,
        "retention": "long_term"
    })

@memory_bp.route("/retrieve", methods=["POST"])
def retrieve():
    """Retrieve endpoint for the memory system module"""
    # This is a mock implementation - in a real system, you would retrieve memories
    query = request.json.get("query", "")
    
    # Mock a memory retrieval
    return jsonify({
        "status": "success",
        "memories": [
            {
                "id": "mem-1234",
                "content": "Example memory content related to " + query,
                "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "type": "conversation",
                "relevance": 0.92
            }
        ]
    })

@memory_bp.route("/clear", methods=["POST"])
def clear():
    """Clear endpoint for the memory system module"""
    memory_type = request.json.get("type", "all")
    
    return jsonify({
        "status": "success",
        "message": f"Memory cleared successfully for type: {memory_type}",
        "cleared_entries": 5
    })
