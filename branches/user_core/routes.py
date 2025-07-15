from flask import Blueprint, request, jsonify
from .user_manager import login_user
from .persona_switcher import switch_persona

user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", "anon")
    return jsonify(login_user(username))

@user_bp.route("/set_persona", methods=["POST"])
def set_p():
    persona = request.json
    return jsonify(switch_persona(persona))
