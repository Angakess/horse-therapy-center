from os import fstat
from flask import render_template,request, url_for, redirect, current_app
from core import equipo, jya, situacionPrevisional, trabajo, institucion, parienteTutor, ecuestre
from flask import Blueprint
from flask import flash

bprint = Blueprint("jya", __name__, url_prefix="/jya")

@bprint.get("/")
def index():
    amount_per_page = 10
    query = request.args.get("query", "")
    order = request.args.get("order", "asc")
    by = request.args.get("by", "")
    page = int(request.args.get("pag", "1"))

    total = jya.get_total_jinetes_amazonas()
    jinetes_amazonas = jya.list_jinetes_amazonas_page(query, page, amount_per_page, order, by)

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
    try:
        chosen_jinete_amazona = jya.get_jinete_amazona(id)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(
            url_for("jya.index")
        )

    return render_template(
        "jya/profile.html", info=chosen_jinete_amazona
    )


@bprint.get("/agregar")
def enter_add():
    return render_template("jya/add_jya.html")

@bprint.post("/agregar")
def add_jya():
    new_data = {
        "nombre": request.form["nombre"].capitalize(),
        "apellido": request.form["apellido"].capitalize(),
        "edad": request.form["edad"],
        "fecha_nacimiento": request.form["fecha_nacimiento"],
        "lugar_nacimiento": request.form["lugar_nacimiento"],
        "domicilio_actual": request.form["domicilio_actual"],
        "telefono_actual": request.form["telefono_actual"],
        "contacto_emergencia": request.form["contacto_emergencia"],
        "telefono": request.form["tel"],
        "becado": True if request.form["becado"] == "True" else False,
        "porcentaje_beca": request.form["porcentaje_beca"],
        "profesionales_atienden": request.form["profesionales_atienden"],
        "certificado_discapacidad": True if request.form["certificado_discapacidad"] == "True" else False,
        "asignacion_familiar": True if request.form["asignacion_familiar"] == "True" else False,
        "tipo_asignacion_familiar": request.form["tipo_asignacion_familiar"],
        "beneficiario_pension": request.form["beneficiario_pension"],
        "beneficiario_pension_tipo": True if request.form["beneficiario_pension_tipo"] == "True" else False,
        "discapacidad": request.form["discapacidad"],
        "otra_discapacidad": request.form["otra_discapacidad"],
        "tipo_discapacidad": request.form["tipo_discapacidad"],
    }
    
    try:
        new_jinete_amazona = jya.create_jinetes_amazonas(**new_data)

        datos_situacion_previsional = {
            "obra_social": request.form["obra_social"],
            "nroafiliado": request.form["nroafiliado"],
            "curatela": True if request.form["curatela"] == "True" else False,
            "observaciones": request.form["observaciones"],
        }
        new_situacion_previsional = situacionPrevisional.create_situacion_previsional(datos_situacion_previsional)
        jya.assing_situacion_previsional(new_jinete_amazona, new_situacion_previsional)

        datos_institucion_escolar = {
            "nombre": request.form["nombre"],
            "direccion": request.form["direccion"],
            "telefono": request.form["telefono"],
            "grado_actual": request.form["grado_actual"],
            "observaciones": request.form["observaciones"],
        }
        new_institucion_escolar = institucion.create_institucion_escolar(datos_institucion_escolar)
        jya.assing_institucion_escolar(new_jinete_amazona, new_institucion_escolar)

        datos_responsable = {
            "parentesco": request.form["parentesco"],
            "nombre": request.form["nombre"],
            "apellido": request.form["apellido"],
            "dni": request.form["dni"],
            "domicilio_actual": request.form["domicilio_actual"],
            "celular_actual": request.form["celular_actual"],
            "email": request.form["email"],
            "nivel_escolaridad": request.form["nivel_escolaridad"],
            "actividad_ocupacion": request.form["actividad_ocupacion"],
        }
        new_responsable = parienteTutor.create_parentesco_tutor(datos_responsable)
        jya.assing_parentesco_tutor(new_jinete_amazona, new_responsable)

        datos_trabajo = {
            "propuestra_trabajo_institucional": request.form["propuestra_trabajo_institucional"],
            "condicion": request.form["condicion"],
            "sede": request.form["sede"],
            "lunes": True if request.form["lunes"] == "True" else False,
            "martes": True if request.form["martes"] == "True" else False,
            "miercoles": True if request.form["miercoles"] == "True" else False,
            "jueves": True if request.form["jueves"] == "True" else False,
            "viernes": True if request.form["viernes"] == "True" else False,
            "sabado": True if request.form["sabado"] == "True" else False,
            "domingo": True if request.form["domingo"] == "True" else False,
        }
        new_trabajo =  trabajo.create_trabajo(datos_trabajo)

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
            return redirect(url_for("ecuestre.get_profile", id=id))    
        
        jya.assing_trabajo(new_jinete_amazona, new_trabajo)
        flash("Jinete/Amazona creado con éxito", "success")
    except Exception as e:
        flash(f"Error al crear Jinete/Amazona: {str(e)}", "danger")

    return redirect(url_for("jya.get_profile"))

@bprint.post("/borrar/<id>")
def delete(id):
    try:
        chosen_jinete_amazona = jya.get_jinete_amazona(id)
        archivos_asociados = chosen_jinete_amazona.archivos
        client = current_app.storage.client
        for archivo in archivos_asociados:
            client.remove_object("grupo28",f"{archivo.id}-{archivo.nombre}")
            jya.delete_archivo(archivo.id)

        situacion_previsional_asociada = chosen_jinete_amazona.situacion_previsional
        situacionPrevisional.delete_situacion_previsional(situacion_previsional_asociada.id)

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
    try:
        chosen_jinete_amazona = jya.get_jinete_amazona(id)
        return render_template(
            "jya/profile_editing.html",
            info=chosen_jinete_amazona,
            archivos=chosen_jinete_amazona.archivos,
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
        jinete_amazona_modificar = jya.get_jinete_amazona(id)

        if not jinete_amazona_modificar:
            flash("Jinete/Amazona no encontrado", "danger")
            return redirect(url_for("jya.index"))

        new_data = {
        "nombre": request.form["nombre"].capitalize(),
        "apellido": request.form["apellido"].capitalize(),
        "edad": request.form["edad"],
        "fecha_nacimiento": request.form["fecha_nacimiento"],
        "lugar_nacimiento": request.form["lugar_nacimiento"],
        "domicilio_actual": request.form["domicilio_actual"],
        "telefono_actual": request.form["telefono_actual"],
        "contacto_emergencia": request.form["contacto_emergencia"],
        "telefono": request.form["tel"],
        "becado": True if request.form["becado"] == "True" else False,
        "porcentaje_beca": request.form["porcentaje_beca"],
        "profesionales_atienden": request.form["profesionales_atienden"],
        "certificado_discapacidad": True if request.form["certificado_discapacidad"] == "True" else False,
        "asignacion_familiar": True if request.form["asignacion_familiar"] == "True" else False,
        "tipo_asignacion_familiar": request.form["tipo_asignacion_familiar"],
        "beneficiario_pension": request.form["beneficiario_pension"],
        "beneficiario_pension_tipo": True if request.form["beneficiario_pension_tipo"] == "True" else False,
        "discapacidad": request.form["discapacidad"],
        "otra_discapacidad": request.form["otra_discapacidad"],
        "tipo_discapacidad": request.form["tipo_discapacidad"],
    }

        try:
            situacion_previsional_id = request.form.get("situacion_previsional_id")
            if situacion_previsional_id:
                situacion_previsional = situacionPrevisional.get_situacion_previsional(situacion_previsional_id)
                if situacion_previsional:
                    jya.assing_situacion_previsional(jinete_amazona_modificar, situacion_previsional)
                else:
                    flash("Situación previsional no encontrada", "warning")

            institucion_escolar_id = request.form.get("institucion_escolar_id")
            if institucion_escolar_id:
                institucion_escolar = institucion.get_institucion(institucion_escolar_id)
                if institucion_escolar:
                    jya.assing_institucion_escolar(jinete_amazona_modificar, institucion_escolar)
                else:
                    flash("Institución no encontrada", "warning")

            parentesco_tutor_id = request.form.get("parentesco_tutor_id")
            if parentesco_tutor_id:
                parentesco_tutor = parienteTutor.get_responsable(parentesco_tutor_id)
                if parentesco_tutor:
                    jya.assing_parentesco_tutor(jinete_amazona_modificar, parentesco_tutor)
                else:
                    flash("Pariente o tutor no encontrado", "warning")

            trabajo_id = request.form.get("trabajo_id")
            if trabajo_id:
                trabajo_relacion = trabajo.get_trabajo(trabajo_id)
                if trabajo_relacion:
                    jya.assing_trabajo(jinete_amazona_modificar, trabajo_relacion)
                else:
                    flash("Ocupación no encontrada", "warning")                    
        except ValueError as e:
            flash(str(e), "danger")

        ALLOWED_MIME_TYPES = {"application/pdf", "image/png", "image/jpeg", "text/plain"}

        archivo_subido = request.files["archivos"]

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
                return redirect(url_for("ecuestre.get_profile", id=id))

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
            jya.edit_jya(id,new_data)
        except ValueError as e:
            flash(str(e), "danger")
            return redirect(url_for("jya.get_profile", id=id))

        try:
            client = current_app.storage.client
            archivos_a_eliminar = request.form.getlist("archivos_a_eliminar")
            for archivo_id in archivos_a_eliminar:
                archivo = jya.get_archivo(
                    archivo_id
                )
                client.remove_object(
                    "grupo28", f"{archivo.id}-{archivo.nombre}"
                )
                jya.delete_archivo(archivo_id)
        except ValueError as e:
            flash(str(e), "danger")
            return redirect(url_for("ecuestre.get_profile", id=id)) 

        flash("Datos guardados con exito.", "success")
        return redirect(url_for("ecuestre.get_profile", id=id))

@bprint.get("/<id>/descargar-archivo")
def download_archivo(id):
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