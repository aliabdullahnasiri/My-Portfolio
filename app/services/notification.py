from app.extensions import db
from app.models.notification import Notification, NotificationType
from app.sockets.notification import notify_new_message


def create_notification(
    message: str, notif_type: NotificationType = NotificationType.INFO
) -> Notification:
    notification = Notification()

    notification.message = message
    notification.type = notif_type
    notification.is_read = False

    db.session.add(notification)

    notify_new_message(notification)

    return notification
