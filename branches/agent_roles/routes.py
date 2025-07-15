from flask import Blueprint, request, jsonify
from .agent_core import simulate
agent_bp = Blueprint("agent_bp", __name__)

@agent_bp.route("/simulate", methods=["POST"])
def simulate_role():
    data = request.json
    return jsonify(simulate(data))
