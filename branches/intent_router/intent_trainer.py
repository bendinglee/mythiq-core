_new_intents = {}

def learn_intent(label, examples):
    _new_intents[label] = examples
    return True
