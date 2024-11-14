from datetime import datetime
from flask import flash, redirect, render_template, request, url_for
from flask import session, abort

from flask import Blueprint

from core import contacto
from web.helpers.auth import check_permission, is_authenticated

bprint = Blueprint("contacto", __name__, url_prefix="/contacto")

@bprint.get("/")
def index():
    """Página principal que muestra la lista de consultas con paginación, filtro por fechas y estado."""
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "contacto_index"):
        return abort(403)

    consultas = contacto.list_consultas()

    return render_template("contacto/contacto.html",consultas=consultas)