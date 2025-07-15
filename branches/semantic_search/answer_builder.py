def build_answer(matches):
    return f"The top concept related is: {matches[0]}" if matches else "No match found."
