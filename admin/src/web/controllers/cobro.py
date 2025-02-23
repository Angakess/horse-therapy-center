from datetime import datetime
from flask import flash, redirect, render_template, request, url_for
from flask import session, abort
from core import equipo, pago, cobro, jya
from flask import Blueprint
from web.helpers.auth import check_permission, is_authenticated
import unicodedata

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
        medios = request.args.getlist("medioDePago")
        todosLosMedios = cobro.list_medio_de_pago()

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

        query = request.args.get("query", "")

        cobros = cobro.list_cobros_page(
            amount_per_page, page, fecha_min, fecha_max, order, query, medios
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
        query=query,
        medios=medios,
        todosLosMedios=todosLosMedios,
    )


@bprint.get("/<id>")
def get_info(id):
    """Muestra la información detallada de un cobro específico."""
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "cobro_get_info"):
        return abort(403)
    try:
        chosen_cobro = cobro.get_one(id)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("cobro.index"))

    return render_template("cobro/cobro_info.html", info=chosen_cobro)


@bprint.get("<id>/edit")
def enter_edit(id):
    """Permite editar un cobro existente, cargando los datos actuales del cobro."""
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "cobro_enter_edit"):
        return abort(403)
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
        jyas = jya.list_jinetes_amazonas_page(
            query="", page=page, amount_per_page=amount_per_page, order="asc", by=""
        )

        medios = cobro.list_medio_de_pago()
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
        medios=medios,
    )


@bprint.post("<id>/edit")
def save_edit(id):
    """Guarda los cambios realizados a un cobro existente."""
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "cobro_save_edit"):
        return abort(403)
    try:

        try:
            chosen_medio = request.form["chosen-medio"]
        except:
            flash("No se seleccionó un medio de pago", "danger")
            return redirect(url_for("cobro"))

        new_data = {
            "observaciones": request.form["observaciones"],
            "monto": request.form["monto"],
            "fecha": request.form["fecha"],
            "jya": jya.get_jinete_amazona(request.form["chosen-jya"]),
            "equipo": equipo.get_one(request.form["chosen-equipo"]),
            "medio_pago": cobro.get_one_medio(chosen_medio),
        }

        edited_cobro = cobro.edit(id, new_data)

    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("cobro.enter_edit", id=id))

    flash("Operación realizada con éxito", "success")
    return render_template("cobro/cobro_info.html", info=edited_cobro)


@bprint.post("/<id>/borrar")
def delete(id):
    """Elimina un cobro por su ID."""
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "cobro_delete"):
        return abort(403)
    try:
        cobro.delete_cobro(id)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("get_info", id=id))

    flash("Cobro borrado con éxito", "success")
    return redirect(url_for("cobro.index"))


@bprint.get("/agregar")
def enter_add():
    """Permite agregar un nuevo cobro, mostrando un formulario para ingresar los datos."""
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "cobro_enter_add"):
        return abort(403)

    empleados = equipo.list_equipos_apellido_asc()

    jyas = jya.list_jinetes_amazonas_apellido_asc()

    medios = cobro.list_medio_de_pago()

    observaciones = request.args.get("observaciones", "")
    monto = request.args.get("monto", "")
    fecha = request.args.get("fecha", "")

    return render_template(
        "cobro/cobro_adding.html",
        jyas=jyas,
        empleados=empleados,
        observaciones=observaciones,
        monto=monto,
        fecha=fecha,
        medios=medios,
    )


@bprint.post("/agregar")
def add():
    """Crea un nuevo cobro basado en los datos ingresados en el formulario."""
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "cobro_add"):
        return abort(403)
    try:

        try:
            chosen_jya = request.form["chosen-jya"]
        except:
            flash("No se seleccionó un Jinetes y Amazonas", "danger")
            return redirect(url_for("cobro.enter_add"))
        
        try:
            chosen_equipo = request.form["chosen-equipo"]
        except:
            flash("No se seleccionó un cobrador", "danger")
            return redirect(url_for("cobro.enter_add"))
        
        try:
            chosen_medio = request.form["chosen-medio"]
        except:
            flash("No se seleccionó un medio de pago", "danger")
            return redirect(url_for("cobro.enter_add"))
        

        new_data = {
            "observaciones": request.form["observaciones"],
            "monto": request.form["monto"],
            "fecha": request.form["fecha"],
            "jya": jya.get_jinete_amazona(chosen_jya),
            "equipo": equipo.get_one(chosen_equipo),
            "medio_pago": cobro.get_one_medio(chosen_medio),
        }

        new_cobro = cobro.create_cobro(**new_data)

    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("cobro.enter_edit", id=id))

    flash("Operación realizada con éxito", "success")
    return render_template("cobro/cobro_info.html", info=new_cobro)


@bprint.get("/<id>/<endeudado>")
def set_endeudado(id, endeudado):
    """
    Esta función setea el valor de tiene_deuda del jinete y amazonas
    del cobro con el id pasado por parámetro con el valor del parámetro endeudado
    (solo puede ser booleano)
    """

    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "cobro_set_endeudado"):
        return abort(403)

    try:
        if endeudado == "True":
            endeudado = True
        if endeudado == "False":
            endeudado = False
        chosen_cobro = cobro.get_one(id)
        chosen_jya = jya.set_jinete_amazona_deuda(chosen_cobro.jya.id, endeudado)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("cobro.index"))

    return render_template("cobro/cobro_info.html", info=chosen_cobro)
