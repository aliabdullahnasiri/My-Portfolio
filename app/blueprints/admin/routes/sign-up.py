from flask import render_template

from app.blueprints.admin import bp
from app.forms.signup import SignUpForm


@bp.get("/sign-up")
def sign_up():
    return render_template(
        "admin/pages/sign-up.html", title="Sign Up", form=SignUpForm()
    )
