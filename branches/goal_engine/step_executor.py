def execute_goal(steps):
    from branches.intent_router.classifier import classify_intent
    return [classify_intent(step) for step in steps]
