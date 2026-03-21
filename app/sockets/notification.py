from app.extensions import socketio
from app.models.notification import Notification


@socketio.on("connect")
def handle_connect():
    print("User connected")


def notify_new_message(notification: Notification):
    socketio.emit("new_notification", notification.to_dict())
