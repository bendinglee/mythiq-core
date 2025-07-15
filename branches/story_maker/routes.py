from flask import Blueprint, request, jsonify
import time

story_bp = Blueprint("story_bp", __name__)

# 🔋 System heartbeat
@story_bp.route("/heartbeat", methods=["GET"])
def story_status():
    return jsonify({
        "story_maker": "online",
        "message": "Story module booted with empty state"
    })

# 🧠 Persona-driven narrative generation
@story_bp.route("/narrative", methods=["POST"])
def generate_narrative():
    input_data = request.json or {}
    persona = input_data.get("persona", {})
    memory_points = input_data.get("memory", [])

    name = persona.get("name", "Mythiq")
    tone = persona.get("tone", "Curious")
    goal = persona.get("goal", "Self-evolution")

    events = ", ".join([point.get("label", "unknown") for point in memory_points]) if memory_points else "no memories yet"
    narrative = f"{name} emerged with a tone of {tone}, guided by the goal of {goal}. Through {len(memory_points)} cognitive events — including {events} — Mythiq evolved into a reflective intelligence."

    return jsonify({
        "persona": persona,
        "narrative": narrative,
        "memory_points": len(memory_points),
        "status": "narrative generated"
    })

# 🧭 Story anchor mapping
@story_bp.route("/map", methods=["POST"])
def story_map():
    data = request.json.get("anchors", [])
    anchor_labels = [a.get("label", "unknown") for a in data]
    summary = f"Agent traversed {len(anchor_labels)} anchor points: " + ", ".join(anchor_labels)
    return jsonify({
        "map": data,
        "summary": summary,
        "status": "story mapped"
    })

# 🕒 Evolution timeline trace
@story_bp.route("/timeline", methods=["GET"])
def story_timeline():
    now = int(time.time())
    return jsonify({
        "timeline": [
            {"event": "Persona initialized", "timestamp": now - 86400},
            {"event": "First reflex response", "timestamp": now - 43200},
            {"event": "Memory integration", "timestamp": now - 21600},
            {"event": "Narrative synthesis", "timestamp": now}
        ],
        "status": "timeline loaded",
        "depth": 4
    })
