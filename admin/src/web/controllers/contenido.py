from datetime import datetime
from flask import flash, redirect, render_template, request, url_for
from flask import session, abort
from core import contenido
from flask import Blueprint
from web.helpers.auth import check_permission, is_authenticated
from web.controllers import find_user_by_email
import unicodedata

bprint = Blueprint("contenido", __name__, url_prefix="/contenido")


@bprint.get("/")
def index():
    """Página principal que muestra la lista de contenidos con paginación, filtro por fechas"""
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "contenido_index"):
        return abort(403)
    amount_per_page = 10
    try:
        page = int(request.args.get("pag", "1"))
        order = request.args.get("order", "desc")
        estados = request.args.getlist("estado")
        todosLosEstados = contenido.list_estados()

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

        contenidos = contenido.list_contenidos_page(
            amount_per_page, page, fecha_min, fecha_max, order, query, estados
        )
        total = contenido.get_total(fecha_min, fecha_max)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect("/")

    return render_template(
        "contenido/index.html",
        contenidos=contenidos,
        pag=page,
        page_amount=(total + amount_per_page - 1) // amount_per_page,
        fecha_min=("" if fecha_min == datetime.min else fecha_min),
        fecha_max=("" if fecha_max == datetime.max else fecha_max),
        order=order,
        query=query,
        estados=estados,
        todosLosEstados=todosLosEstados,
    )


@bprint.get("/<id>")
def get_info(id):
    """Muestra la información detallada de un contenido específico."""
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "contenido_get_info"):
        return abort(403)
    try:
        chosen_contenido = contenido.get_one(id)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("contenido.index"))

    return render_template("contenido/contenido_info.html", info=chosen_contenido)


@bprint.get("<id>/edit")
def enter_edit(id):
    """Permite editar un contenido existente, cargando los datos actuales del contenido."""
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "contenido_enter_edit"):
        return abort(403)
    try:
        chosen_contenido = contenido.get_one(id)

        amount_per_page = 5

        page = int(request.args.get("pag", "1"))

        titulo = request.args.get("titulo", chosen_contenido.titulo)
        copete = request.args.get("copete", chosen_contenido.copete)
        conteni2 = request.args.get("contenido", chosen_contenido.contenido)
        page_amount = amount_per_page

    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("contenido.get_one", id=id))

    return render_template(
        "contenido/contenido_editing.html",
        info=chosen_contenido,
        pag=page,
        page_amount=page_amount,
        titulo=titulo,
        copete=copete,
        contenido=conteni2,
    )


@bprint.post("<id>/edit")
def save_edit(id):
    """Guarda los cambios realizados a un contenido existente."""
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "contenido_save_edit"):
        return abort(403)
    try:
        titulo = request.form['titulo']
        if len(titulo) > 30:
            flash("El título excede los 30 caracteres", "danger")
            return redirect(url_for("contenido.enter_edit", id=id))
        new_data = {
            "titulo": request.form["titulo"],
            "copete": request.form["copete"],
            "contenido": request.form["contenido"],
        }

        edited_contenido = contenido.edit(id, new_data)

    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("contenido.enter_edit", id=id))

    flash("Operación realizada con éxito", "success")
    return render_template("contenido/contenido_info.html", info=edited_contenido)


@bprint.post("/<id>/borrar")
def delete(id):
    """Elimina un contenido por su ID."""
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "contenido_delete"):
        return abort(403)
    try:
        contenido.delete_contenido(id)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("get_info", id=id))

    flash("Contenido borrado con éxito", "success")
    return redirect(url_for("contenido.index"))


@bprint.get("/agregar")
def enter_add():
    """Permite agregar un nuevo contenido, mostrando un formulario para ingresar los datos."""
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "contenido_enter_add"):
        return abort(403)

    publicarAhora = request.args.get("publicarAhora", "false")
    if publicarAhora == "True":
        publicarAhora = True
    else:
        publicarAhora = False
    titulo = request.args.get("titulo", "")
    copete = request.args.get("copete", "")
    contenido = request.args.get("contenido", "")

    return render_template(
        "contenido/contenido_adding.html",
        titulo=titulo,
        copete=copete,
        contenido=contenido,
        publicarAhora=publicarAhora,
    )


@bprint.post("/agregar")
def add():
    """Crea un nuevo cntenido basado en los datos ingresados en el formulario."""
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "contenido_add"):
        return abort(403)
    try:
        titulo = request.form['titulo']
        if len(titulo) > 30:
            flash("El título excede los 30 caracteres", "danger")
            return redirect(url_for("contenido.enter_add", id=id))
        new_data = {
            "titulo": request.form["titulo"],
            "copete": request.form["copete"],
            "contenido": request.form["contenido"],
            "autor": find_user_by_email(session.get("user"))
        }
        if request.form["publicarAhora"] == "True":
            new_data["fecha_de_publicacion"] = datetime.now()
            new_data["estado"] = contenido.get_one_estado_by_name("Publicado")
        else:
            new_data["estado"] = contenido.get_one_estado_by_name("Borrador")

        new_contenido = contenido.create_contenido(**new_data)

    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("contenido.enter_edit", id=id))

    flash("Operación realizada con éxito", "success")
    return render_template("contenido/contenido_info.html", info=new_contenido)


@bprint.get("/<id>/<estado>")
def set_estado(id, estado):
    """
    Esta función setea el valor de estado del contenido
    con el id pasado por parámetro con el valor del parámetro estado
    (si exste un estado con ese nombre)
    """

    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "contenido_set_estado"):
        return abort(403)

    try:
        if estado == "":
            flash("No se seleccionó un estado", "danger")
            return redirect(url_for("contenido.index"))
        chosen_contenido = contenido.set_estado(id, estado)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("contenido.index"))

    return render_template("contenido/contenido_info.html", info=chosen_contenido)
