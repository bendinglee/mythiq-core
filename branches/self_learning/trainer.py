def update_routing(flow_map, feedback_score):
    if feedback_score["confidence_score"] < 50:
        flow_map["fallback"] = "core_dispatcher"
    return flow_map
