def validate_output(prompt, response):
    if "error" in response.lower() or "undefined" in response.lower():
        return "❌ Validation failed"
    if len(response.strip()) < 10:
        return "⚠️ Possibly incomplete"
    return "✅ Output verified"
