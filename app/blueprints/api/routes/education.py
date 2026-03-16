import json
from typing import Dict, List, Tuple, Union

from flask import Response
from flask_login import login_required

from app.blueprints.api import bp
from app.extensions import db
from app.forms.education import AddEducationForm, UpdateEducationForm
from app.func import render_td
from app.models.education import Education
from app.models.permission import Permission
from app.models.user import permission_required
from app.types import ColumnID, ColumnName

cols: List[Tuple[ColumnID, ColumnName]] = [
    (ColumnID("uid"), ColumnName("UID")),
]


@bp.get("/fetch/educations")
@login_required
@permission_required(Permission.get("FETCH_EDUCATIONS"))
def fetch_educations() -> Response:
    educations: List[Education] = [
        education.to_dict() for education in Education.query.all()
    ]

    response: Response = Response(
        json.dumps(educations), headers={"Content-Type": "application/json"}
    )
    response.status_code = 200

    return response


@bp.get("/fetch/rows/educations")
@login_required
@permission_required(Permission.get("FETCH_EDUCATIONS"))
def fetch_educations_rows() -> Response:
    educations: List[Education] = Education.query.all()

    rows: List[List] = []

    for education in educations:
        row = [render_td(col_id, education) for col_id, _ in cols]
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


@bp.get("/fetch/row/education/<string:uid>")
@login_required
@permission_required(Permission.get("FETCH_EDUCATION"))
def fetch_education_row(uid) -> Response:
    response: Response = Response()

    education: Union[Education, None] = Education.query.filter_by(uid=uid).first()

    if education:
        response.response = json.dumps(
            {
                key: val
                for key, val in zip(
                    [col_id for col_id, _ in cols],
                    [render_td(col_id, education) for col_id, _ in cols],
                )
            }
        )
        response.status_code = 200

    else:
        dct = {
            "message": "Education with the given ID was not found :(",
            "category": "error",
        }

        response.response = json.dumps(dct)
        response.status_code = 404

    return response


@bp.get("/fetch/education/<string:uid>")
@login_required
@permission_required(Permission.get("FETCH_EDUCATION"))
def fetch_education(uid) -> Response:
    education = Education.query.filter_by(uid=uid).first()

    if education:
        response: Response = Response(
            json.dumps(education.to_dict()),
            status=200,
            headers={"Content-Type": "application/json"},
        )

        return response

    return Response(
        json.dumps(
            {
                "message": "Education with the given ID was not found :(",
                "category": "error",
            }
        ),
        headers={"Content-Type": "application/json"},
        status=404,
    )


@bp.post("/update/education")
@login_required
@permission_required(
    Permission.get("FETCH_EDUCATION") | Permission.get("UPDATE_EDUCATION")
)
def update_education() -> Response:
    form = UpdateEducationForm()

    response: Dict = {}

    if form.validate_on_submit():
        education: Union[None, Education] = Education.query.filter_by(
            uid=form.uid.data
        ).scalar()

        if education:
            education.profile_uid = form.profile_uid.data
            education.institution = form.institution.data
            education.degree = form.degree.data
            education.field_of_study = form.field_of_study.data
            education.location = form.location.data
            education.start_date = form.start_date.data
            education.end_date = form.end_date.data
            education.is_current = form.is_current.data
            education.description = form.description.data

            db.session.commit()

            response["title"] = "Good job!"
            response["category"] = "success"
            response["message"] = "Education updated successfully!"

    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response), headers={"Content-Type": "application/json"}, status=200
    )


@bp.delete("/delete/education/<string:uid>")
@login_required
@permission_required(
    Permission.get("FETCH_EDUCATION") | Permission.get("DELETE_EDUCATION")
)
def delete_education(uid):
    response = {}

    if education := Education.query.filter_by(uid=uid).first():
        db.session.delete(education)
        db.session.commit()

        response["title"] = "Deleted!"
        response["message"] = "Education deleted successfully"
        response["category"] = "success"
        response["status"] = 200

    else:
        response["title"] = "Error :("
        response["message"] = "Education not found"
        response["category"] = "error"
        response["status"] = 404

    return Response(
        json.dumps(response),
        status=response["status"],
        headers={"Content-Type": "application/json"},
    )


@bp.post("/add/education")
@login_required
@permission_required(Permission.get("CREATE_EDUCATION"))
def add_education() -> Response:
    form = AddEducationForm()

    response: Dict = {}

    if form.validate_on_submit():
        education = Education()

        education.profile_uid = form.profile_uid.data
        education.institution = form.institution.data
        education.degree = form.degree.data
        education.field_of_study = form.field_of_study.data
        education.location = form.location.data
        education.start_date = form.start_date.data
        education.end_date = form.end_date.data
        education.is_current = form.is_current.data
        education.description = form.description.data

        db.session.add(education)
        db.session.commit()

        response["message"] = "Education added successfully"
        response["category"] = "success"
        response["title"] = "Education Added"
        response["id"] = getattr(education, "uid")

    else:
        response["errors"] = form.errors
    print(form.errors)

    return Response(json.dumps(response))
