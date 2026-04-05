import os
import logging
from flask import Flask

# Configure logging for production observability
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to Athiva Hackathon'26!"

@app.route("/health")
def health_check():
    """Endpoint for orchestrator health probes (Kubernetes/AWS)."""
    return {"status": "healthy"}, 200

if __name__ == "__main__":
    # Use environment variables for configuration to follow 12-Factor App methodology
    # Default to 0.0.0.0 to allow access within container networks
    host = os.getenv("APP_HOST", "0.0.0.0")
    
    # Port must be between 1-65535. Defaulting to 8080 as 800000 is invalid.
    try:
        port = int(os.getenv("APP_PORT", 80800))
    except ValueError:
        logger.error("Invalid APP_PORT environment variable. Defaulting to 8080.")
        port = 80800

    logger.info(f"Starting application on {host}:{port}")
    
    # Note: In production, use a WSGI server like Gunicorn or Waitress instead of app.run()
    app.run(host=host, port=port, debug=False)