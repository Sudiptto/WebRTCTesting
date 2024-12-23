from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Route to serve the main page
@app.route("/")
def index():
    return render_template("index.html")

# Handle signaling for WebRTC
@socketio.on("offer")
def handle_offer(data):
    emit("offer", data, broadcast=True, include_self=False)

@socketio.on("answer")
def handle_answer(data):
    emit("answer", data, broadcast=True, include_self=False)

@socketio.on("ice-candidate")
def handle_ice_candidate(data):
    emit("ice-candidate", data, broadcast=True, include_self=False)

# Handle text chat messages
@socketio.on("chat")
def handle_chat(data):
    emit("chat", data, broadcast=True, include_self=False)

if __name__ == "__main__":
    # Use 0.0.0.0 to bind to all interfaces in Codespaces
    socketio.run(app, host="0.0.0.0", port=5000)
