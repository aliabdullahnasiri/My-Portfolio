import json
import re

from flask_wtf import FlaskForm
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

from app.models.permission import Permission
from app.models.role import Role


class AddSkillForm(FlaskForm):
    pass


class UpdateSkillForm(FlaskForm):
    pass
