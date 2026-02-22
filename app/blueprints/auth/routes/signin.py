from flask import Blueprint, jsonify, url_for
from flask_bcrypt import check_password_hash
from flask_login import login_user
from werkzeug.security import check_password_hash

from app.blueprints.auth import bp
from app.forms.signin import SignInForm
from app.models.user import User


@bp.post("/sign-in")
def sign_in():
    form = SignInForm()

    if not form.validate_on_submit():
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Invalid form data",
                    "errors": form.errors,
                    "category": "error",
                }
            ),
            400,
        )

    user = User.query.filter_by(email=form.email.data).first()

    if not user or not user.check_password(form.password.data):
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Email or password is incorrect",
                    "error_code": "INVALID_CREDENTIALS",
                    "category": "error",
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
                    "is_admin": (is_admin := user.is_administrator()),
                    "category": "success",
                    "redirect": url_for("admin.dashboard" if is_admin else "main.home"),
                },
            }
        ),
        200,
    )
