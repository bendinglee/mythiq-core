from flask import Blueprint, jsonify

mesh_bp_mapper = Blueprint("mesh_bp_mapper", __name__)

@mesh_bp_mapper.route("/scan", methods=["GET"])
def mesh_scan():
    return jsonify({
        "mesh": "scan complete",
        "status": "mapper online"
    })
