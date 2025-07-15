def edit_dream(dream, user_tweak):
    if "add forest" in user_tweak:
        dream["narrative"] += " The city fades into a mist-shrouded forest filled with whispering echoes."
    return dream
