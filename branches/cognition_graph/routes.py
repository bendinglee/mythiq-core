from flask import Blueprint, jsonify
from .node_mapper import map_nodes
from .association_tracer import trace_associations

graph_bp = Blueprint("graph_bp", __name__)

@graph_bp.route("/view", methods=["GET"])
def view():
    return jsonify({ "nodes": map_nodes(), "links": trace_associations() })
