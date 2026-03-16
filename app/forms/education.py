from wtforms import (
    BooleanField,
    DateField,
    HiddenField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, Optional

from app.forms import Form


class AddEducationForm(Form):
    profile_uid = StringField("Profile UID", validators=[DataRequired()])

    institution = StringField(
        "Institution", validators=[DataRequired(), Length(max=150)]
    )

    degree = StringField("Degree", validators=[DataRequired(), Length(max=150)])

    field_of_study = StringField(
        "Field of Study", validators=[Optional(), Length(max=150)]
    )

    location = StringField("Location", validators=[Optional(), Length(max=120)])

    start_date = DateField("Start Date", validators=[Optional()])

    end_date = DateField("End Date", validators=[Optional()])

    is_current = BooleanField("Currently Studying")

    description = TextAreaField(
        "Description", validators=[Optional(), Length(max=1000)]
    )

    submit = SubmitField("Add")


class UpdateEducationForm(AddEducationForm):
    uid = HiddenField("UID", validators=[DataRequired()])

    submit = SubmitField("Update")
