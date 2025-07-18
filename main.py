"""
Mythiq Gateway Enterprise - Main Application

This is the main application file for the Mythiq Gateway Enterprise system.
It provides a comprehensive AI platform with advanced capabilities including:
- Dynamic blueprint registration
- Enterprise module integration
- Cognitive processing
- System monitoring and diagnostics
- Advanced error handling and recovery
- Comprehensive logging and analytics

Author: Mythiq AI Team
Version: 3.0.0
License: Proprietary
"""

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

try:
    import psutil
except ImportError:
    os.system('pip install psutil')
    import psutil

try:
    import requests
except ImportError:
    os.system('pip install requests')
    import requests

try:
    from flask import Flask, jsonify, request, render_template, send_file, abort, redirect, url_for, session, Blueprint, g, current_app, make_response, send_from_directory
    from werkzeug.utils import secure_filename
    from werkzeug.exceptions import HTTPException
except ImportError:
    os.system('pip install flask')
    from flask import Flask, jsonify, request, render_template, send_file, abort, redirect, url_for, session, Blueprint, g, current_app, make_response, send_from_directory
    from werkzeug.utils import secure_filename
    from werkzeug.exceptions import HTTPException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('mythiq_gateway.log')
    ]
)
logger = logging.getLogger('mythiq_gateway')

# Create Flask application
app = Flask(__name__)

# Load configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_for_testing')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload size
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', os.path.join(tempfile.gettempdir(), 'mythiq_uploads'))
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'mp4', 'wav'}
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=7)
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', '0') == '1'
app.config['TESTING'] = os.environ.get('FLASK_TESTING', '0') == '1'
app.config['ENV'] = os.environ.get('FLASK_ENV', 'production')

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Blueprint routes configuration
BLUEPRINT_ROUTES = [
    ("branches.auth_gate.routes", "auth_bp", "/api/auth"),
    ("branches.pro_router.routes", "pro_router_bp", "/api/proxy"),
    ("branches.quota.routes", "quota_bp", "/api/quota"),
    ("branches.memory.routes", "memory_bp", "/api/memory"),
    ("branches.reasoning.routes", "reasoning_bp", "/api/reason"),
    ("branches.self_validate.routes", "validation_bp", "/api/validate"),
    ("branches.system.routes", "system_bp", "/api/system")
]

# AI API configuration
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"

# System metrics
system_metrics = {
    'startup_time': datetime.datetime.now(),
    'request_count': 0,
    'error_count': 0,
    'ai_request_count': 0,
    'ai_error_count': 0,
    'blueprint_count': 0,
    'last_error': None,
    'response_times': []
}

# Request tracking
request_history = []
MAX_REQUEST_HISTORY = 100

# Thread-local storage
thread_local = threading.local()

# ===== Utility Classes =====

class FreeAIEngine:
    """
    Fallback AI engine that provides basic responses when external APIs are unavailable.
    This ensures the system remains operational even without API access.
    """
    def __init__(self):
        self.version = "1.0.0"
        self.name = "FreeAIEngine"
        self.capabilities = ["text_generation", "basic_reasoning", "simple_qa"]
        
    def generate_response(self, prompt: str, context: Optional[List[Dict[str, str]]] = None) -> str:
        """Generate a response based on the prompt and optional context"""
        # Log the request
        logger.info(f"FreeAIEngine generating response for prompt: {prompt[:50]}...")
        
        # Simple response generation
        if not prompt:
            return "I didn't receive a question. How can I help you?"
        
        # Extract question type
        question_type = self._classify_question(prompt)
        
        # Generate appropriate response based on question type
        if question_type == "greeting":
            return self._generate_greeting()
        elif question_type == "factual":
            return self._generate_factual_response(prompt)
        elif question_type == "opinion":
            return self._generate_opinion_response(prompt)
        elif question_type == "help":
            return self._generate_help_response()
        else:
            return self._generate_generic_response(prompt)
    
    def _classify_question(self, prompt: str) -> str:
        """Classify the type of question being asked"""
        prompt_lower = prompt.lower()
        
        # Check for greetings
        if any(greeting in prompt_lower for greeting in ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening"]):
            return "greeting"
        
        # Check for help requests
        if any(help_term in prompt_lower for help_term in ["help", "assist", "support", "guide", "how do i", "how to"]):
            return "help"
        
        # Check for factual questions
        if any(factual_term in prompt_lower for factual_term in ["what is", "who is", "where is", "when is", "why is", "how does", "explain"]):
            return "factual"
        
        # Default to opinion
        return "opinion"
    
    def _generate_greeting(self) -> str:
        """Generate a greeting response"""
        greetings = [
            "Hello! I'm the Mythiq Gateway AI assistant. How can I help you today?",
            "Hi there! I'm here to assist you. What can I do for you?",
            "Greetings! I'm your AI assistant. How may I be of service?",
            "Hello! I'm the free version of the Mythiq AI. What would you like to know?"
        ]
        return random.choice(greetings)
    
    def _generate_factual_response(self, prompt: str) -> str:
        """Generate a response for factual questions"""
        return (
            "I'm the free version of Mythiq AI, so I don't have access to real-time information or specialized knowledge. "
            "For factual questions, you might want to use the full version of Mythiq Gateway with external AI integration. "
            "However, I can still help with basic questions and provide general guidance."
        )
    
    def _generate_opinion_response(self, prompt: str) -> str:
        """Generate a response for opinion questions"""
        return (
            "As a basic AI assistant, I don't form personal opinions. "
            "I'm designed to provide helpful, harmless, and honest responses based on general knowledge. "
            "For more nuanced discussions, the full version of Mythiq Gateway can provide more detailed responses."
        )
    
    def _generate_help_response(self) -> str:
        """Generate a help response"""
        return (
            "I'm the free version of Mythiq AI, and I can help with basic questions and tasks. "
            "The Mythiq Gateway platform offers the following features:\n\n"
            "1. AI-powered conversations and assistance\n"
            "2. Enterprise modules for authentication, routing, and quota management\n"
            "3. Cognitive modules for memory, reasoning, and validation\n"
            "4. System monitoring and diagnostics\n\n"
            "For more advanced features, consider using the external AI integration."
        )
    
    def _generate_generic_response(self, prompt: str) -> str:
        """Generate a generic response based on the prompt"""
        # Extract keywords from prompt
        keywords = self._extract_keywords(prompt)
        
        # Generate response based on keywords
        if not keywords:
            return "I understand you're asking something, but I'm not sure what specifically. Could you please provide more details?"
        
        return f"I understand you're asking about {', '.join(keywords)}. As the free version of Mythiq AI, I have limited knowledge. For more detailed information on this topic, please use the full version of Mythiq Gateway with external AI integration."
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract key terms from the text"""
        # Simple keyword extraction
        common_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "with", "by", "about", "like", "through", "over", "before", "after", "since", "during", "above", "below", "from", "up", "down", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did", "will", "would", "shall", "should", "may", "might", "must", "can", "could"}
        
        # Tokenize and filter
        words = re.findall(r'\b\w+\b', text.lower())
        keywords = [word for word in words if word not in common_words and len(word) > 3]
        
        # Return unique keywords, up to 3
        unique_keywords = list(set(keywords))
        return unique_keywords[:3]

class AIProvider:
    """
    Abstract base class for AI providers.
    This provides a common interface for different AI services.
    """
    def __init__(self, api_key: str, api_url: str):
        self.api_key = api_key
        self.api_url = api_url
        self.name = "BaseAIProvider"
    
    def generate_response(self, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 1024) -> Tuple[Optional[str], Optional[str]]:
        """Generate a response from the AI provider"""
        raise NotImplementedError("Subclasses must implement generate_response")
    
    def _log_request(self, messages: List[Dict[str, str]]):
        """Log the request for monitoring"""
        prompt_preview = messages[-1]['content'][:50] + "..." if messages and 'content' in messages[-1] else "No content"
        logger.info(f"{self.name} request: {prompt_preview}")
    
    def _log_response(self, response: str):
        """Log the response for monitoring"""
        response_preview = response[:50] + "..." if response else "No response"
        logger.info(f"{self.name} response: {response_preview}")
    
    def _log_error(self, error: str):
        """Log an error for monitoring"""
        logger.error(f"{self.name} error: {error}")

class GroqAIProvider(AIProvider):
    """
    Groq AI provider implementation.
    """
    def __init__(self, api_key: str):
        super().__init__(api_key, GROQ_API_URL)
        self.name = "GroqAI"
    
    def generate_response(self, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 1024) -> Tuple[Optional[str], Optional[str]]:
        """Generate a response using the Groq API"""
        if not self.api_key:
            return None, "Groq API key not configured"
        
        self._log_request(messages)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "llama3-70b-8192",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                response_text = result['choices'][0]['message']['content']
                self._log_response(response_text)
                return response_text, None
            else:
                error_message = f"Groq API Error: {response.status_code} - {response.text}"
                self._log_error(error_message)
                return None, error_message
        except Exception as e:
            error_message = f"Exception: {str(e)}"
            self._log_error(error_message)
            return None, error_message

class OpenAIProvider(AIProvider):
    """
    OpenAI provider implementation.
    """
    def __init__(self, api_key: str):
        super().__init__(api_key, OPENAI_API_URL)
        self.name = "OpenAI"
    
    def generate_response(self, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 1024) -> Tuple[Optional[str], Optional[str]]:
        """Generate a response using the OpenAI API"""
        if not self.api_key:
            return None, "OpenAI API key not configured"
        
        self._log_request(messages)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                response_text = result['choices'][0]['message']['content']
                self._log_response(response_text)
                return response_text, None
            else:
                error_message = f"OpenAI API Error: {response.status_code} - {response.text}"
                self._log_error(error_message)
                return None, error_message
        except Exception as e:
            error_message = f"Exception: {str(e)}"
            self._log_error(error_message)
            return None, error_message

class AnthropicProvider(AIProvider):
    """
    Anthropic provider implementation.
    """
    def __init__(self, api_key: str):
        super().__init__(api_key, ANTHROPIC_API_URL)
        self.name = "Anthropic"
    
    def generate_response(self, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 1024) -> Tuple[Optional[str], Optional[str]]:
        """Generate a response using the Anthropic API"""
        if not self.api_key:
            return None, "Anthropic API key not configured"
        
        self._log_request(messages)
        
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        # Convert messages to Anthropic format
        system_message = ""
        user_messages = []
        
        for message in messages:
            if message["role"] == "system":
                system_message = message["content"]
            else:
                user_messages.append(message)
        
        # If no user messages, return error
        if not user_messages:
            return None, "No user messages provided"
        
        data = {
            "model": "claude-2.1",
            "system": system_message,
            "messages": user_messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                response_text = result['content'][0]['text']
                self._log_response(response_text)
                return response_text, None
            else:
                error_message = f"Anthropic API Error: {response.status_code} - {response.text}"
                self._log_error(error_message)
                return None, error_message
        except Exception as e:
            error_message = f"Exception: {str(e)}"
            self._log_error(error_message)
            return None, error_message

class AIManager:
    """
    Manages multiple AI providers and handles fallback logic.
    """
    def __init__(self):
        self.providers = []
        self.free_ai = FreeAIEngine()
        
        # Initialize providers if API keys are available
        if GROQ_API_KEY:
            self.providers.append(GroqAIProvider(GROQ_API_KEY))
        
        if OPENAI_API_KEY:
            self.providers.append(OpenAIProvider(OPENAI_API_KEY))
        
        if ANTHROPIC_API_KEY:
            self.providers.append(AnthropicProvider(ANTHROPIC_API_KEY))
    
    def generate_response(self, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 1024) -> Tuple[str, str, str]:
        """
        Generate a response using available AI providers with fallback logic.
        Returns (response, provider_name, status)
        """
        # Track AI request
        system_metrics['ai_request_count'] += 1
        
        # Try each provider in order
        for provider in self.providers:
            response, error = provider.generate_response(messages, temperature, max_tokens)
            
            if response:
                return response, provider.name, "success"
            
            # Log the error but continue to next provider
            logger.warning(f"Provider {provider.name} failed: {error}")
        
        # If all providers fail, use free AI engine
        if self.providers:
            system_metrics['ai_error_count'] += 1
            system_metrics['last_error'] = f"All AI providers failed, falling back to free AI engine"
            logger.warning(system_metrics['last_error'])
        
        # Extract the last user message
        user_message = ""
        for message in reversed(messages):
            if message["role"] == "user":
                user_message = message["content"]
                break
        
        free_response = self.free_ai.generate_response(user_message, messages)
        return free_response, "free-ai", "fallback"

# ===== Utility Functions =====

def allowed_file(filename: str) -> bool:
    """Check if a file has an allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_file_extension(filename: str) -> str:
    """Get the extension of a file"""
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

def generate_unique_filename(filename: str) -> str:
    """Generate a unique filename to prevent collisions"""
    extension = get_file_extension(filename)
    unique_id = str(uuid.uuid4())
    return f"{unique_id}.{extension}" if extension else unique_id

def get_request_ip() -> str:
    """Get the IP address of the current request"""
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0]
    return request.remote_addr or "unknown"

def get_request_info() -> Dict[str, Any]:
    """Get information about the current request"""
    return {
        'id': str(uuid.uuid4()),
        'timestamp': datetime.datetime.now().isoformat(),
        'method': request.method,
        'path': request.path,
        'ip': get_request_ip(),
        'user_agent': request.headers.get('User-Agent', 'unknown'),
        'content_type': request.headers.get('Content-Type', 'unknown'),
        'content_length': request.headers.get('Content-Length', 'unknown')
    }

def log_request() -> None:
    """Log information about the current request"""
    request_info = get_request_info()
    
    # Add to request history
    request_history.append(request_info)
    
    # Trim history if needed
    if len(request_history) > MAX_REQUEST_HISTORY:
        request_history.pop(0)
    
    # Log request
    logger.info(f"Request: {request_info['method']} {request_info['path']} from {request_info['ip']}")
    
    # Update metrics
    system_metrics['request_count'] += 1

def log_response(response_time: float) -> None:
    """Log information about the response"""
    # Update metrics
    system_metrics['response_times'].append(response_time)
    
    # Trim response times if needed
    if len(system_metrics['response_times']) > 100:
        system_metrics['response_times'].pop(0)
    
    # Log response time
    logger.info(f"Response time: {response_time:.4f}s")

def log_error(error: Exception) -> None:
    """Log information about an error"""
    # Update metrics
    system_metrics['error_count'] += 1
    system_metrics['last_error'] = str(error)
    
    # Log error
    logger.error(f"Error: {str(error)}")
    logger.error(traceback.format_exc())

def get_system_info() -> Dict[str, Any]:
    """Get information about the system"""
    return {
        'platform': platform.platform(),
        'python_version': platform.python_version(),
        'hostname': socket.gethostname(),
        'ip_address': socket.gethostbyname(socket.gethostname()),
        'cpu_count': os.cpu_count(),
        'memory': psutil.virtual_memory()._asdict() if 'psutil' in sys.modules else 'psutil not available',
        'disk': psutil.disk_usage('/')._asdict() if 'psutil' in sys.modules else 'psutil not available',
        'uptime': (datetime.datetime.now() - system_metrics['startup_time']).total_seconds()
    }

def register_blueprints(app: Flask) -> int:
    """
    Dynamically register all blueprints from the branches directory.
    Returns the number of registered blueprints.
    """
    import_errors = []
    registered_blueprints = []
    
    # Ensure branches directory exists
    branches_dir = os.path.join(os.path.dirname(__file__), 'branches')
    os.makedirs(branches_dir, exist_ok=True)
    
    # Create __init__.py if it doesn't exist
    init_file = os.path.join(branches_dir, '__init__.py')
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write('# Blueprint modules package\n')
    
    # Add branches to path if needed
    if branches_dir not in sys.path:
        sys.path.insert(0, os.path.dirname(__file__))
    
    # First try the static blueprint routes
    for module_path, blueprint_name, url_prefix in BLUEPRINT_ROUTES:
        try:
            # Extract module directory and ensure it exists
            module_parts = module_path.split('.')
            if len(module_parts) >= 2:
                module_dir = os.path.join(branches_dir, module_parts[1])
                os.makedirs(module_dir, exist_ok=True)
                
                # Create __init__.py if it doesn't exist
                module_init = os.path.join(module_dir, '__init__.py')
                if not os.path.exists(module_init):
                    with open(module_init, 'w') as f:
                        f.write(f'# {module_parts[1]} blueprint package\n')
                
                # Create routes.py with template if it doesn't exist
                routes_file = os.path.join(module_dir, 'routes.py')
                if not os.path.exists(routes_file):
                    with open(routes_file, 'w') as f:
                        f.write(f'''from flask import Blueprint, jsonify, request

{blueprint_name} = Blueprint('{blueprint_name}', __name__)

@{blueprint_name}.route('/test', methods=['GET'])
def test():
    """Test endpoint to verify the blueprint is working"""
    return jsonify({{
        "status": "success",
        "module": "{module_parts[1]}",
        "message": "{module_parts[1].replace('_', ' ').title()} module is operational"
    }})

@{blueprint_name}.route('/status', methods=['GET'])
def status():
    """Status endpoint to check module health"""
    return jsonify({{
        "status": "operational",
        "version": "1.0.0",
        "features": ["{module_parts[1].replace('_', ' ')}"]
    }})
''')
            
            # Import the module
            module = importlib.import_module(module_path)
            blueprint = getattr(module, blueprint_name, None)
            
            if blueprint and isinstance(blueprint, Blueprint):
                app.register_blueprint(blueprint, url_prefix=url_prefix)
                registered_blueprints.append({
                    'name': blueprint.name,
                    'module': module_path,
                    'url_prefix': url_prefix
                })
                logger.info(f"Registered static blueprint: {blueprint.name} from {module_path} with prefix {url_prefix}")
            else:
                import_errors.append({
                    'module': module_path,
                    'error': f"Blueprint '{blueprint_name}' not found or not a Blueprint object"
                })
                logger.warning(f"Error: Blueprint '{blueprint_name}' not found in {module_path}")
        except Exception as e:
            import_errors.append({
                'module': module_path,
                'error': str(e)
            })
            logger.error(f"Error importing {module_path}: {e}")
            logger.error(traceback.format_exc())
    
    # Then try dynamic discovery for any additional blueprints
    for finder, name, is_pkg in pkgutil.iter_modules([branches_dir]):
        if is_pkg:
            # Ensure module directory has __init__.py
            module_dir = os.path.join(branches_dir, name)
            module_init = os.path.join(module_dir, '__init__.py')
            if not os.path.exists(module_init):
                with open(module_init, 'w') as f:
                    f.write(f'# {name} blueprint package\n')
            
            # Try to import routes.py
            routes_file = os.path.join(module_dir, 'routes.py')
            if not os.path.exists(routes_file):
                continue
                
            try:
                # Skip if already registered via static routes
                module_path = f'branches.{name}.routes'
                if any(bp['module'] == module_path for bp in registered_blueprints):
                    continue
                
                # Import the module
                module = importlib.import_module(module_path)
                
                # Look for Blueprint objects
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, Blueprint):
                        # Generate URL prefix based on module name
                        url_prefix = f'/api/{name.replace("_", "")}'
                        
                        # Special case handling for known modules
                        if name == 'auth_gate':
                            url_prefix = '/api/auth'
                        elif name == 'pro_router':
                            url_prefix = '/api/proxy'
                        elif name == 'self_validate':
                            url_prefix = '/api/validate'
                        elif name == 'reasoning':
                            url_prefix = '/api/reason'
                        
                        # Register the blueprint
                        app.register_blueprint(attr, url_prefix=url_prefix)
                        registered_blueprints.append({
                            'name': attr.name,
                            'module': module_path,
                            'url_prefix': url_prefix
                        })
                        logger.info(f"Registered dynamic blueprint: {attr.name} from {module_path} with prefix {url_prefix}")
                        break
            except Exception as e:
                import_errors.append({
                    'module': module_path,
                    'error': str(e)
                })
                logger.error(f"Error importing {module_path}: {e}")
                logger.error(traceback.format_exc())
    
    # Store blueprint info in app config for diagnostics
    app.config['REGISTERED_BLUEPRINTS'] = registered_blueprints
    app.config['BLUEPRINT_IMPORT_ERRORS'] = import_errors
    
    # Update metrics
    system_metrics['blueprint_count'] = len(registered_blueprints)
    
    return len(registered_blueprints)

# ===== Request Handlers =====

@app.before_request
def before_request():
    """Execute before each request"""
    # Store request start time
    g.start_time = time.time()
    
    # Log request
    log_request()

@app.after_request
def after_request(response):
    """Execute after each request"""
    # Calculate response time
    if hasattr(g, 'start_time'):
        response_time = time.time() - g.start_time
        log_response(response_time)
    
    return response

@app.errorhandler(Exception)
def handle_exception(e):
    """Handle exceptions"""
    # Log error
    log_error(e)
    
    # Return error response
    if isinstance(e, HTTPException):
        return jsonify({
            "error": str(e),
            "status": "error",
            "code": e.code
        }), e.code
    
    return jsonify({
        "error": str(e),
        "status": "error",
        "code": 500
    }), 500

# ===== Routes =====

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.datetime.now().isoformat(),
        "version": "3.0.0"
    })

@app.route('/api/brain', methods=['POST'])
def brain():
    """AI brain endpoint for generating responses"""
    data = request.json
    if not data or 'prompt' not in data:
        return jsonify({"error": "No prompt provided"}), 400
    
    prompt = data['prompt']
    
    # Create AI manager
    ai_manager = AIManager()
    
    # Prepare messages
    messages = [
        {"role": "system", "content": "You are a helpful assistant that provides accurate, informative responses."},
        {"role": "user", "content": prompt}
    ]
    
    # Generate response
    response, provider, status = ai_manager.generate_response(messages)
    
    return jsonify({
        "response": response,
        "model": f"{provider}-model",
        "status": status
    })

@app.route('/api/ai-proxy', methods=['POST'])
def ai_proxy():
    """AI proxy endpoint for generating responses with detailed metadata"""
    data = request.json
    if not data or 'prompt' not in data:
        return jsonify({"error": "No prompt provided"}), 400
    
    prompt = data['prompt']
    
    # Get optional parameters
    temperature = float(data.get('temperature', 0.7))
    max_tokens = int(data.get('max_tokens', 1024))
    system_message = data.get('system_message', "You are a helpful assistant that provides accurate, informative responses.")
    
    # Create AI manager
    ai_manager = AIManager()
    
    # Prepare messages
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
    ]
    
    # Generate response
    response, provider, status = ai_manager.generate_response(messages, temperature, max_tokens)
    
    # Calculate token estimate (rough approximation)
    prompt_tokens = len(prompt) // 4
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
def enterprise_status():
    """Get the status of enterprise features"""
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
    
    return jsonify({
        "enterprise_score": f"{enterprise_count}/{len(enterprise_blueprints)}",
        "cognitive_score": f"{cognitive_count}/{len(cognitive_blueprints)}",
        "system_score": f"{system_count}/{len(system_blueprints)}",
        "overall_score": round(overall_score * 100),
        "license_type": license_type,
        "registered_blueprints": registered_blueprints
    })

@app.route('/api/import-errors', methods=['GET'])
def import_errors():
    """Get blueprint import errors"""
    errors = app.config.get('BLUEPRINT_IMPORT_ERRORS', [])
    error_count = len(errors)
    
    recommendations = []
    if error_count > 0:
        recommendations.append("Ensure blueprint variable names match expected names")
        recommendations.append("Check if blueprint files exist in correct locations")
        recommendations.append("Verify directory structure includes __init__.py files")
    
    return jsonify({
        "error_count": error_count,
        "errors": errors,
        "recommendations": recommendations
    })

@app.route('/api/blueprints', methods=['GET'])
def list_blueprints():
    """List all registered blueprints and their status"""
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
def metrics():
    """Get system metrics"""
    # Calculate average response time
    avg_response_time = sum(system_metrics['response_times']) / len(system_metrics['response_times']) if system_metrics['response_times'] else 0
    
    # Get system info
    system_info = get_system_info()
    
    return jsonify({
        "request_count": system_metrics['request_count'],
        "error_count": system_metrics['error_count'],
        "error_rate": system_metrics['error_count'] / system_metrics['request_count'] if system_metrics['request_count'] else 0,
        "ai_request_count": system_metrics['ai_request_count'],
        "ai_error_count": system_metrics['ai_error_count'],
        "ai_error_rate": system_metrics['ai_error_count'] / system_metrics['ai_request_count'] if system_metrics['ai_request_count'] else 0,
        "blueprint_count": system_metrics['blueprint_count'],
        "avg_response_time": avg_response_time,
        "uptime": (datetime.datetime.now() - system_metrics['startup_time']).total_seconds(),
        "startup_time": system_metrics['startup_time'].isoformat(),
        "system_info": system_info
    })

@app.route('/api/diagnostics', methods=['GET'])
def diagnostics():
    """Get comprehensive system diagnostics"""
    # Get system info
    system_info = get_system_info()
    
    # Get request history
    recent_requests = request_history[-10:] if request_history else []
    
    # Get blueprint info
    registered_blueprints = app.config.get('REGISTERED_BLUEPRINTS', [])
    import_errors = app.config.get('BLUEPRINT_IMPORT_ERRORS', [])
    
    # Get environment variables (filtered for security)
    env_vars = {
        "PORT": os.environ.get("PORT", "Not set"),
        "FLASK_ENV": os.environ.get("FLASK_ENV", "Not set"),
        "FLASK_DEBUG": os.environ.get("FLASK_DEBUG", "Not set"),
        "PYTHONPATH": os.environ.get("PYTHONPATH", "Not set")
    }
    
    # Check for AI providers
    ai_providers = []
    if GROQ_API_KEY:
        ai_providers.append("groq")
    if OPENAI_API_KEY:
        ai_providers.append("openai")
    if ANTHROPIC_API_KEY:
        ai_providers.append("anthropic")
    
    return jsonify({
        "system": system_info,
        "metrics": {
            "request_count": system_metrics['request_count'],
            "error_count": system_metrics['error_count'],
            "ai_request_count": system_metrics['ai_request_count'],
            "ai_error_count": system_metrics['ai_error_count'],
            "blueprint_count": system_metrics['blueprint_count'],
            "uptime": (datetime.datetime.now() - system_metrics['startup_time']).total_seconds(),
        },
        "blueprints": {
            "registered": registered_blueprints,
            "import_errors": import_errors
        },
        "recent_requests": recent_requests,
        "environment": env_vars,
        "ai_providers": ai_providers,
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload a file"""
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
    unique_filename = generate_unique_filename(filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(file_path)
    
    return jsonify({
        "message": "File uploaded successfully",
        "filename": unique_filename,
        "original_filename": filename,
        "path": file_path,
        "size": os.path.getsize(file_path),
        "type": get_file_extension(filename)
    })

@app.route('/api/files/<filename>', methods=['GET'])
def get_file(filename):
    """Get a file"""
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # Check if file exists
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404
    
    # Return file
    return send_file(file_path)

@app.route('/api/files', methods=['GET'])
def list_files():
    """List all files"""
    files = []
    
    # Get all files in upload folder
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Skip directories
        if os.path.isdir(file_path):
            continue
        
        # Get file info
        files.append({
            "filename": filename,
            "path": file_path,
            "size": os.path.getsize(file_path),
            "type": get_file_extension(filename),
            "created": datetime.datetime.fromtimestamp(os.path.getctime(file_path)).isoformat()
        })
    
    return jsonify({
        "files": files,
        "count": len(files),
        "total_size": sum(file["size"] for file in files)
    })

# ===== Main =====

if __name__ == '__main__':
    # Register blueprints
    num_blueprints = register_blueprints(app)
    logger.info(f"Registered {num_blueprints} blueprints")
    
    # Run the app
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting Mythiq Gateway on port {port}")
    app.run(host='0.0.0.0', port=port)
