from operator import call

from app.extensions import db


class Experience(db.Model):
    __tablename__ = "experiences"

    profile_uid = db.Column(
        db.String(8), db.ForeignKey("profiles.uid"), nullable=False, index=True
    )

    company = db.Column(db.String(150), nullable=False)
    position = db.Column(db.String(150), nullable=False)

    employment_type = db.Column(db.String(50))
    location = db.Column(db.String(120))

    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    is_current = db.Column(db.Boolean, default=False)

    description = db.Column(db.Text)

    company_url = db.Column(db.String(255))

    profile = db.relationship(
        "Profile",
        backref=db.backref("experiences", lazy="dynamic", cascade="all, delete-orphan"),
    )

    def to_dict(self):
        return {
            "profile_uid": self.profile_uid,
            "company": self.company,
            "position": self.position,
            "location": self.location,
            "employment_type": self.employment_type,
            "start_date": call(getattr(self, "display_date"), "start_date", 1),
            "end_date": call(getattr(self, "display_date"), "end_date", 1),
            "is_current": self.is_current,
            "company_url": self.company_url,
            "description": self.description,
            **call(getattr(super(), "to_dict")),
        }

    def __repr__(self):
        return f"<Experience {self.company} - {self.position}>"

    def __str__(self):
        return f"{self.position} at {self.company}"
