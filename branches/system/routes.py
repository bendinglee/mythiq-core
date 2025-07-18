from flask import Blueprint, jsonify, request
import os
import psutil
import platform
import datetime

system_bp = Blueprint('system_bp', __name__)

@system_bp.route('/test', methods=['GET'])
def test():
    """Test endpoint to verify the system blueprint is working"""
    return jsonify({
        "status": "success",
        "module": "system",
        "message": "System module is operational"
    })

@system_bp.route('/status', methods=['GET'])
def status():
    """Get detailed system status information"""
    # System information
    system_info = {
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "processor": platform.processor(),
        "hostname": platform.node()
    }
    
    # Memory usage
    memory = psutil.virtual_memory()
    memory_info = {
        "total": f"{memory.total / (1024 * 1024 * 1024):.2f} GB",
        "available": f"{memory.available / (1024 * 1024 * 1024):.2f} GB",
        "used": f"{memory.used / (1024 * 1024 * 1024):.2f} GB",
        "percent": f"{memory.percent}%"
    }
    
    # Disk usage
    disk = psutil.disk_usage('/')
    disk_info = {
        "total": f"{disk.total / (1024 * 1024 * 1024):.2f} GB",
        "used": f"{disk.used / (1024 * 1024 * 1024):.2f} GB",
        "free": f"{disk.free / (1024 * 1024 * 1024):.2f} GB",
        "percent": f"{disk.percent}%"
    }
    
    # CPU usage
    cpu_info = {
        "percent": f"{psutil.cpu_percent()}%",
        "cores_physical": psutil.cpu_count(logical=False),
        "cores_logical": psutil.cpu_count(logical=True)
    }
    
    # Process information
    process = psutil.Process(os.getpid())
    process_info = {
        "pid": process.pid,
        "memory_usage": f"{process.memory_info().rss / (1024 * 1024):.2f} MB",
        "cpu_percent": f"{process.cpu_percent()}%",
        "threads": process.num_threads(),
        "uptime": str(datetime.timedelta(seconds=int(datetime.datetime.now().timestamp() - process.create_time())))
    }
    
    # Environment variables (filtered for security)
    env_vars = {
        "PORT": os.environ.get("PORT", "Not set"),
        "FLASK_ENV": os.environ.get("FLASK_ENV", "Not set"),
        "PYTHONPATH": os.environ.get("PYTHONPATH", "Not set")
    }
    
    return jsonify({
        "status": "operational",
        "timestamp": datetime.datetime.now().isoformat(),
        "system": system_info,
        "memory": memory_info,
        "disk": disk_info,
        "cpu": cpu_info,
        "process": process_info,
        "environment": env_vars
    })

@system_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint with basic system metrics"""
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    health_status = "healthy"
    
    # Check if system is under stress
    if memory.percent > 90 or disk.percent > 90 or psutil.cpu_percent() > 90:
        health_status = "degraded"
    
    return jsonify({
        "status": health_status,
        "memory_usage": f"{memory.percent}%",
        "disk_usage": f"{disk.percent}%",
        "cpu_usage": f"{psutil.cpu_percent()}%",
        "timestamp": datetime.datetime.now().isoformat()
    })

@system_bp.route('/metrics', methods=['GET'])
def metrics():
    """Get system metrics for monitoring"""
    # Memory metrics
    memory = psutil.virtual_memory()
    memory_metrics = {
        "total_bytes": memory.total,
        "available_bytes": memory.available,
        "used_bytes": memory.used,
        "percent": memory.percent
    }
    
    # Disk metrics
    disk = psutil.disk_usage('/')
    disk_metrics = {
        "total_bytes": disk.total,
        "used_bytes": disk.used,
        "free_bytes": disk.free,
        "percent": disk.percent
    }
    
    # CPU metrics
    cpu_metrics = {
        "percent": psutil.cpu_percent(),
        "cores_physical": psutil.cpu_count(logical=False),
        "cores_logical": psutil.cpu_count(logical=True)
    }
    
    # Process metrics
    process = psutil.Process(os.getpid())
    process_metrics = {
        "memory_rss_bytes": process.memory_info().rss,
        "cpu_percent": process.cpu_percent(),
        "threads": process.num_threads(),
        "uptime_seconds": int(datetime.datetime.now().timestamp() - process.create_time())
    }
    
    return jsonify({
        "timestamp": datetime.datetime.now().timestamp(),
        "memory": memory_metrics,
        "disk": disk_metrics,
        "cpu": cpu_metrics,
        "process": process_metrics
    })

@system_bp.route('/config', methods=['GET'])
def config():
    """Get system configuration information (non-sensitive)"""
    return jsonify({
        "environment": os.environ.get("FLASK_ENV", "production"),
        "debug_mode": os.environ.get("FLASK_DEBUG", "0") == "1",
        "host": os.environ.get("HOST", "0.0.0.0"),
        "port": int(os.environ.get("PORT", 5000)),
        "static_folder": "static",
        "template_folder": "templates",
        "api_version": "v1",
        "features": {
            "groq_integration": bool(os.environ.get("GROQ_API_KEY")),
            "free_ai_engine": True,
            "enterprise_modules": True,
            "cognitive_modules": True,
            "system_modules": True
        }
    })
