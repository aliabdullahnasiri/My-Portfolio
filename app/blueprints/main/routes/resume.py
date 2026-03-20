from typing import Union

from flask import jsonify, render_template, request
from sqlalchemy import and_

from app.blueprints.main import bp
from app.models.profile import Profile


@bp.get("/resume", endpoint="resume_page")
@bp.get("/resume.pdf", endpoint="resume_pdf")
@bp.get("/<string:profile_uid>/resume", endpoint="profile_resume_page")
@bp.get("/<string:profile_uid>/resume.pdf", endpoint="profile_resume_pdf")
def resume(profile_uid: Union[str, None] = None):
    args = (Profile.is_active == True,)

    if profile_uid is not None:
        args = (*args, getattr(Profile, "uid") == profile_uid)

    profile = (
        Profile.query.filter(and_(*args))
        .order_by(getattr(Profile, "updated_at").desc())
        .first()
    )

    match request.path:
        case p if p.endswith("/resume"):
            return render_template("main/pages/resume.html")

    return jsonify(profile and profile.to_dict() or {})
