from flask import Blueprint, request, jsonify
from branches.tool_router.dispatch import route_tool
from branches.validation_core.verify import validate_output

reasoning_bp = Blueprint("reasoning_bp", __name__)

@reasoning_bp.route("/reason", methods=["POST"])
def reason():
    prompt = request.json.get("prompt", "").strip()
    if not prompt:
        return jsonify({ "error": "Missing prompt", "status": "failed" }), 400

    # Step 1: Chain-of-thought breakdown
    steps = [f"Step 1: Understand → {prompt}", "Step 2: Select tool", "Step 3: Generate response"]

    # Step 2: Route to appropriate tool
    response = route_tool(prompt)

    # Step 3: Validate output
    verified = validate_output(prompt, response)

    return jsonify({
        "input": prompt,
        "response": response,
        "reasoning_trace": steps,
        "validated": verified,
        "status": "success"
    })
