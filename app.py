import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to Athiva Hackathon'26!"

@app.route("/health")
def health_check():
    # Standard health check endpoint for monitoring and orchestration
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    # Use environment variables for configuration to follow 12-factor app methodology
    host = os.getenv("APP_HOST", "0.0.0.0")
    # Port 8000000 was invalid (max 65535). Defaulting to 8080.
    port = int(os.getenv("APP_PORT", 8080))
    
    # debug=False is critical for production security
    app.run(host=host, port=port, debug=False)