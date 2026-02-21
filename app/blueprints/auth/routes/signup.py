from flask import jsonify
from sqlalchemy.exc import IntegrityError

from app.blueprints.auth import bp
from app.extensions import db
from app.forms.signup import SignupForm
from app.models.user import User


@bp.post("/signup")
def signup():
    form = SignupForm()

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

    if User.query.filter(
        (User.email == form.email.data) | (User.user_name == form.user_name.data)
    ).count():
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Username or email already exists",
                    "error_code": "USER_ALREADY_EXISTS",
                }
            ),
            409,
        )

    user = User()
    user.user_name = form.user_name.data
    user.email = form.email.data
    user.set_password(form.password.data)
    user.update_roles()

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Database integrity error",
                    "error_code": "DATABASE_ERROR",
                }
            ),
            500,
        )

    return (
        jsonify(
            {
                "success": True,
                "message": "Registration successful",
                "data": {
                    "id": getattr(user, "id"),
                    "username": user.user_name,
                    "email": user.email,
                },
            }
        ),
        201,
    )
