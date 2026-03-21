from app.extensions import db


class ContactMessage(db.Model):
    __tablename__ = "contact_messages"

    uid = None

    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(150), nullable=False)

    message = db.Column(db.Text)

    def __repr__(self):
        return f"<ContactMessage {self.email}>"
