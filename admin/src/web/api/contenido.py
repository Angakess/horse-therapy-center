from datetime import datetime
from flask import flash, redirect, render_template, request, url_for
from flask import session, abort
from json import dumps
from flask import Blueprint, Response
from core import contenido
from web.helpers.auth import check_permission, is_authenticated
from web.schemas.contenido import contenidos_schema

bprint = Blueprint("contenido_api", __name__, url_prefix="/api/contenido")


@bprint.get("/")
def index():
    """Página principal que muestra la lista de contenidos con paginación, filtro por fechas y autor"""
    try:
        autor = request.args.get("author","")
        fecha_min = request.args.get("published_from", datetime.min)
        fecha_max = request.args.get("published_to", datetime.max)
        page = int(request.args.get("page","1"))
        per_page = int(request.args.get("per_page","10"))

        total = contenido.get_total(
            fecha_min,
            fecha_max,
            autor,
            ["Publicado"]
        )

        contenidos = contenido.list_contenidos_page(
            per_page,
            page,
            fecha_min,
            fecha_max,
            "asc",
            autor,
            ["Publicado"]
        )

        data = contenidos_schema.dump(contenidos)
        
        completo = {
            "data": data,
            "page": page,
            "per_page": per_page,
            "total": total
        }

        return Response(
            dumps(completo),
            mimetype="application/json",
            status=200
        )
    except:
        return Response(
            dumps({"error": "Parámetros inválidos o faltantes en la solicitud."}),
            mimetype="application/json",
            status = 400
        )