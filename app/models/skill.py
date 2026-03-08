from operator import call

from app.extensions import db


class SkillCategory(db.Model):
    __tablename__ = "skill_categories"

    name = db.Column(db.String(100), nullable=False, unique=True)

    description = db.Column(db.Text, nullable=True)

    icon = db.Column(db.String(100), nullable=True)

    order = db.Column(db.Integer, default=0)

    is_visible = db.Column(db.Boolean, default=True)

    def to_dict(self, include_skills=False):
        data = {
            "name": self.name,
            "description": self.description,
            "icon": self.icon,
            "order": self.order,
            "is_visible": self.is_visible,
            **call(getattr(super(), "to_dict")),
        }

        if include_skills and hasattr(self, "skills"):
            data["skills"] = [
                skill.to_dict() for skill in getattr(self, "skills").all()
            ]

        return data

    def __repr__(self):
        return f"<SkillCategory name='{self.name}'>"

    def __str__(self):
        return self.name


class Skill(db.Model):
    __tablename__ = "skills"

    profile_uid = db.Column(db.String(8), db.ForeignKey("profiles.uid"), nullable=False)
    category_uid = db.Column(
        db.String(8), db.ForeignKey("skill_categories.uid"), nullable=False
    )

    name = db.Column(db.String(100), nullable=False)

    category = db.Column(db.String(100), nullable=True)

    level = db.Column(db.Integer, nullable=False, default=0)

    icon = db.Column(db.String(100), nullable=True)

    order = db.Column(db.Integer, default=0)

    is_visible = db.Column(db.Boolean, default=True)

    profile = db.relationship(
        "Profile",
        backref=db.backref("skills", lazy="dynamic", cascade="all, delete-orphan"),
    )
    category = db.relationship(
        "SkillCategory",
        backref=db.backref("skills", lazy="dynamic", cascade="all, delete-orphan"),
    )

    def to_dict(self, include_category=False):
        data = {
            "name": self.name,
            "level": self.level,
            "icon": self.icon,
            "order": self.order,
            "category_uid": self.category_uid,
            **call(getattr(super(), "to_dict")),
        }

        if include_category and self.category:
            data["category"] = self.category.to_dict()

        return data

    def __repr__(self):
        return f"<Skill name='{self.name}' level={self.level}>"

    def __str__(self):
        return self.name
