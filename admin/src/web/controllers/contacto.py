from datetime import datetime
from flask import flash, redirect, render_template, request, url_for
from flask import session, abort

from flask import Blueprint

from core import contacto
from web.helpers.auth import check_permission, is_authenticated

bprint = Blueprint("contacto", __name__, url_prefix="/contacto")

@bprint.get("/")
def index():
    """Página principal que muestra la lista de consultas con paginación, filtro por fechas y estado."""
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "contacto_index"):
        return abort(403)

    amount_per_page = 10
    order = request.args.get("order", "asc")
    page = int(request.args.get("pag", "1"))
    estado = request.args.get('estado', None)



    consultas = contacto.search_consultas(estado=estado, page=page,order=order)


    return render_template("contacto/contacto.html",consultas=consultas,pagination=consultas,pag=page)


@bprint.post("/delete_consulta")
def delete_consulta():
    '''
        Función que elimina fisicamente una consulta de la bd
        Parameters: Ninguno(Depende en los parametros de la query)
        Raise: ValueError propagado por delete_user() 
     '''
    if not is_authenticated(session):
        return abort(401)
    
    if not check_permission(session, "destroy_consulta"):
        return abort(403)
    

    id = request.form.get("id")  
    try:
        contacto.delete_consulta(id) 
        flash("Consulta eliminada correctamente.", "success")  
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for('contacto.index'))

@bprint.get("/<id>/edit")
def enter_edit(id):
    """
    Función que muestra el formulario para editar una consulta.
    Parameters: id (int), ID de la consulta.
    Returns: Renderiza la plantilla HTML para la edición de la consulta.
    """
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "contacto_show"):
        return abort(403)
    try:
        consulta = contacto.get_one(id)
        return render_template(
            "contacto/edit_consulta.html",
            info=consulta,
        )
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(
            url_for(
                "contacto/contacto.html",
                info=consulta,
            )
        )
    
@bprint.get("/<id>")
def get_detail(id):
    """
    Función que muestra el detalle de una consulta por su ID.
    Parameters: id (int), ID de consulta.
    Returns: Renderiza la plantilla HTML del detalle de la consulta.
    """
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "contacto_show"):
        return abort(403)
    try:
        query = contacto.get_one(id)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("contacto.index"))

    return render_template(
        "contacto/save_edit.html", info=query)


@bprint.post("/<id>/edit")
def save_edit(id):
    """
    Función que guarda los cambios realizados en el perfil de una consulta.
    Parameters: id (int), ID de la consulta.
    Returns: Redirige a la página de perfil de la consulta después de guardar los cambios.
    """
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "contacto_update"):
        return abort(403)

    new_data = {
        "estado": request.form["estado"].capitalize(),
        "desc": request.form["desc"].capitalize(),
    }

    try:
        contacto.edit(id, new_data)

    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("contacto.get_detail", id=id)) 

    flash("Datos guardados con éxito.", "success")
    query = contacto.get_one(id)

    return render_template(
        "contacto/edit_consulta.html", info=query) 
