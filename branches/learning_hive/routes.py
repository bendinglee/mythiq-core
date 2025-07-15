from flask import Blueprint, request, jsonify
from .curriculum_builder import build_curriculum
from .agent_trainer import train_agent
from .feedback_parser import parse_agent_feedback

hive_bp = Blueprint("hive_bp", __name__)

@hive_bp.route("/api/train/assist", methods=["POST"])
def assist_train():
    data = request.json
    topic = data.get("topic", "generic AI")
    steps = build_curriculum(topic)
    return jsonify({ "curriculum": steps })

@hive_bp.route("/api/train/instruct", methods=["POST"])
def instruct_agent():
    data = request.json
    agent_id = data.get("agent_id")
    lesson = data.get("lesson")
    result = train_agent(agent_id, lesson)
    return jsonify(result)

@hive_bp.route("/api/train/feedback", methods=["POST"])
def feedback():
    logs = request.json.get("logs", "")
    suggestion = parse_agent_feedback(logs)
    return jsonify({ "next_action": suggestion })
