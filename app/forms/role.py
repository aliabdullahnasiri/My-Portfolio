from sqlalchemy import and_
from wtforms import (
    BooleanField,
    HiddenField,
    StringField,
    SubmitField,
    TextAreaField,
    ValidationError,
)
from wtforms.validators import DataRequired, Length, Optional

from app.forms import Form
from app.models.role import Role


class AddRoleForm(Form):
    name = StringField("Name", validators=[DataRequired(), Length(max=255)])

    description = TextAreaField(
        "Description", validators=[Optional(), Length(max=2500)]
    )

    default = BooleanField(
        "Default Role (assigned automatically to new users)",
        default=False,
        validators=[Optional()],
    )

    permissions = StringField("Permissions", validators=[Optional()])

    submit = SubmitField("Add Role")


class UpdateRoleForm(AddRoleForm):
    uid = HiddenField("Role UID", validators=[DataRequired()])
    name = StringField("Name", validators=[Optional(), Length(max=255)])

    submit = SubmitField("Update Role")

    def validate_name(self, name):
        if Role.query.filter(
            and_(getattr(Role, "uid") != self.uid.data, Role.name == name.data)
        ).first():
            raise ValidationError("A role with this name already exists.")
