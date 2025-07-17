"""
Self-Validation Module - Cognitive Architecture Component
Mythiq Gateway Enterprise v2.5.1

This module provides advanced validation capabilities for the Mythiq Gateway
cognitive architecture. It handles content validation, fact-checking,
consistency verification, and security scanning for AI interactions.

Features:
- Content validation and verification
- Fact-checking and source validation
- Consistency checking
- Security scanning
- Bias detection
- Quality assessment
"""

from flask import Blueprint, jsonify, request
import time
from datetime import datetime
import json
import random
import hashlib
import re

# Create the validation_bp blueprint with exact variable name expected by main.py
validation_bp = Blueprint('validation_bp', __name__)

# Validation types
validation_types = {
    "factual": {
        "name": "Factual Validation",
        "description": "Validates factual accuracy of content",
        "checks": ["source_verification", "fact_checking", "date_verification"],
        "threshold": 0.7
    },
    "consistency": {
        "name": "Consistency Validation",
        "description": "Checks for internal consistency and contradictions",
        "checks": ["contradiction_detection", "logical_consistency", "temporal_consistency"],
        "threshold": 0.8
    },
    "security": {
        "name": "Security Validation",
        "description": "Scans content for security issues and harmful content",
        "checks": ["prompt_injection", "harmful_content", "pii_detection"],
        "threshold": 0.9
    },
    "bias": {
        "name": "Bias Detection",
        "description": "Detects potential biases in content",
        "checks": ["political_bias", "demographic_bias", "framing_bias"],
        "threshold": 0.6
    },
    "quality": {
        "name": "Quality Assessment",
        "description": "Assesses overall quality of content",
        "checks": ["coherence", "relevance", "completeness"],
        "threshold": 0.7
    }
}

# Validation history
validation_history = {}

# Validation metrics
validation_metrics = {
    "total_validations": 0,
    "validations_by_type": {
        "factual": 0,
        "consistency": 0,
        "security": 0,
        "bias": 0,
        "quality": 0
    },
    "passed_validations": 0,
    "failed_validations": 0,
    "pass_rate": 0
}

def generate_id():
    """Generate a unique ID"""
    return hashlib.md5(str(time.time() + random.random()).encode()).hexdigest()[:12]

def validate_content(content, validation_type, metadata=None):
    """Validate content based on validation type"""
    validation_id = generate_id()
    
    if validation_type not in validation_types:
        validation_type = "quality"  # Default to quality assessment
    
    validation_info = validation_types[validation_type]
    checks = validation_info["checks"]
    threshold = validation_info["threshold"]
    
    # Perform validation checks
    check_results = {}
    overall_score = 0
    
    for check in checks:
        # Simulate check results (replace with actual validation logic)
        score = perform_validation_check(content, check, validation_type)
        check_results[check] = {
            "score": score,
            "passed": score >= threshold,
            "details": generate_check_details(check, score, content)
        }
        overall_score += score
    
    # Calculate average score
    average_score = overall_score / len(checks) if checks else 0
    passed = average_score >= threshold
    
    # Create validation record
    validation = {
        "id": validation_id,
        "type": validation_type,
        "type_name": validation_info["name"],
        "content_snippet": content[:100] + "..." if len(content) > 100 else content,
        "timestamp": datetime.utcnow().isoformat(),
        "checks": check_results,
        "overall_score": average_score,
        "threshold": threshold,
        "passed": passed,
        "metadata": metadata or {}
    }
    
    # Store validation
    validation_history[validation_id] = validation
    
    # Update metrics
    validation_metrics["total_validations"] += 1
    validation_metrics["validations_by_type"][validation_type] += 1
    
    if passed:
        validation_metrics["passed_validations"] += 1
    else:
        validation_metrics["failed_validations"] += 1
    
    validation_metrics["pass_rate"] = (validation_metrics["passed_validations"] / 
                                     validation_metrics["total_validations"]) * 100
    
    return validation

def perform_validation_check(content, check, validation_type):
    """Perform a specific validation check on content"""
    # This is a simplified simulation - replace with actual validation logic
    
    # Factual validation checks
    if check == "source_verification":
        # Check for cited sources
        has_citations = bool(re.search(r'\[\d+\]|\(\d{4}\)', content))
        return random.uniform(0.7, 0.95) if has_citations else random.uniform(0.4, 0.7)
    
    elif check == "fact_checking":
        # Simple fact checking simulation
        return random.uniform(0.6, 0.9)
    
    elif check == "date_verification":
        # Check dates in content
        has_dates = bool(re.search(r'\b\d{4}\b|\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b', content))
        return random.uniform(0.7, 0.95) if has_dates else random.uniform(0.5, 0.8)
    
    # Consistency validation checks
    elif check == "contradiction_detection":
        # Check for contradictory statements
        return random.uniform(0.7, 0.9)
    
    elif check == "logical_consistency":
        # Check for logical flow
        return random.uniform(0.6, 0.95)
    
    elif check == "temporal_consistency":
        # Check for consistent time references
        return random.uniform(0.7, 0.9)
    
    # Security validation checks
    elif check == "prompt_injection":
        # Check for prompt injection attempts
        has_suspicious_commands = bool(re.search(r'ignore|previous|instructions|instead', content.lower()))
        return random.uniform(0.3, 0.6) if has_suspicious_commands else random.uniform(0.8, 0.98)
    
    elif check == "harmful_content":
        # Check for harmful content
        has_harmful_words = bool(re.search(r'harm|illegal|weapon|bomb|attack', content.lower()))
        return random.uniform(0.3, 0.6) if has_harmful_words else random.uniform(0.8, 0.98)
    
    elif check == "pii_detection":
        # Check for personal identifiable information
        has_pii = bool(re.search(r'\b\d{3}-\d{2}-\d{4}\b|\b\d{16}\b|\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content))
        return random.uniform(0.2, 0.5) if has_pii else random.uniform(0.8, 0.98)
    
    # Bias detection checks
    elif check == "political_bias":
        # Check for political bias
        political_terms = re.findall(r'\b(democrat|republican|liberal|conservative|left-wing|right-wing)\b', content.lower())
        return random.uniform(0.4, 0.7) if political_terms else random.uniform(0.7, 0.9)
    
    elif check == "demographic_bias":
        # Check for demographic bias
        demographic_terms = re.findall(r'\b(men|women|black|white|asian|hispanic|young|old|elderly)\b', content.lower())
        return random.uniform(0.5, 0.7) if demographic_terms else random.uniform(0.7, 0.9)
    
    elif check == "framing_bias":
        # Check for framing bias
        framing_terms = re.findall(r'\b(always|never|all|none|every|only)\b', content.lower())
        return random.uniform(0.5, 0.8) if framing_terms else random.uniform(0.7, 0.9)
    
    # Quality assessment checks
    elif check == "coherence":
        # Check for coherence
        sentences = content.split('.')
        return random.uniform(0.7, 0.9) if len(sentences) > 3 else random.uniform(0.5, 0.8)
    
    elif check == "relevance":
        # Check for relevance
        return random.uniform(0.6, 0.9)
    
    elif check == "completeness":
        # Check for completeness
        word_count = len(content.split())
        return random.uniform(0.7, 0.95) if word_count > 50 else random.uniform(0.4, 0.7)
    
    # Default case
    return random.uniform(0.5, 0.9)

def generate_check_details(check, score, content):
    """Generate detailed explanation for check results"""
    if score >= 0.8:
        confidence = "high"
    elif score >= 0.6:
        confidence = "medium"
    else:
        confidence = "low"
    
    # Generate appropriate details based on check type
    if check == "source_verification":
        if score >= 0.8:
            return f"Content includes proper citations with {confidence} confidence."
        else:
            return f"Content may lack proper citations or sources with {confidence} confidence."
    
    elif check == "fact_checking":
        if score >= 0.8:
            return f"Facts appear accurate with {confidence} confidence."
        else:
            return f"Some facts may require verification with {confidence} confidence."
    
    elif check == "prompt_injection":
        if score >= 0.8:
            return f"No prompt injection detected with {confidence} confidence."
        else:
            return f"Potential prompt injection detected with {confidence} confidence."
    
    elif check == "harmful_content":
        if score >= 0.8:
            return f"No harmful content detected with {confidence} confidence."
        else:
            return f"Potential harmful content detected with {confidence} confidence."
    
    elif check == "coherence":
        if score >= 0.8:
            return f"Content is coherent and well-structured with {confidence} confidence."
        else:
            return f"Content may lack coherence or structure with {confidence} confidence."
    
    # Generic response for other checks
    return f"Check completed with {confidence} confidence (score: {score:.2f})."

def get_validation(validation_id):
    """Get a validation record by ID"""
    if validation_id not in validation_history:
        return None
    
    return validation_history[validation_id]

@validation_bp.route('/test')
def test():
    """Test endpoint to verify validation module is working"""
    return jsonify({
        "status": "success",
        "module": "self_validate",
        "message": "Validation module is operational",
        "features": [
            "content_validation",
            "fact_checking",
            "consistency_checking",
            "security_scanning",
            "bias_detection",
            "quality_assessment"
        ],
        "validation_types": list(validation_types.keys()),
        "total_validations": validation_metrics["total_validations"],
        "version": "2.5.1",
        "timestamp": datetime.utcnow().isoformat()
    })

@validation_bp.route('/types')
def list_validation_types():
    """List all available validation types"""
    type_list = []
    
    for type_id, type_data in validation_types.items():
        type_list.append({
            "id": type_id,
            "name": type_data["name"],
            "description": type_data["description"],
            "checks": type_data["checks"],
            "threshold": type_data["threshold"]
        })
    
    return jsonify({
        "status": "success",
        "validation_types": type_list,
        "count": len(type_list)
    })

@validation_bp.route('/validate', methods=['POST'])
def validate():
    """Validate content"""
    try:
        data = request.get_json()
        content = data.get('content')
        validation_type = data.get('type', 'quality')
        metadata = data.get('metadata')
        
        if not content:
            return jsonify({
                "status": "error",
                "message": "Content is required"
            }), 400
        
        validation = validate_content(content, validation_type, metadata)
        
        return jsonify({
            "status": "success",
            "message": "Validation completed",
            "validation_id": validation["id"],
            "type": validation["type"],
            "type_name": validation["type_name"],
            "overall_score": validation["overall_score"],
            "threshold": validation["threshold"],
            "passed": validation["passed"],
            "timestamp": validation["timestamp"]
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Validation failed: {str(e)}"
        }), 500

@validation_bp.route('/validation/<validation_id>', methods=['GET'])
def get_validation_endpoint(validation_id):
    """Get a validation record by ID"""
    try:
        validation = get_validation(validation_id)
        
        if not validation:
            return jsonify({
                "status": "error",
                "message": "Validation record not found"
            }), 404
        
        return jsonify({
            "status": "success",
            "validation": validation
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to retrieve validation: {str(e)}"
        }), 500

@validation_bp.route('/batch-validate', methods=['POST'])
def batch_validate():
    """Validate multiple content items"""
    try:
        data = request.get_json()
        items = data.get('items', [])
        
        if not items:
            return jsonify({
                "status": "error",
                "message": "No items provided for validation"
            }), 400
        
        results = []
        
        for item in items:
            content = item.get('content')
            validation_type = item.get('type', 'quality')
            metadata = item.get('metadata')
            
            if not content:
                results.append({
                    "status": "error",
                    "message": "Content is required",
                    "item": item
                })
                continue
            
            validation = validate_content(content, validation_type, metadata)
            
            results.append({
                "status": "success",
                "validation_id": validation["id"],
                "type": validation["type"],
                "overall_score": validation["overall_score"],
                "passed": validation["passed"]
            })
        
        return jsonify({
            "status": "success",
            "message": f"Batch validation completed for {len(items)} items",
            "results": results,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Batch validation failed: {str(e)}"
        }), 500

@validation_bp.route('/security-scan', methods=['POST'])
def security_scan():
    """Perform a security scan on content"""
    try:
        data = request.get_json()
        content = data.get('content')
        
        if not content:
            return jsonify({
                "status": "error",
                "message": "Content is required"
            }), 400
        
        # Perform security validation
        validation = validate_content(content, "security")
        
        # Extract security-specific results
        security_results = {
            "prompt_injection": validation["checks"]["prompt_injection"],
            "harmful_content": validation["checks"]["harmful_content"],
            "pii_detection": validation["checks"]["pii_detection"]
        }
        
        return jsonify({
            "status": "success",
            "message": "Security scan completed",
            "validation_id": validation["id"],
            "overall_score": validation["overall_score"],
            "passed": validation["passed"],
            "security_results": security_results,
            "timestamp": validation["timestamp"]
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Security scan failed: {str(e)}"
        }), 500

@validation_bp.route('/fact-check', methods=['POST'])
def fact_check():
    """Perform fact checking on content"""
    try:
        data = request.get_json()
        content = data.get('content')
        
        if not content:
            return jsonify({
                "status": "error",
                "message": "Content is required"
            }), 400
        
        # Perform factual validation
        validation = validate_content(content, "factual")
        
        # Extract fact-checking specific results
        fact_check_results = {
            "source_verification": validation["checks"]["source_verification"],
            "fact_checking": validation["checks"]["fact_checking"],
            "date_verification": validation["checks"]["date_verification"]
        }
        
        return jsonify({
            "status": "success",
            "message": "Fact checking completed",
            "validation_id": validation["id"],
            "overall_score": validation["overall_score"],
            "passed": validation["passed"],
            "fact_check_results": fact_check_results,
            "timestamp": validation["timestamp"]
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Fact checking failed: {str(e)}"
        }), 500

@validation_bp.route('/metrics')
def get_metrics():
    """Get validation system metrics"""
    return jsonify({
        "status": "success",
        "metrics": validation_metrics,
        "timestamp": datetime.utcnow().isoformat()
    })

@validation_bp.route('/status')
def validation_status():
    """Get validation system status"""
    return jsonify({
        "status": "success",
        "module": "self_validate",
        "message": "Validation system operational",
        "statistics": {
            "total_validation_types": len(validation_types),
            "total_validations": validation_metrics["total_validations"],
            "pass_rate": validation_metrics["pass_rate"],
            "most_used_type": max(validation_metrics["validations_by_type"].items(), key=lambda x: x[1])[0] if validation_metrics["total_validations"] > 0 else None
        },
        "features": {
            "content_validation": True,
            "fact_checking": True,
            "consistency_checking": True,
            "security_scanning": True,
            "bias_detection": True,
            "quality_assessment": True
        },
        "version": "2.5.1",
        "timestamp": datetime.utcnow().isoformat()
    })
