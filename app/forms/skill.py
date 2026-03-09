from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    HiddenField,
    IntegerField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class AddSkillForm(FlaskForm):
    name = StringField(
        "Skill Name", validators=[DataRequired(), Length(min=2, max=100)]
    )

    category = StringField(
        "Category", validators=[DataRequired(), Length(min=2, max=100)]
    )

    icon = StringField(
        "Icon Class",
        validators=[Optional(), Length(max=100)],
        description="Example: fa-brands fa-python",
    )

    level = IntegerField(
        "Skill Level (%)",
        validators=[Optional(), NumberRange(min=0, max=100)],
        description="Skill proficiency from 0 to 100",
    )

    description = TextAreaField("Description", validators=[Optional(), Length(max=500)])

    submit = SubmitField("Add")


class UpdateSkillForm(AddSkillForm):
    uid = HiddenField("Skill UID", validators=[DataRequired()])

    is_featured = BooleanField("Featured Skill")

    submit = SubmitField("Update")
