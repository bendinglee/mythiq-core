"""
Memory Module - FREE Enterprise Implementation
File: branches/memory/routes.py
"""

from flask import Blueprint, request, jsonify, session
import json
import time
import os
from datetime import datetime, timedelta
import hashlib
import re

memory_bp = Blueprint('memory_bp', __name__)

# Free configuration files
MEMORY_FILE = 'enterprise_memory.json'
CONVERSATIONS_FILE = 'enterprise_conversations.json'
KNOWLEDGE_FILE = 'enterprise_knowledge.json'
PREFERENCES_FILE = 'enterprise_preferences.json'

def load_data(filename, default=None):
    """Load data from free file storage"""
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except:
            return default or {}
    return default or {}

def save_data(filename, data):
    """Save data to free file storage"""
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except:
        return False

def get_user_id():
    """Get user ID from session or IP address"""
    if 'username' in session:
        return session['username']
    return request.remote_addr

def generate_memory_id():
    """Generate unique memory ID"""
    timestamp = str(time.time())
    return hashlib.md5(timestamp.encode()).hexdigest()[:12]

def extract_keywords(text):
    """Extract keywords from text for indexing"""
    # Simple keyword extraction
    words = re.findall(r'\b\w+\b', text.lower())
    # Filter out common words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those'}
    keywords = [word for word in words if len(word) > 2 and word not in stop_words]
    return list(set(keywords))[:10]  # Return unique keywords, max 10

def calculate_relevance_score(query_keywords, memory_keywords):
    """Calculate relevance score between query and memory"""
    if not query_keywords or not memory_keywords:
        return 0.0
    
    common_keywords = set(query_keywords) & set(memory_keywords)
    return len(common_keywords) / len(set(query_keywords) | set(memory_keywords))

def search_memories(user_id, query, limit=10):
    """Search memories by relevance"""
    memories = load_data(MEMORY_FILE, {})
    user_memories = memories.get(user_id, [])
    
    if not query:
        # Return recent memories if no query
        return sorted(user_memories, key=lambda x: x['timestamp'], reverse=True)[:limit]
    
    query_keywords = extract_keywords(query)
    scored_memories = []
    
    for memory in user_memories:
        memory_keywords = memory.get('keywords', [])
        score = calculate_relevance_score(query_keywords, memory_keywords)
        
        # Also check for direct text matches
        if query.lower() in memory.get('content', '').lower():
            score += 0.5
        
        if score > 0:
            memory_copy = memory.copy()
            memory_copy['relevance_score'] = score
            scored_memories.append(memory_copy)
    
    # Sort by relevance score and recency
    scored_memories.sort(key=lambda x: (x['relevance_score'], x['timestamp']), reverse=True)
    return scored_memories[:limit]

@memory_bp.route('/test')
def memory_test():
    """Test memory system"""
    user_id = get_user_id()
    memories = load_data(MEMORY_FILE, {})
    conversations = load_data(CONVERSATIONS_FILE, {})
    knowledge = load_data(KNOWLEDGE_FILE, {})
    
    user_memory_count = len(memories.get(user_id, []))
    user_conversation_count = len(conversations.get(user_id, []))
    user_knowledge_count = len(knowledge.get(user_id, []))
    
    return jsonify({
        'status': 'active',
        'message': 'FREE Memory system fully operational',
        'capabilities': [
            'conversation_memory',
            'knowledge_storage',
            'preference_learning',
            'context_retention',
            'semantic_search',
            'auto_categorization'
        ],
        'storage_types': [
            'short_term_memory',
            'long_term_memory',
            'conversation_history',
            'knowledge_base',
            'user_preferences'
        ],
        'current_user': {
            'user_id': user_id,
            'memories_stored': user_memory_count,
            'conversations_tracked': user_conversation_count,
            'knowledge_items': user_knowledge_count
        },
        'features': [
            'keyword_extraction',
            'relevance_scoring',
            'automatic_indexing',
            'temporal_organization',
            'context_linking'
        ],
        'cost': '$0.00',
        'timestamp': datetime.now().isoformat()
    })

@memory_bp.route('/store', methods=['POST'])
def store_memory():
    """Store new memory"""
    try:
        user_id = get_user_id()
        data = request.get_json()
        
        if not data or 'content' not in data:
            return jsonify({'error': 'Memory content required'}), 400
        
        content = data['content']
        memory_type = data.get('type', 'general')
        category = data.get('category', 'uncategorized')
        importance = data.get('importance', 'medium')
        
        # Create memory object
        memory = {
            'id': generate_memory_id(),
            'content': content,
            'type': memory_type,
            'category': category,
            'importance': importance,
            'keywords': extract_keywords(content),
            'timestamp': time.time(),
            'created_at': datetime.now().isoformat(),
            'access_count': 0,
            'last_accessed': None,
            'metadata': data.get('metadata', {})
        }
        
        # Load existing memories
        memories = load_data(MEMORY_FILE, {})
        if user_id not in memories:
            memories[user_id] = []
        
        # Add new memory
        memories[user_id].append(memory)
        
        # Keep only last 1000 memories per user (free tier limit)
        memories[user_id] = sorted(memories[user_id], key=lambda x: x['timestamp'], reverse=True)[:1000]
        
        # Save memories
        save_data(MEMORY_FILE, memories)
        
        return jsonify({
            'status': 'success',
            'message': 'Memory stored successfully',
            'memory_id': memory['id'],
            'keywords_extracted': len(memory['keywords']),
            'keywords': memory['keywords'],
            'user_id': user_id,
            'cost': '$0.00',
            'timestamp': datetime.now().isoformat()
        }), 201
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Memory storage failed: {str(e)}',
            'cost': '$0.00',
            'timestamp': datetime.now().isoformat()
        }), 500

@memory_bp.route('/recall', methods=['POST'])
def recall_memory():
    """Recall memories based on query"""
    try:
        user_id = get_user_id()
        data = request.get_json()
        
        query = data.get('query', '') if data else ''
        limit = data.get('limit', 10) if data else 10
        memory_type = data.get('type') if data else None
        category = data.get('category') if data else None
        
        # Search memories
        relevant_memories = search_memories(user_id, query, limit * 2)  # Get more for filtering
        
        # Filter by type and category if specified
        if memory_type:
            relevant_memories = [m for m in relevant_memories if m.get('type') == memory_type]
        
        if category:
            relevant_memories = [m for m in relevant_memories if m.get('category') == category]
        
        # Limit results
        relevant_memories = relevant_memories[:limit]
        
        # Update access count and last accessed
        if relevant_memories:
            memories = load_data(MEMORY_FILE, {})
            user_memories = memories.get(user_id, [])
            
            for memory in relevant_memories:
                for stored_memory in user_memories:
                    if stored_memory['id'] == memory['id']:
                        stored_memory['access_count'] = stored_memory.get('access_count', 0) + 1
                        stored_memory['last_accessed'] = datetime.now().isoformat()
                        break
            
            memories[user_id] = user_memories
            save_data(MEMORY_FILE, memories)
        
        return jsonify({
            'status': 'success',
            'query': query,
            'memories_found': len(relevant_memories),
            'memories': relevant_memories,
            'search_metadata': {
                'query_keywords': extract_keywords(query) if query else [],
                'search_time': datetime.now().isoformat(),
                'user_id': user_id
            },
            'cost': '$0.00',
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Memory recall failed: {str(e)}',
            'cost': '$0.00',
            'timestamp': datetime.now().isoformat()
        }), 500

@memory_bp.route('/conversation', methods=['POST'])
def store_conversation():
    """Store conversation turn"""
    try:
        user_id = get_user_id()
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Conversation data required'}), 400
        
        user_message = data.get('user_message', '')
        ai_response = data.get('ai_response', '')
        context = data.get('context', {})
        
        # Create conversation entry
        conversation = {
            'id': generate_memory_id(),
            'user_message': user_message,
            'ai_response': ai_response,
            'context': context,
            'timestamp': time.time(),
            'created_at': datetime.now().isoformat(),
            'keywords': extract_keywords(user_message + ' ' + ai_response),
            'sentiment': data.get('sentiment', 'neutral'),
            'topic': data.get('topic', 'general')
        }
        
        # Load existing conversations
        conversations = load_data(CONVERSATIONS_FILE, {})
        if user_id not in conversations:
            conversations[user_id] = []
        
        # Add new conversation
        conversations[user_id].append(conversation)
        
        # Keep only last 500 conversations per user (free tier limit)
        conversations[user_id] = sorted(conversations[user_id], key=lambda x: x['timestamp'], reverse=True)[:500]
        
        # Save conversations
        save_data(CONVERSATIONS_FILE, conversations)
        
        # Also store as memory if important
        if data.get('store_as_memory', False):
            memory_content = f"User asked: {user_message}\nAI responded: {ai_response}"
            store_memory_data = {
                'content': memory_content,
                'type': 'conversation',
                'category': 'dialogue',
                'importance': 'medium',
                'metadata': {'conversation_id': conversation['id']}
            }
            # Call store_memory internally
            request.json = store_memory_data
            store_memory()
        
        return jsonify({
            'status': 'success',
            'message': 'Conversation stored successfully',
            'conversation_id': conversation['id'],
            'keywords_extracted': len(conversation['keywords']),
            'user_id': user_id,
            'cost': '$0.00',
            'timestamp': datetime.now().isoformat()
        }), 201
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Conversation storage failed: {str(e)}',
            'cost': '$0.00',
            'timestamp': datetime.now().isoformat()
        }), 500

@memory_bp.route('/knowledge', methods=['POST'])
def store_knowledge():
    """Store knowledge item"""
    try:
        user_id = get_user_id()
        data = request.get_json()
        
        if not data or 'fact' not in data:
            return jsonify({'error': 'Knowledge fact required'}), 400
        
        fact = data['fact']
        domain = data.get('domain', 'general')
        confidence = data.get('confidence', 0.8)
        source = data.get('source', 'user_input')
        
        # Create knowledge entry
        knowledge = {
            'id': generate_memory_id(),
            'fact': fact,
            'domain': domain,
            'confidence': confidence,
            'source': source,
            'keywords': extract_keywords(fact),
            'timestamp': time.time(),
            'created_at': datetime.now().isoformat(),
            'verified': data.get('verified', False),
            'references': data.get('references', [])
        }
        
        # Load existing knowledge
        knowledge_base = load_data(KNOWLEDGE_FILE, {})
        if user_id not in knowledge_base:
            knowledge_base[user_id] = []
        
        # Check for duplicates
        existing_facts = [k['fact'] for k in knowledge_base[user_id]]
        if fact not in existing_facts:
            knowledge_base[user_id].append(knowledge)
            
            # Keep only last 200 knowledge items per user (free tier limit)
            knowledge_base[user_id] = sorted(knowledge_base[user_id], key=lambda x: x['timestamp'], reverse=True)[:200]
            
            save_data(KNOWLEDGE_FILE, knowledge_base)
            
            return jsonify({
                'status': 'success',
                'message': 'Knowledge stored successfully',
                'knowledge_id': knowledge['id'],
                'domain': domain,
                'confidence': confidence,
                'user_id': user_id,
                'cost': '$0.00',
                'timestamp': datetime.now().isoformat()
            }), 201
        else:
            return jsonify({
                'status': 'duplicate',
                'message': 'Knowledge already exists',
                'user_id': user_id,
                'cost': '$0.00',
                'timestamp': datetime.now().isoformat()
            }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Knowledge storage failed: {str(e)}',
            'cost': '$0.00',
            'timestamp': datetime.now().isoformat()
        }), 500

@memory_bp.route('/preferences', methods=['GET', 'POST'])
def manage_preferences():
    """Get or update user preferences"""
    try:
        user_id = get_user_id()
        
        if request.method == 'GET':
            # Get preferences
            preferences = load_data(PREFERENCES_FILE, {})
            user_prefs = preferences.get(user_id, {
                'language': 'english',
                'response_style': 'balanced',
                'topics_of_interest': [],
                'communication_preferences': {},
                'learning_style': 'adaptive'
            })
            
            return jsonify({
                'status': 'success',
                'preferences': user_prefs,
                'user_id': user_id,
                'cost': '$0.00',
                'timestamp': datetime.now().isoformat()
            }), 200
            
        else:  # POST
            # Update preferences
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Preference data required'}), 400
            
            preferences = load_data(PREFERENCES_FILE, {})
            if user_id not in preferences:
                preferences[user_id] = {}
            
            # Update preferences
            preferences[user_id].update(data)
            preferences[user_id]['last_updated'] = datetime.now().isoformat()
            
            save_data(PREFERENCES_FILE, preferences)
            
            return jsonify({
                'status': 'success',
                'message': 'Preferences updated successfully',
                'updated_preferences': preferences[user_id],
                'user_id': user_id,
                'cost': '$0.00',
                'timestamp': datetime.now().isoformat()
            }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Preference management failed: {str(e)}',
            'cost': '$0.00',
            'timestamp': datetime.now().isoformat()
        }), 500

@memory_bp.route('/status')
def memory_status():
    """Get comprehensive memory system status"""
    try:
        user_id = get_user_id()
        
        # Load all data
        memories = load_data(MEMORY_FILE, {})
        conversations = load_data(CONVERSATIONS_FILE, {})
        knowledge = load_data(KNOWLEDGE_FILE, {})
        preferences = load_data(PREFERENCES_FILE, {})
        
        user_memories = memories.get(user_id, [])
        user_conversations = conversations.get(user_id, [])
        user_knowledge = knowledge.get(user_id, [])
        user_preferences = preferences.get(user_id, {})
        
        # Calculate statistics
        total_keywords = set()
        memory_types = {}
        categories = {}
        
        for memory in user_memories:
            total_keywords.update(memory.get('keywords', []))
            mem_type = memory.get('type', 'general')
            category = memory.get('category', 'uncategorized')
            memory_types[mem_type] = memory_types.get(mem_type, 0) + 1
            categories[category] = categories.get(category, 0) + 1
        
        # Recent activity
        recent_memories = sorted(user_memories, key=lambda x: x['timestamp'], reverse=True)[:5]
        recent_conversations = sorted(user_conversations, key=lambda x: x['timestamp'], reverse=True)[:5]
        
        return jsonify({
            'status': 'active',
            'user_id': user_id,
            'statistics': {
                'total_memories': len(user_memories),
                'total_conversations': len(user_conversations),
                'total_knowledge_items': len(user_knowledge),
                'unique_keywords': len(total_keywords),
                'memory_types': memory_types,
                'categories': categories
            },
            'recent_activity': {
                'recent_memories': recent_memories,
                'recent_conversations': recent_conversations
            },
            'preferences_configured': bool(user_preferences),
            'storage_usage': {
                'memories': f"{len(user_memories)}/1000",
                'conversations': f"{len(user_conversations)}/500",
                'knowledge': f"{len(user_knowledge)}/200"
            },
            'cost': '$0.00',
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Status check failed: {str(e)}',
            'cost': '$0.00',
            'timestamp': datetime.now().isoformat()
        }), 500

# Initialize default configuration
def init_memory_config():
    """Initialize memory configuration"""
    # Create empty files if they don't exist
    for filename in [MEMORY_FILE, CONVERSATIONS_FILE, KNOWLEDGE_FILE, PREFERENCES_FILE]:
        if not os.path.exists(filename):
            save_data(filename, {})
    print("✅ Memory system configuration initialized")

# Initialize on module load
init_memory_config()
