import json
from typing import Dict, List, Tuple, Union

from flask import Response, request
from flask_login import login_required

from app.blueprints.api import bp
from app.extensions import db
from app.forms.certificate import AddCertificateForm, UpdateCertificateForm
from app.func import render_td
from app.models.certificate import Certificate
from app.models.permission import Permission
from app.models.user import permission_required
from app.types import ColumnID, ColumnName

cols: List[Tuple[ColumnID, ColumnName]] = [
    (ColumnID("uid"), ColumnName("UID")),
]


@bp.get("/fetch/certificates")
@login_required
@permission_required(Permission.get("FETCH_CERTIFICATES"))
def fetch_certificates() -> Response:
    certificates: List[Certificate] = [
        certificate.to_dict() for certificate in Certificate.query.all()
    ]

    response: Response = Response(
        json.dumps(certificates), headers={"Content-Type": "application/json"}
    )
    response.status_code = 200

    return response


@bp.get("/fetch/rows/certificates")
@login_required
@permission_required(Permission.get("FETCH_CERTIFICATES"))
def fetch_certificates_rows() -> Response:
    certificates: List[Certificate] = Certificate.query.all()

    rows: List[List] = []

    for certificate in certificates:
        row = [render_td(col_id, certificate) for col_id, _ in cols]
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


@bp.get("/fetch/row/certificate/<string:uid>")
@login_required
@permission_required(Permission.get("FETCH_CERTIFICATE"))
def fetch_certificate_row(uid) -> Response:
    response: Response = Response()

    certificate: Union[Certificate, None] = Certificate.query.filter_by(uid=uid).first()

    if certificate:
        response.response = json.dumps(
            {
                key: val
                for key, val in zip(
                    [col_id for col_id, _ in cols],
                    [render_td(col_id, certificate) for col_id, _ in cols],
                )
            }
        )
        response.status_code = 200

    else:
        dct = {
            "message": "Certificate with the given ID was not found :(",
            "category": "error",
        }

        response.response = json.dumps(dct)
        response.status_code = 404

    return response


@bp.get("/fetch/certificate/<string:uid>")
@login_required
@permission_required(Permission.get("FETCH_CERTIFICATE"))
def fetch_certificate(uid) -> Response:
    certificate = Certificate.query.filter_by(uid=uid).first()

    if certificate:
        response: Response = Response(
            json.dumps(certificate.to_dict()),
            status=200,
            headers={"Content-Type": "application/json"},
        )

        return response

    return Response(
        json.dumps(
            {
                "message": "Certificate with the given ID was not found :(",
                "category": "error",
            }
        ),
        headers={"Content-Type": "application/json"},
        status=404,
    )


@bp.post("/update/certificate")
@login_required
@permission_required(
    Permission.get("FETCH_CERTIFICATE") | Permission.get("UPDATE_CERTIFICATE")
)
def update_certificate() -> Response:
    form = UpdateCertificateForm()

    response: Dict = {}

    if form.validate_on_submit():
        certificate: Union[None, Certificate] = Certificate.query.filter_by(
            uid=form.uid.data
        ).scalar()

        if certificate:
            certificate.profile_uid = form.profile_uid.data
            certificate.title = form.title.data
            certificate.description = form.description.data
            certificate.issuer = form.issuer.data
            certificate.issuer_url = form.issuer_url.data
            certificate.credential_id = form.credential_id.data
            certificate.credential_url = form.credential_url.data
            certificate.issue_date = form.issue_date.data
            certificate.verification_code = form.verification_code.data
            certificate.expiration_date = form.expiration_date.data
            certificate.display_order = form.display_order.data
            certificate.is_featured = form.is_featured.data
            certificate.is_public = form.is_public.data
            certificate.file_id = None

            if files := request.form.get("files"):
                try:
                    files = json.loads(files)

                    if file := files.get("file"):
                        if type(file) is list and len(file) == 1:
                            (file_id,) = file
                            certificate.file_id = file_id

                except json.JSONDecodeError as err:
                    print(err)

            db.session.commit()

            response["title"] = "Good job!"
            response["category"] = "success"
            response["message"] = "Certificate updated successfully!"

    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response), headers={"Content-Type": "application/json"}, status=200
    )


@bp.delete("/delete/certificate/<string:uid>")
@login_required
@permission_required(
    Permission.get("FETCH_CERTIFICATE") | Permission.get("DELETE_CERTIFICATE")
)
def delete_certificate(uid):
    response = {}

    if certificate := Certificate.query.filter_by(uid=uid).first():
        db.session.delete(certificate)
        db.session.commit()

        response["title"] = "Deleted!"
        response["message"] = "Certificate deleted successfully"
        response["category"] = "success"
        response["status"] = 200

    else:
        response["title"] = "Error :("
        response["message"] = "Certificate not found"
        response["category"] = "error"
        response["status"] = 404

    return Response(
        json.dumps(response),
        status=response["status"],
        headers={"Content-Type": "application/json"},
    )


@bp.post("/add/certificate")
@login_required
@permission_required(Permission.get("CREATE_CERTIFICATE"))
def add_certificate() -> Response:
    form = AddCertificateForm()

    response: Dict = {}

    if form.validate_on_submit():
        certificate = Certificate()

        certificate.profile_uid = form.profile_uid.data
        certificate.title = form.title.data
        certificate.description = form.description.data
        certificate.issuer = form.issuer.data
        certificate.issuer_url = form.issuer_url.data
        certificate.credential_id = form.credential_id.data
        certificate.credential_url = form.credential_url.data
        certificate.verification_code = form.verification_code.data
        certificate.issue_date = form.issue_date.data
        certificate.expiration_date = form.expiration_date.data
        certificate.display_order = form.display_order.data

        if files := request.form.get("files"):
            try:
                files = json.loads(files)

                if file := files.get("file"):
                    if type(file) is list and len(file) == 1:
                        (file_id,) = file
                        certificate.file_id = file_id

            except json.JSONDecodeError as err:
                print(err)

        db.session.add(certificate)
        db.session.commit()

        response["message"] = "Certificate added successfully"
        response["category"] = "success"
        response["title"] = "Certificate Added"
        response["id"] = getattr(certificate, "uid")

    else:
        response["errors"] = form.errors

    return Response(json.dumps(response))
