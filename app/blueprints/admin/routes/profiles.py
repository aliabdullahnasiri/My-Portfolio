from flask import render_template

from app.blueprints.admin import bp
from app.forms.profile import AddProfileForm, UpdateProfileForm
from app.models.user import admin_required


@bp.get("/profiles")
@admin_required
def profiles():
    return render_template(
        "admin/pages/profiles.html",
        title="Profiles",
        form={"a": AddProfileForm(), "u": UpdateProfileForm()},
    )
