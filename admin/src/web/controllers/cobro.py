from datetime import datetime
from flask import flash, redirect, render_template, request, url_for
from flask import session, abort
from core import equipo, pago, cobro, jya
from flask import Blueprint
from web.helpers.auth import check_permission, is_authenticated

bprint = Blueprint("cobro", __name__, url_prefix="/cobro")


@bprint.get("/")
def index():
    """Página principal que muestra la lista de cobros con paginación, filtro por fechas"""
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "cobro_index"):
        return abort(403)
    amount_per_page = 10
    try:
        page = int(request.args.get("pag", "1"))
        order = request.args.get("order", "desc")

        fecha_min = request.args.get("fechamin", "")

        if fecha_min:
            fecha_min = fecha_min.split(" ")[0]
            fecha_min = datetime.strptime(fecha_min, "%Y-%m-%d")
        else:
            fecha_min = datetime.min

        fecha_max = request.args.get("fechamax", "")
        if fecha_max:
            fecha_max = fecha_max.split(" ")[0]
            fecha_max = datetime.strptime(fecha_max, "%Y-%m-%d")
        else:
            fecha_max = datetime.max

        cobros = cobro.list_cobros_page(
            amount_per_page, page, fecha_min, fecha_max, order
        )
        total = cobro.get_total(fecha_min, fecha_max)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect("/")

    return render_template(
        "cobro/index.html",
        cobros=cobros,
        pag=page,
        page_amount=(total + amount_per_page - 1) // amount_per_page,
        fecha_min=("" if fecha_min == datetime.min else fecha_min),
        fecha_max=("" if fecha_max == datetime.max else fecha_max),
        order=order,
    )


@bprint.get("/<id>")
def get_info(id):
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "cobro_get_info"):
        return abort(403)
    """Muestra la información detallada de un cobro específico."""
    try:
        chosen_cobro = cobro.get_one(id)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("cobro.index"))

    return render_template("cobro/cobro_info.html", info=chosen_cobro)


@bprint.get("<id>/edit")
def enter_edit(id):
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "cobro_enter_edit"):
        return abort(403)
    """Permite editar un cobro existente, cargando los datos actuales del cobro."""
    try:
        chosen_cobro = cobro.get_one(id)

        amount_per_page = 5

        page = int(request.args.get("pag", "1"))

        observaciones = request.args.get("observaciones", chosen_cobro.observaciones)
        monto = request.args.get("monto", chosen_cobro.monto)
        fecha = request.args.get("fecha", chosen_cobro.fecha.strftime("%Y-%m-%d"))
        page_amount = amount_per_page


        empleados = equipo.list_equipos_page(page=page, amount_per_page=amount_per_page)
        total_empleados = equipo.get_total()
        page_amount = (total_empleados + amount_per_page - 1) // amount_per_page

        total_jyas = jya.get_total_jinetes_amazonas()
        page_amount_jya = (total_jyas + amount_per_page - 1) // amount_per_page

        jyas = jya.list_jinetes_amazonas_page(query = "", page=page, amount_per_page=amount_per_page, order = "asc", by = "")
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("cobro.get_one", id=id))

    return render_template(
        "cobro/cobro_editing.html",
        info=chosen_cobro,
        pag=page,
        page_amount=page_amount,
        page_amount_jya=page_amount_jya,
        observaciones=observaciones,
        monto=monto,
        fecha=fecha,
        jyas=jyas,
        empleados=empleados,
    )


@bprint.post("<id>/edit")
def save_edit(id):
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "cobro_save_edit"):
        return abort(403)
    """Guarda los cambios realizados a un cobro existente."""
    try:
        new_data = {
            "observaciones": request.form["observaciones"],
            "monto": request.form["monto"],
            "fecha": request.form["fecha"],
            "jya": jya.get_jinete_amazona(request.form["chosen-jya"]),
            "equipo": equipo.get_one(request.form["chosen-equipo"]),
        }

        edited_cobro = cobro.edit(id, new_data)


    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("cobro.enter_edit", id=id))

    flash("Operación realizada con éxito", "success")
    return render_template("cobro/cobro_info.html", info=edited_cobro)


@bprint.post("/<id>/borrar")
def delete(id):
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "cobro_delete"):
        return abort(403)
    """Elimina un cobro por su ID."""
    try:
        cobro.delete_cobro(id)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("get_info", id=id))

    flash("Cobro borrado con éxito", "success")
    return redirect(url_for("cobro.index"))


@bprint.get("/agregar")
def enter_add():
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "pago_enter_add"):
        return abort(403)
    """Permite agregar un nuevo pago, mostrando un formulario para ingresar los datos."""
    amount_per_page = 5

    page = int(request.args.get("pag", "1"))
    empleados = equipo.list_equipos_page(page=page, amount_per_page=amount_per_page)
    total_empleados = equipo.get_total()
    page_amount = (total_empleados + amount_per_page - 1) // amount_per_page

    desc = request.args.get("desc", "")
    monto = request.args.get("monto", "")
    fecha = request.args.get("fecha", "")
    tipo = request.args.get("tipo", "")

    return render_template(
        "pago/pago_adding.html",
        empleados=empleados,
        pag=page,
        page_amount=page_amount,
        other_page=(True if page > 1 else False),
        desc=desc,
        monto=monto,
        fecha=fecha,
        tipo=tipo,
    )


@bprint.post("/agregar")
def add():
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "pago_add"):
        return abort(403)
    """Crea un nuevo pago basado en los datos ingresados en el formulario."""
    try:
        new_data = {
            "desc": request.form["desc"],
            "monto": request.form["monto"],
            "fecha": request.form["fecha"],
            "tipo": request.form["tipo"],
        }

        new_pago = pago.create_pago(**new_data)

        if new_data["tipo"] == "Honorario":
            try:
                new_person_id = request.form["chosen-beneficiario"]
            except:
                flash("No se seleccionó un beneficiario", "danger")
                return redirect(url_for("pago.enter_edit", id=id))
            new_person = equipo.get_one(new_person_id)
            pago.assign_pago(new_person, new_pago)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("pago.enter_edit", id=id))

    flash("Operación realizada con éxito", "success")
    return render_template("pago/pago_info.html", info=new_pago)

