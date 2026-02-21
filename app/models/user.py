from datetime import date
from functools import wraps
from operator import call
from typing import Dict, List, Union

from flask import abort, current_app
from flask_login import AnonymousUserMixin, UserMixin, current_user

from app.extensions import bcrypt, db, login_manager
from app.models.permission import Permission
from app.models.role import Role


class AnonymousUser(AnonymousUserMixin):
    def can(self, _):
        return False

    def is_administrator(self):
        return False


class User(UserMixin, db.Model):
    __tablename__ = "users"

    first_name = db.Column(db.String(50))
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    user_name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)

    password_hash = db.Column(db.String(128), nullable=False)

    birthday = db.Column(db.Date)

    phones = db.relationship(
        "Phone",
        back_populates="user",
        cascade="all, delete, delete-orphan",
        lazy="dynamic",
    )
    files = db.relationship(
        "File",
        back_populates="user",
        cascade="all, delete, delete-orphan",
        lazy="dynamic",
    )
    roles = db.relationship(
        "Role",
        secondary="users_roles",
        backref=db.backref("users", lazy="dynamic"),
        lazy="dynamic",
    )

    @property
    def permissions(self):
        permissions = 0x0001

        for role in self.roles.all():
            permissions |= role.hex_permissions

        return permissions

    def can(self, permissions):
        return (self.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.administer())

    def to_dict(self) -> Dict:
        dct = {
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "user_name": self.user_name,
            "full_name": self.full_name,
            "email": self.email,
            "birthday": self.display_birthday,
            "age": self.age,
            "roles": [r.id for r in self.roles.all()],
            **call(getattr(super(), "to_dict")),
        }

        return dct

    def get_id(self):
        return str(self.__getattribute__("id"))

    def set_password(self, password: str) -> None:
        self.password_hash = bcrypt.generate_password_hash(password).decode()

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.user_name}>"

    @property
    def full_name(self) -> str:
        """Return full name with middle name if exists."""
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name or 'N/A'} {self.last_name or 'N/A'}"

    @property
    def age(self) -> int | None:
        if self.birthday is None:
            return None
        today = date.today()
        return (
            today.year
            - self.birthday.year
            - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
        )

    @property
    def display_birthday(self):
        if self.birthday:
            return self.birthday.strftime("%Y-%m-%d")

        return "N/A"

    def update_roles(self, roles: Union[List[int], None] = None):
        current_roles = {role.id: role for role in self.roles.all()}

        if self.email == current_app.config["FLASKY_ADMIN"]:
            admin_role = Role.administrator()
            if admin_role and admin_role.id not in current_roles:
                self.roles.append(admin_role)

            return

        if roles is None:
            default_role = Role.query.filter_by(default=True).first()
            if default_role and default_role.id not in current_roles:
                self.roles.append(default_role)

            return

        roles_set = set(roles)

        for role_id, role in current_roles.items():
            if role_id not in roles_set:
                self.roles.remove(role)

        existing_ids = set(current_roles.keys())
        for role_id in roles_set:
            if role_id not in existing_ids:
                if role_obj := Role.query.get(role_id):
                    self.roles.append(role_obj)


@login_manager.user_loader
def load_user(id: str):
    return User.query.filter_by(id=id).first()


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)

            return f(*args, **kwargs)

        return decorated_function

    return decorator
