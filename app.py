from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to Athiva Hackathon'26!"

if __name__ == "__main__":
            app.run(host="0.0.0.0", port=80000000000)