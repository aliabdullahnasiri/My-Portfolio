from operator import call

from app.extensions import db


class Certificate(db.Model):
    __tablename__ = "certificates"

    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

    issuer = db.Column(db.String(255), nullable=False)
    issuer_url = db.Column(db.String(255))

    credential_id = db.Column(db.String(255))
    credential_url = db.Column(db.String(500))

    issue_date = db.Column(db.Date)
    expiration_date = db.Column(db.Date)

    verification_code = db.Column(db.String(255))

    profile_uid = db.Column(
        db.String(8), db.ForeignKey("profiles.uid"), nullable=False, index=True
    )
    file_id = db.Column(db.Integer, db.ForeignKey("files.id"))

    profile = db.relationship("Profile", backref="certificates")
    file = db.relationship("File")

    is_featured = db.Column(db.Boolean, default=False)
    is_public = db.Column(db.Boolean, default=True)
    display_order = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<Certificate {self.title}>"

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "issuer": self.issuer,
            "issuer_url": self.issuer_url,
            "credential_id": self.credential_id,
            "credential_url": self.credential_url,
            "verification_code": self.verification_code,
            "issue_date": call(getattr(self, "display_date"), "issue_date", 1),
            "expiration_date": call(
                getattr(self, "display_date"), "expiration_date", 1
            ),
            "file_id": self.file_id,
            "profile_uid": self.profile_uid,
            "is_featured": self.is_featured,
            "is_public": self.is_public,
            "display_order": self.display_order,
            "file": [self.file.to_dict() if self.file else None],
            **call(getattr(super(), "to_dict")),
        }
