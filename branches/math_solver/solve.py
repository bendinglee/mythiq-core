from sympy import sympify, solve

def solve_math(prompt):
    try:
        expr = sympify(prompt.split("solve")[-1])
        result = solve(expr)
        return f"🧮 Solution: {result}"
    except Exception as e:
        return f"[Math error] {str(e)}"
