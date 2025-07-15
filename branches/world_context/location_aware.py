def detect_region(text):
    if "color" in text.lower():
        return "US/CA"
    elif "colour" in text.lower():
        return "UK"
    return "Global"

def localize_response(text, region):
    if region == "UK":
        return text.replace("customize", "customise")
    return text
