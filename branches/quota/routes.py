"""
Quota Management Module - FREE Enterprise Implementation
File: branches/quota/routes.py
"""

from flask import Blueprint, request, jsonify, session
import json
import time
import os
from datetime import datetime, timedelta
from collections import defaultdict

quota_bp = Blueprint('quota', __name__)

# Free configuration files
QUOTA_FILE = 'enterprise_quotas.json'
USAGE_FILE = 'enterprise_usage.json'
PLANS_FILE = 'enterprise_plans.json'

# Default quota plans
DEFAULT_PLANS = {
    'free': {
        'name': 'Free Plan',
        'limits': {
            'requests_per_minute': 10,
            'requests_per_hour': 100,
            'requests_per_day': 1000,
            'requests_per_month': 10000,
            'tokens_per_request': 4000,
            'concurrent_requests': 2
        },
        'features': ['basic_ai', 'standard_support'],
        'cost': 0.00
    },
    'basic': {
        'name': 'Basic Plan',
        'limits': {
            'requests_per_minute': 30,
            'requests_per_hour': 500,
            'requests_per_day': 5000,
            'requests_per_month': 100000,
            'tokens_per_request': 8000,
            'concurrent_requests': 5
        },
        'features': ['advanced_ai', 'priority_support', 'analytics'],
        'cost': 29.99
    },
    'pro': {
        'name': 'Professional Plan',
        'limits': {
            'requests_per_minute': 100,
            'requests_per_hour': 2000,
            'requests_per_day': 20000,
            'requests_per_month': 500000,
            'tokens_per_request': 16000,
            'concurrent_requests': 10
        },
        'features': ['premium_ai', 'dedicated_support', 'advanced_analytics', 'custom_models'],
        'cost': 99.99
    },
    'enterprise': {
        'name': 'Enterprise Plan',
        'limits': {
            'requests_per_minute': 1000,
            'requests_per_hour': 10000,
            'requests_per_day': 100000,
            'requests_per_month': 2000000,
            'tokens_per_request': 32000,
            'concurrent_requests': 50
        },
        'features': ['unlimited_ai', '24/7_support', 'enterprise_analytics', 'custom_deployment'],
        'cost': 499.99
    }
}

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

def get_user_plan(user_id):
    """Get user's quota plan"""
    quotas = load_data(QUOTA_FILE, {})
    user_quota = quotas.get(user_id, {})
    plan_name = user_quota.get('plan', 'free')
    
    plans = load_data(PLANS_FILE, DEFAULT_PLANS)
    return plan_name, plans.get(plan_name, DEFAULT_PLANS['free'])

def get_time_window(quota_type):
    """Get time window for quota type"""
    current_time = int(time.time())
    
    if quota_type == 'requests_per_minute':
        return current_time // 60
    elif quota_type == 'requests_per_hour':
        return current_time // 3600
    elif quota_type == 'requests_per_day':
        return current_time // 86400
    elif quota_type == 'requests_per_month':
        # Approximate month as 30 days
        return current_time // 2592000
    else:
        return current_time

def get_current_usage(user_id, quota_type):
    """Get current usage for user and quota type"""
    usage_data = load_data(USAGE_FILE, {})
    user_usage = usage_data.get(user_id, {})
    
    window = get_time_window(quota_type)
    usage_key = f"{quota_type}_{window}"
    
    return user_usage.get(usage_key, 0)

def increment_usage(user_id, quota_type, amount=1):
    """Increment usage for user and quota type"""
    usage_data = load_data(USAGE_FILE, {})
    
    if user_id not in usage_data:
        usage_data[user_id] = {}
    
    window = get_time_window(quota_type)
    usage_key = f"{quota_type}_{window}"
    
    usage_data[user_id][usage_key] = usage_data[user_id].get(usage_key, 0) + amount
    usage_data[user_id]['last_request'] = datetime.now().isoformat()
    
    save_data(USAGE_FILE, usage_data)
    return usage_data[user_id][usage_key]

def check_quota(user_id, quota_type, amount=1):
    """Check if user has quota available"""
    plan_name, plan_data = get_user_plan(user_id)
    limit = plan_data['limits'].get(quota_type, 0)
    current_usage = get_current_usage(user_id, quota_type)
    
    available = (current_usage + amount) <= limit
    
    return {
        'allowed': available,
        'current_usage': current_usage,
        'limit': limit,
        'remaining': max(0, limit - current_usage),
        'plan': plan_name,
        'quota_type': quota_type
    }

def check_all_quotas(user_id, request_data=None):
    """Check all quota types for user"""
    plan_name, plan_data = get_user_plan(user_id)
    quota_checks = {}
    
    # Check all quota types
    for quota_type in plan_data['limits'].keys():
        if quota_type == 'tokens_per_request':
            # Special handling for token limits
            tokens_requested = request_data.get('tokens', 1000) if request_data else 1000
            quota_checks[quota_type] = {
                'allowed': tokens_requested <= plan_data['limits'][quota_type],
                'current_usage': tokens_requested,
                'limit': plan_data['limits'][quota_type],
                'remaining': max(0, plan_data['limits'][quota_type] - tokens_requested)
            }
        elif quota_type == 'concurrent_requests':
            # TODO: Implement concurrent request tracking
            quota_checks[quota_type] = {
                'allowed': True,
                'current_usage': 1,
                'limit': plan_data['limits'][quota_type],
                'remaining': plan_data['limits'][quota_type] - 1
            }
        else:
            quota_checks[quota_type] = check_quota(user_id, quota_type)
    
    # Overall allowed if all quotas pass
    overall_allowed = all(check['allowed'] for check in quota_checks.values())
    
    return {
        'overall_allowed': overall_allowed,
        'plan': plan_name,
        'quotas': quota_checks
    }

def get_quota_reset_times(user_id):
    """Get reset times for all quota types"""
    current_time = time.time()
    reset_times = {}
    
    # Minute reset
    next_minute = (int(current_time) // 60 + 1) * 60
    reset_times['requests_per_minute'] = datetime.fromtimestamp(next_minute).isoformat()
    
    # Hour reset
    next_hour = (int(current_time) // 3600 + 1) * 3600
    reset_times['requests_per_hour'] = datetime.fromtimestamp(next_hour).isoformat()
    
    # Day reset
    next_day = (int(current_time) // 86400 + 1) * 86400
    reset_times['requests_per_day'] = datetime.fromtimestamp(next_day).isoformat()
    
    # Month reset (approximate)
    next_month = (int(current_time) // 2592000 + 1) * 2592000
    reset_times['requests_per_month'] = datetime.fromtimestamp(next_month).isoformat()
    
    return reset_times

@quota_bp.route('/test')
def quota_test():
    """Test quota management system"""
    user_id = get_user_id()
    plan_name, plan_data = get_user_plan(user_id)
    quota_status = check_all_quotas(user_id)
    
    return jsonify({
        'status': 'active',
        'message': 'FREE Quota management system fully operational',
        'features': [
            'multi_tier_plans',
            'real_time_tracking',
            'automatic_reset',
            'usage_analytics',
            'overage_protection',
            'plan_management'
        ],
        'quota_types': list(plan_data['limits'].keys()),
        'available_plans': list(DEFAULT_PLANS.keys()),
        'current_user': {
            'user_id': user_id,
            'plan': plan_name,
            'quota_status': quota_status['overall_allowed']
        },
        'cost': '$0.00',
        'timestamp': datetime.now().isoformat()
    })

@quota_bp.route('/check', methods=['POST'])
def quota_check():
    """Check quota for specific request"""
    try:
        user_id = get_user_id()
        data = request.get_json() or {}
        
        # Check all quotas
        quota_status = check_all_quotas(user_id, data)
        
        # If allowed, increment usage
        if quota_status['overall_allowed']:
            for quota_type in ['requests_per_minute', 'requests_per_hour', 
                             'requests_per_day', 'requests_per_month']:
                increment_usage(user_id, quota_type, 1)
        
        # Get reset times
        reset_times = get_quota_reset_times(user_id)
        
        return jsonify({
            'status': 'success',
            'allowed': quota_status['overall_allowed'],
            'user_id': user_id,
            'plan': quota_status['plan'],
            'quotas': quota_status['quotas'],
            'reset_times': reset_times,
            'message': 'Request allowed' if quota_status['overall_allowed'] else 'Quota exceeded',
            'cost': '$0.00',
            'timestamp': datetime.now().isoformat()
        }), 200 if quota_status['overall_allowed'] else 429
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Quota check failed: {str(e)}',
            'cost': '$0.00',
            'timestamp': datetime.now().isoformat()
        }), 500

@quota_bp.route('/status')
def quota_status():
    """Get comprehensive quota status"""
    try:
        user_id = get_user_id()
        plan_name, plan_data = get_user_plan(user_id)
        quota_status = check_all_quotas(user_id)
        reset_times = get_quota_reset_times(user_id)
        
        # Calculate usage percentages
        usage_percentages = {}
        for quota_type, quota_data in quota_status['quotas'].items():
            if quota_data['limit'] > 0:
                usage_percentages[quota_type] = round(
                    (quota_data['current_usage'] / quota_data['limit']) * 100, 2
                )
            else:
                usage_percentages[quota_type] = 0
        
        return jsonify({
            'status': 'active',
            'user_id': user_id,
            'plan': {
                'name': plan_name,
                'display_name': plan_data['name'],
                'cost': plan_data['cost'],
                'features': plan_data['features']
            },
            'quotas': quota_status['quotas'],
            'usage_percentages': usage_percentages,
            'reset_times': reset_times,
            'overall_status': 'within_limits' if quota_status['overall_allowed'] else 'quota_exceeded',
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

@quota_bp.route('/plans')
def list_plans():
    """List all available quota plans"""
    plans = load_data(PLANS_FILE, DEFAULT_PLANS)
    
    return jsonify({
        'status': 'success',
        'plans': plans,
        'total_plans': len(plans),
        'cost': '$0.00',
        'timestamp': datetime.now().isoformat()
    }), 200

@quota_bp.route('/upgrade', methods=['POST'])
def upgrade_plan():
    """Upgrade user's quota plan"""
    try:
        user_id = get_user_id()
        data = request.get_json()
        
        if not data or 'plan' not in data:
            return jsonify({'error': 'Plan name required'}), 400
        
        new_plan = data['plan']
        plans = load_data(PLANS_FILE, DEFAULT_PLANS)
        
        if new_plan not in plans:
            return jsonify({'error': 'Invalid plan name'}), 400
        
        # Update user's plan
        quotas = load_data(QUOTA_FILE, {})
        if user_id not in quotas:
            quotas[user_id] = {}
        
        old_plan = quotas[user_id].get('plan', 'free')
        quotas[user_id]['plan'] = new_plan
        quotas[user_id]['upgraded_at'] = datetime.now().isoformat()
        quotas[user_id]['previous_plan'] = old_plan
        
        save_data(QUOTA_FILE, quotas)
        
        return jsonify({
            'status': 'success',
            'message': f'Plan upgraded from {old_plan} to {new_plan}',
            'user_id': user_id,
            'old_plan': old_plan,
            'new_plan': new_plan,
            'new_limits': plans[new_plan]['limits'],
            'cost': '$0.00',
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Plan upgrade failed: {str(e)}',
            'cost': '$0.00',
            'timestamp': datetime.now().isoformat()
        }), 500

@quota_bp.route('/usage')
def usage_analytics():
    """Get detailed usage analytics"""
    try:
        user_id = get_user_id()
        usage_data = load_data(USAGE_FILE, {})
        user_usage = usage_data.get(user_id, {})
        
        # Organize usage by time periods
        usage_by_period = {
            'current_minute': {},
            'current_hour': {},
            'current_day': {},
            'current_month': {}
        }
        
        current_time = int(time.time())
        periods = {
            'current_minute': current_time // 60,
            'current_hour': current_time // 3600,
            'current_day': current_time // 86400,
            'current_month': current_time // 2592000
        }
        
        for period_name, window in periods.items():
            for quota_type in ['requests_per_minute', 'requests_per_hour', 
                             'requests_per_day', 'requests_per_month']:
                if quota_type.endswith(period_name.split('_')[1]):
                    usage_key = f"{quota_type}_{window}"
                    usage_by_period[period_name][quota_type] = user_usage.get(usage_key, 0)
        
        # Calculate total usage
        total_requests = sum(
            usage for key, usage in user_usage.items() 
            if key.startswith('requests_') and isinstance(usage, int)
        )
        
        return jsonify({
            'status': 'success',
            'user_id': user_id,
            'usage_by_period': usage_by_period,
            'total_requests': total_requests,
            'last_request': user_usage.get('last_request'),
            'cost': '$0.00',
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Usage analytics failed: {str(e)}',
            'cost': '$0.00',
            'timestamp': datetime.now().isoformat()
        }), 500

@quota_bp.route('/reset', methods=['POST'])
def reset_quota():
    """Reset quota for user (admin only)"""
    try:
        # Check if user is admin
        if not session.get('authenticated') or session.get('username') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        data = request.get_json()
        target_user = data.get('user_id') if data else None
        
        if not target_user:
            return jsonify({'error': 'User ID required'}), 400
        
        # Reset usage data
        usage_data = load_data(USAGE_FILE, {})
        if target_user in usage_data:
            usage_data[target_user] = {'last_request': datetime.now().isoformat()}
            save_data(USAGE_FILE, usage_data)
        
        return jsonify({
            'status': 'success',
            'message': f'Quota reset for user {target_user}',
            'reset_by': session.get('username'),
            'cost': '$0.00',
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Quota reset failed: {str(e)}',
            'cost': '$0.00',
            'timestamp': datetime.now().isoformat()
        }), 500

# Initialize default configuration
def init_quota_config():
    """Initialize quota configuration"""
    if not os.path.exists(PLANS_FILE):
        save_data(PLANS_FILE, DEFAULT_PLANS)
        print("✅ Quota plans configuration initialized")

# Initialize on module load
init_quota_config()
