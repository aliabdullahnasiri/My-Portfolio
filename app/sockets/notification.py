from app.extensions import socketio
from app.models.notification import Notification


def notify_new_message(notification: Notification):
    socketio.emit("new_notification", notification.to_dict())
