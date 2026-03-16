import json
from typing import Dict, List, Tuple, Union

from flask import Response
from flask_login import login_required

from app.blueprints.api import bp
from app.extensions import db
from app.forms.experience import AddExperienceForm, UpdateExperienceForm
from app.func import render_td
from app.models.experience import Experience
from app.models.permission import Permission
from app.models.user import permission_required
from app.types import ColumnID, ColumnName

cols: List[Tuple[ColumnID, ColumnName]] = [
    (ColumnID("uid"), ColumnName("UID")),
]


@bp.get("/fetch/experiences")
@login_required
@permission_required(Permission.get("FETCH_EXPERIENCES"))
def fetch_experiences() -> Response:
    experiences: List[Experience] = [
        experience.to_dict() for experience in Experience.query.all()
    ]

    response: Response = Response(
        json.dumps(experiences), headers={"Content-Type": "application/json"}
    )
    response.status_code = 200

    return response


@bp.get("/fetch/rows/experiences")
@login_required
@permission_required(Permission.get("FETCH_EXPERIENCES"))
def fetch_experiences_rows() -> Response:
    experiences: List[Experience] = Experience.query.all()

    rows: List[List] = []

    for experience in experiences:
        row = [render_td(col_id, experience) for col_id, _ in cols]
        rows.append(row)

    dct: Dict = {
        "cols": cols,
        "rows": rows,
    }

    response: Response = Response(
        json.dumps(dct),
        status=200,
        headers={"Content-Type": "application/json"},
    )

    return response


@bp.get("/fetch/row/experience/<string:uid>")
@login_required
@permission_required(Permission.get("FETCH_EXPERIENCE"))
def fetch_experience_row(uid) -> Response:
    response: Response = Response()

    experience: Union[Experience, None] = Experience.query.filter_by(uid=uid).first()

    if experience:
        response.response = json.dumps(
            {
                key: val
                for key, val in zip(
                    [col_id for col_id, _ in cols],
                    [render_td(col_id, experience) for col_id, _ in cols],
                )
            }
        )
        response.status_code = 200

    else:
        dct = {
            "message": "Experience with the given ID was not found :(",
            "category": "error",
        }

        response.response = json.dumps(dct)
        response.status_code = 404

    return response


@bp.get("/fetch/experience/<string:uid>")
@login_required
@permission_required(Permission.get("FETCH_EXPERIENCE"))
def fetch_experience(uid) -> Response:
    experience = Experience.query.filter_by(uid=uid).first()

    if experience:
        response: Response = Response(
            json.dumps(experience.to_dict()),
            status=200,
            headers={"Content-Type": "application/json"},
        )

        return response

    return Response(
        json.dumps(
            {
                "message": "Experience with the given ID was not found :(",
                "category": "error",
            }
        ),
        headers={"Content-Type": "application/json"},
        status=404,
    )


@bp.post("/update/experience")
@login_required
@permission_required(
    Permission.get("FETCH_EXPERIENCE") | Permission.get("UPDATE_EXPERIENCE")
)
def update_experience() -> Response:
    form = UpdateExperienceForm()

    response: Dict = {}

    if form.validate_on_submit():
        experience: Union[None, Experience] = Experience.query.filter_by(
            uid=form.uid.data
        ).scalar()

        if experience:
            experience.profile_uid = form.profile_uid.data
            experience.company = form.company.data
            experience.position = form.position.data
            experience.employment_type = form.employment_type.data
            experience.location = form.location.data
            experience.company_url = form.company_url.data
            experience.start_date = form.start_date.data
            experience.end_date = form.end_date.data
            experience.is_current = form.is_current.data
            experience.description = form.description.data
            db.session.commit()

            response["title"] = "Good job!"
            response["category"] = "success"
            response["message"] = "Experience updated successfully!"

    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response), headers={"Content-Type": "application/json"}, status=200
    )


@bp.delete("/delete/experience/<string:uid>")
@login_required
@permission_required(
    Permission.get("FETCH_EXPERIENCE") | Permission.get("DELETE_EXPERIENCE")
)
def delete_experience(uid):
    response = {}

    if experience := Experience.query.filter_by(uid=uid).first():
        db.session.delete(experience)
        db.session.commit()

        response["title"] = "Deleted!"
        response["message"] = "Experience deleted successfully"
        response["category"] = "success"
        response["status"] = 200

    else:
        response["title"] = "Error :("
        response["message"] = "Experience not found"
        response["category"] = "error"
        response["status"] = 404

    return Response(
        json.dumps(response),
        status=response["status"],
        headers={"Content-Type": "application/json"},
    )


@bp.post("/add/experience")
@login_required
@permission_required(Permission.get("CREATE_EXPERIENCE"))
def add_experience() -> Response:
    form = AddExperienceForm()

    response: Dict = {}

    if form.validate_on_submit():
        experience = Experience()

        experience.profile_uid = form.profile_uid.data
        experience.company = form.company.data
        experience.position = form.position.data
        experience.employment_type = form.employment_type.data
        experience.location = form.location.data
        experience.company_url = form.company_url.data
        experience.start_date = form.start_date.data
        experience.end_date = form.end_date.data
        experience.is_current = form.is_current.data
        experience.description = form.description.data

        db.session.add(experience)
        db.session.commit()

        response["message"] = "Experience added successfully"
        response["category"] = "success"
        response["title"] = "Experience Added"
        response["id"] = getattr(experience, "uid")

    else:
        response["errors"] = form.errors

    return Response(json.dumps(response))
