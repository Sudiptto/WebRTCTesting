from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Store the current state of the canvas
canvas_state = {
    "elements": [],  # Stores shapes, drawings, or images
    "cursors": {}    # Tracks cursor positions by user
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

# Handle new client connections and send the current canvas state
@socketio.on("connect")
def on_connect():
    emit("init-canvas", canvas_state)

if __name__ == "__main__":
    # Use 0.0.0.0 to bind to all interfaces in Codespaces
    socketio.run(app, host="0.0.0.0", port=5000)
