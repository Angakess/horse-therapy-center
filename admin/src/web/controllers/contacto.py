from datetime import datetime
from flask import flash, redirect, render_template, request, url_for
from flask import session, abort

from flask import Blueprint

bprint = Blueprint("contacto", __name__, url_prefix="/contacto")

@bprint.get("/")
def index():
    """Página principal que muestra la lista de consultas con paginación, filtro por fechas y estado."""
    
    return render_template("contacto/contacto.html")