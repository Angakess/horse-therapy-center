from flask import Blueprint, render_template, request
from src.core.issue import issues

issue_blueprint = Blueprint("issues", __name__, url_prefix="/issues")

@issue_blueprint.route("/")
def issues_index():
    return render_template("issues/index.html", issues=issues)

