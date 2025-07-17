"""
Reasoning Module - Cognitive Architecture Component
Mythiq Gateway Enterprise v2.5.1

This module provides advanced reasoning capabilities for the Mythiq Gateway
cognitive architecture. It handles logical analysis, problem solving,
decision making, and structured reasoning for AI interactions.

Features:
- Logical analysis and inference
- Problem solving frameworks
- Decision making algorithms
- Structured reasoning
- Chain-of-thought processing
- Verification and validation
"""

from flask import Blueprint, jsonify, request
import time
from datetime import datetime
import json
import random
import hashlib

# Create the reasoning_bp blueprint with exact variable name expected by main.py
reasoning_bp = Blueprint('reasoning_bp', __name__)

# Reasoning frameworks
frameworks = {
    "logical": {
        "name": "Logical Analysis",
        "description": "Structured logical analysis using deductive and inductive reasoning",
        "steps": ["premise", "analysis", "conclusion"],
        "suitable_for": ["factual_verification", "logical_problems", "consistency_checking"]
    },
    "problem_solving": {
        "name": "Problem Solving",
        "description": "Systematic approach to solving complex problems",
        "steps": ["problem_definition", "analysis", "solution_generation", "evaluation", "implementation"],
        "suitable_for": ["technical_problems", "optimization", "troubleshooting"]
    },
    "decision_making": {
        "name": "Decision Making",
        "description": "Structured approach to making decisions with multiple factors",
        "steps": ["options_identification", "criteria_definition", "evaluation", "selection", "justification"],
        "suitable_for": ["choices", "prioritization", "risk_assessment"]
    },
    "chain_of_thought": {
        "name": "Chain of Thought",
        "description": "Step-by-step reasoning process to solve complex problems",
        "steps": ["initial_thoughts", "step_by_step_reasoning", "intermediate_conclusions", "final_conclusion"],
        "suitable_for": ["math_problems", "complex_reasoning", "multi-step_problems"]
    },
    "socratic": {
        "name": "Socratic Method",
        "description": "Question-based approach to explore ideas and uncover assumptions",
        "steps": ["initial_question", "exploration", "clarification", "examination", "conclusion"],
        "suitable_for": ["philosophical_questions", "belief_examination", "critical_thinking"]
    }
}

# Reasoning history
reasoning_history = {}

# Reasoning metrics
reasoning_metrics = {
    "total_reasoning_sessions": 0,
    "reasoning_by_framework": {
        "logical": 0,
        "problem_solving": 0,
        "decision_making": 0,
        "chain_of_thought": 0,
        "socratic": 0
    },
    "average_steps": 0,
    "success_rate": 0,
    "total_successful": 0,
    "total_failed": 0
}

def generate_id():
    """Generate a unique ID"""
    return hashlib.md5(str(time.time() + random.random()).encode()).hexdigest()[:12]

def select_framework(reasoning_type):
    """Select the most appropriate reasoning framework"""
    if reasoning_type in frameworks:
        return reasoning_type
    
    # Default to logical framework
    return "logical"

def create_reasoning_session(reasoning_type, input_data, metadata=None):
    """Create a new reasoning session"""
    session_id = generate_id()
    framework = select_framework(reasoning_type)
    
    session = {
        "id": session_id,
        "framework": framework,
        "framework_name": frameworks[framework]["name"],
        "steps": frameworks[framework]["steps"].copy(),
        "current_step": 0,
        "input": input_data,
        "output": {},
        "status": "in_progress",
        "created": datetime.utcnow().isoformat(),
        "updated": datetime.utcnow().isoformat(),
        "completed": None,
        "metadata": metadata or {}
    }
    
    reasoning_history[session_id] = session
    reasoning_metrics["total_reasoning_sessions"] += 1
    reasoning_metrics["reasoning_by_framework"][framework] += 1
    
    return session

def update_reasoning_step(session_id, step_output, advance=True):
    """Update a reasoning step and optionally advance to next step"""
    if session_id not in reasoning_history:
        return None
    
    session = reasoning_history[session_id]
    
    if session["status"] == "completed":
        return session
    
    current_step = session["current_step"]
    step_name = session["steps"][current_step]
    
    # Update output for current step
    session["output"][step_name] = step_output
    session["updated"] = datetime.utcnow().isoformat()
    
    # Advance to next step if requested
    if advance:
        if current_step < len(session["steps"]) - 1:
            session["current_step"] += 1
        else:
            # Final step completed
            session["status"] = "completed"
            session["completed"] = datetime.utcnow().isoformat()
            
            # Update metrics
            reasoning_metrics["total_successful"] += 1
            reasoning_metrics["success_rate"] = (reasoning_metrics["total_successful"] / 
                                               (reasoning_metrics["total_successful"] + reasoning_metrics["total_failed"])) * 100
    
    return session

def get_reasoning_session(session_id):
    """Get a reasoning session by ID"""
    if session_id not in reasoning_history:
        return None
    
    return reasoning_history[session_id]

def fail_reasoning_session(session_id, reason):
    """Mark a reasoning session as failed"""
    if session_id not in reasoning_history:
        return None
    
    session = reasoning_history[session_id]
    
    session["status"] = "failed"
    session["failure_reason"] = reason
    session["updated"] = datetime.utcnow().isoformat()
    
    # Update metrics
    reasoning_metrics["total_failed"] += 1
    reasoning_metrics["success_rate"] = (reasoning_metrics["total_successful"] / 
                                       (reasoning_metrics["total_successful"] + reasoning_metrics["total_failed"])) * 100
    
    return session

def get_framework_details(framework_id):
    """Get details about a reasoning framework"""
    if framework_id not in frameworks:
        return None
    
    return frameworks[framework_id]

@reasoning_bp.route('/test')
def test():
    """Test endpoint to verify reasoning module is working"""
    return jsonify({
        "status": "success",
        "module": "reasoning",
        "message": "Reasoning module is operational",
        "features": [
            "logical_analysis",
            "problem_solving",
            "decision_making",
            "structured_reasoning",
            "chain_of_thought",
            "verification"
        ],
        "frameworks": list(frameworks.keys()),
        "active_sessions": len(reasoning_history),
        "version": "2.5.1",
        "timestamp": datetime.utcnow().isoformat()
    })

@reasoning_bp.route('/frameworks')
def list_frameworks():
    """List all available reasoning frameworks"""
    framework_list = []
    
    for framework_id, framework_data in frameworks.items():
        framework_list.append({
            "id": framework_id,
            "name": framework_data["name"],
            "description": framework_data["description"],
            "steps": framework_data["steps"],
            "suitable_for": framework_data["suitable_for"]
        })
    
    return jsonify({
        "status": "success",
        "frameworks": framework_list,
        "count": len(framework_list)
    })

@reasoning_bp.route('/framework/<framework_id>')
def get_framework(framework_id):
    """Get details about a specific reasoning framework"""
    framework = get_framework_details(framework_id)
    
    if not framework:
        return jsonify({
            "status": "error",
            "message": "Framework not found"
        }), 404
    
    return jsonify({
        "status": "success",
        "framework": {
            "id": framework_id,
            "name": framework["name"],
            "description": framework["description"],
            "steps": framework["steps"],
            "suitable_for": framework["suitable_for"]
        }
    })

@reasoning_bp.route('/session', methods=['POST'])
def create_session():
    """Create a new reasoning session"""
    try:
        data = request.get_json()
        reasoning_type = data.get('type', 'logical')
        input_data = data.get('input')
        metadata = data.get('metadata')
        
        if not input_data:
            return jsonify({
                "status": "error",
                "message": "Input data is required"
            }), 400
        
        session = create_reasoning_session(reasoning_type, input_data, metadata)
        
        return jsonify({
            "status": "success",
            "message": "Reasoning session created",
            "session_id": session["id"],
            "framework": session["framework"],
            "framework_name": session["framework_name"],
            "steps": session["steps"],
            "current_step": session["steps"][session["current_step"]],
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to create reasoning session: {str(e)}"
        }), 500

@reasoning_bp.route('/session/<session_id>', methods=['GET'])
def get_session(session_id):
    """Get a reasoning session by ID"""
    try:
        session = get_reasoning_session(session_id)
        
        if not session:
            return jsonify({
                "status": "error",
                "message": "Reasoning session not found"
            }), 404
        
        return jsonify({
            "status": "success",
            "session": session
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to retrieve reasoning session: {str(e)}"
        }), 500

@reasoning_bp.route('/session/<session_id>/step', methods=['POST'])
def update_step(session_id):
    """Update the current reasoning step"""
    try:
        data = request.get_json()
        step_output = data.get('output')
        advance = data.get('advance', True)
        
        if not step_output:
            return jsonify({
                "status": "error",
                "message": "Step output is required"
            }), 400
        
        session = update_reasoning_step(session_id, step_output, advance)
        
        if not session:
            return jsonify({
                "status": "error",
                "message": "Reasoning session not found"
            }), 404
        
        response = {
            "status": "success",
            "message": "Reasoning step updated",
            "session_id": session["id"],
            "session_status": session["status"]
        }
        
        if session["status"] == "in_progress":
            current_step = session["current_step"]
            response["current_step"] = session["steps"][current_step]
            response["step_number"] = current_step + 1
            response["total_steps"] = len(session["steps"])
        elif session["status"] == "completed":
            response["message"] = "Reasoning completed"
            response["completed_at"] = session["completed"]
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to update reasoning step: {str(e)}"
        }), 500

@reasoning_bp.route('/session/<session_id>/fail', methods=['POST'])
def fail_session(session_id):
    """Mark a reasoning session as failed"""
    try:
        data = request.get_json()
        reason = data.get('reason', 'Unknown failure reason')
        
        session = fail_reasoning_session(session_id, reason)
        
        if not session:
            return jsonify({
                "status": "error",
                "message": "Reasoning session not found"
            }), 404
        
        return jsonify({
            "status": "success",
            "message": "Reasoning session marked as failed",
            "session_id": session["id"],
            "failure_reason": reason,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to update reasoning session: {str(e)}"
        }), 500

@reasoning_bp.route('/analyze', methods=['POST'])
def analyze():
    """Perform a complete reasoning analysis in one request"""
    try:
        data = request.get_json()
        reasoning_type = data.get('type', 'logical')
        input_data = data.get('input')
        analysis = data.get('analysis')
        
        if not input_data or not analysis:
            return jsonify({
                "status": "error",
                "message": "Input data and analysis are required"
            }), 400
        
        # Create session
        session = create_reasoning_session(reasoning_type, input_data)
        session_id = session["id"]
        
        # Process each step
        framework = frameworks[session["framework"]]
        steps = framework["steps"]
        
        # Check if analysis has all required steps
        for step in steps:
            if step not in analysis:
                return jsonify({
                    "status": "error",
                    "message": f"Missing analysis for step: {step}"
                }), 400
        
        # Update each step
        for i, step in enumerate(steps):
            is_last_step = i == len(steps) - 1
            update_reasoning_step(session_id, analysis[step], advance=True)
        
        # Get completed session
        completed_session = get_reasoning_session(session_id)
        
        return jsonify({
            "status": "success",
            "message": "Reasoning analysis completed",
            "session_id": session_id,
            "framework": session["framework"],
            "framework_name": framework["name"],
            "input": input_data,
            "output": completed_session["output"],
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Reasoning analysis failed: {str(e)}"
        }), 500

@reasoning_bp.route('/metrics')
def get_metrics():
    """Get reasoning system metrics"""
    return jsonify({
        "status": "success",
        "metrics": reasoning_metrics,
        "timestamp": datetime.utcnow().isoformat()
    })

@reasoning_bp.route('/status')
def reasoning_status():
    """Get reasoning system status"""
    return jsonify({
        "status": "success",
        "module": "reasoning",
        "message": "Reasoning system operational",
        "statistics": {
            "total_frameworks": len(frameworks),
            "total_sessions": reasoning_metrics["total_reasoning_sessions"],
            "active_sessions": len(reasoning_history),
            "success_rate": reasoning_metrics["success_rate"],
            "most_used_framework": max(reasoning_metrics["reasoning_by_framework"].items(), key=lambda x: x[1])[0]
        },
        "features": {
            "logical_analysis": True,
            "problem_solving": True,
            "decision_making": True,
            "structured_reasoning": True,
            "chain_of_thought": True,
            "verification": True
        },
        "version": "2.5.1",
        "timestamp": datetime.utcnow().isoformat()
    })
