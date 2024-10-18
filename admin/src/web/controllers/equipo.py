from os import fstat
from flask import (
    flash,
    redirect,
    render_template,
    request,
    url_for,
    current_app,
    session,
    abort,
)
from core import equipo
from flask import Blueprint
from src.web.helpers.auth import is_authenticated, check_permission

bprint = Blueprint("equipo", __name__, url_prefix="/equipo")


@bprint.get("/")
def index():
    """if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "list_equipos_page"):
        return abort(403)"""

    """
    Función que muestra la lista paginada de equipos y permite búsqueda.
    Parameters: Ninguno (Los parámetros se obtienen de la query de la URL).
    Returns: Renderiza la plantilla HTML para mostrar la lista de equipos.
    """

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
    """
    Función que activa o desactiva un equipo seleccionado.
    Parameters: Ninguno (Los parámetros se obtienen del formulario).
    Returns: Redirige a la página correspondiente según el origen de la solicitud.
    """
    chosen_id = request.form["id"]
    from_page = request.form["from"]
    try:
        equipo.toggle_a(chosen_id)
        flash("Acción realizada con éxito", "success")
    except ValueError as e:
        flash(str(e), "danger")

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
    """
    Función que muestra el perfil de un equipo por su ID.
    Parameters: id (int), ID del equipo.
    Returns: Renderiza la plantilla HTML del perfil del equipo.
    """
    try:
        chosen_equipo = equipo.get_one(id)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("equipo.index"))

    return render_template(
        "equipo/profile.html", info=chosen_equipo, archivos=chosen_equipo.archivos
    )


@bprint.get("/<id>/edit")
def enter_edit(id):
    """
    Función que muestra el formulario para editar un equipo.
    Parameters: id (int), ID del equipo.
    Returns: Renderiza la plantilla HTML para la edición del equipo.
    """
    try:
        chosen_equipo = equipo.get_one(id)
        return render_template(
            "equipo/profile_editing.html",
            info=chosen_equipo,
            archivos=chosen_equipo.archivos,
        )
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(
            url_for(
                "equipo/profile.html",
                info=chosen_equipo,
                archivos=chosen_equipo.archivos,
            )
        )


@bprint.post("/<id>/edit")
def save_edit(id):
    """
    Función que guarda los cambios realizados en el perfil de un equipo.
    Parameters: id (int), ID del equipo.
    Returns: Redirige a la página de perfil del equipo después de guardar los cambios.
    """
    new_data = {
        "nombre": request.form["nombre"].capitalize(),
        "apellido": request.form["apellido"].capitalize(),
        "dni": request.form["dni"],
        "email": request.form["email"],
        "dir": request.form["domicilio"],
        "localidad": request.form["localidad"].capitalize(),
        "tel": request.form["telefono"],
        "contacto_emergencia_nombre": request.form["emergencia_nombre"].capitalize(),
        "contacto_emergencia_tel": request.form["emergencia_telefono"],
        "profesion": request.form["profesion"],
        "puesto": request.form["puesto"],
        "fecha_inicio": request.form["fecha_inicio"],
        "fecha_fin": request.form["fecha_fin"],
        "obra_social": request.form["obra_social"].capitalize(),
        "num_afiliado": request.form["n_afiliado"],
        "condicion": request.form["condicion"],
    }

    ALLOWED_MIME_TYPES = {"application/pdf", "image/png", "image/jpeg", "text/plain"}

    archivo_subido = request.files["archivos"]

    if archivo_subido:
        if archivo_subido.content_type not in ALLOWED_MIME_TYPES:
            flash(
                "Tipo de archivo no permitido. Solo se permiten PDF, PNG, JPG o TXT.",
                "danger",
            )
            return redirect(url_for("equipo.get_profile", id=id))

        size = fstat(archivo_subido.fileno()).st_size
        if size > 5 * 1024 * 1024:
            flash(
                "El archivo es demasiado grande. El tamaño máximo permitido es 5 MB.",
                "danger",
            )
            return redirect(url_for("equipo.get_profile", id=id))

        try:
            new_archivo = equipo.create_archivo(nombre=archivo_subido.filename)
            chosen_equipo = equipo.get_one(id)
            equipo.assign_archivo(chosen_equipo, new_archivo)

            client = current_app.storage.client
            client.put_object(
                "grupo28",
                f"{new_archivo.id}-{new_archivo.nombre}",
                archivo_subido,
                size,
                content_type=archivo_subido.content_type,
            )
        except ValueError as e:
            flash(str(e), "danger")
            return redirect(url_for("equipo.get_profile", id=id))
    try:
        equipo.edit(id, new_data)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("equipo.get_profile", id=id))

    try:
        client = current_app.storage.client
        archivos_a_eliminar = request.form.getlist("archivos_a_eliminar")
        for archivo_id in archivos_a_eliminar:
            archivo = equipo.get_archivo(
                archivo_id
            )  # Obtener el archivo de la base de datos
            client.remove_object(
                "grupo28", f"/equipo/{archivo.id}-{archivo.nombre}"
            )  # Eliminar de MinIO
            equipo.delete_archivo(archivo_id)  # Eliminar de la base de datos
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("equipo.get_profile", id=id))

    flash("Datos guardados con exito.", "success")
    return redirect(url_for("equipo.get_profile", id=id))


@bprint.get("/agregar")
def enter_add():
    """
    Función que muestra el formulario para agregar un nuevo equipo.
    Returns: Renderiza la plantilla HTML para agregar un equipo.
    """
    return render_template("equipo/add_equipo.html")


@bprint.post("/agregar")
def add_equipo():
    """
    Función que crea un nuevo equipo con los datos proporcionados.
    Parameters: Ninguno (Los datos se obtienen del formulario).
    Returns: Redirige al perfil del equipo creado.
    """
    new_data = {
        "nombre": request.form["nombre"].capitalize(),
        "apellido": request.form["apellido"].capitalize(),
        "dni": request.form["dni"],
        "dir": request.form["domicilio"],
        "email": request.form["email"],
        "localidad": request.form["localidad"].capitalize(),
        "tel": request.form["telefono"],
        "profesion": request.form["profesion"],
        "puesto": request.form["puesto"],
        "fecha_inicio": request.form["fecha_inicio"],
        "fecha_fin": request.form["fecha_fin"],
        "contacto_emergencia_nombre": request.form["emergencia_nombre"].capitalize(),
        "contacto_emergencia_tel": request.form["emergencia_telefono"],
        "obra_social": request.form["obra_social"].capitalize(),
        "num_afiliado": request.form["n_afiliado"],
        "condicion": request.form["condicion"],
        "activo": True,
    }

    try:
        new_equipo = equipo.create_equipo(**new_data)
        flash("Equipo creado con éxito", "success")
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("equipo.get_profile", id=new_equipo.id))


@bprint.get("/<id>/descargar-archivo")
def download_archivo(id):
    """
    Función que permite descargar un archivo asociado a un equipo.
    Parameters: id (int), ID del archivo.
    Returns: Redirige a la URL generada para la descarga del archivo.
    """
    try:
        chosen_archivo = equipo.get_archivo(id)
        client = current_app.storage.client
        minio_url = client.presigned_get_object(
            "grupo28", f"{chosen_archivo.id}-{chosen_archivo.nombre}"
        )
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("equipo.get_profile", id=chosen_archivo.equipo_id))

    return redirect(minio_url)


@bprint.post("/<id>/borrar")
def delete(id):
    """
    Función que elimina un equipo y sus archivos asociados.
    Parameters: id (int), ID del equipo.
    Returns: Redirige a la lista de equipos tras la eliminación.
    """
    try:
        chosen_equipo = equipo.delete_equipo(id)
        archivos_asociados = chosen_equipo.archivos
        client = current_app.storage.client
        for archivo in archivos_asociados:
            client.remove_object("grupo28", f"/equipo/{archivo.id}-{archivo.nombre}")
            equipo.delete_archivo(archivo.id)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("equipo.get_profile", id=id))

    flash("Equipo borrado con éxito", "success")
    return redirect(url_for("equipo.index"))
