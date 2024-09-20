from flask import render_template
from src.core import board
from flask import Blueprint

bprint = Blueprint("issues", __name__, url_prefix="/consultas")

@bprint.get("/")
def index():
    issues = board.list_issues()
    return render_template("issues/index.html", issues=issues)