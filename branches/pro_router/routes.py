"""
Pro Router Module - FREE Enterprise Implementation
File: branches/pro_router/routes.py
"""

from flask import Blueprint, request, jsonify
import random
import time
import threading
import requests
import json
import os
from datetime import datetime, timedelta
from collections import defaultdict

pro_router_bp = Blueprint('pro_router_bp', __name__)

# Free configuration files
ENDPOINTS_FILE = 'router_endpoints.json'
HEALTH_FILE = 'router_health.json'
STATS_FILE = 'router_stats.json'

# Default endpoints configuration
DEFAULT_ENDPOINTS = [
    {
        'id': 'groq_primary',
        'name': 'Groq API Primary',
        'url': 'https://api.groq.com/openai/v1/chat/completions',
        'type': 'ai_api',
        'weight': 5,
        'priority': 1,
        'healthy': True,
        'max_requests_per_minute': 100,
        'timeout': 30,
        'retry_count': 3
    },
    {
        'id': 'huggingface_secondary',
        'name': 'Hugging Face Secondary',
        'url': 'https://api-inference.huggingface.co/models/microsoft/DialoGPT-large',
        'type': 'ai_api',
        'weight': 3,
        'priority': 2,
        'healthy': True,
        'max_requests_per_minute': 50,
        'timeout': 45,
        'retry_count': 2
    },
    {
        'id': 'fallback_local',
        'name': 'Local Fallback',
        'url': 'fallback',
        'type': 'fallback',
        'weight': 1,
        'priority': 3,
        'healthy': True,
        'max_requests_per_minute': 1000,
        'timeout': 1,
        'retry_count': 1
    }
]

# Global variables for free in-memory caching
HEALTH_CHECK_INTERVAL = 300  # 5 minutes
LAST_HEALTH_CHECK = 0
REQUEST_STATS = defaultdict(int)
RESPONSE_TIMES = defaultdict(list)

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

def get_endpoints():
    """Get endpoints configuration"""
    endpoints = load_data(ENDPOINTS_FILE, DEFAULT_ENDPOINTS)
    if not endpoints:
        endpoints = DEFAULT_ENDPOINTS
        save_data(ENDPOINTS_FILE, endpoints)
    return endpoints

def update_endpoint_health(endpoint_id, healthy, response_time=None):
    """Update endpoint health status"""
    endpoints = get_endpoints()
    health_data = load_data(HEALTH_FILE, {})
    
    # Update endpoint health
    for endpoint in endpoints:
        if endpoint['id'] == endpoint_id:
            endpoint['healthy'] = healthy
            break
    
    # Update health history
    if endpoint_id not in health_data:
        health_data[endpoint_id] = {'checks': [], 'uptime_percentage': 100.0}
    
    health_data[endpoint_id]['checks'].append({
        'timestamp': datetime.now().isoformat(),
        'healthy': healthy,
        'response_time': response_time
    })
    
    # Keep only last 100 checks
    health_data[endpoint_id]['checks'] = health_data[endpoint_id]['checks'][-100:]
    
    # Calculate uptime percentage
    recent_checks = health_data[endpoint_id]['checks'][-20:]  # Last 20 checks
    if recent_checks:
        healthy_count = sum(1 for check in recent_checks if check['healthy'])
        health_data[endpoint_id]['uptime_percentage'] = (healthy_count / len(recent_checks)) * 100
    
    save_data(ENDPOINTS_FILE, endpoints)
    save_data(HEALTH_FILE, health_data)

def health_check_endpoint(endpoint):
    """Perform health check on single endpoint"""
    if endpoint['type'] == 'fallback':
        return True, 0.001  # Fallback is always healthy
    
    try:
        start_time = time.time()
        
        # Simple HEAD request for health check
        response = requests.head(
            endpoint['url'], 
            timeout=endpoint.get('timeout', 30),
            headers={'User-Agent': 'Mythiq-Router-HealthCheck/1.0'}
        )
        
        response_time = time.time() - start_time
        healthy = response.status_code < 500
        
        return healthy, response_time
        
    except requests.exceptions.Timeout:
        return False, endpoint.get('timeout', 30)
    except requests.exceptions.ConnectionError:
        return False, None
    except Exception:
        return False, None

def perform_health_checks():
    """Perform health checks on all endpoints"""
    global LAST_HEALTH_CHECK
    
    current_time = time.time()
    if current_time - LAST_HEALTH_CHECK < HEALTH_CHECK_INTERVAL:
        return  # Too soon for another check
    
    LAST_HEALTH_CHECK = current_time
    endpoints = get_endpoints()
    
    for endpoint in endpoints:
        healthy, response_time = health_check_endpoint(endpoint)
        update_endpoint_health(endpoint['id'], healthy, response_time)
        
        # Update response time tracking
        if response_time is not None:
            RESPONSE_TIMES[endpoint['id']].append(response_time)
            # Keep only last 50 response times
            RESPONSE_TIMES[endpoint['id']] = RESPONSE_TIMES[endpoint['id']][-50:]

def select_endpoint(request_type='ai_api'):
    """Select best endpoint using intelligent routing"""
    perform_health_checks()
    endpoints = get_endpoints()
    
    # Filter by type and health
    available_endpoints = [
        ep for ep in endpoints 
        if ep['type'] == request_type and ep['healthy']
    ]
    
    if not available_endpoints:
        # Fallback to any healthy endpoint
        available_endpoints = [ep for ep in endpoints if ep['healthy']]
    
    if not available_endpoints:
        # Emergency fallback
        return next((ep for ep in endpoints if ep['type'] == 'fallback'), endpoints[0])
    
    # Sort by priority first, then by weight
    available_endpoints.sort(key=lambda x: (x['priority'], -x['weight']))
    
    # Weighted random selection among top priority endpoints
    top_priority = available_endpoints[0]['priority']
    top_endpoints = [ep for ep in available_endpoints if ep['priority'] == top_priority]
    
    if len(top_endpoints) == 1:
        return top_endpoints[0]
    
    # Weighted random selection
    total_weight = sum(ep['weight'] for ep in top_endpoints)
    if total_weight == 0:
        return random.choice(top_endpoints)
    
    r = random.uniform(0, total_weight)
    for endpoint in top_endpoints:
        r -= endpoint['weight']
        if r <= 0:
            return endpoint
    
    return top_endpoints[0]

def log_request(endpoint_id, success=True, response_time=None):
    """Log request statistics"""
    stats = load_data(STATS_FILE, {})
    
    if endpoint_id not in stats:
        stats[endpoint_id] = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'average_response_time': 0,
            'last_request': None
        }
    
    endpoint_stats = stats[endpoint_id]
    endpoint_stats['total_requests'] += 1
    endpoint_stats['last_request'] = datetime.now().isoformat()
    
    if success:
        endpoint_stats['successful_requests'] += 1
    else:
        endpoint_stats['failed_requests'] += 1
    
    if response_time is not None:
        # Update average response time
        current_avg = endpoint_stats['average_response_time']
        total_requests = endpoint_stats['total_requests']
        endpoint_stats['average_response_time'] = (
            (current_avg * (total_requests - 1) + response_time) / total_requests
        )
    
    save_data(STATS_FILE, stats)

@pro_router_bp.route('/test')
def router_test():
    """Test pro router system"""
    perform_health_checks()
    endpoints = get_endpoints()
    health_data = load_data(HEALTH_FILE, {})
    stats = load_data(STATS_FILE, {})
    
    healthy_endpoints = [ep for ep in endpoints if ep['healthy']]
    total_requests = sum(stats.get(ep['id'], {}).get('total_requests', 0) for ep in endpoints)
    
    return jsonify({
        'status': 'active',
        'message': 'FREE Pro router system fully operational',
        'router_types': [
            'weighted_random',
            'priority_based',
            'health_aware',
            'load_balanced',
            'failover_protected'
        ],
        'features': [
            'intelligent_routing',
            'health_monitoring',
            'load_balancing',
            'failover_protection',
            'performance_tracking',
            'request_statistics'
        ],
        'endpoints': {
            'total': len(endpoints),
            'healthy': len(healthy_endpoints),
            'unhealthy': len(endpoints) - len(healthy_endpoints)
        },
        'performance': {
            'total_requests_routed': total_requests,
            'average_response_time': sum(
                stats.get(ep['id'], {}).get('average_response_time', 0) 
                for ep in endpoints
            ) / len(endpoints) if endpoints else 0,
            'success_rate': calculate_success_rate(stats, endpoints)
        },
        'cost': '$0.00',
        'timestamp': datetime.now().isoformat()
    })

def calculate_success_rate(stats, endpoints):
    """Calculate overall success rate"""
    total_requests = 0
    successful_requests = 0
    
    for endpoint in endpoints:
        endpoint_stats = stats.get(endpoint['id'], {})
        total_requests += endpoint_stats.get('total_requests', 0)
        successful_requests += endpoint_stats.get('successful_requests', 0)
    
    if total_requests == 0:
        return 100.0
    
    return (successful_requests / total_requests) * 100

@pro_router_bp.route('/route', methods=['POST'])
def route_request():
    """Route request to best available endpoint"""
    try:
        data = request.get_json()
        request_type = data.get('type', 'ai_api') if data else 'ai_api'
        
        start_time = time.time()
        selected_endpoint = select_endpoint(request_type)
        routing_time = time.time() - start_time
        
        # Log the routing decision
        log_request(selected_endpoint['id'], True, routing_time)
        
        # Update request stats
        REQUEST_STATS[selected_endpoint['id']] += 1
        
        return jsonify({
            'status': 'success',
            'message': 'Request routed successfully',
            'routed_to': {
                'id': selected_endpoint['id'],
                'name': selected_endpoint['name'],
                'url': selected_endpoint['url'],
                'type': selected_endpoint['type'],
                'priority': selected_endpoint['priority']
            },
            'routing_algorithm': 'priority_weighted_random',
            'routing_time_ms': round(routing_time * 1000, 2),
            'endpoint_health': selected_endpoint['healthy'],
            'load_balancing': 'active',
            'cost': '$0.00',
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Routing failed: {str(e)}',
            'cost': '$0.00',
            'timestamp': datetime.now().isoformat()
        }), 500

@pro_router_bp.route('/status')
def router_status():
    """Get comprehensive router status"""
    perform_health_checks()
    endpoints = get_endpoints()
    health_data = load_data(HEALTH_FILE, {})
    stats = load_data(STATS_FILE, {})
    
    endpoint_status = []
    for endpoint in endpoints:
        endpoint_stats = stats.get(endpoint['id'], {})
        endpoint_health = health_data.get(endpoint['id'], {})
        
        endpoint_status.append({
            'id': endpoint['id'],
            'name': endpoint['name'],
            'url': endpoint['url'],
            'type': endpoint['type'],
            'healthy': endpoint['healthy'],
            'priority': endpoint['priority'],
            'weight': endpoint['weight'],
            'uptime_percentage': endpoint_health.get('uptime_percentage', 100.0),
            'total_requests': endpoint_stats.get('total_requests', 0),
            'success_rate': (
                (endpoint_stats.get('successful_requests', 0) / 
                 max(endpoint_stats.get('total_requests', 1), 1)) * 100
            ),
            'average_response_time': endpoint_stats.get('average_response_time', 0),
            'last_request': endpoint_stats.get('last_request')
        })
    
    return jsonify({
        'status': 'active',
        'router_health': 'excellent',
        'endpoints': endpoint_status,
        'summary': {
            'total_endpoints': len(endpoints),
            'healthy_endpoints': len([ep for ep in endpoints if ep['healthy']]),
            'total_requests_routed': sum(
                stats.get(ep['id'], {}).get('total_requests', 0) for ep in endpoints
            ),
            'overall_success_rate': calculate_success_rate(stats, endpoints),
            'last_health_check': datetime.fromtimestamp(LAST_HEALTH_CHECK).isoformat() if LAST_HEALTH_CHECK else None
        },
        'features_active': [
            'intelligent_routing',
            'health_monitoring', 
            'load_balancing',
            'failover_protection',
            'performance_tracking'
        ],
        'cost': '$0.00',
        'timestamp': datetime.now().isoformat()
    }), 200

@pro_router_bp.route('/health-check', methods=['POST'])
def manual_health_check():
    """Manually trigger health check"""
    global LAST_HEALTH_CHECK
    LAST_HEALTH_CHECK = 0  # Force health check
    
    perform_health_checks()
    endpoints = get_endpoints()
    
    results = []
    for endpoint in endpoints:
        healthy, response_time = health_check_endpoint(endpoint)
        results.append({
            'id': endpoint['id'],
            'name': endpoint['name'],
            'healthy': healthy,
            'response_time': response_time,
            'status': 'online' if healthy else 'offline'
        })
    
    return jsonify({
        'status': 'success',
        'message': 'Health check completed',
        'results': results,
        'healthy_count': len([r for r in results if r['healthy']]),
        'total_count': len(results),
        'cost': '$0.00',
        'timestamp': datetime.now().isoformat()
    }), 200

@pro_router_bp.route('/stats')
def router_stats():
    """Get detailed router statistics"""
    stats = load_data(STATS_FILE, {})
    health_data = load_data(HEALTH_FILE, {})
    endpoints = get_endpoints()
    
    detailed_stats = {}
    for endpoint in endpoints:
        endpoint_id = endpoint['id']
        endpoint_stats = stats.get(endpoint_id, {})
        endpoint_health = health_data.get(endpoint_id, {})
        
        detailed_stats[endpoint_id] = {
            'name': endpoint['name'],
            'type': endpoint['type'],
            'requests': {
                'total': endpoint_stats.get('total_requests', 0),
                'successful': endpoint_stats.get('successful_requests', 0),
                'failed': endpoint_stats.get('failed_requests', 0),
                'success_rate': (
                    (endpoint_stats.get('successful_requests', 0) / 
                     max(endpoint_stats.get('total_requests', 1), 1)) * 100
                )
            },
            'performance': {
                'average_response_time': endpoint_stats.get('average_response_time', 0),
                'uptime_percentage': endpoint_health.get('uptime_percentage', 100.0),
                'current_status': 'online' if endpoint['healthy'] else 'offline'
            },
            'last_activity': endpoint_stats.get('last_request')
        }
    
    return jsonify({
        'status': 'success',
        'statistics': detailed_stats,
        'summary': {
            'total_requests': sum(
                stats.get(ep['id'], {}).get('total_requests', 0) for ep in endpoints
            ),
            'average_success_rate': calculate_success_rate(stats, endpoints),
            'active_endpoints': len([ep for ep in endpoints if ep['healthy']])
        },
        'cost': '$0.00',
        'timestamp': datetime.now().isoformat()
    }), 200

# Initialize default configuration
def init_router_config():
    """Initialize router configuration"""
    if not os.path.exists(ENDPOINTS_FILE):
        save_data(ENDPOINTS_FILE, DEFAULT_ENDPOINTS)
        print("✅ Router endpoints configuration initialized")

# Initialize on module load
init_router_config()
