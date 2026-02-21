from app.blueprints.admin import bp


@bp.get("/")
@bp.get("/dashboard")
def dashboard():
    return "Hello"
