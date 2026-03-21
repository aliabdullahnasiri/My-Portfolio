from app.extensions import socketio


@socketio.on("connect")
def handle_connect():
    print("User connected")


def notify_new_message(message):
    socketio.emit("new_notification", {"text": message})
