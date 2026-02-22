from flask import render_template

from app.blueprints.admin import bp
from app.forms.signin import SignInForm


@bp.get("/sign-in")
def sign_in():
    return render_template(
        "admin/pages/sign-in.html", title="Sign In", form=SignInForm()
    )
