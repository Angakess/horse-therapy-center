from datetime import datetime
from flask import render_template, request
from core import pago
from flask import Blueprint

bprint = Blueprint("pago", __name__, url_prefix="/pago")


@bprint.get("/")
def index():
    amount_per_page = 10

    page = int(request.args.get("pag", "1"))
    order = request.args.get("order", "desc")
    tipos = request.args.getlist("tipo-pago")

    fecha_min = request.args.get("fecha-min", "")
    if fecha_min:
        fecha_min = datetime.strptime(fecha_min, "%Y-%m-%d")
    else:
        fecha_min = datetime.min

    fecha_max = request.args.get("fecha-max", "")
    if fecha_max:
        fecha_max = datetime.strptime(fecha_max, "%Y-%m-%d")
    else:
        fecha_max = datetime.max

    pagos = pago.list_pagos_page(amount_per_page, page, fecha_min, fecha_max, tipos, order)
    total = pago.get_total(fecha_min,fecha_max,tipos)

    return render_template(
        "pago/index.html",
        pagos=pagos,
        pag=page,
        page_amount=(total + amount_per_page - 1) // amount_per_page,
        tipos=tipos,
        fecha_min=("" if fecha_min == datetime.min else fecha_min),
        fecha_max=("" if fecha_max == datetime.max else fecha_max),
        order=order
    )
