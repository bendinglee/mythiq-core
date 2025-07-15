def map_style_to_modifiers(style, emotion):
    style_map = {
        "formal": "eloquent, structured response",
        "casual": "friendly, relaxed tone",
        "dark": "mysterious, philosophical",
        "playful": "witty, energetic language"
    }
    emotion_map = {
        "calm": "soothing rhythm",
        "angry": "assertive delivery",
        "joyful": "enthusiastic word choice"
    }
    return f"{style_map.get(style, '')}, {emotion_map.get(emotion, '')}"
