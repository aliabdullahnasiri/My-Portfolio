from operator import call
from typing import List

from app.extensions import db
from app.models.technology import Technology


class Project(db.Model):
    __tablename__ = "projects"

    # Basic Info
    title = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(180), unique=True, index=True)
    short_description = db.Column(db.String(300))
    description = db.Column(db.Text)

    # Links
    github_url = db.Column(db.String(255))
    demo_url = db.Column(db.String(255))
    documentation_url = db.Column(db.String(255))

    # Project details
    project_type = db.Column(db.String(50))  # web, mobile, tool, script
    status = db.Column(db.String(50))  # completed, ongoing

    # Display settings
    is_featured = db.Column(db.Boolean, default=False)
    is_public = db.Column(db.Boolean, default=True)

    # Sorting
    display_order = db.Column(db.Integer, default=0)

    # Dates
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    # Cover Image
    cover_image_id = db.Column(db.Integer, db.ForeignKey("files.id"))
    profile_uid = db.Column(
        db.String(8), db.ForeignKey("profiles.uid"), nullable=False, index=True
    )

    # Relationships
    cover_image = db.relationship("File", foreign_keys=[cover_image_id])
    profile = db.relationship("Profile", foreign_keys=[profile_uid])
    technologies = db.relationship(
        "Technology",
        secondary="project_technologies",
        backref=db.backref("projects", lazy="dynamic"),
        lazy="dynamic",
    )

    def __repr__(self):
        return f"<Project {self.title}>"

    def __str__(self):
        return self.title

    def to_dict(self):
        return {
            "profile_uid": self.profile_uid,
            "title": self.title,
            "slug": self.slug,
            "short_description": self.short_description,
            "documentation_url": self.documentation_url,
            "description": self.description,
            "github_url": self.github_url,
            "demo_url": self.demo_url,
            "project_type": self.project_type,
            "status": self.status,
            "start_date": call(getattr(self, "display_date"), "start_date", 1),
            "end_date": call(getattr(self, "display_date"), "end_date", 1),
            "is_featured": self.is_featured,
            "is_public": self.is_public,
            "display_order": self.display_order,
            "cover": [self.cover_image.to_dict()] if self.cover_image_id else None,
            "technologies": [t.name for t in self.technologies.all()],
            **call(getattr(super(), "to_dict")),
        }

    def update_technologies(self, technologies: List[str]):
        for technology in self.technologies.all():
            if technology.name not in technologies:
                self.technologies.remove(technology)

        for technology in technologies:
            if not self.technologies.filter_by(name=technology).count():
                self.technologies.append(
                    Technology(**dict(name=technology))
                    if not (
                        project_technology := Technology.query.filter_by(
                            name=technology
                        ).scalar()
                    )
                    else project_technology
                )


class ProjectTechnology(db.Model):
    __tablename__ = "project_technologies"

    uid = None
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))
    technology_id = db.Column(db.Integer, db.ForeignKey("technologies.id"))
