import pathlib
from datetime import datetime, timezone
from enum import Enum
from operator import call
from typing import Self

import humanize

from app.const import APP_DIR
from app.extensions import db


class FileForEnum(str, Enum):
    AVATAR = "avatar"
    PROJECT_IMAGE = "project_image"
    CERTIFICATE = "certificate"
    BLOG_COVER = "blog_cover"
    REGULAR = "regular"


class File(db.Model):
    __tablename__ = "files"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # File Info
    file_name = db.Column(
        db.String(255),
        nullable=False,
        default=lambda: datetime.now(timezone.utc).date(),
    )
    file_description = db.Column(db.String(255))
    file_for = db.Column(
        db.Enum(FileForEnum), nullable=False, default=FileForEnum.REGULAR
    )
    file_url = db.Column(db.String(255), nullable=False)

    user = db.relationship("User", back_populates="files")

    @property
    def path(self: Self) -> pathlib.Path:
        return pathlib.Path(f"{APP_DIR}/{self.file_url}")

    @property
    def exists(self: Self) -> bool:
        return self.path.exists()

    @property
    def size(self: Self) -> int:
        return self.path.stat().st_size if self.exists else 0

    @property
    def human_size(self: Self) -> str:
        return humanize.naturalsize(self.size) if self.size else "0 B"

    def to_dict(self) -> dict:
        return {
            "file_name": self.file_name,
            "file_description": self.file_description,
            "file_for": self.file_for,
            "file_url": self.file_url,
            "size": self.size,
            "human_size": self.human_size,
            "exists": self.exists,
            **call(getattr(super(), "to_dict")),
        }

    def __repr__(self):
        return f"<File name={self.file_name!r} size={self.human_size!r}>"
