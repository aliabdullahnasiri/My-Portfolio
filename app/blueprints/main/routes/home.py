from typing import List, Tuple

from flask import render_template

from app.blueprints.main import bp
from app.forms.contact import ContactForm, QuickContactForm
from app.models.profile import Profile


@bp.get("/")
@bp.get("/home")
def home():
    profile = (
        Profile.query.filter_by(is_active=True)
        .order_by(getattr(Profile, "updated_at").desc())
        .first()
    )

    nav_links: List[Tuple] = [("Home", "#home"), ("About", "#about")]

    if hasattr(profile, "certificates") and getattr(profile, "certificates").count():
        nav_links.append(("Certifications", "#certifications"))

    if hasattr(profile, "projects") and getattr(profile, "projects").count():
        nav_links.append(("Projects", "#projects"))

    if hasattr(profile, "skills") and getattr(profile, "skills").count():
        nav_links.append(("Skills", "#skills"))

    if hasattr(profile, "education") and getattr(profile, "education").count():
        nav_links.append(("Education", "#education"))

    nav_links.append(("Contact", "#contact"))

    return render_template(
        "main/pages/home.html",
        title="Home",
        enumerate=enumerate,
        profile=profile,
        contact_form=ContactForm(),
        quick_contact_form=QuickContactForm(),
        nav_links=nav_links,
    )
