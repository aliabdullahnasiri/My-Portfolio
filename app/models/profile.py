from sqlalchemy.ext.mutable import MutableDict

from app.extensions import db


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

    social_links = db.Column(MutableDict.as_mutable(db.JSON), default=dict)

    years_of_experience = db.Column(
        db.Integer,
        nullable=True,
    )

    is_active = db.Column(
        db.Boolean,
    )

    is_primary = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
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
