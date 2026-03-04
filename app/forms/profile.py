from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import (
    BooleanField,
    DecimalField,
    FileField,
    HiddenField,
    MultipleFileField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Email, Length, Optional


class AddProfileForm(FlaskForm):
    full_name = StringField("Full Name", validators=[DataRequired(), Length(max=120)])

    headline = StringField(
        "Headline",
        validators=[
            Optional(),
            Length(max=255, message="Headline cannot exceed 255 characters."),
        ],
    )

    bio = TextAreaField(
        "Biography",
        validators=[
            Optional(),
        ],
    )

    short_bio = TextAreaField(
        "Short Biography",
        validators=[
            Optional(),
        ],
    )

    years_of_experience = DecimalField("Years of experience", validators=[Optional()])

    avatar = FileField("Upload profile picture.")

    resume = FileField("Resume")

    public_email = StringField(
        "Public Email",
        validators=[Length(max=255), Email(message="Enter a valid email address")],
    )

    phone = StringField("Phone", validators=[Optional()])

    is_active = BooleanField("Active this profile")

    submit = SubmitField("Add")


class UpdateProfileForm(AddProfileForm):
    uid = HiddenField("UID", validators=[DataRequired()])

    submit = SubmitField("Update")
