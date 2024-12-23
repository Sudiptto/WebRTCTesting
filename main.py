from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Store the current state of the canvas and participants
canvas_state = {
    "elements": [],  # Stores shapes, drawings, or images
    "cursors": {},   # Tracks cursor positions by user
    "participants": {}  # Tracks participant video streams
}

@app.route("/")
def index():
    return render_template("index.html")

# Handle drawing updates
@socketio.on("update-drawing")
def update_drawing(data):
    canvas_state["elements"].append(data)
    emit("update-drawing", data, broadcast=True, include_self=False)

# Handle cursor updates
@socketio.on("update-cursor")
def update_cursor(data):
    canvas_state["cursors"][data["id"]] = data
    emit("update-cursor", data, broadcast=True, include_self=False)

# Handle video signaling
@socketio.on("offer")
def handle_offer(data):
    emit("offer", data, broadcast=True, include_self=False)

@socketio.on("answer")
def handle_answer(data):
    emit("answer", data, broadcast=True, include_self=False)

@socketio.on("ice-candidate")
def handle_ice_candidate(data):
    emit("ice-candidate", data, broadcast=True, include_self=False)

# Handle participant connection
@socketio.on("participant-joined")
def participant_joined(data):
    canvas_state["participants"][data["id"]] = data
    emit("participant-joined", data, broadcast=True, include_self=False)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
