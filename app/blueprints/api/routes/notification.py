import json
from typing import List

from flask import Response
from flask_login import login_required

from app.blueprints.api import bp
from app.models.notification import Notification
from app.models.permission import Permission
from app.models.user import permission_required


@bp.get("/fetch/notifications")
@login_required
@permission_required(Permission.get("FETCH_NOTIFICATIONS"))
def fetch_notifications() -> Response:
    notifications: List[Notification] = [
        notification.to_dict() for notification in Notification.query.all()
    ]

    response: Response = Response(
        json.dumps(notifications), headers={"Content-Type": "application/json"}
    )
    response.status_code = 200

    return response


@bp.get("/fetch/notification/<int:id>")
@login_required
@permission_required(Permission.get("FETCH_NOTIFICATION"))
def fetch_notification(id: int) -> Response:
    notification = Notification.query.get(id)

    if notification:
        response: Response = Response(
            json.dumps(notification.to_dict()),
            status=200,
            headers={"Content-Type": "application/json"},
        )

        return response

    return Response(
        json.dumps(
            {
                "message": "Notification with the given ID was not found :(",
                "category": "error",
            }
        ),
        headers={"Content-Type": "application/json"},
        status=404,
    )
