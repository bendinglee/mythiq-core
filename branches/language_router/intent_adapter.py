def route_intent(lang, text):
    if lang == "Spanish":
        return "api/intent/route_es"
    return "api/intent/route"
