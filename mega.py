from flask import Flask, request
from flask_cors import CORS
import pandas as pd
from datetime import datetime
import os
import threading
import time

# 👁️ Face + Phone Detection Function (from yolov1.py)
from yolov1 import run_focusai_combined

# ---------------------- FLASK APP FOR URL LOGGING ---------------------- #

app = Flask(__name__)
CORS(app)

csv_file = "url_log.csv"
if os.path.exists(csv_file):
    url_log = pd.read_csv(csv_file).to_dict(orient='records')
else:
    url_log = []

def classify_url(url):
    distracting = ['youtube', 'facebook', 'netflix', 'instagram', 'twitter', 'reddit']
    productive = ['google', 'gmail', 'stackoverflow', 'wikipedia', 'notion', 'github']

    url = url.lower()
    if any(x in url for x in distracting):
        return 'Distracting'
    elif any(x in url for x in productive):
        return 'Productive'
    else:
        return 'Neutral'

@app.route('/log_url', methods=['POST'])
def log_url():
    data = request.json
    url = data.get('url')
    timestamp = data.get('timestamp', str(datetime.now()))
    category = classify_url(url)

    log_entry = {'url': url, 'timestamp': timestamp, 'category': category}
    url_log.append(log_entry)

    df = pd.DataFrame(url_log)
    df.to_csv(csv_file, index=False)

    print(f"✅ Logged: {url} ({category}) at {timestamp}")
    return "Logged", 200

# ---------------------- THREAD RUNNERS ---------------------- #

def run_flask_server():
    print("🌐 Starting Flask API on http://localhost:5000")
    app.run(debug=False, use_reloader=False)

def run_focusai_vision():
    print("📸 Starting Focus face + phone tracker...")
    run_focusai_combined()

# ---------------------- MASTER ENTRY POINT ---------------------- #

def main():
    print("🚀 Launching Focus Master System...")

    flask_thread = threading.Thread(target=run_flask_server)
    vision_thread = threading.Thread(target=run_focusai_vision)

    flask_thread.start()
    vision_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("❌ Program interrupted by user. Shutting down...")

if __name__ == '__main__':
    main()
