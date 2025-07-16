import os
import ast

def scan_branches():
    root = "branches"
    results = []

    for dirpath, _, filenames in os.walk(root):
        for file in filenames:
            if file == "routes.py":
                filepath = os.path.join(dirpath, file)
                branch = dirpath.replace(root + "/", "")
                issues = []

                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        tree = ast.parse(f.read(), filename=filepath)

                    blueprint_found = False
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Assign):
                            if hasattr(node.value, "func") and isinstance(node.value.func, ast.Name):
                                if node.value.func.id == "Blueprint":
                                    blueprint_found = True
                                    break

                    if not blueprint_found:
                        issues.append("❌ Missing Blueprint declaration")

                except Exception as e:
                    issues.append(f"❌ Failed to parse ({e.__class__.__name__}): {str(e)}")

                results.append((branch, issues))

    return results


if __name__ == "__main__":
    print("🔍 Scanning Mythiq module structure...\n")
    scan_report = scan_branches()

    for branch, issues in scan_report:
        if issues:
            print(f"⚠️ {branch}/routes.py:")
            for issue in issues:
                print(f"   - {issue}")
        else:
            print(f"✅ {branch}/routes.py is blueprint-ready.")

    print("\n✅ Scan complete. All modules checked.")
