"""
Mythiq Blueprint Validator - Development Mode
"""

from mythiq_blueprint_validator import validate_blueprints

if __name__ == "__main__":
    print("🔍 Mythiq Blueprint Validator v2.5.1\n")
    results = validate_blueprints()
    success = sum(1 for r in results if r["status"] == "✅ Injected")
    failed = len(results) - success

    for r in results:
        print(f"{r['status']} {r['module_path']} → {r['url_prefix']}")
        if r['status'] == "❌ Failed":
            print(f"   ⛔ Error: {r['error']}")
            print(f"   📁 File Exists: {r['file_exists']}")
            print()

    print("\n📊 Summary:")
    print(f"   ✅ Successful Blueprints: {success}")
    print(f"   ❌ Failed Blueprints: {failed}")
    print(f"   📋 Total Checked: {len(results)}")
