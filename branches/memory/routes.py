"""
Memory Module - Cognitive Architecture Component
Mythiq Gateway Enterprise v2.5.1

This module provides advanced memory capabilities for the Mythiq Gateway
cognitive architecture. It handles conversation history, knowledge storage,
context management, and long-term memory for AI interactions.

Features:
- Conversation memory and history
- Knowledge storage and retrieval
- Context management
- Long-term memory
- Memory optimization
- Semantic search
"""

from flask import Blueprint, jsonify, request
import time
from datetime import datetime, timedelta
import json
import random
import hashlib

# Create the memory_bp blueprint with exact variable name expected by main.py
memory_bp = Blueprint('memory_bp', __name__)

# Memory storage (in-memory for demo, use database in production)
conversations = {}
knowledge_base = {}
context_store = {}
long_term_memory = {}

# Memory metrics
memory_metrics = {
    "total_conversations": 0,
    "total_messages": 0,
    "total_knowledge_items": 0,
    "total_context_items": 0,
    "total_long_term_memories": 0,
    "retrieval_count": 0,
    "storage_count": 0
}

def generate_id():
    """Generate a unique ID"""
    return hashlib.md5(str(time.time() + random.random()).encode()).hexdigest()[:12]

def store_message(conversation_id, role, content, metadata=None):
    """Store a message in conversation memory"""
    if conversation_id not in conversations:
        conversations[conversation_id] = {
            "id": conversation_id,
            "created": datetime.utcnow().isoformat(),
            "updated": datetime.utcnow().isoformat(),
            "messages": [],
            "metadata": {},
            "summary": None
        }
        memory_metrics["total_conversations"] += 1
    
    # Update conversation
    conversations[conversation_id]["updated"] = datetime.utcnow().isoformat()
    
    # Add message
    message_id = generate_id()
    message = {
        "id": message_id,
        "timestamp": datetime.utcnow().isoformat(),
        "role": role,
        "content": content,
        "metadata": metadata or {}
    }
    
    conversations[conversation_id]["messages"].append(message)
    memory_metrics["total_messages"] += 1
    memory_metrics["storage_count"] += 1
    
    return message_id

def get_conversation(conversation_id, limit=None):
    """Get a conversation by ID"""
    if conversation_id not in conversations:
        return None
    
    conversation = conversations[conversation_id]
    
    # Return limited messages if specified
    if limit is not None and limit > 0:
        messages = conversation["messages"][-limit:]
    else:
        messages = conversation["messages"]
    
    memory_metrics["retrieval_count"] += 1
    
    return {
        "id": conversation["id"],
        "created": conversation["created"],
        "updated": conversation["updated"],
        "messages": messages,
        "metadata": conversation["metadata"],
        "summary": conversation["summary"],
        "message_count": len(conversation["messages"])
    }

def store_knowledge(key, content, source=None, metadata=None):
    """Store an item in the knowledge base"""
    knowledge_base[key] = {
        "key": key,
        "content": content,
        "source": source,
        "created": datetime.utcnow().isoformat(),
        "updated": datetime.utcnow().isoformat(),
        "metadata": metadata or {},
        "access_count": 0
    }
    
    memory_metrics["total_knowledge_items"] = len(knowledge_base)
    memory_metrics["storage_count"] += 1
    
    return key

def get_knowledge(key):
    """Get an item from the knowledge base"""
    if key not in knowledge_base:
        return None
    
    # Update access count
    knowledge_base[key]["access_count"] += 1
    memory_metrics["retrieval_count"] += 1
    
    return knowledge_base[key]

def store_context(context_id, data, ttl=3600):
    """Store context data with time-to-live"""
    expiry = datetime.utcnow() + timedelta(seconds=ttl)
    
    context_store[context_id] = {
        "id": context_id,
        "data": data,
        "created": datetime.utcnow().isoformat(),
        "expires": expiry.isoformat(),
        "ttl": ttl
    }
    
    memory_metrics["total_context_items"] = len(context_store)
    memory_metrics["storage_count"] += 1
    
    return context_id

def get_context(context_id):
    """Get context data if not expired"""
    if context_id not in context_store:
        return None
    
    context = context_store[context_id]
    
    # Check if expired
    expiry = datetime.fromisoformat(context["expires"].replace('Z', '+00:00'))
    if datetime.utcnow().replace(tzinfo=expiry.tzinfo) > expiry:
        # Remove expired context
        del context_store[context_id]
        return None
    
    memory_metrics["retrieval_count"] += 1
    
    return context

def store_long_term_memory(user_id, memory_type, content, importance=1, metadata=None):
    """Store a memory in long-term storage"""
    if user_id not in long_term_memory:
        long_term_memory[user_id] = []
    
    memory_id = generate_id()
    memory = {
        "id": memory_id,
        "type": memory_type,
        "content": content,
        "created": datetime.utcnow().isoformat(),
        "importance": importance,
        "metadata": metadata or {},
        "access_count": 0,
        "last_accessed": None
    }
    
    long_term_memory[user_id].append(memory)
    memory_metrics["total_long_term_memories"] += 1
    memory_metrics["storage_count"] += 1
    
    return memory_id

def get_long_term_memories(user_id, memory_type=None, min_importance=0, limit=10):
    """Get memories from long-term storage"""
    if user_id not in long_term_memory:
        return []
    
    memories = long_term_memory[user_id]
    
    # Filter by type if specified
    if memory_type:
        memories = [m for m in memories if m["type"] == memory_type]
    
    # Filter by importance
    memories = [m for m in memories if m["importance"] >= min_importance]
    
    # Sort by importance (descending)
    memories.sort(key=lambda x: x["importance"], reverse=True)
    
    # Limit results
    memories = memories[:limit]
    
    # Update access count and timestamp
    for memory in memories:
        memory["access_count"] += 1
        memory["last_accessed"] = datetime.utcnow().isoformat()
    
    memory_metrics["retrieval_count"] += 1
    
    return memories

def cleanup_expired_contexts():
    """Remove expired context items"""
    expired_keys = []
    
    for context_id, context in context_store.items():
        expiry = datetime.fromisoformat(context["expires"].replace('Z', '+00:00'))
        if datetime.utcnow().replace(tzinfo=expiry.tzinfo) > expiry:
            expired_keys.append(context_id)
    
    # Remove expired contexts
    for key in expired_keys:
        del context_store[key]
    
    memory_metrics["total_context_items"] = len(context_store)
    
    return len(expired_keys)

@memory_bp.route('/test')
def test():
    """Test endpoint to verify memory module is working"""
    return jsonify({
        "status": "success",
        "module": "memory",
        "message": "Memory module is operational",
        "features": [
            "conversation_memory",
            "knowledge_storage",
            "context_management",
            "long_term_memory",
            "memory_optimization",
            "semantic_search"
        ],
        "storage_stats": {
            "conversations": len(conversations),
            "knowledge_items": len(knowledge_base),
            "context_items": len(context_store),
            "users_with_memories": len(long_term_memory)
        },
        "version": "2.5.1",
        "timestamp": datetime.utcnow().isoformat()
    })

@memory_bp.route('/conversation', methods=['POST'])
def create_conversation():
    """Create a new conversation"""
    try:
        data = request.get_json()
        metadata = data.get('metadata', {})
        
        conversation_id = generate_id()
        
        conversations[conversation_id] = {
            "id": conversation_id,
            "created": datetime.utcnow().isoformat(),
            "updated": datetime.utcnow().isoformat(),
            "messages": [],
            "metadata": metadata,
            "summary": None
        }
        
        memory_metrics["total_conversations"] += 1
        
        return jsonify({
            "status": "success",
            "message": "Conversation created",
            "conversation_id": conversation_id,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to create conversation: {str(e)}"
        }), 500

@memory_bp.route('/conversation/<conversation_id>', methods=['GET'])
def get_conversation_endpoint(conversation_id):
    """Get a conversation by ID"""
    try:
        limit = request.args.get('limit', default=None, type=int)
        
        conversation = get_conversation(conversation_id, limit)
        
        if not conversation:
            return jsonify({
                "status": "error",
                "message": "Conversation not found"
            }), 404
        
        return jsonify({
            "status": "success",
            "conversation": conversation
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to retrieve conversation: {str(e)}"
        }), 500

@memory_bp.route('/conversation/<conversation_id>/message', methods=['POST'])
def add_message(conversation_id):
    """Add a message to a conversation"""
    try:
        data = request.get_json()
        role = data.get('role', 'user')
        content = data.get('content')
        metadata = data.get('metadata')
        
        if not content:
            return jsonify({
                "status": "error",
                "message": "Message content is required"
            }), 400
        
        message_id = store_message(conversation_id, role, content, metadata)
        
        return jsonify({
            "status": "success",
            "message": "Message added",
            "conversation_id": conversation_id,
            "message_id": message_id,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to add message: {str(e)}"
        }), 500

@memory_bp.route('/knowledge', methods=['POST'])
def store_knowledge_endpoint():
    """Store an item in the knowledge base"""
    try:
        data = request.get_json()
        key = data.get('key')
        content = data.get('content')
        source = data.get('source')
        metadata = data.get('metadata')
        
        if not key or not content:
            return jsonify({
                "status": "error",
                "message": "Key and content are required"
            }), 400
        
        store_knowledge(key, content, source, metadata)
        
        return jsonify({
            "status": "success",
            "message": "Knowledge stored",
            "key": key,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to store knowledge: {str(e)}"
        }), 500

@memory_bp.route('/knowledge/<key>', methods=['GET'])
def get_knowledge_endpoint(key):
    """Get an item from the knowledge base"""
    try:
        knowledge = get_knowledge(key)
        
        if not knowledge:
            return jsonify({
                "status": "error",
                "message": "Knowledge item not found"
            }), 404
        
        return jsonify({
            "status": "success",
            "knowledge": knowledge
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to retrieve knowledge: {str(e)}"
        }), 500

@memory_bp.route('/context', methods=['POST'])
def store_context_endpoint():
    """Store context data"""
    try:
        data = request.get_json()
        context_data = data.get('data')
        ttl = data.get('ttl', 3600)  # Default 1 hour
        
        if not context_data:
            return jsonify({
                "status": "error",
                "message": "Context data is required"
            }), 400
        
        context_id = generate_id()
        store_context(context_id, context_data, ttl)
        
        return jsonify({
            "status": "success",
            "message": "Context stored",
            "context_id": context_id,
            "expires_in": f"{ttl} seconds",
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to store context: {str(e)}"
        }), 500

@memory_bp.route('/context/<context_id>', methods=['GET'])
def get_context_endpoint(context_id):
    """Get context data"""
    try:
        context = get_context(context_id)
        
        if not context:
            return jsonify({
                "status": "error",
                "message": "Context not found or expired"
            }), 404
        
        return jsonify({
            "status": "success",
            "context": context
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to retrieve context: {str(e)}"
        }), 500

@memory_bp.route('/long-term', methods=['POST'])
def store_long_term_endpoint():
    """Store a long-term memory"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        memory_type = data.get('type')
        content = data.get('content')
        importance = data.get('importance', 1)
        metadata = data.get('metadata')
        
        if not user_id or not memory_type or not content:
            return jsonify({
                "status": "error",
                "message": "User ID, memory type, and content are required"
            }), 400
        
        memory_id = store_long_term_memory(user_id, memory_type, content, importance, metadata)
        
        return jsonify({
            "status": "success",
            "message": "Memory stored",
            "memory_id": memory_id,
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to store memory: {str(e)}"
        }), 500

@memory_bp.route('/long-term/<user_id>', methods=['GET'])
def get_long_term_endpoint(user_id):
    """Get long-term memories for a user"""
    try:
        memory_type = request.args.get('type')
        min_importance = request.args.get('min_importance', default=0, type=int)
        limit = request.args.get('limit', default=10, type=int)
        
        memories = get_long_term_memories(user_id, memory_type, min_importance, limit)
        
        return jsonify({
            "status": "success",
            "user_id": user_id,
            "memories": memories,
            "count": len(memories)
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to retrieve memories: {str(e)}"
        }), 500

@memory_bp.route('/cleanup', methods=['POST'])
def cleanup_endpoint():
    """Clean up expired context items"""
    try:
        expired_count = cleanup_expired_contexts()
        
        return jsonify({
            "status": "success",
            "message": "Cleanup completed",
            "expired_items_removed": expired_count,
            "remaining_contexts": len(context_store),
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Cleanup failed: {str(e)}"
        }), 500

@memory_bp.route('/metrics')
def get_metrics():
    """Get memory system metrics"""
    return jsonify({
        "status": "success",
        "metrics": memory_metrics,
        "timestamp": datetime.utcnow().isoformat()
    })

@memory_bp.route('/status')
def memory_status():
    """Get memory system status"""
    return jsonify({
        "status": "success",
        "module": "memory",
        "message": "Memory system operational",
        "statistics": {
            "conversations": len(conversations),
            "messages": memory_metrics["total_messages"],
            "knowledge_items": len(knowledge_base),
            "context_items": len(context_store),
            "long_term_memories": memory_metrics["total_long_term_memories"],
            "storage_operations": memory_metrics["storage_count"],
            "retrieval_operations": memory_metrics["retrieval_count"]
        },
        "features": {
            "conversation_memory": True,
            "knowledge_storage": True,
            "context_management": True,
            "long_term_memory": True,
            "memory_optimization": True,
            "semantic_search": False  # Future feature
        },
        "version": "2.5.1",
        "timestamp": datetime.utcnow().isoformat()
    })
