from flask import redirect, render_template, request, url_for
from core import equipo
from flask import Blueprint

bprint = Blueprint("equipo", __name__, url_prefix="/equipo")


@bprint.get("/")
def index():
    amount_per_page = 10

    query = request.args.get("query", "")
    order = request.args.get("order", "asc")
    by = request.args.get("by", "")
    page = int(request.args.get("pag", "1"))

    total = equipo.get_total(query)
    equipos = equipo.list_equipos_page(query, page, amount_per_page, order, by)

    return render_template(
        "equipo/index.html",
        equipos=equipos,
        parametro=query,
        order=order,
        by=by,
        pag=page,
        page_amount=(total + amount_per_page - 1) // amount_per_page,
    )


@bprint.post("/toggle-active")
def toggle_activate():
    chosen_id = request.form["id"]
    equipo.toggle_a(chosen_id)

    # guardo todo lo demas para no resetearlo
    query = request.form["query"]
    order = request.form["order"]
    by = request.form["by"]
    page = request.form["pag"]

    return redirect(url_for("equipo.index", query=query, order=order, by=by, pag=page))

@bprint.get("/<id>")
def get_profile(id):
    chosen_equipo = equipo.get_one(id)

    return render_template("equipo/profile.html", info=chosen_equipo)
