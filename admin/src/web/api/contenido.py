from datetime import datetime
from flask import flash, redirect, render_template, request, url_for
from flask import session, abort
from flask import Blueprint
from core import contenido
from web.helpers.auth import check_permission, is_authenticated

bprint = Blueprint("contenido_api", __name__, url_prefix="/api/contenido")


@bprint.get("/")
def index():
    """Página principal que muestra la lista de contenidos con paginación, filtro por fechas"""
    autor = request.args.get("author","")
    fecha_min = request.args.get("published_from", datetime.min)
    fecha_max = request.args.get("published_to", datetime.max)
    page = int(request.args.get("page","1"))
    per_page = int(request.args.get("per_page","10"))

    contenidos = contenido.list_contenidos_page(per_page,page,fecha_min,fecha_max,"asc",autor,["Publicado"])
    data = []
    for conten in contenidos:
        data.append(
            {
                "titulo":conten.titulo,
                "autor":conten.autor.alias,
                "copete":conten.copete,
                "contenido":conten.contenido,
                "fecha de publicacion":conten.fecha_de_publicacion,
            }
        )
    return data, 200