from flask import Blueprint
from flask_bcrypt import check_password_hash
from flask_login import login_user

from app.forms.login import LoginForm
from app.models.user import User

bp = Blueprint("auth", __name__)


from flask import jsonify
from flask_login import login_user
from werkzeug.security import check_password_hash


@bp.post("/login")
def login():
    form = LoginForm()

    if not form.validate_on_submit():
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Invalid form data",
                    "errors": form.errors,
                }
            ),
            400,
        )

    user = User.query.filter_by(email=form.email.data).first()

    if not user or not check_password_hash(user.password_hash, form.password.data):
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Email or password is incorrect",
                    "error_code": "INVALID_CREDENTIALS",
                }
            ),
            401,
        )

    login_user(user, remember=True)

    return (
        jsonify(
            {
                "success": True,
                "message": f"Welcome back, {user.user_name}!",
                "data": {
                    "id": user.id,
                    "username": user.user_name,
                    "email": user.email,
                    "is_admin": user.is_administrator(),
                },
            }
        ),
        200,
    )
