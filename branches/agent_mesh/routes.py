from flask import Blueprint, request, jsonify
from .task_relay import relay_task
from .agent_registry import connect_agent

mesh_bp = Blueprint("mesh_bp", __name__)

@mesh_bp.route("/connect", methods=["POST"])
def connect():
    return jsonify(connect_agent(request.json))

@mesh_bp.route("/task/relay", methods=["POST"])
def relay():
    return jsonify(relay_task(request.json))
