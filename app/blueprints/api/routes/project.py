import json
from typing import Dict, List, Tuple, Union

from flask import Response, request
from flask_login import login_required

from app.blueprints.api import bp
from app.extensions import db
from app.forms import profile
from app.forms.project import AddProjectForm, UpdateProjectForm
from app.func import render_td
from app.models.permission import Permission
from app.models.project import Project, ProjectImage
from app.models.user import permission_required
from app.types import ColumnID, ColumnName

cols: List[Tuple[ColumnID, ColumnName]] = [
    (ColumnID("uid"), ColumnName("UID")),
]


@bp.get("/fetch/projects")
@login_required
@permission_required(Permission.get("FETCH_PROJECTS"))
def fetch_projects() -> Response:
    projects: List[Project] = [project.to_dict() for project in Project.query.all()]

    response: Response = Response(
        json.dumps(projects), headers={"Content-Type": "application/json"}
    )
    response.status_code = 200

    return response


@bp.get("/fetch/rows/projects")
@login_required
@permission_required(Permission.get("FETCH_PROJECTS"))
def fetch_projects_rows() -> Response:
    projects: List[Project] = Project.query.all()

    rows: List[List] = []

    for project in projects:
        row = [render_td(col_id, project) for col_id, _ in cols]
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


@bp.get("/fetch/row/project/<string:uid>")
@login_required
@permission_required(Permission.get("FETCH_PROJECT"))
def fetch_project_row(uid) -> Response:
    response: Response = Response()

    project: Union[Project, None] = Project.query.filter_by(uid=uid).first()

    if project:
        response.response = json.dumps(
            {
                key: val
                for key, val in zip(
                    [col_id for col_id, _ in cols],
                    [render_td(col_id, project) for col_id, _ in cols],
                )
            }
        )
        response.status_code = 200

    else:
        dct = {
            "message": "Project with the given ID was not found :(",
            "category": "error",
        }

        response.response = json.dumps(dct)
        response.status_code = 404

    return response


@bp.get("/fetch/project/<string:uid>")
@login_required
@permission_required(Permission.get("FETCH_PROJECT"))
def fetch_project(uid) -> Response:
    project = Project.query.filter_by(uid=uid).first()

    if project:
        response: Response = Response(
            json.dumps(project.to_dict()),
            status=200,
            headers={"Content-Type": "application/json"},
        )

        return response

    return Response(
        json.dumps(
            {
                "message": "Project with the given ID was not found :(",
                "category": "error",
            }
        ),
        headers={"Content-Type": "application/json"},
        status=404,
    )


@bp.post("/update/project")
@login_required
@permission_required(Permission.get("FETCH_PROJECT") | Permission.get("UPDATE_PROJECT"))
def update_project() -> Response:
    form = UpdateProjectForm()

    response: Dict = {}

    if form.validate_on_submit():
        project: Union[None, Project] = Project.query.filter_by(
            uid=form.uid.data
        ).scalar()

        if project:
            db.session.commit()

            response["title"] = "Good job!"
            response["category"] = "success"
            response["message"] = "Project updated successfully!"

    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response), headers={"Content-Type": "application/json"}, status=200
    )


@bp.delete("/delete/project/<string:uid>")
@login_required
@permission_required(Permission.get("FETCH_PROJECT") | Permission.get("DELETE_PROJECT"))
def delete_project(uid):
    response = {}

    if project := Project.query.filter_by(uid=uid).first():
        db.session.delete(project)
        db.session.commit()

        response["title"] = "Deleted!"
        response["message"] = "Project deleted successfully"
        response["category"] = "success"
        response["status"] = 200

    else:
        response["title"] = "Error :("
        response["message"] = "Project not found"
        response["category"] = "error"
        response["status"] = 404

    return Response(
        json.dumps(response),
        status=response["status"],
        headers={"Content-Type": "application/json"},
    )


@bp.post("/add/project")
@login_required
@permission_required(Permission.get("CREATE_PROJECT"))
def add_project() -> Response:
    form = AddProjectForm()

    response: Dict = {}

    if form.validate_on_submit():
        project = Project()

        project.profile_uid = form.profile_uid.data
        project.title = form.title.data
        project.slug = form.slug.data
        project.description = form.description.data
        project.short_description = form.short_description.data
        project.github_url = form.github_url.data
        project.demo_url = form.demo_url.data
        project.documentation_url = form.documentation_url.data
        project.project_type = form.project_type.data
        project.status = form.status.data
        project.display_order = form.display_order.data
        project.status = form.status.data
        project.start_date = form.start_date.data
        project.end_date = form.end_date.data

        db.session.add(project)
        db.session.commit()

        if files := request.form.get("files"):
            try:
                files = json.loads(files)

                for name, ids in files.items():
                    match name:
                        case "cover" if ids:
                            project.cover_image_id = ids.pop()
                        case "images" if ids:
                            for id in ids:
                                pi = ProjectImage()

                                pi.project_id = getattr(project, "id")
                                pi.file_id = id

                                db.session.add(pi)

                print(files)

            except json.JSONDecodeError as err:
                print(err)

        db.session.commit()

        response["message"] = "Project added successfully"
        response["category"] = "success"
        response["title"] = "Project Added"
        response["id"] = getattr(project, "uid")

    else:
        response["errors"] = form.errors

    return Response(json.dumps(response))
