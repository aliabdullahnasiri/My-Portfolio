from typing import Dict

from flask import jsonify

from app.blueprints.api import bp
from app.extensions import db
from app.forms.contact import ContactForm
from app.models.contact import ContactMessage


@bp.post("/contact")
def contact():
    form = ContactForm()

    response: Dict = {}

    if form.validate_on_submit():
        m = ContactMessage()

        m.first_name = form.first_name.data
        m.last_name = form.last_name.data
        m.email = form.email.data
        m.message = form.message.data

        db.session.add(m)
        db.session.commit()

        response.update(
            **{
                "category": "success",
                "message": "Message sent successfully",
            }
        )

    else:
        response["errors"] = form.errors

    return jsonify(response)
