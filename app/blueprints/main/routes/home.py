from flask import render_template

from app.blueprints.main import bp
from app.models.profile import Profile


@bp.get("/")
@bp.get("/home")
def home():
    return render_template(
        "main/pages/home.html",
        title="Home",
        profile=Profile.query.filter_by(is_active=True)
        .order_by(getattr(Profile, "updated_at").desc())
        .first(),
    )
