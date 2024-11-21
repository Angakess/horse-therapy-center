from os import fstat
from flask import current_app, redirect, render_template, request, url_for, flash
from core import ecuestre, equipo, jya
from flask import Blueprint

from core.equipo.equipo import Equipo
from core.jya import JinetesAmazonas

from flask import session, abort
from web.helpers.auth import check_permission, is_authenticated

bprint = Blueprint("ecuestre", __name__, url_prefix="/ecuestre")


@bprint.get("/")
def index():
    """
    Función que muestra una lista paginada de ecuestres y permite realizar una búsqueda.
    Returns:
        - Si el usuario no está autenticado o no tiene permiso, aborta con los códigos 401 o 403 respectivamente.
        - Si tiene permisos, renderiza la plantilla 'ecuestre/index.html' mostrando los ecuestres filtrados y paginados.
    """

    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "ecuestre_index"):
        return abort(403)
    amount_per_page = 10
    query = request.args.get("query", "")
    order = request.args.get("order", "asc")
    by = request.args.get("by", "")
    page = int(request.args.get("pag", "1"))
    jya = request.args.get("jya", None)
    total = ecuestre.get_total_ecuestre()
    ecuestres = ecuestre.list_ecuestres_page(
        query, page, amount_per_page, order, by, jya
    )

    return render_template(
        "ecuestre/index.html",
        ecuestres=ecuestres,
        parametro=query,
        order=order,
        by=by,
        pag=page,
        page_amount=(total + amount_per_page - 1) // amount_per_page,
    )


@bprint.get("/<id>")
def get_profile(id):
    """
    Función que muestra el perfil de un ecuestre por su ID.
    Parameters:
        id (int): El ID del ecuestre a mostrar.
    Returns:
        - Si el usuario no está autenticado o no tiene permiso, aborta con los códigos 401 o 403 respectivamente.
        - Si el ecuestre con el ID proporcionado no existe, muestra un mensaje de error y redirige al índice.
        - Si tiene permisos y el ecuestre es válido, renderiza la plantilla 'ecuestre/profile.html' con la información correspondiente.
    """

    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "ecuestre_get_profile"):
        return abort(403)
    try:
        chosen_ecuestre = ecuestre.get_ecuestre(id)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("ecuestre.index"))

    return render_template("ecuestre/profile.html", info=chosen_ecuestre)


@bprint.get("/<id>/edit")
def enter_edit(id):
    """
    Función que permite acceder a la página de edición de un ecuestre.
    Parameters:
        - id (int): ID del ecuestre a editar.
    Returns:
        - Renderiza la plantilla de edición del perfil con los datos del ecuestre seleccionado y las listas
          de equipos y jinetes/amazonas disponibles para su selección.
        - Si el usuario no está autenticado o no tiene permiso, aborta con los códigos 401 o 403 respectivamente.
        - Si ocurre un error al obtener los datos, redirige a la página de perfil con un mensaje de error.
    """

    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "ecuestre_enter_edit"):
        return abort(403)
    equipos = Equipo.query.all()
    jya = JinetesAmazonas.query.all()
    try:
        chosen_ecuestre = ecuestre.get_ecuestre(id)
        return render_template(
            "ecuestre/profile_editing.html",
            info=chosen_ecuestre,
            archivos=chosen_ecuestre.docs,
            equipos=equipos,
            jya=jya,
        )
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(
            url_for(
                "ecuestre/profile.html",
                info=chosen_ecuestre,
                archivos=chosen_ecuestre.docs,
            )
        )


@bprint.post("/<id>/edit")
def save_edit(id):
    """
    Función que guarda los cambios realizados en el perfil de un ecuestre.
    Parameters:
        - id (int): ID del ecuestre a editar.
    Returns:
        - Redirige a la página del perfil del ecuestre editado con un mensaje de éxito si la edición fue exitosa.
        - Si el usuario no está autenticado o no tiene permiso, aborta con los códigos 401 o 403 respectivamente.
        - Si el ecuestre no se encuentra o se produce un error, muestra un mensaje de error y redirige a la página correspondiente.
    """

    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "ecuestre_save_edit"):
        return abort(403)
    ecuestre_modificar = ecuestre.get_ecuestre(id)

    if not ecuestre_modificar:
        flash("Ecuestre no encontrado", "danger")
        return redirect(url_for("ecuestre.index"))

    new_data = {
        "nombre": request.form["nombre"],
        "fecha_nacimiento": request.form["fecha_nacimiento"],
        "sexo": request.form["sexo"],
        "raza": request.form["raza"],
        "pelaje": request.form["pelaje"],
        "tipo_adquisicion": request.form["tipo_adquisicion"],
        "fecha_ingreso": request.form["fecha_ingreso"],
        "sede_asignada": request.form["sede_asignada"],
    }

    try:
        equipos_ids_nuevos = set(request.form.getlist("equipos-asignados"))
        equipos_ids_actuales = {str(equipo.id) for equipo in ecuestre_modificar.equipos}

        equipos_ids_a_eliminar = equipos_ids_actuales - equipos_ids_nuevos
        equipos_ids_a_agregar = equipos_ids_nuevos - equipos_ids_actuales

        # Eliminar relaciones que ya no deberían existir
        for equipo_id in equipos_ids_a_eliminar:
            equipo_a_sacar = equipo.get_one(equipo_id)
            ecuestre.unassing_equipo(ecuestre_modificar, equipo_a_sacar)

        # Agregar nuevas relaciones
        for equipo_id in equipos_ids_a_agregar:
            equipo_asignar = equipo.get_one(equipo_id)
            ecuestre.assing_equipo(ecuestre_modificar, equipo_asignar)

        j_y_a_id = request.form.get("j_y_a_id")
        if j_y_a_id:
            j_y_a_designado = jya.get_jinete_amazona(j_y_a_id)
            if j_y_a_designado:
                ecuestre.assing_j_y_a(ecuestre_modificar, j_y_a_designado)
            else:
                flash("Jinete/Amazona no encontrado", "warning")
    except ValueError as e:
        flash(str(e), "danger")

    try:
        j_y_a_id_a_borrar = request.form.get("j_y_a_id")
        if j_y_a_id_a_borrar:
            j_y_a_designado_borrar = jya.get_jinete_amazona(j_y_a_id_a_borrar)
            if j_y_a_designado_borrar:
                ecuestre.unassing_j_y_a(ecuestre_modificar, j_y_a_designado_borrar)
            else:
                flash("Jinete/Amazona no encontrado", "warning")
    except ValueError as e:
        flash(str(e), "danger")

    ALLOWED_MIME_TYPES = {"application/pdf", "image/png", "image/jpeg", "text/plain"}

    archivo_subido = request.files["archivos_ecuestre"]

    if archivo_subido:
        if archivo_subido.content_type not in ALLOWED_MIME_TYPES:
            flash(
                "Tipo de archivo no permitido. Solo se permiten PDF, PNG, JPG o TXT.",
                "danger",
            )
            return redirect(url_for("ecuestre.get_profile", id=id))

        size = fstat(archivo_subido.fileno()).st_size
        if size > 5 * 1024 * 1024:
            flash(
                "El archivo es demasiado grande. El tamaño máximo permitido es 5 MB.",
                "danger",
            )
            return redirect(url_for("ecuestre.get_profile", id=id))

        try:
            new_archivo = ecuestre.create_archivo(nombre=archivo_subido.filename)
            ecuestre.assign_archivo(ecuestre_modificar, new_archivo)

            client = current_app.storage.client
            client.put_object(
                "grupo28",
                f"/ecuestre/{new_archivo.id}-{new_archivo.nombre}",
                archivo_subido,
                size,
                content_type=archivo_subido.content_type,
            )
        except ValueError as e:
            flash(str(e), "danger")
            return redirect(url_for("ecuestre.get_profile", id=id))
    try:
        ecuestre.edit_ecuestre(id, new_data)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("ecuestre.get_profile", id=id))

    try:
        client = current_app.storage.client
        archivos_a_eliminar = request.form.getlist("archivos_a_eliminar")
        for archivo_id in archivos_a_eliminar:
            archivo = ecuestre.get_archivo(archivo_id)
            client.remove_object("grupo28", f"{archivo.id}-{archivo.nombre}")
            ecuestre.delete_archivo(archivo_id)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("ecuestre.get_profile", id=id))

    flash("Datos guardados con exito.", "success")
    return redirect(url_for("ecuestre.get_profile", id=id))


@bprint.get("/agregar")
def enter_add():
    """
    Función que muestra el formulario para agregar un nuevo ecuestre.
    Parameters: Ninguno.
    Returns:
        - Si el usuario no está autenticado o no tiene permiso, aborta con los códigos 401 o 403 respectivamente.
        - Si tiene permisos, renderiza la plantilla 'ecuestre/add_ecuestre.html' con las listas de equipos y ecuestres.
    """

    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "ecuestre_enter_add"):
        return abort(403)
    equipos = Equipo.query.all()
    jya = JinetesAmazonas.query.all()
    return render_template("ecuestre/add_ecuestre.html", equipos=equipos, jya=jya)


@bprint.post("/agregar")
def add_ecuestre():
    """
    Función para agregar un nuevo ecuestre junto con su equipo y Jinete/Amazona el cual se utilizará su trabajo a posteriori para realizar las busquedas.
    Parameters: Ninguno (Los parámetros se obtienen del formulario de la solicitud POST).
    Returns:
        - Si el usuario no está autenticado o no tiene permiso, aborta con los códigos 401 o 403 respectivamente.
        - Si se crea exitosamente el ecuestre junto con sus relaciones, redirige al perfil del ecuestre con un mensaje de éxito.
        - Si ocurre algún error durante la creación, muestra un mensaje de error y redirige al índice.
    """

    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "ecuestre_add_ecuestre"):
        return abort(403)
    new_data = {
        "nombre": request.form["nombre"],
        "fecha_nacimiento": request.form["fecha_nacimiento"],
        "sexo": request.form["sexo"],
        "raza": request.form["raza"],
        "pelaje": request.form["pelaje"],
        "tipo_adquisicion": request.form["tipo_adquisicion"],
        "fecha_ingreso": request.form["fecha_ingreso"],
        "sede_asignada": request.form["sede_asignada"],
    }

    try:
        new_ecuestre = ecuestre.create_ecuestre(**new_data)

        equipo_id = request.form.get("equipo")
        if equipo_id:
            equipo_designado = equipo.get_one(equipo_id)
            if equipo_designado:
                ecuestre.assing_equipo(new_ecuestre, equipo_designado)

        j_y_a_id = request.form.get("j_y_a")
        if j_y_a_id:
            j_y_a_designado = jya.get_jinete_amazona(j_y_a_id)
            if j_y_a_designado:
                ecuestre.assing_j_y_a(new_ecuestre, j_y_a_designado)

        flash("Ecuestre creado con éxito", "success")
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("ecuestre.get_profile", id=new_ecuestre.id))


@bprint.post("/borrar/<id>")
def delete(id):
    """
    Función para eliminar un ecuestre junto con sus archivos y todas sus asociaciones
    (equipo y jinete/amazona).
    Parameters:
        - id (int): ID del ecuestre a eliminar.
    Returns:
        - Si el usuario no está autenticado o no tiene permiso, aborta con los códigos 401 o 403 respectivamente.
        - Si la eliminación es exitosa, redirige al índice de ecuestres con un mensaje de éxito.
        - Si ocurre un error durante el proceso, redirige al perfil del ecuestre con un mensaje de error.
    """

    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "ecuestre_delete"):
        return abort(403)
    try:
        chosen_ecuestre = ecuestre.get_ecuestre(id)
        archivos_asociados = chosen_ecuestre.docs
        client = current_app.storage.client
        for archivo in archivos_asociados:
            client.remove_object("grupo28", f"{archivo.id}-{archivo.nombre}")
            ecuestre.delete_archivo(archivo.id)

        ecuestre.delete_ecuestre(id)

    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("ecuestre.get_profile", id=id))

    flash("Ecuestre borrado con éxito", "success")
    return redirect(url_for("ecuestre.index"))


@bprint.get("/<id>/descargar-archivo")
def download_archivo(id):
    """
    Función que permite descargar un archivo asociado a un ecuestre.
    Parameters:
        - id (int): ID del archivo a descargar.
    Returns:
        - Redirige a la URL del archivo para su descarga.
        - Si el usuario no está autenticado o no tiene permiso, aborta con los códigos 401 o 403 respectivamente.
        - Si ocurre un error al obtener el archivo, muestra un mensaje de error y redirige a la página del perfil del ecuestre asociado.
    """

    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "ecuestre_download_archivo"):
        return abort(403)
    try:
        chosen_archivo = ecuestre.get_archivo(id)
        client = current_app.storage.client
        minio_url = client.presigned_get_object(
            "grupo28", f"/ecuestre/{chosen_archivo.id}-{chosen_archivo.nombre}"
        )
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("ecuestre.get_profile", id=chosen_archivo.ecuestre_id))

    return redirect(minio_url)


@bprint.get("/<id>/documentos")
def enter_docs(id):
    """
    Función que permite acceder a los documentos asociados a un ecuestre.
    Parameters:
        - id (int): ID del ecuestre.
    Returns:
        - Renderiza la plantilla de documentos del perfil del ecuestre.
        - Si el usuario no está autenticado o no tiene permiso, aborta con los códigos 401 o 403 respectivamente.
        - Si ocurre un error al obtener los documentos, muestra un mensaje de error y redirige a la página del perfil del ecuestre asociado.
    """

    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "ecuestre_enter_docs"):
        return abort(403)
    try:
        amount_per_page = 5

        pag = int(request.args.get("pag", 1))
        query = request.args.get("query", "")
        order = request.args.get("order", "asc")
        tipos = request.args.getlist("tipoarchivo")
        by = request.args.get("by", "")

        total = ecuestre.get_total_docs(id, query, tipos)

        chosen_ecuestre = ecuestre.get_ecuestre(id)

        archivos = ecuestre.list_archivos_page(
            id,
            query,
            order,
            tipos,
            by,
            pag,
            amount_per_page,
        )

        return render_template(
            "ecuestre/profile_docs.html",
            info=chosen_ecuestre,
            archivos=archivos,
            by=by,
            tipos=tipos,
            order=order,
            query=query,
            pag=pag,
            page_amount=(total + amount_per_page - 1) // amount_per_page,
        )
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(
            url_for(
                "ecuestre/profile.html",
                info=chosen_ecuestre,
                archivos=chosen_ecuestre.docs,
            )
        )


@bprint.post("/<id>/agregar-archivo")
def add_archivo(id):
    """
    Función que permite agregar un archivo asociado a un ecuestre.
    Parameters:
        - id (int): ID del ecuestre.
    Returns:
        - Redirige a la página de documentos del ecuestre.
        - Si el usuario no está autenticado o no tiene permiso, aborta con los códigos 401 o 403 respectivamente.
        - Si se produce un error al cargar el archivo, muestra un mensaje de error.
    """

    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "ecuestre_add_archivo"):
        return abort(403)
    try:

        ecuestre_modificar = ecuestre.get_ecuestre(id)

        ALLOWED_MIME_TYPES = {
            "application/pdf",
            "image/png",
            "image/jpeg",
            "text/plain",
            "application/vnd.ms-excel",
            "application/msword",
        }

        archivo_subido = request.files["archivos_Ecuestre"]
        archivo_tipo = request.form["tipo"]

        if not archivo_subido or not archivo_tipo:
            flash("Debe ingresar un archivo y seleccionar un tipo.", "error")
            return redirect(url_for("ecuestre.enter_docs", id=id))

        if archivo_subido:
            if archivo_subido.content_type not in ALLOWED_MIME_TYPES:
                flash(
                    "Tipo de archivo no permitido. Solo se permiten PDF, PNG, JPG, TXT, XLS o DOC.",
                    "danger",
                )
                return redirect(url_for("ecuestre.enter_docs", id=id))

            size = fstat(archivo_subido.fileno()).st_size
            if size > 5 * 1024 * 1024:
                flash(
                    "El archivo es demasiado grande. El tamaño máximo permitido es 5 MB.",
                    "danger",
                )
                return redirect(url_for("ecuestre.enter_docs", id=id))

            try:
                new_archivo = ecuestre.create_archivo(
                    nombre=archivo_subido.filename, tipo=archivo_tipo, es_archivo=True
                )
                ecuestre.assign_archivo(ecuestre_modificar, new_archivo)

                client = current_app.storage.client
                client.put_object(
                    "grupo28",
                    f"/ecuestre/{new_archivo.id}-{new_archivo.nombre}",
                    archivo_subido,
                    size,
                    content_type=archivo_subido.content_type,
                )
            except ValueError as e:
                flash(str(e), "danger")
                return redirect(url_for("ecuestre.enter_docs", id=id))

        flash("Archivo subido con éxito", "success")
        return redirect(url_for("ecuestre.enter_docs", id=id))
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("ecuestre.enter_docs", id=id))


@bprint.post("/<id>/agregar-enlace")
def add_enlace(id):
    """
    Función que permite agregar un enlace asociado a un ecuestre.
    Parameters:
        - id (int): ID del ecuestre.
    Returns:
        - Redirige a la página de documentos del ecuestre.
        - Si el usuario no está autenticado o no tiene permiso, aborta con los códigos 401 o 403 respectivamente.
        - Si se produce un error al agregar el enlace, muestra un mensaje de error.
    """

    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "ecuestre_add_enlace"):
        return abort(403)
    try:

        ecuestre_modificar = ecuestre.get_ecuestre(id)

        nombre_enlace = request.form["nombre-enlace"]
        tipo = request.form["tipo"]

        if not nombre_enlace or not tipo:
            flash("Debe ingresar un enlace y seleccionar un tipo.", "error")
            return redirect(url_for("ecuestre.enter_docs", id=id))

        nuevo_enlace = ecuestre.create_archivo(nombre=nombre_enlace, tipo=tipo)

        ecuestre.assign_archivo(ecuestre_modificar, nuevo_enlace)

        flash("Enlace agregado con éxito", "success")
        return redirect(url_for("ecuestre.enter_docs", id=id))

    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("ecuestre.enter_docs", id=id))
    pass


@bprint.post("/<id>/borrar-archivo/<id_archivo>")
def delete_archivo(id, id_archivo):
    """
    Función que permite eliminar un archivo asociado a un ecuestre.
    Parameters:
        - id (int): ID del ecuestre.
        - id_archivo (int): ID del archivo a eliminar.
    Returns:
        - Redirige a la página de documentos del ecuestre.
        - Si el usuario no está autenticado o no tiene permiso, aborta con los códigos 401 o 403 respectivamente.
        - Si se produce un error al eliminar el archivo, muestra un mensaje de error.
    """

    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "ecuestre_delete_archivo"):
        return abort(403)
    try:
        archivo = ecuestre.delete_archivo(id_archivo)

        client = current_app.storage.client

        client.remove_object("grupo28", f"/ecuestre/{archivo.id}-{archivo.nombre}")

        flash("Archivo eliminado con éxito", "danger")
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("ecuestre.enter_docs", id=id))


@bprint.post("/<id>/borrar-enlace/<id_enlace>")
def delete_enlace(id, id_enlace):
    """
    Función que permite eliminar un enlace asociado a un ecuestre.
    Parameters:
        - id (int): ID del ecuestre.
        - id_enlace (int): ID del enlace a eliminar.
    Returns:
        - Redirige a la página de documentos del ecuestre.
        - Si el usuario no está autenticado o no tiene permiso, aborta con los códigos 401 o 403 respectivamente.
        - Si se produce un error al eliminar el enlace, muestra un mensaje de error.
    """

    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "ecuestre_delete_enlace"):
        return abort(403)
    try:
        ecuestre.delete_archivo(id_enlace)
        flash("Enlace eliminado con éxito", "danger")
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("ecuestre.enter_docs", id=id))
