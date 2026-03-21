import json
from typing import Dict, List, Tuple, Union
from urllib.parse import urlparse

import tldextract
from flask import Response, request
from flask_login import current_user, login_required

from app.blueprints.api import bp
from app.extensions import db
from app.forms.profile import AddProfileForm, UpdateProfileForm
from app.func import get_file_url, render_td
from app.models.permission import Permission
from app.models.profile import Profile
from app.models.social_link import SocialLink
from app.models.user import permission_required
from app.types import ColumnID, ColumnName

cols: List[Tuple[ColumnID, ColumnName]] = [
    (ColumnID("uid"), ColumnName("UID")),
    (ColumnID("temp_profile"), ColumnName("Profile")),
    (ColumnID("headline"), ColumnName("Headline")),
    (ColumnID("years_of_experience"), ColumnName("Experience")),
]


@bp.get("/fetch/profiles")
@login_required
@permission_required(Permission.get("FETCH_PROFILES"))
def fetch_profiles() -> Response:
    profiles: List[Profile] = [profile.to_dict() for profile in Profile.query.all()]

    response: Response = Response(
        json.dumps(profiles), headers={"Content-Type": "application/json"}
    )
    response.status_code = 200

    return response


@bp.get("/fetch/rows/profiles")
@login_required
@permission_required(Permission.get("FETCH_PROFILES"))
def fetch_profiles_rows() -> Response:
    profiles: List[Profile] = Profile.query.all()

    rows: List[List] = []

    for profile in profiles:
        row = [render_td(col_id, profile) for col_id, _ in cols]
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


@bp.get("/fetch/row/profile/<string:uid>")
@login_required
@permission_required(Permission.get("FETCH_PROFILE"))
def fetch_profile_row(uid) -> Response:
    response: Response = Response()

    profile: Union[Profile, None] = Profile.query.filter_by(uid=uid).first()

    if profile:
        response.response = json.dumps(
            {
                key: val
                for key, val in zip(
                    [col_id for col_id, _ in cols],
                    [render_td(col_id, profile) for col_id, _ in cols],
                )
            }
        )
        response.status_code = 200

    else:
        dct = {
            "message": "Profile with the given ID was not found :(",
            "category": "error",
        }

        response.response = json.dumps(dct)
        response.status_code = 404

    return response


@bp.get("/fetch/profile/<string:uid>")
@login_required
@permission_required(Permission.get("FETCH_PROFILE"))
def fetch_profile(uid) -> Response:
    profile = Profile.query.filter_by(uid=uid).first()

    if profile:
        response: Response = Response(
            json.dumps(profile.to_dict()),
            status=200,
            headers={"Content-Type": "application/json"},
        )

        return response

    return Response(
        json.dumps(
            {
                "message": "Profile with the given ID was not found :(",
                "category": "error",
            }
        ),
        headers={"Content-Type": "application/json"},
        status=404,
    )


@bp.post("/update/profile")
@login_required
@permission_required(Permission.get("FETCH_PROFILE") | Permission.get("UPDATE_PROFILE"))
def update_profile() -> Response:
    form = UpdateProfileForm()

    response: Dict = {}

    if form.validate_on_submit():
        profile = Profile.query.filter_by(uid=form.uid.data).first()

        if profile:
            profile.headline = form.headline.data
            profile.bio = form.bio.data
            profile.short_bio = form.short_bio.data
            profile.public_email = form.public_email.data
            profile.phone = form.phone.data
            profile.years_of_experience = form.years_of_experience.data
            profile.is_active = form.is_active.data

            if data := form.social_links.data:
                try:
                    links = json.loads(data)

                    for link in profile.social_links.all():
                        if link.url not in links:
                            profile.social_links.remove(link)

                    for link in links:
                        if not SocialLink.query.filter_by(url=link).count():
                            link = urlparse(link)

                            l = SocialLink()
                            l.platform = link.hostname
                            l.url = link.geturl()
                            l.icon = tldextract.extract(l.url).domain

                            profile.social_links.add(l)

                except json.JSONDecodeError as err:
                    print(err)

            if files := request.form.get("files"):
                try:
                    files = json.loads(files)

                    if fid := files.get("avatar"):
                        profile.avatar_url = get_file_url(fid)

                    profile.resume_url = (
                        get_file_url(resume[0])
                        if (resume := files.get("resume"))
                        else None
                    )

                except json.JSONDecodeError as err:
                    print(err)

            db.session.commit()

            response["title"] = "Good job!"
            response["category"] = "success"
            response["message"] = "Profile updated successfully!"

    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response), headers={"Content-Type": "application/json"}, status=200
    )


@bp.delete("/delete/profile/<string:uid>")
@login_required
@permission_required(Permission.get("FETCH_PROFILE") | Permission.get("DELETE_PROFILE"))
def delete_profile(uid):
    response = {}

    if profile := Profile.query.filter_by(uid=uid).first():
        db.session.delete(profile)
        db.session.commit()

        response["title"] = "Deleted!"
        response["message"] = "Profile deleted successfully"
        response["category"] = "success"
        response["status"] = 200

    else:
        response["title"] = "Error :("
        response["message"] = "Profile not found"
        response["category"] = "error"
        response["status"] = 404

    return Response(
        json.dumps(response),
        status=response["status"],
        headers={"Content-Type": "application/json"},
    )


@bp.post("/add/profile")
@login_required
@permission_required(Permission.get("CREATE_PROFILE"))
def add_profile() -> Response:
    form = AddProfileForm()

    response: Dict = {}

    if form.validate_on_submit():
        profile = Profile()

        profile.user_id = current_user.id
        profile.headline = form.headline.data
        profile.bio = form.bio.data
        profile.short_bio = form.short_bio.data
        profile.public_email = form.public_email.data
        profile.phone = form.phone.data
        profile.years_of_experience = form.years_of_experience.data

        profile.is_active = False

        db.session.add(profile)
        db.session.commit()

        response["message"] = "Profile added successfully"
        response["category"] = "success"
        response["title"] = "Profile Added"
        response["id"] = getattr(profile, "uid")

    else:
        response["errors"] = form.errors

    return Response(json.dumps(response))
