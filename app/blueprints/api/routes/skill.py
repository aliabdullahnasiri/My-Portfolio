import json
from typing import Dict, List, Tuple, Union

from flask import Response
from flask_login import login_required

from app.blueprints.api import bp
from app.extensions import db
from app.forms.skill import AddSkillForm, UpdateSkillForm
from app.func import render_td
from app.models.permission import Permission
from app.models.skill import Skill, SkillCategory
from app.models.user import permission_required
from app.types import ColumnID, ColumnName

cols: List[Tuple[ColumnID, ColumnName]] = [
    (ColumnID("uid"), ColumnName("UID")),
]


@bp.get("/fetch/skills")
@login_required
@permission_required(Permission.get("FETCH_SKILLS"))
def fetch_skills() -> Response:
    skills: List[Skill] = [skill.to_dict() for skill in Skill.query.all()]

    response: Response = Response(
        json.dumps(skills), headers={"Content-Type": "application/json"}
    )
    response.status_code = 200

    return response


@bp.get("/fetch/rows/skills")
@login_required
@permission_required(Permission.get("FETCH_SKILLS"))
def fetch_skills_rows() -> Response:
    skills: List[Skill] = Skill.query.all()

    rows: List[List] = []

    for skill in skills:
        row = [render_td(col_id, skill) for col_id, _ in cols]
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


@bp.get("/fetch/row/skill/<string:uid>")
@login_required
@permission_required(Permission.get("FETCH_SKILL"))
def fetch_skill_row(uid) -> Response:
    response: Response = Response()

    skill: Union[Skill, None] = Skill.query.filter_by(uid=uid).first()

    if skill:
        response.response = json.dumps(
            {
                key: val
                for key, val in zip(
                    [col_id for col_id, _ in cols],
                    [render_td(col_id, skill) for col_id, _ in cols],
                )
            }
        )
        response.status_code = 200

    else:
        dct = {
            "message": "Skill with the given ID was not found :(",
            "category": "error",
        }

        response.response = json.dumps(dct)
        response.status_code = 404

    return response


@bp.get("/fetch/skill/<string:uid>")
@login_required
@permission_required(Permission.get("FETCH_SKILL"))
def fetch_skill(uid) -> Response:
    skill = Skill.query.filter_by(uid=uid).first()

    if skill:
        response: Response = Response(
            json.dumps(skill.to_dict()),
            status=200,
            headers={"Content-Type": "application/json"},
        )

        return response

    return Response(
        json.dumps(
            {
                "message": "Skill with the given ID was not found :(",
                "category": "error",
            }
        ),
        headers={"Content-Type": "application/json"},
        status=404,
    )


@bp.post("/update/skill")
@login_required
@permission_required(Permission.get("FETCH_SKILL") | Permission.get("UPDATE_SKILL"))
def update_skill() -> Response:
    form = UpdateSkillForm()

    response: Dict = {}

    if form.validate_on_submit():
        skill = Skill.query.filter_by(uid=form.uid.data).first()

        if skill:
            skill.profile_uid = form.profile_uid.data
            skill.name = form.name.data
            skill.icon = form.icon.data
            skill.level = form.level.data
            skill.description = form.description.data
            skill.display_order = form.display_order.data
            skill.is_visible = form.is_visible.data
            skill.is_featured = form.is_featured.data
            skill.category.name = form.category.data

            db.session.commit()

            response["title"] = "Good job!"
            response["category"] = "success"
            response["message"] = "Skill updated successfully!"

    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response), headers={"Content-Type": "application/json"}, status=200
    )


@bp.delete("/delete/skill/<string:uid>")
@login_required
@permission_required(Permission.get("FETCH_SKILL") | Permission.get("DELETE_SKILL"))
def delete_skill(uid):
    response = {}

    if skill := Skill.query.filter_by(uid=uid).first():
        db.session.delete(skill)
        db.session.commit()

        response["title"] = "Deleted!"
        response["message"] = "Skill deleted successfully"
        response["category"] = "success"
        response["status"] = 200

    else:
        response["title"] = "Error :("
        response["message"] = "Skill not found"
        response["category"] = "error"
        response["status"] = 404

    return Response(
        json.dumps(response),
        status=response["status"],
        headers={"Content-Type": "application/json"},
    )


@bp.post("/add/skill")
@login_required
@permission_required(Permission.get("CREATE_SKILL"))
def add_skill() -> Response:
    form = AddSkillForm()

    response: Dict = {}

    if form.validate_on_submit():
        category = (
            category
            if (
                category := SkillCategory.query.filter_by(
                    name=form.category.data
                ).scalar()
            )
            else SkillCategory()
        )

        if not SkillCategory.query.filter_by(name=form.category.data).count():
            category.name = form.category.data

            db.session.add(category)

        skill = Skill()

        skill.profile_uid = form.profile_uid.data
        skill.name = form.name.data
        skill.icon = form.icon.data
        skill.level = form.level.data
        skill.description = form.description.data
        setattr(skill, "category", category)

        db.session.add(skill)
        db.session.commit()

        response["message"] = "Skill added successfully"
        response["category"] = "success"
        response["title"] = "Skill Added"
        response["id"] = getattr(skill, "uid")

    else:
        response["errors"] = form.errors

    return Response(json.dumps(response))
