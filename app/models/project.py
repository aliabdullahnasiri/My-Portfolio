from operator import call

from app.extensions import db


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
        "ProjectTechnology", back_populates="project", cascade="all, delete-orphan"
    )

    images = db.relationship(
        "ProjectImage", back_populates="project", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Project {self.title}>"

    def __str__(self):
        return self.title

    def to_dict(self):
        return {
            "title": self.title,
            "slug": self.slug,
            "short_description": self.short_description,
            "description": self.description,
            "github_url": self.github_url,
            "demo_url": self.demo_url,
            "status": self.status,
            "is_featured": self.is_featured,
            "is_public": self.is_public,
            "display_order": self.display_order,
            **call(getattr(super(), "to_dict")),
        }


class ProjectTechnology(db.Model):
    __tablename__ = "project_technologies"

    uid = None
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))
    name = db.Column(db.String(100))
    icon = db.Column(db.String(50))

    project = db.relationship("Project", back_populates="technologies")

    def __repr__(self):
        return f"<Tech {self.name}>"

    def to_dict(self):
        return {
            "name": self.name,
            "project_id": self.project_id,
            "icon": self.icon,
            **call(getattr(super(), "to_dict")),
        }


class ProjectImage(db.Model):
    __tablename__ = "project_images"

    uid = None
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))
    file_id = db.Column(db.Integer, db.ForeignKey("files.id"))

    caption = db.Column(db.String(200))
    display_order = db.Column(db.Integer, default=0)

    project = db.relationship("Project", back_populates="images")
    file = db.relationship("File")

    def __repr__(self):
        return f"<ProjectImage {getattr(self, 'id')}>"

    def to_dict(self):

        return {
            "project_id": self.project_id,
            "file_id": self.file_id,
            "caption": self.caption,
            "display_order": self.display_order,
            **call(getattr(super(), "to_dict")),
        }
