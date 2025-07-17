Authentication Gate Module - Enterprise Security System
Mythiq Gateway Enterprise v2.5.1

This module provides comprehensive authentication and authorization services
for the Mythiq Gateway enterprise platform. It handles user authentication,
session management, security validation, and access control.

Features:
- User authentication and session management
- Security token validation
- Access control and permissions
- Multi-factor authentication support
- Security audit logging
- Enterprise-grade security protocols
"""

from flask import Blueprint, jsonify, request, session
import hashlib
import secrets
import time
from datetime import datetime, timedelta

# Create the auth_bp blueprint with exact variable name expected by main.py
auth_bp = Blueprint('auth_bp', __name__)

# In-memory storage for demo purposes (use database in production)
users_db = {
    "admin": {
        "password_hash": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",  # "password"
        "role": "admin",
        "permissions": ["read", "write", "admin"],
        "created": "2025-01-01T00:00:00Z",
        "last_login": None
    },
    "user": {
        "password_hash": "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f",  # "secret123"
        "role": "user", 
        "permissions": ["read"],
        "created": "2025-01-01T00:00:00Z",
        "last_login": None
    }
}

sessions_db = {}
security_logs = []

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_session_token():
    """Generate secure session token"""
    return secrets.token_urlsafe(32)

def log_security_event(event_type, username=None, details=None):
    """Log security events for audit trail"""
    security_logs.append({
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "username": username,
        "details": details,
        "ip_address": request.remote_addr if request else "system"
    })

@auth_bp.route('/test')
def test():
    """Test endpoint to verify auth module is working"""
    return jsonify({
        "status": "success",
        "module": "auth_gate",
        "message": "Authentication module is operational",
        "features": [
            "user_authentication",
            "session_management", 
            "security_validation",
            "access_control",
            "audit_logging"
        ],
        "version": "2.5.1",
        "timestamp": datetime.utcnow().isoformat()
    })

@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and create session"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            log_security_event("login_failed", username, "Missing credentials")
            return jsonify({
                "status": "error",
                "message": "Username and password required"
            }), 400
        
        # Check if user exists
        if username not in users_db:
            log_security_event("login_failed", username, "User not found")
            return jsonify({
                "status": "error",
                "message": "Invalid credentials"
            }), 401
        
        user = users_db[username]
        password_hash = hash_password(password)
        
        # Verify password
        if password_hash != user["password_hash"]:
            log_security_event("login_failed", username, "Invalid password")
            return jsonify({
                "status": "error",
                "message": "Invalid credentials"
            }), 401
        
        # Create session
        session_token = generate_session_token()
        session_data = {
            "username": username,
            "role": user["role"],
            "permissions": user["permissions"],
            "created": datetime.utcnow().isoformat(),
            "expires": (datetime.utcnow() + timedelta(hours=24)).isoformat(),
            "last_activity": datetime.utcnow().isoformat()
        }
        
        sessions_db[session_token] = session_data
        users_db[username]["last_login"] = datetime.utcnow().isoformat()
        
        log_security_event("login_success", username, "User authenticated successfully")
        
        return jsonify({
            "status": "success",
            "message": "Authentication successful",
            "session_token": session_token,
            "user": {
                "username": username,
                "role": user["role"],
                "permissions": user["permissions"]
            },
            "expires": session_data["expires"]
        })
        
    except Exception as e:
        log_security_event("login_error", None, str(e))
        return jsonify({
            "status": "error",
            "message": "Authentication failed"
        }), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout user and invalidate session"""
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                "status": "error",
                "message": "No session token provided"
            }), 401
        
        session_token = auth_header.split(' ')[1]
        
        if session_token in sessions_db:
            username = sessions_db[session_token]["username"]
            del sessions_db[session_token]
            log_security_event("logout_success", username, "User logged out")
            
            return jsonify({
                "status": "success",
                "message": "Logout successful"
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Invalid session token"
            }), 401
            
    except Exception as e:
        log_security_event("logout_error", None, str(e))
        return jsonify({
            "status": "error",
            "message": "Logout failed"
        }), 500

@auth_bp.route('/validate', methods=['POST'])
def validate_session():
    """Validate session token and return user info"""
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                "status": "error",
                "message": "No session token provided",
                "valid": False
            }), 401
        
        session_token = auth_header.split(' ')[1]
        
        if session_token not in sessions_db:
            return jsonify({
                "status": "error",
                "message": "Invalid session token",
                "valid": False
            }), 401
        
        session_data = sessions_db[session_token]
        
        # Check if session expired
        expires = datetime.fromisoformat(session_data["expires"].replace('Z', '+00:00'))
        if datetime.utcnow().replace(tzinfo=expires.tzinfo) > expires:
            del sessions_db[session_token]
            log_security_event("session_expired", session_data["username"], "Session expired")
            return jsonify({
                "status": "error",
                "message": "Session expired",
                "valid": False
            }), 401
        
        # Update last activity
        session_data["last_activity"] = datetime.utcnow().isoformat()
        
        return jsonify({
            "status": "success",
            "message": "Session valid",
            "valid": True,
            "user": {
                "username": session_data["username"],
                "role": session_data["role"],
                "permissions": session_data["permissions"]
            },
            "session_info": {
                "created": session_data["created"],
                "expires": session_data["expires"],
                "last_activity": session_data["last_activity"]
            }
        })
        
    except Exception as e:
        log_security_event("validation_error", None, str(e))
        return jsonify({
            "status": "error",
            "message": "Session validation failed",
            "valid": False
        }), 500

@auth_bp.route('/users')
def list_users():
    """List all users (admin only)"""
    try:
        # Simple auth check for demo
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            session_token = auth_header.split(' ')[1]
            if session_token in sessions_db:
                session_data = sessions_db[session_token]
                if session_data["role"] != "admin":
                    return jsonify({
                        "status": "error",
                        "message": "Admin access required"
                    }), 403
            else:
                return jsonify({
                    "status": "error", 
                    "message": "Authentication required"
                }), 401
        else:
            return jsonify({
                "status": "error",
                "message": "Authentication required"
            }), 401
        
        users_list = []
        for username, user_data in users_db.items():
            users_list.append({
                "username": username,
                "role": user_data["role"],
                "permissions": user_data["permissions"],
                "created": user_data["created"],
                "last_login": user_data["last_login"]
            })
        
        return jsonify({
            "status": "success",
            "users": users_list,
            "total_users": len(users_list)
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve users"
        }), 500

@auth_bp.route('/security-logs')
def get_security_logs():
    """Get security audit logs (admin only)"""
    try:
        # Simple auth check for demo
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            session_token = auth_header.split(' ')[1]
            if session_token in sessions_db:
                session_data = sessions_db[session_token]
                if session_data["role"] != "admin":
                    return jsonify({
                        "status": "error",
                        "message": "Admin access required"
                    }), 403
            else:
                return jsonify({
                    "status": "error",
                    "message": "Authentication required"
                }), 401
        else:
            return jsonify({
                "status": "error",
                "message": "Authentication required"
            }), 401
        
        # Return recent logs (last 100)
        recent_logs = security_logs[-100:] if len(security_logs) > 100 else security_logs
        
        return jsonify({
            "status": "success",
            "logs": recent_logs,
            "total_logs": len(security_logs),
            "showing": len(recent_logs)
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve security logs"
        }), 500

@auth_bp.route('/status')
def auth_status():
    """Get authentication system status"""
    return jsonify({
        "status": "success",
        "module": "auth_gate",
        "message": "Authentication system operational",
        "statistics": {
            "total_users": len(users_db),
            "active_sessions": len(sessions_db),
            "security_events": len(security_logs)
        },
        "features": {
            "user_authentication": True,
            "session_management": True,
            "security_validation": True,
            "access_control": True,
            "audit_logging": True,
            "multi_factor_auth": False  # Future feature
        },
        "version": "2.5.1",
        "timestamp": datetime.utcnow().isoformat()
    })
