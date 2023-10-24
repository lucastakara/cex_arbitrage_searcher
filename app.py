from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
from threading import Lock
import time
from cex_arb.arb_searcher import ArbitrageOpportunityFinder

# Setup Flask app and SocketIO
app = Flask(__name__)
socketio = SocketIO(app)
thread = None
thread_lock = Lock()


def background_thread():
    """
    Background thread that checks for new opportunities and emits data.
    """
    arb_searcher = ArbitrageOpportunityFinder()
    while True:
        # Assuming the get_opportunities method fetches new opportunities data
        opportunities = arb_searcher.find_opportunities(1000)
        print(opportunities)
        if opportunities:
            socketio.emit('newdata', {'data': opportunities})
        # Sleep for some time before the next check
        socketio.sleep(10)  # Sleep for 5 seconds (or any other desired interval)


@app.route('/')
def index():
    """
    Serve the index HTML page at the root URL.
    """
    return render_template('opportunity_table.html')  # Assuming your HTML file is named 'index.html'


@socketio.on('connect')
def on_connect():
    """
    Handle client connection and start the background thread if not already running.
    """
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)


# if __name__ == '__main__':
#     if __name__ == "__main__":
#         # '0.0.0.0' makes the server available externally
#         socketio.run(app, host='0.0.0.0', port=5000, debug=True,
#                      allow_unsafe_werkzeug=True)  # Not recommended for production
