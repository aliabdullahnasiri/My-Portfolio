from app.extensions import db


class Certificate(db.Model):
    __tablename__ = "certificates"

    profile_uid = db.Column(
        db.String(8), db.ForeignKey("profiles.uid"), nullable=False, index=True
    )
