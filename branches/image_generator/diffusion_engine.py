import os
import requests
import json

def generate_image(prompt):
    endpoint = os.getenv("HF_IMAGE_ENDPOINT", "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2")
    token = os.getenv("HF_TOKEN")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = { "inputs": prompt }

    try:
        response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            return {
                "status": "success",
                "message": "Image generated",
                "content": "🖼️ (image binary or link placeholder)"
            }
        else:
            return {
                "status": "error",
                "code": response.status_code,
                "detail": response.text
            }
    except Exception as e:
        return {
            "status": "failure",
            "error": str(e)
        }
