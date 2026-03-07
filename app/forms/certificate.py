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
)
from wtforms.validators import URL, DataRequired, Length, Optional


class AddCertificateForm(FlaskForm):

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

    is_featured = BooleanField("Featured")
    is_public = BooleanField("Public")

    display_order = IntegerField("Display Order", validators=[Optional()])

    submit = SubmitField("Add")


class UpdateCertificateForm(AddCertificateForm):
    uid = HiddenField("UID", validators=[DataRequired()])
    submit = SubmitField("Update")
