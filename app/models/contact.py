from app.extensions import db


class ContactMessage(db.Model):
    __tablename__ = "contact_messages"

    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)

    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<ContactMessage {self.email}>"
