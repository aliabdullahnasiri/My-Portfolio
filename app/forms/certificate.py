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

from app.forms import Form


class AddCertificateForm(Form):

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


class UpdateCertificateForm(AddCertificateForm):
    uid = HiddenField("UID", validators=[DataRequired()])

    is_featured = BooleanField("Show this item as Featured")
    is_public = BooleanField("Make this item Publicly Visible")

    submit = SubmitField("Update")
