import os
import logging
import sys
import json
from flask import Flask, Response

# Configure logging for production observability
# Using stdout for container log collectors (Fluentd/Promtail)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [ %(filename)s:%(lineno)d ] - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.after_request
def add_security_headers(response):
    """Inject security headers into every response."""
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

@app.route("/")
def home():
    return "Welcome to Athiva Hackathon'26!"

@app.route("/health")
def health_check():
    """Endpoint for orchestrator health probes (Kubernetes/AWS)."""
    data = {"status": "healthy", "version": "1.0.0"}
    return Response(json.dumps(data), status=200, mimetype='application/json')

if __name__ == "__main__":
    # Use environment variables for configuration to follow 12-Factor App methodology
    host = os.getenv("APP_HOST", "0.0.0.0")
    
    # Port validation: Must be between 1-65535
    try:
        port_env = os.getenv("APP_PORT", "8080")
        port = int(port_env)
        if not (1 <= port <= 65535):
            raise ValueError(f"Port {port} out of range.")
    except ValueError as e:
        logger.warning(f"Invalid APP_PORT '{os.getenv('APP_PORT')}': {e}. Falling back to 8080.")
        port = 8080

    logger.info(f"Starting application on {host}:{port}")
    logger.warning("PRODUCTION WARNING: Using Flask development server. Use Gunicorn/Waitress in production.")
    
    # debug=False is forced for security; threaded=True handles concurrent health checks better
    app.run(host=host, port=port, debug=False, threaded=True)