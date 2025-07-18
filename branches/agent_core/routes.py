from flask import Blueprint, request, jsonify
import time

agent_bp = Blueprint('agent_bp', __name__)

@agent_bp.route('/test')
def test():
    return jsonify({
        "status": "success",
        "module": "agent_core",
        "message": "Agent module is operational",
        "version": "1.0",
        "timestamp": time.time()
    })

@agent_bp.route('/run', methods=['POST'])
def run_agent():
    data = request.get_json()
    task = data.get("task", "No task provided")

    plan = [f"Analyze task: {task}", "Select tools", "Execute steps", "Return result"]

    return jsonify({
        "status": "executed",
        "task": task,
        "plan": plan,
        "result": f"Simulated execution of: {task}",
        "timestamp": time.time()
    })
