from flask import render_template, request
from core import pago
from flask import Blueprint

bprint = Blueprint("pago", __name__, url_prefix="/pago")


@bprint.get("/")
def index():
    amount_per_page = 10

    page = int(request.args.get("pag", "1"))

    pagos = pago.list_pagos_page(amount_per_page, page)
    total = pago.get_total()

    return render_template("pago/index.html", pagos=pagos, pag=page, page_amount=(total + amount_per_page - 1) // amount_per_page,)
