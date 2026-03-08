import datetime
import os
import pathlib
import uuid
from operator import call

from app.const import APP_DIR
from app.extensions import db
from app.func import extract_credential_urls, generate_certificate_preview, is_url_alive


class Certificate(db.Model):
    __tablename__ = "certificates"

    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

    issuer = db.Column(db.String(255), nullable=False)
    issuer_url = db.Column(db.String(255))

    credential_id = db.Column(db.String(255))
    credential_url = db.Column(db.String(500))

    issue_date = db.Column(db.Date)
    expiration_date = db.Column(db.Date)

    verification_code = db.Column(db.String(255))

    profile_uid = db.Column(
        db.String(8), db.ForeignKey("profiles.uid"), nullable=False, index=True
    )
    file_id = db.Column(db.Integer, db.ForeignKey("files.id"))

    profile = db.relationship("Profile", backref="certificates")
    file = db.relationship("File")

    is_featured = db.Column(db.Boolean, default=False)
    is_public = db.Column(db.Boolean, default=True)
    display_order = db.Column(db.Integer, default=0)

    preview_image = db.Column(db.String(255))

    def __repr__(self):
        return f"<Certificate {self.title}>"

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "issuer": self.issuer,
            "issuer_url": self.issuer_url,
            "credential_id": self.credential_id,
            "credential_url": self.credential_url,
            "verification_code": self.verification_code,
            "issue_date": call(getattr(self, "display_date"), "issue_date", 1),
            "expiration_date": call(
                getattr(self, "display_date"), "expiration_date", 1
            ),
            "file_id": self.file_id,
            "profile_uid": self.profile_uid,
            "is_featured": self.is_featured,
            "is_public": self.is_public,
            "display_order": self.display_order,
            "file": [self.file.to_dict() if self.file else None],
            "preview_image_src": self.preview_image_src,
            **call(getattr(super(), "to_dict")),
        }

    @property
    def _credential_url(self):
        if self.credential_url is None and self.file_id and self.file.exists:
            pdf = pathlib.Path(os.path.join(APP_DIR, self.file.file_url.strip(chr(47))))
            if (
                (urls := extract_credential_urls(pdf))
                and (url := urls.pop())
                and is_url_alive(url)
            ):
                self.credential_url = url
                db.session.commit()

        return self.credential_url

    @property
    def preview_image_src(self):
        if self.preview_image is None and self.file_id and self.file.exists:
            dir = pathlib.Path(
                os.path.join(
                    APP_DIR,
                    "static",
                    "uploads",
                    datetime.datetime.now().strftime("%Y-%m-%d"),
                )
            )

            if not dir.exists():
                dir.mkdir()

            output = pathlib.Path(
                os.path.join(
                    dir,
                    f"{uuid.uuid4()}.jpg",
                )
            )

            generate_certificate_preview(
                os.path.join("app", self.file.file_url.strip(chr(47))), output
            )

            self.preview_image = str(output).strip(APP_DIR)

            db.session.commit()

        return self.preview_image
