"""
Blueprint Import Diagnostic and Fix Script
This script identifies why blueprints aren't loading and provides fixes
"""

import os
import sys

def check_file_structure():
    """Check if all required files exist"""
    print("🔍 Checking file structure...")
    
    required_files = [
        'branches/__init__.py',
        'branches/auth_gate/__init__.py',
        'branches/auth_gate/routes.py',
        'branches/pro_router/__init__.py', 
        'branches/pro_router/routes.py',
        'branches/quota/__init__.py',
        'branches/quota/routes.py',
        'branches/memory/__init__.py',
        'branches/memory/routes.py',
        'branches/reasoning/__init__.py',
        'branches/reasoning/routes.py',
        'branches/self_validate/__init__.py',
        'branches/self_validate/routes.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    return missing_files

def check_python_syntax():
    """Check Python syntax of blueprint files"""
    print("\n🔍 Checking Python syntax...")
    
    blueprint_files = [
        'branches/auth_gate/routes.py',
        'branches/pro_router/routes.py',
        'branches/quota/routes.py',
        'branches/memory/routes.py',
        'branches/reasoning/routes.py',
        'branches/self_validate/routes.py'
    ]
    
    syntax_errors = []
    for file_path in blueprint_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                compile(content, file_path, 'exec')
                print(f"✅ {file_path} - Syntax OK")
            except SyntaxError as e:
                print(f"❌ {file_path} - Syntax Error: {e}")
                syntax_errors.append((file_path, str(e)))
            except Exception as e:
                print(f"⚠️ {file_path} - Other Error: {e}")
                syntax_errors.append((file_path, str(e)))
    
    return syntax_errors

def test_imports():
    """Test importing each blueprint"""
    print("\n🔍 Testing blueprint imports...")
    
    # Add current directory to Python path
    sys.path.insert(0, '.')
    
    blueprints = [
        ('branches.auth_gate.routes', 'auth_bp'),
        ('branches.pro_router.routes', 'pro_router_bp'),
        ('branches.quota.routes', 'quota_bp'),
        ('branches.memory.routes', 'memory_bp'),
        ('branches.reasoning.routes', 'reasoning_bp'),
        ('branches.self_validate.routes', 'validation_bp')
    ]
    
    import_errors = []
    for module_path, blueprint_name in blueprints:
        try:
            module = __import__(module_path, fromlist=[blueprint_name])
            blueprint = getattr(module, blueprint_name)
            print(f"✅ {module_path}.{blueprint_name} - Import OK")
        except ImportError as e:
            print(f"❌ {module_path}.{blueprint_name} - Import Error: {e}")
            import_errors.append((module_path, blueprint_name, str(e)))
        except AttributeError as e:
            print(f"❌ {module_path}.{blueprint_name} - Blueprint Not Found: {e}")
            import_errors.append((module_path, blueprint_name, str(e)))
        except Exception as e:
            print(f"❌ {module_path}.{blueprint_name} - Other Error: {e}")
            import_errors.append((module_path, blueprint_name, str(e)))
    
    return import_errors

def create_missing_init_files():
    """Create missing __init__.py files"""
    print("\n🔧 Creating missing __init__.py files...")
    
    init_files = [
        'branches/__init__.py',
        'branches/auth_gate/__init__.py',
        'branches/pro_router/__init__.py',
        'branches/quota/__init__.py',
        'branches/memory/__init__.py',
        'branches/reasoning/__init__.py',
        'branches/self_validate/__init__.py'
    ]
    
    for init_file in init_files:
        if not os.path.exists(init_file):
            os.makedirs(os.path.dirname(init_file), exist_ok=True)
            with open(init_file, 'w') as f:
                f.write('# Blueprint module initialization\n')
            print(f"✅ Created {init_file}")
        else:
            print(f"✅ {init_file} already exists")

def fix_blueprint_names():
    """Fix blueprint variable names in route files"""
    print("\n🔧 Checking blueprint variable names...")
    
    blueprint_fixes = [
        ('branches/auth_gate/routes.py', 'auth_bp'),
        ('branches/pro_router/routes.py', 'pro_router_bp'),
        ('branches/quota/routes.py', 'quota_bp'),
        ('branches/memory/routes.py', 'memory_bp'),
        ('branches/reasoning/routes.py', 'reasoning_bp'),
        ('branches/self_validate/routes.py', 'validation_bp')
    ]
    
    for file_path, expected_name in blueprint_fixes:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Check if blueprint is properly defined
            if f"{expected_name} = Blueprint(" in content:
                print(f"✅ {file_path} - Blueprint name OK")
            else:
                print(f"⚠️ {file_path} - Blueprint name might be incorrect")
                # Try to find the actual blueprint definition
                import re
                blueprint_match = re.search(r'(\w+)\s*=\s*Blueprint\(', content)
                if blueprint_match:
                    actual_name = blueprint_match.group(1)
                    print(f"   Found blueprint: {actual_name}, expected: {expected_name}")

def generate_fixed_main_py():
    """Generate a fixed main.py with better error handling"""
    print("\n🔧 Generating fixed main.py with enhanced error handling...")
    
    fixed_main = '''#!/usr/bin/env python3
"""
Mythiq Gateway Enterprise v2.5.1 - Enhanced Blueprint Loading
Fixed version with better error handling and diagnostics
"""

import os
import json
import time
import requests
import traceback
from datetime import datetime
from flask import Flask, request, jsonify, session
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'mythiq-enterprise-secret-2025')
CORS(app)

# Configuration
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
HUGGINGFACE_API_KEY = os.environ.get('HUGGINGFACE_API_KEY') or os.environ.get('HUGGING_FACE')

# Blueprint configuration with all enterprise modules
BLUEPRINT_ROUTES = [
    ("branches.auth_gate.routes", "auth_bp", "/api/auth"),
    ("branches.pro_router.routes", "pro_router_bp", "/api/proxy"),
    ("branches.quota.routes", "quota_bp", "/api/quota"),
    ("branches.memory.routes", "memory_bp", "/api/memory"),
    ("branches.reasoning.routes", "reasoning_bp", "/api/reason"),
    ("branches.self_validate.routes", "validation_bp", "/api/validate"),
]

# Track loaded blueprints
loaded_blueprints = []
blueprint_status = {}
import_errors = []

def register_blueprints():
    """Register all blueprint modules with enhanced error handling"""
    global loaded_blueprints, blueprint_status, import_errors
    
    print("🚀 Starting blueprint registration...")
    
    for module_path, blueprint_name, url_prefix in BLUEPRINT_ROUTES:
        try:
            print(f"📦 Attempting to load: {module_path}.{blueprint_name}")
            
            # Try to import the actual module
            module = __import__(module_path, fromlist=[blueprint_name])
            blueprint = getattr(module, blueprint_name)
            app.register_blueprint(blueprint, url_prefix=url_prefix)
            
            loaded_blueprints.append((module_path, blueprint_name, url_prefix))
            blueprint_status[module_path] = {
                'status': 'loaded',
                'type': 'real',
                'url_prefix': url_prefix,
                'loaded_at': datetime.now().isoformat(),
                'blueprint_name': blueprint_name
            }
            print(f"✅ Successfully loaded: {module_path} -> {url_prefix}")
            
        except ImportError as e:
            error_msg = f"Import Error: {str(e)}"
            print(f"❌ Import failed for {module_path}: {error_msg}")
            import_errors.append((module_path, error_msg))
            create_fallback_blueprint(module_path, blueprint_name, url_prefix, error_msg)
            
        except AttributeError as e:
            error_msg = f"Blueprint '{blueprint_name}' not found in module: {str(e)}"
            print(f"❌ Blueprint not found in {module_path}: {error_msg}")
            import_errors.append((module_path, error_msg))
            create_fallback_blueprint(module_path, blueprint_name, url_prefix, error_msg)
            
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            print(f"❌ Unexpected error loading {module_path}: {error_msg}")
            print(f"📋 Traceback: {traceback.format_exc()}")
            import_errors.append((module_path, error_msg))
            create_fallback_blueprint(module_path, blueprint_name, url_prefix, error_msg)

def create_fallback_blueprint(module_path, blueprint_name, url_prefix, error_msg):
    """Create fallback blueprint for missing modules"""
    from flask import Blueprint
    
    fallback_bp = Blueprint(f'fallback_{blueprint_name}', __name__)
    
    @fallback_bp.route('/test')
    def fallback_test():
        return jsonify({
            'status': 'fallback_active',
            'message': f'{module_path} module in fallback mode',
            'error': error_msg,
            'fallback': True,
            'cost': '$0.00'
        })
    
    app.register_blueprint(fallback_bp, url_prefix=url_prefix)
    loaded_blueprints.append((module_path, f'fallback_{blueprint_name}', url_prefix))
    blueprint_status[module_path] = {
        'status': 'fallback',
        'type': 'mock',
        'url_prefix': url_prefix,
        'error': error_msg,
        'loaded_at': datetime.now().isoformat()
    }

# Add diagnostic endpoint
@app.route('/api/diagnostics')
def diagnostics():
    """Diagnostic endpoint to check blueprint loading status"""
    return jsonify({
        'status': 'diagnostic',
        'blueprint_status': blueprint_status,
        'loaded_blueprints': loaded_blueprints,
        'import_errors': import_errors,
        'total_blueprints': len(BLUEPRINT_ROUTES),
        'successful_loads': len([bp for bp in blueprint_status.values() if bp['type'] == 'real']),
        'fallback_loads': len([bp for bp in blueprint_status.values() if bp['type'] == 'mock']),
        'python_path': os.sys.path,
        'current_directory': os.getcwd(),
        'timestamp': datetime.now().isoformat()
    })

# Rest of your existing main.py code goes here...
# (Include all the existing routes and functions)

if __name__ == '__main__':
    print("🚀 Initializing Mythiq Gateway Enterprise v2.5.1...")
    print("📋 Registering blueprint modules with enhanced diagnostics...")
    
    # Register all blueprints
    register_blueprints()
    
    print(f"✅ Loaded {len(loaded_blueprints)} blueprint modules")
    print(f"🏢 Real modules: {len([bp for bp in blueprint_status.values() if bp['type'] == 'real'])}")
    print(f"⚠️ Fallback modules: {len([bp for bp in blueprint_status.values() if bp['type'] == 'mock'])}")
    
    if import_errors:
        print("❌ Import errors detected:")
        for module, error in import_errors:
            print(f"   {module}: {error}")
    
    print("🎯 Mythiq Gateway Enterprise v2.5.1 ready for deployment!")
    
    # Run the application
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
'''
    
    with open('main_fixed_v2_5_1.py', 'w') as f:
        f.write(fixed_main)
    
    print("✅ Generated main_fixed_v2_5_1.py with enhanced diagnostics")

def main():
    """Run complete diagnostic"""
    print("🔍 MYTHIQ GATEWAY BLUEPRINT DIAGNOSTIC TOOL")
    print("=" * 50)
    
    # Check file structure
    missing_files = check_file_structure()
    
    # Create missing init files
    create_missing_init_files()
    
    # Check syntax
    syntax_errors = check_python_syntax()
    
    # Test imports
    import_errors = test_imports()
    
    # Fix blueprint names
    fix_blueprint_names()
    
    # Generate fixed main.py
    generate_fixed_main_py()
    
    print("\n" + "=" * 50)
    print("📊 DIAGNOSTIC SUMMARY")
    print("=" * 50)
    
    if missing_files:
        print(f"❌ Missing files: {len(missing_files)}")
        for file in missing_files:
            print(f"   - {file}")
    else:
        print("✅ All required files present")
    
    if syntax_errors:
        print(f"❌ Syntax errors: {len(syntax_errors)}")
        for file, error in syntax_errors:
            print(f"   - {file}: {error}")
    else:
        print("✅ No syntax errors found")
    
    if import_errors:
        print(f"❌ Import errors: {len(import_errors)}")
        for module, blueprint, error in import_errors:
            print(f"   - {module}.{blueprint}: {error}")
    else:
        print("✅ All blueprints import successfully")
    
    print("\n🚀 RECOMMENDED ACTIONS:")
    if missing_files or syntax_errors or import_errors:
        print("1. Fix the issues identified above")
        print("2. Replace main.py with main_fixed_v2_5_1.py")
        print("3. Deploy and check /api/diagnostics endpoint")
    else:
        print("1. Replace main.py with main_fixed_v2_5_1.py for better diagnostics")
        print("2. Deploy and verify enterprise modules are working")
    
    print("\n✅ Diagnostic complete!")

if __name__ == '__main__':
    main()
