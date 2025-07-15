def build_storyboard(inputs):
    return {
        "image": inputs.get("image", ""),
        "voice": inputs.get("voice", ""),
        "caption": inputs.get("text", "")
    }
