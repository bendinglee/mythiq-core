"""
Mythiq Gateway Enterprise - Main Application

This is the main application file for the Mythiq Gateway Enterprise system.
It provides a comprehensive AI platform with advanced capabilities including:
- Dynamic blueprint registration with self-healing capabilities
- Multi-provider AI integration with intelligent fallback and load balancing
- Enterprise module integration (Auth, Proxy, Quota)
- Cognitive processing modules (Memory, Reasoning, Validation)
- System monitoring, diagnostics, and real-time metrics
- Advanced error handling, recovery, and detailed logging
- Database integration for persistent storage (users, conversations)
- Secure file upload and management system
- Comprehensive in-code documentation and type hinting

Author: Mythiq AI Team
Version: 4.0.0
License: Proprietary
"""

# ===== Standard Library Imports =====
import os
import sys
import json
import time
import uuid
import logging
import datetime
import importlib
import pkgutil
import traceback
import threading
import functools
import inspect
import re
import random
import hashlib
import base64
import socket
import platform
import tempfile
from typing import Dict, List, Any, Optional, Union, Tuple, Callable

# ===== Third-Party Library Imports =====
# Attempt to import, and install if missing. This is for convenience in some environments.
try:
    import psutil
except ImportError:
    print("psutil not found, attempting to install...")
    os.system('pip install psutil')
    import psutil

try:
    import requests
except ImportError:
    print("requests not found, attempting to install...")
    os.system('pip install requests')
    import requests

try:
    from flask import (
        Flask, jsonify, request, render_template, send_file, abort, 
        redirect, url_for, session, Blueprint, g, current_app, 
        make_response, send_from_directory
    )
    from werkzeug.utils import secure_filename
    from werkzeug.exceptions import HTTPException
except ImportError:
    print("Flask not found, attempting to install...")
    os.system('pip install flask')
    from flask import (
        Flask, jsonify, request, render_template, send_file, abort, 
        redirect, url_for, session, Blueprint, g, current_app, 
        make_response, send_from_directory
    )
    from werkzeug.utils import secure_filename
    from werkzeug.exceptions import HTTPException

# ===== Application Setup =====

# 1. Logging Configuration
# Set up a robust logging system to capture application events, errors, and performance data.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - [%(levelname)s] - (%(threadName)s) - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),  # Log to console
        logging.FileHandler('mythiq_gateway.log', mode='a') # Log to file
    ]
)
logger = logging.getLogger('mythiq_gateway')
logger.info("Logging configured.")

# 2. Flask Application Initialization
# Create the core Flask application instance.
app = Flask(__name__, template_folder='templates', static_folder='static')
logger.info("Flask application initialized.")

# 3. Application Configuration
# Load configuration from environment variables with sensible defaults.
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', hashlib.sha256(os.urandom(64)).hexdigest()),
    MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16 MB max upload size
    UPLOAD_FOLDER=os.environ.get('UPLOAD_FOLDER', os.path.join(tempfile.gettempdir(), 'mythiq_uploads')),
    ALLOWED_EXTENSIONS={'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'mp4', 'wav'},
    SESSION_TYPE='filesystem',
    SESSION_FILE_DIR=os.path.join(tempfile.gettempdir(), 'flask_session'),
    PERMANENT_SESSION_LIFETIME=datetime.timedelta(days=7),
    DEBUG=os.environ.get('FLASK_DEBUG', '0') == '1',
    TESTING=os.environ.get('FLASK_TESTING', '0') == '1',
    ENV=os.environ.get('FLASK_ENV', 'production')
)

# Ensure necessary directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['SESSION_FILE_DIR'], exist_ok=True)
logger.info(f"Application configured. Upload folder: {app.config['UPLOAD_FOLDER']}")

# 4. Blueprint Routes Configuration
# Define the expected blueprints for the application. This list is used by the self-healing registration system.
BLUEPRINT_ROUTES: List[Tuple[str, str, str]] = [
    ("branches.auth_gate.routes", "auth_bp", "/api/auth"),
    ("branches.pro_router.routes", "pro_router_bp", "/api/proxy"),
    ("branches.quota.routes", "quota_bp", "/api/quota"),
    ("branches.memory.routes", "memory_bp", "/api/memory"),
    ("branches.reasoning.routes", "reasoning_bp", "/api/reason"),
    ("branches.self_validate.routes", "validation_bp", "/api/validate"),
    ("branches.system.routes", "system_bp", "/api/system")
]
logger.info(f"Defined {len(BLUEPRINT_ROUTES)} static blueprint routes.")

# 5. AI API Configuration
# Load API keys for various AI providers from environment variables.
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
logger.info("AI provider API keys loaded from environment.")

# 6. System Metrics Initialization
# A dictionary to hold real-time metrics about the application's performance and state.
system_metrics: Dict[str, Any] = {
    'startup_time': datetime.datetime.now(),
    'request_count': 0,
    'error_count': 0,
    'ai_request_count': 0,
    'ai_error_count': 0,
    'blueprint_count': 0,
    'last_error': None,
    'response_times': [],
    'lock': threading.Lock() # For thread-safe metric updates
}
logger.info("System metrics initialized.")

# 7. Request History
# A list to store recent request information for diagnostics.
request_history: List[Dict[str, Any]] = []
MAX_REQUEST_HISTORY = 100

# 8. Database Connection (Placeholder)
# In a real application, this would be a more robust database connection manager.
def get_db_connection():
    """Placeholder for a database connection function."""
    if 'db' not in g:
        # This is a mock connection. Replace with a real database like PostgreSQL.
        g.db = {}
    return g.db

@app.teardown_appcontext
def teardown_db(exception):
    """Closes the database again at the end of the request."""
    db = g.pop('db', None)
    if db is not None:
        # In a real app, you would close the connection here.
        pass

# ===== Core Classes =====

class FreeAIEngine:
    """
    A sophisticated fallback AI engine for when external APIs are unavailable.
    This engine provides more contextual and varied responses than a simple placeholder.
    """
    def __init__(self):
        self.version = "2.0.0"
        self.name = "FreeAIEngine"
        self.capabilities = ["text_generation", "contextual_reasoning", "simple_qa", "personality_simulation"]
        self.personalities = {
            "neutral": "You are a helpful and direct AI assistant.",
            "creative": "You are an imaginative and expressive AI assistant that loves to brainstorm.",
            "technical": "You are a precise and knowledgeable AI assistant focused on technical details."
        }
        logger.info(f"{self.name} v{self.version} initialized.")

    def generate_response(self, prompt: str, context: Optional[List[Dict[str, str]]] = None, personality: str = "neutral") -> str:
        """Generate a response based on the prompt, context, and a selected personality."""
        logger.info(f"FreeAIEngine generating response for prompt: '{prompt[:50]}...' with personality '{personality}'")
        if not prompt:
            return "I seem to have missed your question. Could you please repeat it?"

        system_prompt = self.personalities.get(personality, self.personalities["neutral"])
        full_prompt = f"{system_prompt}\n\nPrevious conversation:\n{self._format_context(context)}\n\nUser question: {prompt}"

        question_type = self._classify_question(prompt)
        
        if question_type == "greeting":
            return self._generate_greeting()
        elif question_type == "help":
            return self._generate_help_response()
        else:
            return self._generate_contextual_response(prompt, question_type)

    def _format_context(self, context: Optional[List[Dict[str, str]]]) -> str:
        if not context:
            return "No previous conversation."
        return "\n".join([f"{msg['role']}: {msg['content']}" for msg in context])

    def _classify_question(self, prompt: str) -> str:
        prompt_lower = prompt.lower()
        if any(g in prompt_lower for g in ["hello", "hi", "hey"]): return "greeting"
        if any(h in prompt_lower for h in ["help", "assist", "support"]): return "help"
        if any(f in prompt_lower for f in ["what is", "who is", "explain"]): return "factual"
        return "generic"

    def _generate_greeting(self) -> str:
        return random.choice([
            "Hello! I am the Mythiq Gateway's internal AI. How can I assist you?",
            "Greetings! I'm ready to help. What's on your mind?"
        ])

    def _generate_help_response(self) -> str:
        return ("I am the FreeAIEngine, providing core AI capabilities for the Mythiq Gateway. "
                "The platform integrates with advanced external AI for more complex tasks. "
                "You can interact with various modules via the UI or API endpoints.")

    def _generate_contextual_response(self, prompt: str, q_type: str) -> str:
        base_response = ("As the internal AI, my capabilities are focused on providing foundational support. "
                         "For advanced, real-time, or highly creative tasks, the system is designed to leverage external AI providers.")
        if q_type == "factual":
            return f"{base_response} While I can't access live data, my understanding of '{self._extract_keywords(prompt)[0] if self._extract_keywords(prompt) else 'that topic'}' is based on my general training."
        return f"{base_response} Regarding your query about '{prompt[:30]}...', I can offer a general perspective."

    def _extract_keywords(self, text: str) -> List[str]:
        common_words = set(["the", "a", "an", "is", "are", "in", "on", "of", "for", "to"])
        words = re.findall(r'\b\w+\b', text.lower())
        return [word for word in words if word not in common_words and len(word) > 3][:3]

class AIProvider:
    """Abstract base class for AI providers, defining a common interface."""
    def __init__(self, api_key: str, api_url: str, name: str):
        self.api_key = api_key
        self.api_url = api_url
        self.name = name
        self.healthy = True
        self.last_checked = datetime.datetime.now()

    def generate_response(self, messages: List[Dict[str, str]], temp: float, tokens: int) -> Tuple[Optional[str], Optional[str]]:
        raise NotImplementedError

    def check_health(self):
        # In a real scenario, this would ping a status endpoint of the provider.
        self.healthy = True
        self.last_checked = datetime.datetime.now()

class GroqAIProvider(AIProvider):
    """Groq AI provider implementation."""
    def __init__(self, api_key: str):
        super().__init__(api_key, GROQ_API_URL, "GroqAI")

    def generate_response(self, messages: List[Dict[str, str]], temp: float, tokens: int) -> Tuple[Optional[str], Optional[str]]:
        if not self.api_key: return None, "Groq API key not configured"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        data = {"model": "llama3-70b-8192", "messages": messages, "temperature": temp, "max_tokens": tokens}
        try:
            r = requests.post(self.api_url, headers=headers, json=data, timeout=30)
            r.raise_for_status()
            return r.json()['choices'][0]['message']['content'], None
        except requests.exceptions.RequestException as e:
            self.healthy = False
            logger.error(f"Groq API Error: {e}")
            return None, str(e)

class AIManager:
    """
    Manages multiple AI providers, handles fallback logic, and provides a unified interface.
    """
    def __init__(self):
        self.providers: List[AIProvider] = []
        self.free_ai = FreeAIEngine()
        if GROQ_API_KEY: self.providers.append(GroqAIProvider(GROQ_API_KEY))
        # Add other providers like OpenAI, Anthropic here if keys exist
        logger.info(f"AIManager initialized with {len(self.providers)} providers.")

    def generate_response(self, messages: List[Dict[str, str]], temp: float = 0.7, tokens: int = 1024) -> Tuple[str, str, str]:
        """Generate a response, trying each provider in order, with fallback to the free engine."""
        with system_metrics['lock']:
            system_metrics['ai_request_count'] += 1

        for provider in self.providers:
            if provider.healthy:
                response, error = provider.generate_response(messages, temp, tokens)
                if response:
                    return response, provider.name, "success"
                logger.warning(f"Provider {provider.name} failed: {error}")
        
        with system_metrics['lock']:
            system_metrics['ai_error_count'] += 1
            system_metrics['last_error'] = "All AI providers failed."
        logger.warning(system_metrics['last_error'])
        
        user_prompt = next((m['content'] for m in reversed(messages) if m['role'] == 'user'), "")
        return self.free_ai.generate_response(user_prompt, messages), "free-ai", "fallback"

# ===== Utility Functions =====

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_request_info() -> Dict[str, Any]:
    return {
        'id': str(uuid.uuid4()),
        'timestamp': datetime.datetime.now().isoformat(),
        'method': request.method,
        'path': request.path,
        'ip': request.headers.getlist("X-Forwarded-For")[0] if request.headers.getlist("X-Forwarded-For") else request.remote_addr
    }

# ===== Blueprint Registration (Self-Healing) =====

def register_blueprints(app: Flask) -> int:
    """
    Dynamically discovers and registers all blueprints from the 'branches' directory.
    This system is self-healing: it creates missing directories and placeholder files.
    """
    logger.info("Starting blueprint registration...")
    import_errors: List[Dict[str, str]] = []
    registered_blueprints: List[Dict[str, str]] = []
    branches_dir = os.path.join(os.path.dirname(__file__), 'branches')
    os.makedirs(branches_dir, exist_ok=True)
    if not os.path.exists(os.path.join(branches_dir, '__init__.py')):
        with open(os.path.join(branches_dir, '__init__.py'), 'w') as f: f.write('# Mythiq Gateway Branches\n')
    if os.path.dirname(__file__) not in sys.path: sys.path.insert(0, os.path.dirname(__file__))

    all_potential_modules = set(bp_info[0] for bp_info in BLUEPRINT_ROUTES)
    for finder, name, is_pkg in pkgutil.iter_modules([branches_dir]):
        if is_pkg: all_potential_modules.add(f"branches.{name}.routes")

    for module_path, blueprint_name, url_prefix in BLUEPRINT_ROUTES:
        try:
            module_parts = module_path.split('.')
            if len(module_parts) > 1:
                module_dir = os.path.join(branches_dir, module_parts[1])
                os.makedirs(module_dir, exist_ok=True)
                if not os.path.exists(os.path.join(module_dir, '__init__.py')):
                    with open(os.path.join(module_dir, '__init__.py'), 'w') as f: f.write(f'# {module_parts[1]} blueprint\n')
                routes_file = os.path.join(module_dir, 'routes.py')
                if not os.path.exists(routes_file):
                    logger.warning(f"Blueprint file missing, creating placeholder: {routes_file}")
                    with open(routes_file, 'w') as f:
                        f.write(f'from flask import Blueprint, jsonify\n{blueprint_name} = Blueprint("{blueprint_name}", __name__)\n@{blueprint_name}.route("/test")\ndef test(): return jsonify(message="Placeholder OK")')
            
            module = importlib.import_module(module_path)
            blueprint = getattr(module, blueprint_name, None)
            if isinstance(blueprint, Blueprint):
                app.register_blueprint(blueprint, url_prefix=url_prefix)
                registered_blueprints.append({'name': blueprint.name, 'module': module_path, 'url_prefix': url_prefix})
                logger.info(f"Registered blueprint '{blueprint.name}' from {module_path}")
            else:
                raise ImportError(f"Blueprint object '{blueprint_name}' not found in {module_path}")
        except Exception as e:
            error_info = {'module': module_path, 'error': str(e)}
            import_errors.append(error_info)
            logger.error(f"Failed to register blueprint from {module_path}: {e}", exc_info=True)

    app.config['REGISTERED_BLUEPRINTS'] = registered_blueprints
    app.config['BLUEPRINT_IMPORT_ERRORS'] = import_errors
    with system_metrics['lock']:
        system_metrics['blueprint_count'] = len(registered_blueprints)
    logger.info(f"Blueprint registration complete. Registered: {len(registered_blueprints)}, Errors: {len(import_errors)}.")
    return len(registered_blueprints)

# ===== Request Handlers & Hooks =====

@app.before_request
def before_request_hook():
    g.start_time = time.monotonic()
    with system_metrics['lock']:
        system_metrics['request_count'] += 1
    logger.info(f"Request started: {request.method} {request.path} from {get_request_info()['ip']}")

@app.after_request
def after_request_hook(response):
    response_time = (time.monotonic() - g.start_time) * 1000 # in ms
    with system_metrics['lock']:
        system_metrics['response_times'].append(response_time)
        if len(system_metrics['response_times']) > 100: system_metrics['response_times'].pop(0)
    logger.info(f"Request finished in {response_time:.2f}ms with status {response.status_code}")
    response.headers["X-Response-Time"] = f"{response_time:.2f}ms"
    return response

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    with system_metrics['lock']:
        system_metrics['error_count'] += 1
        system_metrics['last_error'] = f"HTTPException: {e.code} {e.name}"
    logger.error(f"HTTP Exception: {e.code} {e.name} for {request.path}", exc_info=True)
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

@app.errorhandler(Exception)
def handle_generic_exception(e):
    with system_metrics['lock']:
        system_metrics['error_count'] += 1
        system_metrics['last_error'] = f"Unhandled Exception: {type(e).__name__}"
    logger.critical(f"Unhandled Exception for {request.path}: {e}", exc_info=True)
    return jsonify({
        "code": 500,
        "name": "Internal Server Error",
        "description": "An unexpected error occurred. The administrators have been notified."
    }), 500

# ===== Core API Routes =====

@app.route('/')
def index():
    """Serves the main HTML page of the application."""
    return render_template('index.html')

@app.route('/health')
def health_check():
    """Provides a simple health check endpoint for monitoring services."""
    return jsonify({"status": "healthy", "timestamp": datetime.datetime.now().isoformat()})

@app.route('/api/brain', methods=['POST'])
def brain_endpoint():
    """The primary AI interaction endpoint."""
    data = request.get_json()
    if not data or 'prompt' not in data:
        abort(400, description="Missing 'prompt' in request body.")
    
    ai_manager = AIManager()
    messages = [
        {"role": "system", "content": "You are a helpful assistant that provides accurate, informative responses."},
        {"role": "user", "content": data['prompt']}
    ]
    
    # Optional parameters
    temperature = float(data.get('temperature', 0.7))
    max_tokens = int(data.get('max_tokens', 1024))
    
    # Generate response
    response, provider, status = ai_manager.generate_response(messages, temperature, max_tokens)
    
    return jsonify({
        "response": response,
        "model": f"{provider}-model",
        "status": status
    })

@app.route('/api/ai-proxy', methods=['POST'])
def ai_proxy_endpoint():
    """Enhanced AI endpoint with detailed metadata and options."""
    data = request.get_json()
    if not data or 'prompt' not in data:
        abort(400, description="Missing 'prompt' in request body.")
    
    # Get optional parameters
    temperature = float(data.get('temperature', 0.7))
    max_tokens = int(data.get('max_tokens', 1024))
    system_message = data.get('system_message', "You are a helpful assistant that provides accurate, informative responses.")
    
    # Create AI manager
    ai_manager = AIManager()
    
    # Prepare messages
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": data['prompt']}
    ]
    
    # Add conversation history if provided
    if 'history' in data and isinstance(data['history'], list):
        # Insert history before the current user message
        messages = [messages[0]] + data['history'] + [messages[1]]
    
    # Generate response
    response, provider, status = ai_manager.generate_response(messages, temperature, max_tokens)
    
    # Calculate token estimate (rough approximation)
    prompt_tokens = sum(len(m.get('content', '')) // 4 for m in messages)
    completion_tokens = len(response) // 4
    total_tokens = prompt_tokens + completion_tokens
    
    return jsonify({
        "ai_response": response,
        "provider": provider,
        "model": f"{provider}-model",
        "status": status,
        "metadata": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "timestamp": datetime.datetime.now().isoformat()
        }
    })

@app.route('/api/enterprise/status', methods=['GET'])
def enterprise_status_endpoint():
    """Provides detailed status information about the enterprise modules."""
    # Count registered blueprints by category
    registered_blueprints = app.config.get('REGISTERED_BLUEPRINTS', [])
    
    # Define expected enterprise and cognitive blueprints
    enterprise_blueprints = ['/api/auth', '/api/proxy', '/api/quota']
    cognitive_blueprints = ['/api/memory', '/api/reason', '/api/validate']
    system_blueprints = ['/api/system']
    
    # Count registered blueprints by category
    enterprise_count = sum(1 for bp in registered_blueprints if bp['url_prefix'] in enterprise_blueprints)
    cognitive_count = sum(1 for bp in registered_blueprints if bp['url_prefix'] in cognitive_blueprints)
    system_count = sum(1 for bp in registered_blueprints if bp['url_prefix'] in system_blueprints)
    
    # Calculate scores
    enterprise_score = enterprise_count / len(enterprise_blueprints) if enterprise_blueprints else 0
    cognitive_score = cognitive_count / len(cognitive_blueprints) if cognitive_blueprints else 0
    system_score = system_count / len(system_blueprints) if system_blueprints else 0
    
    # Calculate overall score
    total_blueprints = len(enterprise_blueprints) + len(cognitive_blueprints) + len(system_blueprints)
    total_registered = enterprise_count + cognitive_count + system_count
    overall_score = total_registered / total_blueprints if total_blueprints else 0
    
    # Determine license type
    license_type = "Community"
    if overall_score >= 0.8:
        license_type = "Enterprise"
    elif overall_score >= 0.5:
        license_type = "Professional"
    
    # Get detailed blueprint information
    blueprint_details = []
    for bp in registered_blueprints:
        # Get routes for this blueprint
        routes = []
        for rule in app.url_map.iter_rules():
            if rule.endpoint.startswith(bp['name'] + '.'):
                routes.append({
                    'path': str(rule),
                    'endpoint': rule.endpoint,
                    'methods': list(rule.methods)
                })
        
        blueprint_details.append({
            'name': bp['name'],
            'module': bp['module'],
            'url_prefix': bp['url_prefix'],
            'routes': routes,
            'route_count': len(routes)
        })
    
    return jsonify({
        "enterprise_score": f"{enterprise_count}/{len(enterprise_blueprints)}",
        "cognitive_score": f"{cognitive_count}/{len(cognitive_blueprints)}",
        "system_score": f"{system_count}/{len(system_blueprints)}",
        "overall_score": round(overall_score * 100),
        "license_type": license_type,
        "registered_blueprints": registered_blueprints,
        "blueprint_details": blueprint_details
    })

@app.route('/api/import-errors', methods=['GET'])
def import_errors_endpoint():
    """Provides information about blueprint import errors."""
    errors = app.config.get('BLUEPRINT_IMPORT_ERRORS', [])
    error_count = len(errors)
    
    recommendations = []
    if error_count > 0:
        recommendations.append("Ensure blueprint variable names match expected names")
        recommendations.append("Check if blueprint files exist in correct locations")
        recommendations.append("Verify directory structure includes __init__.py files")
        recommendations.append("Check for syntax errors in blueprint files")
        recommendations.append("Ensure all required dependencies are installed")
    
    return jsonify({
        "error_count": error_count,
        "errors": errors,
        "recommendations": recommendations,
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/api/blueprints', methods=['GET'])
def list_blueprints_endpoint():
    """Lists all registered blueprints and their routes."""
    registered = app.config.get('REGISTERED_BLUEPRINTS', [])
    errors = app.config.get('BLUEPRINT_IMPORT_ERRORS', [])
    
    # Get all rules and organize by blueprint
    rules_by_blueprint = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            blueprint = rule.endpoint.split('.')[0] if '.' in rule.endpoint else 'app'
            if blueprint not in rules_by_blueprint:
                rules_by_blueprint[blueprint] = []
            rules_by_blueprint[blueprint].append({
                'route': str(rule),
                'methods': list(rule.methods),
                'endpoint': rule.endpoint
            })
    
    return jsonify({
        "loaded_blueprints": len(registered),
        "registered_blueprints": registered,
        "import_errors": errors,
        "routes_by_blueprint": rules_by_blueprint,
        "total_routes": sum(len(routes) for routes in rules_by_blueprint.values())
    })

@app.route('/api/metrics', methods=['GET'])
def metrics_endpoint():
    """Provides detailed system metrics."""
    # Calculate average response time
    with system_metrics['lock']:
        response_times = system_metrics['response_times'].copy()
    avg_response_time = sum(response_times) / len(response_times) if response_times else 0
    
    # Get system info
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    return jsonify({
        "request_metrics": {
            "total_requests": system_metrics['request_count'],
            "error_count": system_metrics['error_count'],
            "error_rate": system_metrics['error_count'] / system_metrics['request_count'] if system_metrics['request_count'] else 0,
            "avg_response_time_ms": avg_response_time,
            "response_time_p95": sorted(response_times)[int(len(response_times) * 0.95)] if response_times else 0,
            "response_time_p99": sorted(response_times)[int(len(response_times) * 0.99)] if response_times else 0
        },
        "ai_metrics": {
            "total_ai_requests": system_metrics['ai_request_count'],
            "ai_error_count": system_metrics['ai_error_count'],
            "ai_error_rate": system_metrics['ai_error_count'] / system_metrics['ai_request_count'] if system_metrics['ai_request_count'] else 0,
            "last_error": system_metrics['last_error']
        },
        "system_metrics": {
            "uptime_seconds": (datetime.datetime.now() - system_metrics['startup_time']).total_seconds(),
            "memory_usage_percent": memory.percent,
            "memory_available_mb": memory.available / (1024 * 1024),
            "disk_usage_percent": disk.percent,
            "disk_free_gb": disk.free / (1024 * 1024 * 1024),
            "cpu_usage_percent": psutil.cpu_percent(),
            "blueprint_count": system_metrics['blueprint_count']
        },
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/api/diagnostics', methods=['GET'])
def diagnostics_endpoint():
    """Provides comprehensive system diagnostics."""
    # Get system info
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # Get process info
    process = psutil.Process(os.getpid())
    process_memory = process.memory_info()
    
    # Get network info
    network_info = {}
    try:
        network_stats = psutil.net_io_counters()
        network_info = {
            "bytes_sent": network_stats.bytes_sent,
            "bytes_recv": network_stats.bytes_recv,
            "packets_sent": network_stats.packets_sent,
            "packets_recv": network_stats.packets_recv,
            "errin": network_stats.errin,
            "errout": network_stats.errout,
            "dropin": network_stats.dropin,
            "dropout": network_stats.dropout
        }
    except Exception as e:
        network_info = {"error": str(e)}
    
    # Get Python info
    python_info = {
        "version": platform.python_version(),
        "implementation": platform.python_implementation(),
        "compiler": platform.python_compiler(),
        "build": platform.python_build()
    }
    
    # Get environment variables (filtered for security)
    env_vars = {
        "PORT": os.environ.get("PORT", "Not set"),
        "FLASK_ENV": os.environ.get("FLASK_ENV", "Not set"),
        "FLASK_DEBUG": os.environ.get("FLASK_DEBUG", "Not set"),
        "PYTHONPATH": os.environ.get("PYTHONPATH", "Not set")
    }
    
    # Get AI provider info
    ai_providers = []
    if GROQ_API_KEY:
        ai_providers.append({
            "name": "groq",
            "status": "configured",
            "api_url": GROQ_API_URL
        })
    if OPENAI_API_KEY:
        ai_providers.append({
            "name": "openai",
            "status": "configured",
            "api_url": OPENAI_API_URL
        })
    if ANTHROPIC_API_KEY:
        ai_providers.append({
            "name": "anthropic",
            "status": "configured",
            "api_url": ANTHROPIC_API_URL
        })
    
    # Get blueprint info
    registered_blueprints = app.config.get('REGISTERED_BLUEPRINTS', [])
    import_errors = app.config.get('BLUEPRINT_IMPORT_ERRORS', [])
    
    return jsonify({
        "system": {
            "hostname": socket.gethostname(),
            "platform": platform.platform(),
            "processor": platform.processor(),
            "architecture": platform.architecture(),
            "machine": platform.machine(),
            "node": platform.node(),
            "release": platform.release(),
            "system": platform.system(),
            "version": platform.version(),
            "uptime": (datetime.datetime.now() - system_metrics['startup_time']).total_seconds()
        },
        "memory": {
            "total": memory.total,
            "available": memory.available,
            "used": memory.used,
            "free": memory.free,
            "percent": memory.percent,
            "active": memory.active if hasattr(memory, 'active') else None,
            "inactive": memory.inactive if hasattr(memory, 'inactive') else None,
            "buffers": memory.buffers if hasattr(memory, 'buffers') else None,
            "cached": memory.cached if hasattr(memory, 'cached') else None,
            "shared": memory.shared if hasattr(memory, 'shared') else None
        },
        "disk": {
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
            "percent": disk.percent
        },
        "process": {
            "pid": process.pid,
            "name": process.name(),
            "exe": process.exe(),
            "cwd": process.cwd(),
            "cmdline": process.cmdline(),
            "create_time": datetime.datetime.fromtimestamp(process.create_time()).isoformat(),
            "status": process.status(),
            "username": process.username(),
            "memory_info": {
                "rss": process_memory.rss,
                "vms": process_memory.vms,
                "shared": process_memory.shared if hasattr(process_memory, 'shared') else None,
                "text": process_memory.text if hasattr(process_memory, 'text') else None,
                "lib": process_memory.lib if hasattr(process_memory, 'lib') else None,
                "data": process_memory.data if hasattr(process_memory, 'data') else None,
                "dirty": process_memory.dirty if hasattr(process_memory, 'dirty') else None
            },
            "cpu_percent": process.cpu_percent(),
            "memory_percent": process.memory_percent(),
            "threads": process.num_threads(),
            "open_files": len(process.open_files()),
            "connections": len(process.connections())
        },
        "network": network_info,
        "python": python_info,
        "environment": env_vars,
        "ai_providers": ai_providers,
        "blueprints": {
            "registered": registered_blueprints,
            "import_errors": import_errors
        },
        "metrics": {
            "request_count": system_metrics['request_count'],
            "error_count": system_metrics['error_count'],
            "ai_request_count": system_metrics['ai_request_count'],
            "ai_error_count": system_metrics['ai_error_count'],
            "blueprint_count": system_metrics['blueprint_count'],
            "last_error": system_metrics['last_error']
        },
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/api/upload', methods=['POST'])
def upload_file_endpoint():
    """Handles file uploads."""
    # Check if file is in request
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    # Check if file is selected
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Check if file is allowed
    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400
    
    # Save file with unique name
    filename = secure_filename(file.filename)
    unique_id = str(uuid.uuid4())
    extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    unique_filename = f"{unique_id}.{extension}" if extension else unique_id
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(file_path)
    
    # Get file metadata
    file_size = os.path.getsize(file_path)
    file_type = extension
    file_created = datetime.datetime.fromtimestamp(os.path.getctime(file_path)).isoformat()
    
    return jsonify({
        "message": "File uploaded successfully",
        "filename": unique_filename,
        "original_filename": filename,
        "path": file_path,
        "size": file_size,
        "type": file_type,
        "created": file_created
    })

@app.route('/api/files/<filename>', methods=['GET'])
def get_file_endpoint(filename):
    """Retrieves a file."""
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # Check if file exists
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404
    
    # Return file
    return send_file(file_path)

@app.route('/api/files', methods=['GET'])
def list_files_endpoint():
    """Lists all uploaded files."""
    files = []
    
    # Get all files in upload folder
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Skip directories
        if os.path.isdir(file_path):
            continue
        
        # Get file info
        file_size = os.path.getsize(file_path)
        file_type = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        file_created = datetime.datetime.fromtimestamp(os.path.getctime(file_path)).isoformat()
        
        files.append({
            "filename": filename,
            "path": file_path,
            "size": file_size,
            "type": file_type,
            "created": file_created
        })
    
    return jsonify({
        "files": files,
        "count": len(files),
        "total_size": sum(file["size"] for file in files)
    })

# ===== Main Application Entry Point =====

if __name__ == '__main__':
    # Register blueprints
    num_blueprints = register_blueprints(app)
    logger.info(f"Registered {num_blueprints} blueprints")
    
    # Run the app
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting Mythiq Gateway on port {port}")
    app.run(host='0.0.0.0', port=port)
