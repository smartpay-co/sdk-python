from flask import Flask, request
import threading
import requests

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

@app.post('/seriouslykill')
def seriouslykill():
    func = request.environ.get('werkzeug.server.shutdown')
    
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    
    func()

    return "Shutting down..."

class mock_retry_server:
    def init():
        threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)).start()
        # app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)

    def close():
        requests.post('http://127.0.0.1:%s/seriouslykill' % (port, ))