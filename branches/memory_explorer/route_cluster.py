def group_routes():
    return {
        "vision": ["api/image/generate", "api/story/gen"],
        "intent": ["api/intent/route", "api/action/resolve"]
    }
