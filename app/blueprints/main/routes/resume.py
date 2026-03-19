import uuid
from operator import call
from typing import Union

from flask import Response, jsonify, render_template, request
from pdflatex import PDFLaTeX
from sqlalchemy import and_

from app.blueprints.main import bp
from app.models.profile import Profile


@bp.get("/resume")
@bp.get("/resume.pdf")
@bp.get("/<string:profile_uid>/resume")
@bp.get("/<string:profile_uid>/resume.pdf")
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
        case p if p.endswith("/resume.pdf"):
            pdf, *_ = PDFLaTeX.from_binarystring(
                call(
                    getattr(
                        render_template("main/resume.tex", profile=profile), "encode"
                    )
                ),
                f"/tmp/{uuid.uuid4()}",
            ).create_pdf(keep_pdf_file=False, keep_log_file=False)

            return Response(pdf, mimetype="application/pdf")

    return jsonify(profile and profile.to_dict() or {})
