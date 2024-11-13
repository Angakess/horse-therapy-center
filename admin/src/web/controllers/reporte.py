from datetime import datetime
from flask import flash, redirect, render_template, request, url_for
from flask import session, abort
from core import equipo, pago
from flask import Blueprint
from web.helpers.auth import check_permission, is_authenticated

bprint = Blueprint("reporte", __name__, url_prefix="/reporte")


@bprint.get("/")
def index():

    return render_template("reportes/index.html")
