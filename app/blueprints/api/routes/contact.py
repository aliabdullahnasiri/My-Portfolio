from typing import Dict

from flask import jsonify

from app.blueprints.api import bp
from app.extensions import db
from app.forms.contact import ContactForm, QuickContactForm
from app.models.contact import ContactMessage
from app.services.notification import create_notification


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


@bp.post("/quick-contact")
def quick_contact():
    form = QuickContactForm()

    response: Dict = {}

    if form.validate_on_submit():
        m = ContactMessage()

        m.email = form.email.data

        db.session.add(m)
        db.session.commit()

        create_notification(f"New message from {m.email}")

        response.update(
            **{
                "category": "success",
                "message": "Message sent successfully",
            }
        )

    else:
        response["errors"] = form.errors

    return jsonify(response)
