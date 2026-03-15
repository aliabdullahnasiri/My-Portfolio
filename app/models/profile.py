from operator import call
from typing import Dict, Self

from flask import url_for
from sqlalchemy import and_

from app.const import DEFAULT_AVATAR
from app.extensions import db
from app.models.certificate import Certificate
from app.models.project import Project
from app.models.skill import Skill, SkillCategory


class Profile(db.Model):
    __tablename__ = "profiles"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=False,
        index=True,
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
    projects = db.relationship(
        "Project",
        back_populates="profile",
        lazy="dynamic",
    )

    __table_args__ = (
        db.CheckConstraint(
            "years_of_experience >= 0", name="check_years_of_experience_positive"
        ),
    )

    @property
    def display_years_of_experience(self: Self) -> str:
        return f"+{self.years_of_experience:02} years"

    def to_dict(self) -> Dict:
        dct = {
            "headline": self.headline,
            "bio": self.bio,
            "short_bio": self.short_bio,
            "public_email": self.public_email,
            "phone": self.phone,
            "years_of_experience": self.years_of_experience,
            "avatar": self.avatar_url or url_for("static", filename=DEFAULT_AVATAR),
            "is_active": bool(self.is_active),
            "social_links": (
                [link.url for link in getattr(self, "social_links").all()]
                if hasattr(self, "social_links")
                else []
            ),
            "resume": [
                (f := self.user.files.filter_by(file_url=self.resume_url).scalar())
                and f.to_dict()
            ],
            **call(getattr(super(), "to_dict")),
        }

        return dct

    @property
    def skill_categories(self):
        dct = {}

        for uid in list(
            item
            for item, *_ in getattr(self, "skills")
            .with_entities(Skill.category_uid)
            .distinct()
            .all()
        ):
            dct.setdefault(
                SkillCategory.query.filter_by(uid=uid).scalar(),
                getattr(self, "skills")
                .filter(
                    and_(
                        Skill.is_visible == True,
                        Skill.is_featured == True,
                        Skill.category_uid == uid,
                    )
                )
                .order_by(Skill.display_order.asc()),
            )

        return dct

    @property
    def featured_certificates(self: Self):
        return (
            getattr(self, "certificates")
            .filter(
                and_(Certificate.is_public == True, Certificate.is_featured == True)
            )
            .order_by(Certificate.display_order.asc())
        )

    @property
    def featured_projects(self: Self):
        return self.projects.filter(
            and_(Project.is_public == True, Project.is_featured == True)
        ).order_by(Project.display_order.asc())
