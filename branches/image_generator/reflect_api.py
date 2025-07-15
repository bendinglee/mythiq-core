from flask import Blueprint, jsonify
from .reflect import generate_summary

reflect_bp = Blueprint("reflect_bp", __name__)

@reflect_bp.route("/reflect", methods=["GET"])
def reflect_endpoint():
    return jsonify(generate_summary())
