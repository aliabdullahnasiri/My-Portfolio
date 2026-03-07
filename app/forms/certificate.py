import json
import re

from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateField,
    FileField,
    HiddenField,
    IntegerField,
    StringField,
    SubmitField,
    TextAreaField,
    ValidationError,
)
from wtforms.validators import URL, DataRequired, Length, Optional

from app.models.profile import Profile


class AddCertificateForm(FlaskForm):

    profile_uid = StringField("Profile UID", validators=[DataRequired()])

    title = StringField("Title", validators=[DataRequired(), Length(max=255)])

    description = TextAreaField("Description", validators=[Optional()])

    issuer = StringField("Issuer", validators=[DataRequired(), Length(max=255)])

    issuer_url = StringField("Issuer Website", validators=[Optional(), URL()])

    credential_id = StringField(
        "Credential ID", validators=[Optional(), Length(max=255)]
    )

    credential_url = StringField("Credential URL", validators=[Optional(), URL()])

    verification_code = StringField(
        "Verification Code", validators=[Optional(), Length(max=255)]
    )

    issue_date = DateField("Issue Date", format="%Y-%m-%d", validators=[Optional()])

    expiration_date = DateField(
        "Expiration Date", format="%Y-%m-%d", validators=[Optional()]
    )

    file = FileField("File")

    display_order = IntegerField("Display Order", validators=[Optional()])

    submit = SubmitField("Add")

    def validate_profile_uid(self, profile_uid):
        pattern: re.Pattern = re.compile(r"^P.\d{6}$")
        if not pattern.search(profile_uid.data):
            raise ValidationError(f"Not a valid Profile UID.")
        elif not Profile.query.filter_by(uid=profile_uid.data).first():
            raise ValidationError("Profile with the given UID was not found :(")


class UpdateCertificateForm(AddCertificateForm):
    uid = HiddenField("UID", validators=[DataRequired()])

    is_featured = BooleanField("Featured")
    is_public = BooleanField("Public")

    submit = SubmitField("Update")
