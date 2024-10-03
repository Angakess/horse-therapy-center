from flask import render_template, request
from core import equipo
from flask import Blueprint

bprint = Blueprint("equipo", __name__, url_prefix="/equipo")


@bprint.get("/")
def index():
    equipos = equipo.list_equipos()
    query = request.args.get('query','')
    if query:
        equipos = [
            equipo for equipo in equipos if (
                query.lower() in equipo.nombre.lower() or
                query.lower() in equipo.apellido.lower() or
                query.lower() in str(equipo.dni) or
                query.lower() in equipo.email.lower() or
                query.lower() in equipo.puesto.lower()
            )
        ]

    return render_template("equipo/index.html", equipos=equipos, parametro=query)
