from flask import render_template,request, url_for, redirect, current_app
from sqlalchemy import asc,desc
from core import jya, situacionPrevisional, trabajo, institucion, parienteTutor
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

    total = jya.list_jinetes_amazonas(query)
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
        "becado": request.form["becado"],
        "porcentaje_beca": request.form["porcentaje_beca"],
        "profesionales_atienden": request.form["profesionales_atienden"],
        "certificado_discapacidad": request.form["certificado_discapacidad"],
        "asignacion_familiar": request.form["asignacion_familiar"],
        "tipo_asignacion_familiar": request.form["tipo_asignacion_familiar"],
        "beneficiario_pension": request.form["beneficiario_pension"],
        "beneficiario_pension_tipo": request.form["beneficiario_pension_tipo"],
        "discapacidad": request.form["discapacidad"],
        "otra_discapacidad": request.form["otra_discapacidad"],
        "tipo_discapacidad": request.form["tipo_discapacidad"],
    }
    
    try:
        new_jinete_amazona = jya.create_jinetes_amazonas(**new_data)

        situacion_previsional_id = request.form.get("situacion_previsional_id")
        if situacion_previsional_id:
            situacion_previsional = situacionPrevisional.get_situacion_previsional(situacion_previsional_id)
            if situacion_previsional:
                jya.assing_situacion_previsional(new_jinete_amazona, situacion_previsional)

        institucion_escolar_id = request.form.get("institucion_escolar_id")
        if institucion_escolar_id:
            institucion_escolar = institucion.get_institucion(institucion_escolar_id)
            if institucion_escolar:
                jya.assing_institucion_escolar(new_jinete_amazona, institucion_escolar)

        parentesco_tutor_id = request.form.get("parentesco_tutor_id")
        if parentesco_tutor_id:
            parentesco_tutor = parienteTutor.get_responsable(parentesco_tutor_id)
            if parentesco_tutor:
                jya.assing_parentesco_tutor(new_jinete_amazona, parentesco_tutor)

        trabajo_id = request.form.get("trabajo_id")
        if trabajo_id:
            trabajo_relacion = trabajo.get_trabajo(trabajo_id)
            if trabajo_relacion:
                jya.assing_trabajo(new_jinete_amazona, trabajo_relacion)

        flash("Jinete/Amazona creado con éxito", "success")
    except Exception as e:
        flash(f"Error al crear Jinete/Amazona: {str(e)}", "danger")

    return redirect(url_for("jya.get_profile"))

@bprint.post("/borrar")
def delete():
    chosen_id = request.form["id"]
    try:
        chosen_jinete_amazona = jya.get_jinete_amazona(chosen_id)
        # archivos_asociados = chosen_jinete_amazona.archivos
        client = current_app.storage.client
        # for archivo in archivos_asociados:
        #     client.remove_object("grupo28",f"{archivo.id}-{archivo.nombre}")
        #     jya.delete_archivo(archivo.id)

        situacion_previsional_asociada = chosen_jinete_amazona.situacion_previsional
        client.remove_object("grupo28",f"{situacion_previsional_asociada.id}")
        situacionPrevisional.delete_situacion_previsional(situacion_previsional_asociada.id)

        institucion_asociada = chosen_jinete_amazona.institucion_escolar
        client.remove_object("grupo28",f"{institucion_asociada.id}")
        institucion.delete_institucion(institucion_asociada.id)

        parentescos_asociados = chosen_jinete_amazona.parentesco_tutor
        for responsable in parentescos_asociados:
            client.remove_object("grupo28",f"{responsable.id}-{responsable.nombre}-{responsable.apellido}")
            parienteTutor.delete_responsable(responsable.id)     

        trabajo_asociado = chosen_jinete_amazona.trabajo
        client.remove_object("grupo28",f"{trabajo_asociado.id}")
        trabajo.delete_trabajo(trabajo_asociado.id)

        jya.delete_jinetes_amazonas(chosen_id)           
        
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("jya.get_profile", id=chosen_id))

    flash("Jinete/Amazona borrado con éxito", "success")
    return redirect(url_for("jya.index"))

@bprint.get("/<id>/edit")
def enter_edit(id):
    try:
        chosen_jinete_amazona = jya.get_jinete_amazona(id)
        return render_template(
            "jya/profile_editing.html",
            info=chosen_jinete_amazona,
            # archivos=chosen_jinete_amazona.archivos,
        )
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(
            url_for(
                "jya/profile.html",
                info=chosen_jinete_amazona,
                # archivos=chosen_jinete_amazona.archivos,
            )
        )

@bprint.post("/<id>/edit")
def save_edit(id):
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
        "becado": request.form["becado"].capitalize(),
        "porcentaje_beca": request.form["porcentaje_beca"],
        "profesionales_atienden": request.form["profesionales_atienden"],
        "certificado_discapacidad": request.form["certificado_discapacidad"],
        "asignacion_familiar": request.form["asignacion_familiar"],
        "tipo_asignacion_familiar": request.form["tipo_asignacion_familiar"],
        "beneficiario_pension": request.form["beneficiario_pension"],
        "beneficiario_pension_tipo": request.form["beneficiario_pension_tipo"],
        "discapacidad": request.form["discapacidad"],
        "otra_discapacidad": request.form["otra_discapacidad"],
        "tipo_discapacidad": request.form["tipo_discapacidad"],
    }
    