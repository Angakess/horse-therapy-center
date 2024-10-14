from flask import flash, redirect, render_template, request, url_for, current_app
from core import ecuestre
from flask import Blueprint

bprint = Blueprint("ecuestre", __name__, url_prefix="/ecuestre")


@bprint.get("/")
def index():
    ecuestres = ecuestre.list_ecuestres()
    return render_template("ecuestre/index.html", ecuestres=ecuestres)
