from flask import Flask, request
import threading

app = Flask(__name__)
port = 3001

counts = {}

@app.route("/")
def hello_world():
    idempotencyKey = request.headers['idempotency-key']
    count = counts.get(idempotencyKey, 0)

    if count >= 3:
        return "ok"

    counts[idempotencyKey] = count + 1

    return "", 500

class Mock_retry_server:
    def __init__(self):
        self.thread = None
        return
    
    def init(self):
        if self.thread:
            return

        self.thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False))
        self.thread.setDaemon(True)
        self.thread.start()
