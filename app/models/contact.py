from sqlalchemy import event

from app.extensions import db
from app.services.notification import create_notification


class ContactMessage(db.Model):
    __tablename__ = "contact_messages"

    uid = None

    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(150), nullable=False)

    message = db.Column(db.Text)

    def __repr__(self):
        return f"<ContactMessage {self.email}>"


@event.listens_for(ContactMessage, "after_insert", propagate=True)
def notify(mapper, connection, target):
    create_notification(f"New message from {target.email}")
