from os import fstat
from flask import render_template, request, url_for, redirect, current_app
from core import (
    equipo,
    jya,
    situacionPrevisional,
    trabajo,
    institucion,
    parienteTutor,
    ecuestre,
)
from core.equipo import Equipo
from core.ecuestre import Ecuestre
from flask import Blueprint
from flask import flash
from flask import session, abort
from web.helpers.auth import check_permission, is_authenticated

bprint = Blueprint("jya", __name__, url_prefix="/jya")


@bprint.get("/")
def index():
    """
    Función que muestra una lista paginada de Jinetes/Amazonas y permite realizar una búsqueda.
    Parameters: Ninguno (Los parámetros de búsqueda, orden y paginación se obtienen de la query de la URL).
    Returns:
        - Si el usuario no está autenticado o no tiene permiso, aborta con los códigos 401 o 403 respectivamente.
        - Si tiene permisos, renderiza la plantilla 'jya/index.html' mostrando los Jinetes/Amazonas filtrados y paginados.
    """

    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "jya_index"):
        return abort(403)
    amount_per_page = 10
    query = request.args.get("query", "")
    order = request.args.get("order", "asc")
    by = request.args.get("by", "")
    page = int(request.args.get("pag", "1"))

    total = jya.get_total_jinetes_amazonas()
    jinetes_amazonas = jya.list_jinetes_amazonas_page(
        query, page, amount_per_page, order, by
    )

    return render_template(
        "jya/index.html",
        jinetes_amazonas=jinetes_amazonas,
        parametro=query,
        order=order,
        by=by,
        pag=page,
        page_amount=(total + amount_per_page - 1) // amount_per_page,
    )


@bprint.get("/<id>")
def get_profile(id):
    """
    Función que muestra el perfil de un Jinete/Amazona por su ID.
    Parameters:
        id (int): El ID del Jinete/Amazona a mostrar.
    Returns:
        - Si el usuario no está autenticado o no tiene permiso, aborta con los códigos 401 o 403 respectivamente.
        - Si el Jinete/Amazona con el ID proporcionado no existe, muestra un mensaje de error y redirige al índice.
        - Si tiene permisos y el Jinete/Amazona es válido, renderiza la plantilla 'jya/profile.html' con la información correspondiente.
    """
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "jya_get_profile"):
        return abort(403)
    try:
        chosen_jinete_amazona = jya.get_jinete_amazona(id)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("jya.index"))

    return render_template("jya/profile.html", info=chosen_jinete_amazona)


@bprint.get("/agregar")
def enter_add():
    """
    Función que muestra el formulario para agregar un nuevo Jinete/Amazona.
    Parameters: Ninguno.
    Returns:
        - Si el usuario no está autenticado o no tiene permiso, aborta con los códigos 401 o 403 respectivamente.
        - Si tiene permisos, renderiza la plantilla 'jya/add_jya.html' con las listas de equipos y ecuestres.
    """
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "jya_enter_add"):
        return abort(403)
    equipos = Equipo.query.all()
    ecuestres = Ecuestre.query.all()
    return render_template("jya/add_jya.html", equipos=equipos, ecuestres=ecuestres)


@bprint.post("/agregar")
def add_jya():
    """
    Función para agregar un nuevo Jinete/Amazona junto con su situación previsional,
        institución escolar, responsable (pariente/tutor) y trabajo.
    Parameters: Ninguno (Los parámetros se obtienen del formulario de la solicitud POST).
    Returns:
        - Si el usuario no está autenticado o no tiene permiso, aborta con los códigos 401 o 403 respectivamente.
        - Si se crea exitosamente el Jinete/Amazona junto con sus relaciones, redirige al perfil del Jinete/Amazona con un mensaje de éxito.
        - Si ocurre algún error durante la creación, muestra un mensaje de error y redirige al índice.
    """
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "jya_add_jya"):
        return abort(403)
    new_data = {
        "nombre": request.form["nombre"].capitalize(),
        "apellido": request.form["apellido"].capitalize(),
        "dni": request.form["dni"],
        "edad": request.form["edad"],
        "fecha_nacimiento": request.form["fecha_nacimiento"],
        "lugar_nacimiento": request.form["lugar_nacimiento"],
        "domicilio_actual": request.form["domicilio_actual"],
        "telefono_actual": request.form["telefono_actual"],
        "contacto_emergencia": request.form["contacto_emergencia"],
        "tel": request.form["tel"],
        "becado": str_to_bool(request.form["becado"]),
        "porcentaje_beca": request.form["porcentaje_beca"],
        "profesionales_atienden": request.form["profesionales_atienden"],
        "certificado_discapacidad": str_to_bool(
            request.form["certificado_discapacidad"]
        ),
        "asignacion_familiar": str_to_bool(request.form["asignacion_familiar"]),
        "tipo_asignacion_familiar": request.form["tipo_asignacion_familiar"],
        "beneficiario_pension": str_to_bool(request.form["beneficiario_pension"]),
        "beneficiario_pension_tipo": request.form["beneficiario_pension_tipo"],
        "discapacidad": request.form["discapacidad"],
        "otra_discapacidad": request.form["otra_discapacidad"],
        "tipo_discapacidad": request.form["tipo_discapacidad"],
    }

    try:
        new_jinete_amazona = jya.create_jinetes_amazonas(**new_data)

        datos_situacion_previsional = {
            "obra_social": request.form["obra_social"],
            "nroafiliado": request.form["nroafiliado"],
            "curatela": str_to_bool(request.form["curatela"]),
            "observaciones": request.form["observaciones"],
        }
        new_situacion_previsional = situacionPrevisional.create_situacion_previsional(
            **datos_situacion_previsional
        )
        jya.assing_situacion_previsional(new_jinete_amazona, new_situacion_previsional)

        datos_institucion_escolar = {
            "nombre": request.form["nombre_institucion"],
            "direccion": request.form["direccion"],
            "telefono": request.form["telefono_institucion"],
            "grado_actual": request.form["grado_actual"],
            "observaciones": request.form["observaciones_institucion"],
        }
        new_institucion_escolar = institucion.create_institucion_escolar(
            **datos_institucion_escolar
        )
        jya.assing_institucion_escolar(new_jinete_amazona, new_institucion_escolar)

        datos_responsable = {
            "parentesco": request.form["parentesco"],
            "nombre": request.form["nombre_parentesco"],
            "apellido": request.form["apellido_parentesco"],
            "dni": request.form["dni_parentesco"],
            "domicilio_actual": request.form["domicilio_actual_parentesco"],
            "celular_actual": request.form["celular_actual_parentesco"],
            "email": request.form["email_parentesco"],
            "nivel_escolaridad": request.form["nivel_escolaridad_parentesco"],
            "actividad_ocupacion": request.form["actividad_ocupacion_parentesco"],
        }
        new_responsable = parienteTutor.create_parentesco_tutor(**datos_responsable)
        jya.assing_parentesco_tutor(new_jinete_amazona, new_responsable)

        datos_trabajo = {
            "propuestra_trabajo_institucional": request.form[
                "propuestra_trabajo_institucional"
            ],
            "condicion": request.form["condicion_trabajo"],
            "sede": request.form["sede_trabajo"],
            "lunes": str_to_bool(request.form["lunes"]),
            "martes": str_to_bool(request.form["martes"]),
            "miercoles": str_to_bool(request.form["miercoles"]),
            "jueves": str_to_bool(request.form["jueves"]),
            "viernes": str_to_bool(request.form["viernes"]),
            "sabado": str_to_bool(request.form["sabado"]),
            "domingo": str_to_bool(request.form["domingo"]),
        }
        new_trabajo = trabajo.create_trabajo(**datos_trabajo)

        try:
            profesor_terapeuta_id = request.form.get("profesor_terapeuta_id")
            conductor_id = request.form.get("conductor_id")
            auxiliar_pista_id = request.form.get("auxiliar_pista_id")
            caballo_id = request.form.get("caballo_id")

            if profesor_terapeuta_id:
                profesor_terapeuta_asignado = equipo.get_one(profesor_terapeuta_id)
                if profesor_terapeuta_asignado:
                    trabajo.assing_profesor(new_trabajo, profesor_terapeuta_asignado)
                else:
                    flash("Profesor no encontrado", "warning")

            if conductor_id:
                conductor_asignado = equipo.get_one(conductor_id)
                if conductor_asignado:
                    trabajo.assing_conductor(new_trabajo, conductor_asignado)
                else:
                    flash("Conductor no encontrado", "warning")

            if auxiliar_pista_id:
                auxiliar_pista_asignado = equipo.get_one(auxiliar_pista_id)
                if auxiliar_pista_asignado:
                    trabajo.assing_auxiliar_pista(new_trabajo, auxiliar_pista_asignado)
                else:
                    flash("Auxiliar pista no encontrado", "warning")

            if caballo_id:
                caballo_asignado = ecuestre.get_ecuestre(caballo_id)
                if caballo_asignado:
                    trabajo.assing_caballo(new_trabajo, caballo_asignado)
                else:
                    flash("Caballo no encontrado", "warning")

        except ValueError as e:
            flash(str(e), "danger")
            return redirect(url_for("jya.index"))

        jya.assing_trabajo(new_jinete_amazona, new_trabajo)
        flash("Jinete/Amazona creado con éxito", "success")
        return redirect(url_for("jya.get_profile", id=new_jinete_amazona.id))
    except Exception as e:
        flash(f"Error al crear Jinete/Amazona: {str(e)}", "danger")
        return redirect(url_for("jya.index"))


@bprint.post("/borrar/<id>")
def delete(id):
    """
    Función para eliminar un Jinete/Amazona junto con sus archivos y todas sus asociaciones
    (situación previsional, institución escolar, parentesco/tutor y trabajo).
    Parameters:
        - id (int): ID del Jinete/Amazona a eliminar.
    Returns:
        - Si el usuario no está autenticado o no tiene permiso, aborta con los códigos 401 o 403 respectivamente.
        - Si la eliminación es exitosa, redirige al índice de Jinetes/Amazonas con un mensaje de éxito.
        - Si ocurre un error durante el proceso, redirige al perfil del Jinete/Amazona con un mensaje de error.
    """
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "jya_delete"):
        return abort(403)
    try:
        chosen_jinete_amazona = jya.get_jinete_amazona(id)
        archivos_asociados = chosen_jinete_amazona.docs
        client = current_app.storage.client
        for archivo in archivos_asociados:
            client.remove_object("grupo28", f"/jya/{archivo.id}-{archivo.nombre}")
            jya.delete_archivo(archivo.id)

        situacion_previsional_asociada = chosen_jinete_amazona.situacion_previsional
        situacionPrevisional.delete_situacion_previsional(
            situacion_previsional_asociada.id
        )

        institucion_asociada = chosen_jinete_amazona.institucion_escolar
        institucion.delete_institucion(institucion_asociada.id)

        parentescos_asociados = chosen_jinete_amazona.parentesco_tutor
        for responsable in parentescos_asociados:
            parienteTutor.delete_responsable(responsable.id)

        trabajo_asociado = chosen_jinete_amazona.trabajo
        trabajo.delete_trabajo(trabajo_asociado.id)

        jya.delete_jinetes_amazonas(id)

    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("jya.get_profile", id=id))

    flash("Jinete/Amazona borrado con éxito", "success")
    return redirect(url_for("jya.index"))


@bprint.get("/<id>/edit")
def enter_edit(id):
    """
    Función que permite acceder a la página de edición de un Jinete/Amazona.
    Parameters:
        - id (int): ID del Jinete/Amazona a editar.
    Returns:
        - Renderiza la plantilla de edición del perfil con los datos del Jinete/Amazona seleccionado y las listas
          de equipos y ecuestres disponibles para su selección.
        - Si el usuario no está autenticado o no tiene permiso, aborta con los códigos 401 o 403 respectivamente.
        - Si ocurre un error al obtener los datos, redirige a la página de perfil con un mensaje de error.
    """
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "jya_enter_edit"):
        return abort(403)
    equipos = Equipo.query.all()
    ecuestres = Ecuestre.query.all()
    try:
        chosen_jinete_amazona = jya.get_jinete_amazona(id)
        return render_template(
            "jya/profile_editing.html",
            info=chosen_jinete_amazona,
            archivos=chosen_jinete_amazona.docs,
            equipos=equipos,
            ecuestres=ecuestres,
        )
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(
            url_for(
                "jya/profile.html",
                info=chosen_jinete_amazona,
                archivos=chosen_jinete_amazona.docs,
            )
        )


@bprint.post("/<id>/edit")
def save_edit(id):
    """
    Función que guarda los cambios realizados en el perfil de un Jinete/Amazona.
    Parameters:
        - id (int): ID del Jinete/Amazona a editar.
    Returns:
        - Redirige a la página del perfil del Jinete/Amazona editado con un mensaje de éxito si la edición fue exitosa.
        - Si el usuario no está autenticado o no tiene permiso, aborta con los códigos 401 o 403 respectivamente.
        - Si el Jinete/Amazona no se encuentra o se produce un error, muestra un mensaje de error y redirige a la página correspondiente.
    """
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "jya_save_edit"):
        return abort(403)

    jinete_amazona_modificar = jya.get_jinete_amazona(id)

    if not jinete_amazona_modificar:
        flash("Jinete/Amazona no encontrado", "danger")
        return redirect(url_for("jya.index"))

    new_data = {
        "nombre": request.form["nombre"].capitalize(),
        "apellido": request.form["apellido"].capitalize(),
        "dni": request.form["dni"],
        "edad": request.form["edad"],
        "fecha_nacimiento": request.form["fecha_nacimiento"],
        "lugar_nacimiento": request.form["lugar_nacimiento"],
        "domicilio_actual": request.form["domicilio_actual"],
        "telefono_actual": request.form["telefono_actual"],
        "contacto_emergencia": request.form["contacto_emergencia"],
        "tel": request.form["tel"],
        "becado": str_to_bool(request.form["becado"]),
        "porcentaje_beca": request.form["porcentaje_beca"],
        "profesionales_atienden": request.form["profesionales_atienden"],
        "certificado_discapacidad": str_to_bool(
            request.form["certificado_discapacidad"]
        ),
        "asignacion_familiar": str_to_bool(request.form["asignacion_familiar"]),
        "tipo_asignacion_familiar": request.form["tipo_asignacion_familiar"],
        "beneficiario_pension": str_to_bool(request.form["beneficiario_pension"]),
        "beneficiario_pension_tipo": request.form["beneficiario_pension_tipo"],
        "discapacidad": request.form["discapacidad"],
        "otra_discapacidad": request.form["otra_discapacidad"],
        "tipo_discapacidad": request.form["tipo_discapacidad"],
    }

    if (
        new_data["becado"] == False
        and new_data["porcentaje_beca"] != None
        and new_data["porcentaje_beca"] != ""
    ):
        flash("No se puede ingresar un porcentaje si no esta becado", "warning")
        return redirect(url_for("jya.enter_edit", id=id))

    try:
        datos_situacion_previsional = {
            "obra_social": request.form["obra_social"],
            "nroafiliado": request.form["nroafiliado"],
            "curatela": str_to_bool(request.form["curatela"]),
            "observaciones": request.form["observaciones"],
        }
        if jinete_amazona_modificar.situacion_previsional:
            situacionPrevisional.delete_situacion_previsional(
                jinete_amazona_modificar.situacion_previsional.id
            )
        new_situacion_previsional = situacionPrevisional.create_situacion_previsional(
            **datos_situacion_previsional
        )
        jya.assing_situacion_previsional(
            jinete_amazona_modificar, new_situacion_previsional
        )

        datos_institucion_escolar = {
            "nombre": request.form["nombre_institucion"],
            "direccion": request.form["direccion"],
            "telefono": request.form["telefono_institucion"],
            "grado_actual": request.form["grado_actual"],
            "observaciones": request.form["observaciones_institucion"],
        }
        if jinete_amazona_modificar.institucion_escolar:
            institucion.delete_institucion(
                jinete_amazona_modificar.institucion_escolar.id
            )
        new_institucion_escolar = institucion.create_institucion_escolar(
            **datos_institucion_escolar
        )
        jya.assing_institucion_escolar(
            jinete_amazona_modificar, new_institucion_escolar
        )

        datos_responsable = {
            "parentesco": request.form["parentesco"],
            "nombre": request.form["nombre_parentesco"],
            "apellido": request.form["apellido_parentesco"],
            "dni": request.form["dni_parentesco"],
            "domicilio_actual": request.form["domicilio_actual_parentesco"],
            "celular_actual": request.form["celular_actual_parentesco"],
            "email": request.form["email_parentesco"],
            "nivel_escolaridad": request.form["nivel_escolaridad_parentesco"],
            "actividad_ocupacion": request.form["actividad_ocupacion_parentesco"],
        }
        if not parienteTutor.existe(datos_responsable["dni"]):
            new_responsable = parienteTutor.create_parentesco_tutor(**datos_responsable)
            jya.assing_parentesco_tutor(jinete_amazona_modificar, new_responsable)

        datos_trabajo = {
            "propuestra_trabajo_institucional": request.form[
                "propuestra_trabajo_institucional"
            ],
            "condicion": request.form["condicion_trabajo"],
            "sede": request.form["sede_trabajo"],
            "lunes": str_to_bool(request.form["lunes"]),
            "martes": str_to_bool(request.form["martes"]),
            "miercoles": str_to_bool(request.form["miercoles"]),
            "jueves": str_to_bool(request.form["jueves"]),
            "viernes": str_to_bool(request.form["viernes"]),
            "sabado": str_to_bool(request.form["sabado"]),
            "domingo": str_to_bool(request.form["domingo"]),
        }

        trabajo_editado_id = jinete_amazona_modificar.trabajo_id
        trabajo_editado = trabajo.edit_trabajo(trabajo_editado_id, **datos_trabajo)

        try:
            profesor_terapeuta_id = request.form.get("profesor_terapeuta_id")
            conductor_id = request.form.get("conductor_id")
            auxiliar_pista_id = request.form.get("auxiliar_pista_id")
            caballo_id = request.form.get("caballo_id")

            if profesor_terapeuta_id:
                profesor_terapeuta_asignado = equipo.get_one(profesor_terapeuta_id)
                if profesor_terapeuta_asignado:
                    trabajo.assing_profesor(
                        trabajo_editado, profesor_terapeuta_asignado
                    )
                else:
                    flash("Profesor no encontrado", "warning")

            if conductor_id:
                conductor_asignado = equipo.get_one(conductor_id)
                if conductor_asignado:
                    trabajo.assing_conductor(trabajo_editado, conductor_asignado)
                else:
                    flash("Conductor no encontrado", "warning")

            if auxiliar_pista_id:
                auxiliar_pista_asignado = equipo.get_one(auxiliar_pista_id)
                if auxiliar_pista_asignado:
                    trabajo.assing_auxiliar_pista(
                        trabajo_editado, auxiliar_pista_asignado
                    )
                else:
                    flash("Auxiliar pista no encontrado", "warning")

            if caballo_id:
                caballo_asignado = ecuestre.get_ecuestre(caballo_id)
                if caballo_asignado:
                    trabajo.assing_caballo(trabajo_editado, caballo_asignado)
                else:
                    flash("Caballo no encontrado", "warning")

        except Exception as e:
            flash(f"Error al modificar Jinete/Amazona: {str(e)}", "danger")

    except ValueError as e:
        flash(str(e), "danger")

    try:
        jya.edit_jya(id, **new_data)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("jya.get_profile", id=id))

    flash("Datos guardados con exito.", "success")
    return redirect(url_for("jya.get_profile", id=id))


@bprint.get("/<id>/descargar-archivo")
def download_archivo(id):
    """
    Función que permite descargar un archivo asociado a un Jinete/Amazona.
    Parameters:
        - id (int): ID del archivo a descargar.
    Returns:
        - Redirige a la URL del archivo para su descarga.
        - Si el usuario no está autenticado o no tiene permiso, aborta con los códigos 401 o 403 respectivamente.
        - Si ocurre un error al obtener el archivo, muestra un mensaje de error y redirige a la página del perfil del Jinete/Amazona asociado.
    """
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "jya_download_archivo"):
        return abort(403)
    try:
        chosen_archivo = jya.get_archivo(id)
        client = current_app.storage.client
        minio_url = client.presigned_get_object(
            "grupo28", f"/jya/{chosen_archivo.id}-{chosen_archivo.nombre}"
        )
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("jya.get_profile", id=chosen_archivo.jya_id))

    return redirect(minio_url)


@bprint.get("/<id>/documentos")
def enter_docs(id):
    """
    Función que permite acceder a los documentos asociados a un Jinete/Amazona.
    Parameters:
        - id (int): ID del Jinete/Amazona.
    Returns:
        - Renderiza la plantilla de documentos del perfil del Jinete/Amazona.
        - Si el usuario no está autenticado o no tiene permiso, aborta con los códigos 401 o 403 respectivamente.
        - Si ocurre un error al obtener los documentos, muestra un mensaje de error y redirige a la página del perfil del Jinete/Amazona asociado.
    """
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "jya_enter_docs"):
        return abort(403)
    try:
        amount_per_page = 5

        pag = int(request.args.get("pag", 1))
        query = request.args.get("query", "")
        order = request.args.get("order", "asc")
        tipos = request.args.getlist("tipoarchivo")
        by = request.args.get("by", "")

        total = jya.get_total_docs(id, query, tipos)

        chosen_jinete_amazona = jya.get_jinete_amazona(id)

        archivos = jya.list_archivos_page(
            id,
            query,
            order,
            tipos,
            by,
            pag,
            amount_per_page,
        )

        return render_template(
            "jya/profile_docs.html",
            info=chosen_jinete_amazona,
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
                "jya/profile.html",
                info=chosen_jinete_amazona,
                archivos=chosen_jinete_amazona.docs,
            )
        )


@bprint.post("/<id>/agregar-archivo")
def add_archivo(id):
    """
    Función que permite agregar un archivo asociado a un Jinete/Amazona.
    Parameters:
        - id (int): ID del Jinete/Amazona.
    Returns:
        - Redirige a la página de documentos del Jinete/Amazona.
        - Si el usuario no está autenticado o no tiene permiso, aborta con los códigos 401 o 403 respectivamente.
        - Si se produce un error al cargar el archivo, muestra un mensaje de error.
    """
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "jya_add_archivo"):
        return abort(403)
    try:

        jinete_amazona_modificar = jya.get_jinete_amazona(id)

        ALLOWED_MIME_TYPES = {
            "application/pdf",
            "image/png",
            "image/jpeg",
            "text/plain",
            "application/vnd.ms-excel",
            "application/msword",
        }

        archivo_subido = request.files["archivos_JineteAmazonas"]
        archivo_tipo = request.form["tipo"]

        if not archivo_subido or not archivo_tipo:
            flash("Debe ingresar un archivo y seleccionar un tipo.", "error")
            return redirect(url_for("jya.enter_docs", id=id))

        if archivo_subido:
            if archivo_subido.content_type not in ALLOWED_MIME_TYPES:
                flash(
                    "Tipo de archivo no permitido. Solo se permiten PDF, PNG, JPG, TXT, XLS o DOC.",
                    "danger",
                )
                return redirect(url_for("jya.enter_docs", id=id))

            size = fstat(archivo_subido.fileno()).st_size
            if size > 5 * 1024 * 1024:
                flash(
                    "El archivo es demasiado grande. El tamaño máximo permitido es 5 MB.",
                    "danger",
                )
                return redirect(url_for("jya.enter_docs", id=id))

            try:
                new_archivo = jya.create_archivo(
                    nombre=archivo_subido.filename, tipo=archivo_tipo, es_archivo=True
                )
                jya.assign_archivo(jinete_amazona_modificar, new_archivo)

                client = current_app.storage.client
                client.put_object(
                    "grupo28",
                    f"/jya/{new_archivo.id}-{new_archivo.nombre}",
                    archivo_subido,
                    size,
                    content_type=archivo_subido.content_type,
                )
            except ValueError as e:
                flash(str(e), "danger")
                return redirect(url_for("jya.enter_docs", id=id))

        flash("Archivo subido con éxito", "success")
        return redirect(url_for("jya.enter_docs", id=id))
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("jya.enter_docs", id=id))


@bprint.post("/<id>/agregar-enlace")
def add_enlace(id):
    """
    Función que permite agregar un enlace asociado a un Jinete/Amazona.
    Parameters:
        - id (int): ID del Jinete/Amazona.
    Returns:
        - Redirige a la página de documentos del Jinete/Amazona.
        - Si el usuario no está autenticado o no tiene permiso, aborta con los códigos 401 o 403 respectivamente.
        - Si se produce un error al agregar el enlace, muestra un mensaje de error.
    """
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "jya_add_enlace"):
        return abort(403)
    try:

        jinete_amazona_modificar = jya.get_jinete_amazona(id)

        nombre_enlace = request.form["nombre-enlace"]
        tipo = request.form["tipo"]

        if not nombre_enlace or not tipo:
            flash("Debe ingresar un enlace y seleccionar un tipo.", "error")
            return redirect(url_for("jya.enter_docs", id=id))

        nuevo_enlace = jya.create_archivo(nombre=nombre_enlace, tipo=tipo)

        jya.assign_archivo(jinete_amazona_modificar, nuevo_enlace)

        flash("Enlace agregado con éxito", "success")
        return redirect(url_for("jya.enter_docs", id=id))

    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("jya.enter_docs", id=id))


@bprint.post("/<id>/borrar-archivo/<id_archivo>")
def delete_archivo(id, id_archivo):
    """
    Función que permite eliminar un archivo asociado a un Jinete/Amazona.
    Parameters:
        - id (int): ID del Jinete/Amazona.
        - id_archivo (int): ID del archivo a eliminar.
    Returns:
        - Redirige a la página de documentos del Jinete/Amazona.
        - Si el usuario no está autenticado o no tiene permiso, aborta con los códigos 401 o 403 respectivamente.
        - Si se produce un error al eliminar el archivo, muestra un mensaje de error.
    """
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "jya_delete_archivo"):
        return abort(403)
    try:
        archivo = jya.delete_archivo(id_archivo)

        client = current_app.storage.client

        client.remove_object(
            "grupo28", f"/jya/{archivo.id}-{archivo.nombre}"
        )  # Eliminar de MinIO

        flash("Archivo eliminado con éxito", "danger")
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("jya.enter_docs", id=id))


@bprint.post("/<id>/borrar-enlace/<id_enlace>")
def delete_enlace(id, id_enlace):
    """
    Función que permite eliminar un enlace asociado a un Jinete/Amazona.
    Parameters:
        - id (int): ID del Jinete/Amazona.
        - id_enlace (int): ID del enlace a eliminar.
    Returns:
        - Redirige a la página de documentos del Jinete/Amazona.
        - Si el usuario no está autenticado o no tiene permiso, aborta con los códigos 401 o 403 respectivamente.
        - Si se produce un error al eliminar el enlace, muestra un mensaje de error.
    """
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "jya_delete_enlace"):
        return abort(403)
    try:
        jya.delete_archivo(id_enlace)
        flash("Enlace eliminado con éxito", "danger")
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("jya.enter_docs", id=id))


def str_to_bool(value):
    """
    Convierte una cadena a un valor booleano.
    Parameters:
        - value (str): Cadena que se desea convertir.
    Returns:
        - bool: Valor booleano correspondiente a la cadena.
    Raises:
        - ValueError: Si la cadena no representa un valor booleano.
    """
    if isinstance(value, bool):
        return value
    if value.lower() in ("true", "1"):
        return True
    elif value.lower() in ("false", "0"):
        return False
    else:
        raise ValueError("Not a boolean value")
