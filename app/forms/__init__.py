import json
import re

from flask_wtf import FlaskForm
from wtforms import ValidationError

from app.extensions import db
from app.models.phone import Phone
from app.models.profile import Profile
from app.models.role import Permission, Role
from app.models.user import User


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

    def validate_user_name(self, user_name):
        if User.query.filter_by(user_name=user_name.data).first():
            raise ValidationError("Username already exists.")

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Email already exists.")

    def validate_phones(self, phones):
        nums = json.loads(phones.data)

        for num in nums:
            if (
                db.session.query(Phone)
                .filter(
                    Phone.number == num,
                )
                .first()
            ):

                raise ValidationError(f"Duplicate entry {num!r} for phone number!")

    def validate_roles(self, roles):
        roles = json.loads(roles.data)
        pattern: re.Pattern = re.compile(r"^R.\d{6}$")

        for role in roles:
            if not pattern.search(role):
                raise ValidationError(f"Not a valid Role ID.")
            elif not Role.query.filter_by(uid=role).first():
                raise ValidationError("Role with the given ID was not found :(")
