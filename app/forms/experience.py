from wtforms import HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired

from app.forms import Form


class AddExperienceForm(Form):
    profile_uid = StringField("Profile UID", validators=[DataRequired()])

    submit = SubmitField("Add")


class UpdateExperienceForm(AddExperienceForm):
    uid = HiddenField("UID", validators=[DataRequired()])

    submit = SubmitField("Update")
