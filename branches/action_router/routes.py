from flask import Blueprint, request, jsonify
from .trigger_map import resolve_trigger
from .safe_executor import execute_safe

action_bp = Blueprint("action_bp", __name__)

@action_bp.route("/resolve", methods=["POST"])
def resolve_action():
    user_input = request.json.get("input", "")
    trigger = resolve_trigger(user_input)
    result = execute_safe(trigger)
    return jsonify({ "trigger": trigger, "execution": result })
