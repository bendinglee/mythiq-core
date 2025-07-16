from flask import Blueprint, request, jsonify
import pytesseract
from PIL import Image
import io

vision_bp = Blueprint("vision_bp", __name__)

@vision_bp.route("/api/vision", methods=["POST"])
def vision_handler():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_bytes = request.files['image'].read()
    image = Image.open(io.BytesIO(image_bytes))
    extracted_text = pytesseract.image_to_string(image)

    return jsonify({
        "extracted_text": extracted_text.strip(),
        "status": "success"
    })
