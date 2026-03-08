from app.extensions import db


class SocialLink(db.Model):
    __tablename__ = "social_links"

    profile_uid = db.Column(db.String(8), db.ForeignKey("profiles.uid"), nullable=False)

    platform = db.Column(db.String(50), nullable=False)

    url = db.Column(db.String(255), nullable=False)

    icon = db.Column(db.String(100), nullable=True)

    order = db.Column(db.Integer, default=0)

    is_visible = db.Column(db.Boolean, default=True)

    # relationship
    profile = db.relationship(
        "Profile",
        backref=db.backref("social_links", lazy=True, cascade="all, delete-orphan"),
    )
