from flask import render_template

from app.blueprints.admin import bp
from app.forms.skill import AddSkillForm, UpdateSkillForm
from app.models.user import admin_required


@bp.get("/skills")
@admin_required
def skills():
    return render_template(
        "admin/pages/skills.html",
        title="Skills",
        form={"a": AddSkillForm(), "u": UpdateSkillForm()},
    )
