from operator import call
from typing import Dict

from flask import url_for

from app.const import DEFAULT_AVATAR
from app.extensions import console, db
from app.models.file import File, FileForEnum


class Profile(db.Model):
    __tablename__ = "profiles"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=False,
        index=True,
    )

    full_name = db.Column(
        db.String(120),
        nullable=False,
    )

    headline = db.Column(
        db.String(255),
        nullable=True,
        index=True,
        doc="Short professional title (e.g. Cybersecurity Specialist)",
    )

    bio = db.Column(db.Text, nullable=True, doc="Full professional biography")

    short_bio = db.Column(
        db.String(300), nullable=True, doc="Short bio for cards and previews"
    )

    avatar_url = db.Column(
        db.String(500),
        nullable=True,
    )

    resume_url = db.Column(
        db.String(500),
        nullable=True,
    )

    public_email = db.Column(
        db.String(255),
        nullable=True,
        index=True,
    )

    phone = db.Column(
        db.String(32),
        nullable=True,
    )

    years_of_experience = db.Column(
        db.Integer,
        nullable=True,
    )

    is_active = db.Column(
        db.Boolean,
    )

    user = db.relationship(
        "User",
        back_populates="profiles",
        lazy="joined",
    )

    __table_args__ = (
        db.CheckConstraint(
            "years_of_experience >= 0", name="check_years_of_experience_positive"
        ),
    )

    def to_dict(self) -> Dict:
        dct = {
            "full_name": self.full_name,
            "headline": self.headline,
            "bio": self.bio,
            "short_bio": self.short_bio,
            "public_email": self.public_email,
            "phone": self.phone,
            "years_of_experience": self.years_of_experience,
            "avatar": self.avatar_url or url_for("static", filename=DEFAULT_AVATAR),
            "is_active": bool(self.is_active),
            "resume": [
                self.user.files.filter_by(file_url=self.resume_url).scalar().to_dict()
            ],
            **call(getattr(super(), "to_dict")),
        }
        console.print(dct)

        return dct
