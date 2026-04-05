import os
import logging
from flask import Flask, jsonify

# Configure logging for production observability
# Added process ID (%(process)d) for better traceability in multi-worker environments
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - [PID: %(process)d] - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to Athiva Hackathon'26!"

@app.route("/health")
def health_check():
    """Endpoint for orchestrator health probes (Kubernetes/AWS)."""
    # Using jsonify ensures the correct Content-Type: application/json header
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    # Use environment variables for configuration to follow 12-Factor App methodology
    host = os.getenv("APP_HOST", "0.0.0.0")
    
    # Port must be between 1-65535. Fixed default from 80800 to 8080.
    try:
        port = int(os.getenv("APP_PORT", 8080))
        if not (1 <= port <= 65535):
            raise ValueError("Port out of range")
    except ValueError:
        logger.error("Invalid or out-of-range APP_PORT environment variable. Defaulting to 8080.")
        port = 8080

    logger.info(f"Starting application on {host}:{port}")
    
    # Note: In production, use a WSGI server like Gunicorn or Waitress.
    # The app.run() method is only for local development.
    app.run(host=host, port=port, debug=False, threaded=True)