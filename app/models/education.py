from operator import call

from app.extensions import db


class Education(db.Model):
    __tablename__ = "educations"

    profile_uid = db.Column(
        db.String(8), db.ForeignKey("profiles.uid"), nullable=False, index=True
    )

    institution = db.Column(db.String(150), nullable=False)
    degree = db.Column(db.String(150), nullable=False)
    field_of_study = db.Column(db.String(150))

    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    description = db.Column(db.Text)

    location = db.Column(db.String(120))

    is_current = db.Column(db.Boolean, default=False)

    profile = db.relationship(
        "Profile",
        backref=db.backref("educations", lazy="dynamic", cascade="all, delete-orphan"),
    )

    def to_dict(self):
        return {
            "profile_uid": self.profile_uid,
            "institution": self.institution,
            "degree": self.degree,
            "field_of_study": self.field_of_study,
            "location": self.location,
            "start_date": call(getattr(self, "display_date"), "start_date", 1),
            "end_date": call(getattr(self, "display_date"), "end_date", 1),
            "is_current": self.is_current,
            "description": self.description,
            **call(getattr(super(), "to_dict")),
        }

    def __repr__(self):
        return f"<Education {self.institution} - {self.degree}>"

    def __str__(self):
        return f"{self.degree} at {self.institution}"
