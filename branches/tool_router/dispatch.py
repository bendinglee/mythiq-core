from branches.math_solver.solve import solve_math
from branches.code_analyzer.analyze import analyze_code
from branches.search_bridge.lookup import search_web

def route_tool(prompt):
    if any(x in prompt.lower() for x in ["solve", "equation", "integrate", "derivative"]):
        return solve_math(prompt)
    elif any(x in prompt.lower() for x in ["code", "bug", "python", "function"]):
        return analyze_code(prompt)
    elif any(x in prompt.lower() for x in ["search", "find", "lookup", "latest"]):
        return search_web(prompt)
    else:
        return f"[Fallback] No specialized tool matched → '{prompt}'"
