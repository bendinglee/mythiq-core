from flask import Blueprint, request, jsonify
from .goal_planner import plan_goal
from .step_executor import execute_goal
from .goal_memory import log_goal, get_goal_log

goal_bp = Blueprint("goal_bp", __name__)

@goal_bp.route("/create", methods=["POST"])
def create_goal():
    goal_text = request.json.get("goal", "")
    steps = plan_goal(goal_text)
    execution = execute_goal(steps)
    log_goal(goal_text, steps, execution)
    return jsonify({ "goal": goal_text, "steps": steps, "result": execution })

@goal_bp.route("/status", methods=["GET"])
def status():
    return jsonify({ "log": get_goal_log() })
