from flask import Blueprint, Response, stream_with_context
import time

stream_bp = Blueprint("stream_bp", __name__)

@stream_bp.route("/stream", methods=["GET"])
def chat_stream():
    def generate():
        messages = [
            "Initializing conversation...",
            "Reflecting on memory anchors...",
            "Persona adapting in real time...",
            "Ready for dialogue."
        ]
        for msg in messages:
            yield f"data: {msg}\n\n"
            time.sleep(1)
    return Response(stream_with_context(generate()), content_type='text/event-stream')
