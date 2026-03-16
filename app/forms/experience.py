from wtforms import (
    BooleanField,
    DateField,
    HiddenField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import URL, DataRequired, Length, Optional

from app.forms import Form


class AddExperienceForm(Form):
    profile_uid = StringField("Profile UID", validators=[DataRequired()])

    company = StringField("Company", validators=[DataRequired(), Length(max=150)])

    position = StringField("Position", validators=[DataRequired(), Length(max=150)])

    employment_type = SelectField(
        "Employment Type",
        choices=[
            ("full_time", "Full Time"),
            ("part_time", "Part Time"),
            ("freelance", "Freelance"),
            ("internship", "Internship"),
            ("contract", "Contract"),
        ],
        validators=[Optional()],
    )

    location = StringField("Location", validators=[Optional(), Length(max=120)])

    company_url = StringField("Company Website", validators=[Optional(), URL()])

    start_date = DateField("Start Date", validators=[Optional()])

    end_date = DateField("End Date", validators=[Optional()])

    is_current = BooleanField("Currently Working Here")

    description = TextAreaField(
        "Responsibilities / Description", validators=[Optional(), Length(max=2000)]
    )

    submit = SubmitField("Add")


class UpdateExperienceForm(AddExperienceForm):
    uid = HiddenField("UID", validators=[DataRequired()])

    submit = SubmitField("Update")
