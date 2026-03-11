import json
import re

from flask_wtf import FlaskForm
from wtforms import ValidationError

from app.models.profile import Profile
from app.models.role import Permission, Role


class Form(FlaskForm):

    def validate_profile_uid(self, profile_uid):
        pattern: re.Pattern = re.compile(r"^..\d{6}$")
        if not pattern.search(profile_uid.data):
            raise ValidationError(f"Not a valid Profile UID.")
        elif not Profile.query.filter_by(uid=profile_uid.data).first():
            raise ValidationError("Profile with the given UID was not found :(")

    def validate_name(self, name):
        if Role.query.filter_by(name=name.data).first():
            raise ValidationError("A role with this name already exists.")

    def validate_permissions(self, permissions):
        print(self.__class__.__name__)
        permissions = json.loads(permissions.data)
        pattern: re.Pattern = re.compile(r"^P.\d{6}$")

        if any(filter(lambda permission: not pattern.search(permission), permissions)):
            raise ValidationError("Not a valid Permission UID.")

        for permission in permissions:
            if not Permission.query.filter_by(uid=permission).first():
                raise ValidationError("Permission with the given ID was not found :(")
