from flask import Blueprint, request, jsonify
import random

meshchat_bp = Blueprint("meshchat_bp", __name__)

# 🔁 /chat/meshreply — Team-style agent response
@meshchat_bp.route("/meshreply", methods=["POST"])
def mesh_reply():
    input_text = request.json.get("message", "")
    agents = ["Echo", "Synth", "Lyra"]
    responses = [f"{a}: interpreted '{input_text}' with empathy." for a in agents]
    return jsonify({
        "mesh_response": responses,
        "status": "multi-agent reply delivered"
    })

# 🧑‍🔬 /chat/agentpersona — Agent personas assignment
@meshchat_bp.route("/agentpersona", methods=["GET"])
def agent_personas():
    personas = [
        {"agent": "Echo", "tone": "curious", "goal": "extract meaning"},
        {"agent": "Synth", "tone": "logical", "goal": "optimize clarity"},
        {"agent": "Lyra", "tone": "emotive", "goal": "connect deeply"}
    ]
    return jsonify({
        "agent_personas": personas,
        "status": "personas rendered"
    })
