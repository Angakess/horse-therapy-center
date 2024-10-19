from flask import render_template
from core import equipo
from flask import Blueprint
from flask import session, abort
from web.helpers.auth import check_permission, is_authenticated

bprint = Blueprint("issues", __name__, url_prefix="/consultas")

@bprint.get("/")
def index():
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "issues_index"):
        return abort(403)
    issues = equipo.list_issues()
    return render_template("issues/index.html", issues=issues)