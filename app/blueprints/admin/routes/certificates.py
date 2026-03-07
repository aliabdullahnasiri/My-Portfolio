from flask import render_template

from app.blueprints.admin import bp
from app.forms.certificate import AddCertificateForm, UpdateCertificateForm
from app.models.user import admin_required


@bp.get("/certificates")
@admin_required
def certificates():
    return render_template(
        "admin/pages/certificates.html",
        title="Certificates",
        form={"a": AddCertificateForm(), "u": UpdateCertificateForm()},
    )
