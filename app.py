from flask import Flask
import subprocess
import threading
import time
import os
import sys

app = Flask(__name__)

# Path to your script
SCRIPT_PATH = "main.py"

process = None  # store reference to running process


def run_script():
    global process
    # Use Python to run main.py
    process = subprocess.Popen([sys.executable, SCRIPT_PATH])
    process.wait()


@app.route("/")
def home():
    return "✅ Flask server is running. Use /start and /stop to control main.py"


@app.route("/start")
def start_script():
    global process

    # if already running
    if process and process.poll() is None:
        return "⚠️ main.py is already running!"

    thread = threading.Thread(target=run_script, daemon=True)
    thread.start()
    return "✅ main.py script started!"


@app.route("/stop")
def stop_script():
    global process

    if process and process.poll() is None:
        process.terminate()
        return "🛑 main.py script stopped."
    return "⚠️ main.py is not running!"

# Run Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

