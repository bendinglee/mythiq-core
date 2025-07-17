"""
Self-Validation Module - FREE Enterprise Implementation
File: branches/self_validate/routes.py
"""

from flask import Blueprint, request, jsonify, session
import json
import time
import os
import re
from datetime import datetime
from collections import defaultdict

validation_bp = Blueprint('validation_bp', __name__)

# Free configuration files
VALIDATION_FILE = 'enterprise_validation.json'
RULES_FILE = 'enterprise_validation_rules.json'
HISTORY_FILE = 'enterprise_validation_history.json'

# Default validation rules
DEFAULT_VALIDATION_RULES = {
    'content_quality': {
        'min_length': 10,
        'max_length': 10000,
        'required_elements': [],
        'forbidden_elements': ['spam', 'inappropriate'],
        'language_check': True
    },
    'format_validation': {
        'email_pattern': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        'url_pattern': r'https?://(?:[-\w.])+(?:\:[0-9]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?)?',
        'phone_pattern': r'^\+?1?-?\.?\s?\(?([0-9]{3})\)?[-\.\s]?([0-9]{3})[-\.\s]?([0-9]{4})$',
        'date_pattern': r'^\d{4}-\d{2}-\d{2}$'
    },
    'security_validation': {
        'sql_injection_patterns': [
            r'(\bUNION\b|\bSELECT\b|\bINSERT\b|\bDELETE\b|\bUPDATE\b|\bDROP\b)',
            r'(\bOR\b\s+\d+\s*=\s*\d+|\bAND\b\s+\d+\s*=\s*\d+)',
            r'(\'|\")(\s*;\s*|\s*--|\s*/\*)'
        ],
        'xss_patterns': [
            r'<script[^>]*>.*?</script>',
            r'javascript:',
            r'on\w+\s*=',
            r'<iframe[^>]*>.*?</iframe>'
        ],
        'command_injection_patterns': [
            r'(\||&|;|\$\(|\`)',
            r'(rm\s|del\s|format\s|shutdown\s)'
        ]
    },
    'business_rules': {
        'profanity_check': True,
        'sentiment_threshold': -0.5,
        'spam_indicators': ['urgent', 'act now', 'limited time', 'click here'],
        'required_fields': [],
        'data_consistency': True
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

def validate_content_quality(content, rules):
    """Validate content quality based on rules"""
    issues = []
    score = 100
    
    # Length validation
    if len(content) < rules.get('min_length', 0):
        issues.append(f"Content too short (minimum {rules.get('min_length', 0)} characters)")
        score -= 20
    
    if len(content) > rules.get('max_length', 10000):
        issues.append(f"Content too long (maximum {rules.get('max_length', 10000)} characters)")
        score -= 15
    
    # Required elements
    for element in rules.get('required_elements', []):
        if element.lower() not in content.lower():
            issues.append(f"Missing required element: {element}")
            score -= 10
    
    # Forbidden elements
    for element in rules.get('forbidden_elements', []):
        if element.lower() in content.lower():
            issues.append(f"Contains forbidden element: {element}")
            score -= 25
    
    # Basic language check
    if rules.get('language_check', False):
        # Simple checks for readability
        sentences = content.split('.')
        avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        
        if avg_sentence_length > 30:
            issues.append("Sentences may be too long for readability")
            score -= 5
        
        # Check for repeated words
        words = content.lower().split()
        word_count = {}
        for word in words:
            word_count[word] = word_count.get(word, 0) + 1
        
        repeated_words = [word for word, count in word_count.items() if count > len(words) * 0.1 and len(word) > 3]
        if repeated_words:
            issues.append(f"Excessive repetition of words: {', '.join(repeated_words[:3])}")
            score -= 10
    
    return max(0, score), issues

def validate_format(content, format_type, rules):
    """Validate content format"""
    pattern = rules.get('format_validation', {}).get(f'{format_type}_pattern')
    if not pattern:
        return False, f"No validation pattern for {format_type}"
    
    try:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return True, f"Valid {format_type} format"
        else:
            return False, f"Invalid {format_type} format"
    except Exception as e:
        return False, f"Format validation error: {str(e)}"

def validate_security(content, rules):
    """Validate content for security issues"""
    issues = []
    score = 100
    
    security_rules = rules.get('security_validation', {})
    
    # SQL injection check
    for pattern in security_rules.get('sql_injection_patterns', []):
        if re.search(pattern, content, re.IGNORECASE):
            issues.append("Potential SQL injection detected")
            score -= 50
            break
    
    # XSS check
    for pattern in security_rules.get('xss_patterns', []):
        if re.search(pattern, content, re.IGNORECASE):
            issues.append("Potential XSS attack detected")
            score -= 50
            break
    
    # Command injection check
    for pattern in security_rules.get('command_injection_patterns', []):
        if re.search(pattern, content, re.IGNORECASE):
            issues.append("Potential command injection detected")
            score -= 40
            break
    
    return max(0, score), issues

def validate_business_rules(content, rules):
    """Validate content against business rules"""
    issues = []
    score = 100
    
    business_rules = rules.get('business_rules', {})
    
    # Profanity check (basic)
    if business_rules.get('profanity_check', False):
        profanity_words = ['damn', 'hell', 'crap']  # Basic list for demo
        found_profanity = [word for word in profanity_words if word in content.lower()]
        if found_profanity:
            issues.append(f"Inappropriate language detected: {', '.join(found_profanity)}")
            score -= 30
    
    # Spam indicators
    spam_indicators = business_rules.get('spam_indicators', [])
    found_spam = [indicator for indicator in spam_indicators if indicator.lower() in content.lower()]
    if found_spam:
        issues.append(f"Spam indicators detected: {', '.join(found_spam)}")
        score -= 20
    
    # Basic sentiment analysis (simple keyword-based)
    positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic']
    negative_words = ['bad', 'terrible', 'awful', 'horrible', 'disgusting', 'hate']
    
    positive_count = sum(1 for word in positive_words if word in content.lower())
    negative_count = sum(1 for word in negative_words if word in content.lower())
    
    sentiment_score = (positive_count - negative_count) / max(len(content.split()), 1)
    threshold = business_rules.get('sentiment_threshold', -0.5)
    
    if sentiment_score < threshold:
        issues.append(f"Content sentiment too negative (score: {sentiment_score:.2f})")
        score -= 15
    
    return max(0, score), issues

def comprehensive_validation(content, validation_type='general', custom_rules=None):
    """Perform comprehensive validation"""
    rules = custom_rules or load_data(RULES_FILE, DEFAULT_VALIDATION_RULES)
    
    validation_results = {
        'overall_score': 0,
        'overall_status': 'unknown',
        'content_quality': {'score': 0, 'issues': []},
        'security': {'score': 0, 'issues': []},
        'business_rules': {'score': 0, 'issues': []},
        'format_validation': {'valid': True, 'message': 'No format validation requested'}
    }
    
    # Content quality validation
    quality_score, quality_issues = validate_content_quality(content, rules)
    validation_results['content_quality'] = {'score': quality_score, 'issues': quality_issues}
    
    # Security validation
    security_score, security_issues = validate_security(content, rules)
    validation_results['security'] = {'score': security_score, 'issues': security_issues}
    
    # Business rules validation
    business_score, business_issues = validate_business_rules(content, rules)
    validation_results['business_rules'] = {'score': business_score, 'issues': business_issues}
    
    # Calculate overall score
    scores = [quality_score, security_score, business_score]
    validation_results['overall_score'] = sum(scores) / len(scores)
    
    # Determine overall status
    if validation_results['overall_score'] >= 90:
        validation_results['overall_status'] = 'excellent'
    elif validation_results['overall_score'] >= 75:
        validation_results['overall_status'] = 'good'
    elif validation_results['overall_score'] >= 60:
        validation_results['overall_status'] = 'acceptable'
    elif validation_results['overall_score'] >= 40:
        validation_results['overall_status'] = 'poor'
    else:
        validation_results['overall_status'] = 'failed'
    
    return validation_results

@validation_bp.route('/test')
def validation_test():
    """Test validation system"""
    user_id = get_user_id()
    validation_data = load_data(VALIDATION_FILE, {})
    user_validation_count = len(validation_data.get(user_id, []))
    
    return jsonify({
        'status': 'active',
        'message': 'FREE Validation system fully operational',
        'validation_types': [
            'content_quality',
            'format_validation',
            'security_validation',
            'business_rules',
            'data_consistency',
            'compliance_check'
        ],
        'capabilities': [
            'content_analysis',
            'security_scanning',
            'format_checking',
            'business_rule_enforcement',
            'quality_scoring',
            'issue_identification'
        ],
        'security_checks': [
            'sql_injection_detection',
            'xss_prevention',
            'command_injection_detection',
            'profanity_filtering',
            'spam_detection'
        ],
        'current_user': {
            'user_id': user_id,
            'validations_performed': user_validation_count
        },
        'cost': '$0.00',
        'timestamp': datetime.now().isoformat()
    })

@validation_bp.route('/validate', methods=['POST'])
def validate_content():
    """Validate content based on specified criteria"""
    try:
        user_id = get_user_id()
        data = request.get_json()
        
        if not data or 'content' not in data:
            return jsonify({'error': 'Content required for validation'}), 400
        
        content = data['content']
        validation_type = data.get('type', 'general')
        custom_rules = data.get('rules')
        format_type = data.get('format_type')
        
        # Perform comprehensive validation
        validation_results = comprehensive_validation(content, validation_type, custom_rules)
        
        # Format validation if requested
        if format_type:
            rules = custom_rules or load_data(RULES_FILE, DEFAULT_VALIDATION_RULES)
            format_valid, format_message = validate_format(content, format_type, rules)
            validation_results['format_validation'] = {
                'valid': format_valid,
                'message': format_message
            }
        
        # Create validation record
        validation_record = {
            'id': f"validation_{int(time.time())}",
            'content_preview': content[:100] + '...' if len(content) > 100 else content,
            'validation_type': validation_type,
            'format_type': format_type,
            'results': validation_results,
            'timestamp': time.time(),
            'created_at': datetime.now().isoformat(),
            'user_feedback': None
        }
        
        # Store validation record
        validation_data = load_data(VALIDATION_FILE, {})
        if user_id not in validation_data:
            validation_data[user_id] = []
        
        validation_data[user_id].append(validation_record)
        
        # Keep only last 100 validation records per user
        validation_data[user_id] = sorted(validation_data[user_id], key=lambda x: x['timestamp'], reverse=True)[:100]
        
        save_data(VALIDATION_FILE, validation_data)
        
        return jsonify({
            'status': 'success',
            'validation_id': validation_record['id'],
            'overall_score': validation_results['overall_score'],
            'overall_status': validation_results['overall_status'],
            'content_quality': validation_results['content_quality'],
            'security': validation_results['security'],
            'business_rules': validation_results['business_rules'],
            'format_validation': validation_results['format_validation'],
            'recommendations': generate_recommendations(validation_results),
            'user_id': user_id,
            'cost': '$0.00',
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Validation failed: {str(e)}',
            'cost': '$0.00',
            'timestamp': datetime.now().isoformat()
        }), 500

def generate_recommendations(validation_results):
    """Generate recommendations based on validation results"""
    recommendations = []
    
    # Content quality recommendations
    if validation_results['content_quality']['score'] < 80:
        if any('too short' in issue for issue in validation_results['content_quality']['issues']):
            recommendations.append("Consider expanding your content with more details and examples")
        if any('too long' in issue for issue in validation_results['content_quality']['issues']):
            recommendations.append("Consider breaking your content into smaller, more digestible sections")
        if any('readability' in issue for issue in validation_results['content_quality']['issues']):
            recommendations.append("Use shorter sentences and simpler language for better readability")
    
    # Security recommendations
    if validation_results['security']['score'] < 90:
        recommendations.append("Review content for potential security issues and sanitize user inputs")
        recommendations.append("Avoid including executable code or suspicious patterns in content")
    
    # Business rules recommendations
    if validation_results['business_rules']['score'] < 80:
        if any('negative' in issue for issue in validation_results['business_rules']['issues']):
            recommendations.append("Consider using more positive language to improve user experience")
        if any('spam' in issue for issue in validation_results['business_rules']['issues']):
            recommendations.append("Remove promotional language that might be flagged as spam")
    
    # Overall recommendations
    if validation_results['overall_score'] < 70:
        recommendations.append("Overall content quality needs improvement - focus on the main issues identified")
    
    return recommendations

@validation_bp.route('/rules', methods=['GET', 'POST'])
def manage_validation_rules():
    """Get or update validation rules"""
    try:
        user_id = get_user_id()
        
        if request.method == 'GET':
            # Get current rules
            rules = load_data(RULES_FILE, DEFAULT_VALIDATION_RULES)
            
            return jsonify({
                'status': 'success',
                'rules': rules,
                'user_id': user_id,
                'cost': '$0.00',
                'timestamp': datetime.now().isoformat()
            }), 200
            
        else:  # POST
            # Update rules
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Rules data required'}), 400
            
            # Load existing rules and update
            rules = load_data(RULES_FILE, DEFAULT_VALIDATION_RULES)
            rules.update(data)
            
            save_data(RULES_FILE, rules)
            
            return jsonify({
                'status': 'success',
                'message': 'Validation rules updated successfully',
                'updated_rules': rules,
                'user_id': user_id,
                'cost': '$0.00',
                'timestamp': datetime.now().isoformat()
            }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Rules management failed: {str(e)}',
            'cost': '$0.00',
            'timestamp': datetime.now().isoformat()
        }), 500

@validation_bp.route('/history')
def validation_history():
    """Get validation history for user"""
    try:
        user_id = get_user_id()
        validation_data = load_data(VALIDATION_FILE, {})
        user_validations = validation_data.get(user_id, [])
        
        # Sort by timestamp (most recent first)
        user_validations = sorted(user_validations, key=lambda x: x['timestamp'], reverse=True)
        
        # Calculate statistics
        total_validations = len(user_validations)
        average_score = 0
        status_distribution = {}
        
        for record in user_validations:
            score = record.get('results', {}).get('overall_score', 0)
            average_score += score
            
            status = record.get('results', {}).get('overall_status', 'unknown')
            status_distribution[status] = status_distribution.get(status, 0) + 1
        
        if total_validations > 0:
            average_score /= total_validations
        
        return jsonify({
            'status': 'success',
            'user_id': user_id,
            'total_validations': total_validations,
            'average_score': round(average_score, 2),
            'status_distribution': status_distribution,
            'validation_history': user_validations[:20],  # Return last 20 records
            'cost': '$0.00',
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'History retrieval failed: {str(e)}',
            'cost': '$0.00',
            'timestamp': datetime.now().isoformat()
        }), 500

@validation_bp.route('/status')
def validation_status():
    """Get validation system status"""
    try:
        user_id = get_user_id()
        validation_data = load_data(VALIDATION_FILE, {})
        rules = load_data(RULES_FILE, DEFAULT_VALIDATION_RULES)
        
        # Calculate system statistics
        total_users = len(validation_data)
        total_validations = sum(len(user_data) for user_data in validation_data.values())
        
        user_validations = validation_data.get(user_id, [])
        user_validation_count = len(user_validations)
        
        # Recent activity
        recent_validations = sorted(user_validations, key=lambda x: x['timestamp'], reverse=True)[:5]
        
        # Rule statistics
        rule_categories = len(rules)
        total_rules = sum(len(category) if isinstance(category, dict) else 1 for category in rules.values())
        
        return jsonify({
            'status': 'active',
            'validation_engine': 'operational',
            'system_statistics': {
                'total_users': total_users,
                'total_validations': total_validations,
                'rule_categories': rule_categories,
                'total_rules': total_rules
            },
            'user_statistics': {
                'user_id': user_id,
                'validations_performed': user_validation_count,
                'recent_activity': len([v for v in user_validations if time.time() - v['timestamp'] < 86400])  # Last 24 hours
            },
            'recent_validations': recent_validations,
            'capabilities_active': [
                'content_quality_validation',
                'security_validation',
                'business_rules_validation',
                'format_validation',
                'comprehensive_scoring'
            ],
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

@validation_bp.route('/feedback', methods=['POST'])
def provide_validation_feedback():
    """Provide feedback on validation results"""
    try:
        user_id = get_user_id()
        data = request.get_json()
        
        if not data or 'validation_id' not in data or 'feedback' not in data:
            return jsonify({'error': 'Validation ID and feedback required'}), 400
        
        validation_id = data['validation_id']
        feedback = data['feedback']
        rating = data.get('rating', 0)  # 1-5 scale
        
        # Find and update validation record
        validation_data = load_data(VALIDATION_FILE, {})
        user_validations = validation_data.get(user_id, [])
        
        for record in user_validations:
            if record['id'] == validation_id:
                record['user_feedback'] = {
                    'feedback': feedback,
                    'rating': rating,
                    'provided_at': datetime.now().isoformat()
                }
                break
        
        validation_data[user_id] = user_validations
        save_data(VALIDATION_FILE, validation_data)
        
        return jsonify({
            'status': 'success',
            'message': 'Feedback recorded successfully',
            'validation_id': validation_id,
            'feedback_recorded': True,
            'user_id': user_id,
            'cost': '$0.00',
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Feedback recording failed: {str(e)}',
            'cost': '$0.00',
            'timestamp': datetime.now().isoformat()
        }), 500

# Initialize default configuration
def init_validation_config():
    """Initialize validation configuration"""
    if not os.path.exists(RULES_FILE):
        save_data(RULES_FILE, DEFAULT_VALIDATION_RULES)
    
    for filename in [VALIDATION_FILE, HISTORY_FILE]:
        if not os.path.exists(filename):
            save_data(filename, {})
    
    print("✅ Validation system configuration initialized")

# Initialize on module load
init_validation_config()
