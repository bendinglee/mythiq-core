from flask import Blueprint, jsonify
from .strategy_map import get_layout

train_bp = Blueprint("train_bp", __name__)

@train_bp.route("/guide", methods=["GET"])
def guide():
    return jsonify(get_layout())
