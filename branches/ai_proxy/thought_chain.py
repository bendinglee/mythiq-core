def build_chain_prompt(user_query):
    return f"""Let's reason through this step by step.

Question: {user_query}

Step 1: [First idea]
Step 2: [Next point]
Step 3: [Clarify logic]
Conclusion:"""
