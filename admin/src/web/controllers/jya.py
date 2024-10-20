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
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "jya_enter_add"):
        return abort(403)
    equipos = Equipo.query.all()
    ecuestres = Ecuestre.query.all()
    return render_template("jya/add_jya.html", equipos=equipos, ecuestres=ecuestres)


@bprint.post("/agregar")
def add_jya():

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
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "jya_delete"):
        return abort(403)
    try:
        chosen_jinete_amazona = jya.get_jinete_amazona(id)
        archivos_asociados = chosen_jinete_amazona.archivos
        client = current_app.storage.client
        for archivo in archivos_asociados:
            client.remove_object("grupo28", f"{archivo.id}-{archivo.nombre}")
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
            archivos=chosen_jinete_amazona.archivos,
            equipos=equipos,
            ecuestres=ecuestres,
        )
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(
            url_for(
                "jya/profile.html",
                info=chosen_jinete_amazona,
                archivos=chosen_jinete_amazona.archivos,
            )
        )


@bprint.post("/<id>/edit")
def save_edit(id):
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

    ALLOWED_MIME_TYPES = {"application/pdf", "image/png", "image/jpeg", "text/plain"}

    archivo_subido = request.files["archivos_JineteAmazonas"]

    if archivo_subido:
        if archivo_subido.content_type not in ALLOWED_MIME_TYPES:
            flash(
                "Tipo de archivo no permitido. Solo se permiten PDF, PNG, JPG o TXT.",
                "danger",
            )
            return redirect(url_for("jya.get_profile", id=id))

        size = fstat(archivo_subido.fileno()).st_size
        if size > 5 * 1024 * 1024:
            flash(
                "El archivo es demasiado grande. El tamaño máximo permitido es 5 MB.",
                "danger",
            )
            return redirect(url_for("jya.get_profile", id=id))

        try:
            new_archivo = jya.create_archivo(nombre=archivo_subido.filename)
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
            return redirect(url_for("jya.get_profile", id=id))
    try:
        jya.edit_jya(id, **new_data)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("jya.get_profile", id=id))

    try:
        client = current_app.storage.client
        archivos_a_eliminar = request.form.getlist("archivos_a_eliminar")
        for archivo_id in archivos_a_eliminar:
            archivo = jya.get_archivo(archivo_id)
            client.remove_object("grupo28", f"{archivo.id}-{archivo.nombre}")
            jya.delete_archivo(archivo_id)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("jya.get_profile", id=id))

    flash("Datos guardados con exito.", "success")
    return redirect(url_for("jya.get_profile", id=id))


@bprint.get("/<id>/descargar-archivo")
def download_archivo(id):
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


def str_to_bool(value):
    if isinstance(value, bool):
        return value
    if value.lower() in ("true", "1"):
        return True
    elif value.lower() in ("false", "0"):
        return False
    else:
        raise ValueError("Not a boolean value")
