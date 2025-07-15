def generate_summary(session_data):
    if not session_data:
        return {"insight": "No data to reflect on."}

    routes = set(entry["route"] for entry in session_data)
    total = len(session_data)
    recent = session_data[-1]

    return {
        "insight": f"{total} entries analyzed across {len(routes)} routes.",
        "recent_action": recent["route"],
        "confidence": "stable"
    }
