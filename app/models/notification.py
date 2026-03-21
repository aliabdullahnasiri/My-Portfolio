import enum
from operator import call

from app.extensions import db


class NotificationType(enum.Enum):
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


class Notification(db.Model):
    __tablename__ = "notifications"

    uid = None
    message = db.Column(db.String(255))
    type = db.Column(
        db.Enum(NotificationType), default=NotificationType.INFO, nullable=False
    )

    is_read = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "message": self.message,
            "type": self.type.value,
            "is_read": self.is_read,
            **call(getattr(super(), "to_dict")),
        }

    def __repr__(self):
        return f"<Notification type={self.type.value!r} read={self.is_read!r}>"

    def __str__(self):
        return f"[{self.type.value.upper()}] {self.message}"

    def mark_as_read(self):
        self.is_read = True
