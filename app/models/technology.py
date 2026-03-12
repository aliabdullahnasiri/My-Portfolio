from app.extensions import db


class Technology(db.Model):
    __tablename__ = "technologies"

    name = db.Column(db.String(100), nullable=False, unique=True)
    icon = db.Column(db.String(50))
