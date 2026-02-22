from flask import jsonify
from flask_login import current_user, login_required, logout_user

from app.blueprints.auth import bp


@bp.get("/logout")
@login_required
def logout():
    username = current_user.user_name
    logout_user()

    return (
        jsonify(
            {
                "success": True,
                "message": f"User {username!r} has been logged out.",
            }
        ),
        200,
    )
