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
    from_page = request.form["from"]
    equipo.toggle_a(chosen_id)

    if from_page == "profile":
        return redirect(url_for("equipo.get_profile", id=chosen_id))
    else:
        # guardo todo lo demas para no resetearlo
        query = request.form["query"]
        order = request.form["order"]
        by = request.form["by"]
        page = request.form["pag"]

        return redirect(
            url_for("equipo.index", query=query, order=order, by=by, pag=page)
        )


@bprint.get("/<id>")
def get_profile(id):
    chosen_equipo = equipo.get_one(id)

    return render_template("equipo/profile.html", info=chosen_equipo)

@bprint.get("/<id>/edit")
def enter_edit(id):
    chosen_equipo = equipo.get_one(id)

    return render_template("equipo/profile_editing.html", info=chosen_equipo)


@bprint.post("/<id>/edit")
def save_edit(id):
    new_data = {
        "nombre": request.form["nombre"],
        "apellido": request.form["apellido"],
        "dni": request.form["dni"],
        "email": request.form["email"],
        "dir": request.form["domicilio"],
        "localidad": request.form["localidad"],
        "tel": request.form["telefono"],
        "contacto_emergencia_nombre": request.form["emergencia_nombre"],
        "contacto_emergencia_tel": request.form["emergencia_telefono"],
        "profesion": request.form["profesion"],
        "puesto": request.form["puesto"],
        "fecha_inicio": request.form["fecha_inicio"],
        "fecha_fin": request.form["fecha_fin"],
        "obra_social": request.form["obra_social"],
        "num_afiliado": request.form["n_afiliado"],
        "condicion": request.form["condicion"],
    }
    
    equipo.edit(id,new_data)

    return redirect(url_for("equipo.get_profile", id=id))
        