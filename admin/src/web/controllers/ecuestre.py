from os import fstat
from flask import current_app, redirect, render_template, request, url_for, flash
from core import ecuestre, equipo, jya
from flask import Blueprint

from core.equipo.equipo import Equipo

bprint = Blueprint("ecuestre", __name__, url_prefix="/ecuestre")


@bprint.get("/")
def index():
    amount_per_page = 10
    query = request.args.get("query", "")
    order = request.args.get("order", "asc")
    by = request.args.get("by", "")
    page = int(request.args.get("pag", "1"))
    jya =request.args.get('jya', None)
    total = ecuestre.get_total_ecuestre()
    ecuestres = ecuestre.list_ecuestres_page(query, page, amount_per_page, order, by,jya)

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
    try:
        chosen_ecuestre = ecuestre.get_ecuestre(id)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(
            url_for("ecuestre.index")
        )

    return render_template(
        "ecuestre/profile.html", info=chosen_ecuestre
    )

@bprint.get("/<id>/edit")
def enter_edit(id):
    equipos = Equipo.query.all()
    try:
        chosen_ecuestre = ecuestre.get_ecuestre(id)
        return render_template(
            "ecuestre/profile_editing.html",
            info=chosen_ecuestre,
            archivos=chosen_ecuestre.archivos,
            equipos = equipos,
        )
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(
            url_for(
                "ecuestre/profile.html",
                info=chosen_ecuestre,
                archivos=chosen_ecuestre.archivos,
            )
        )

@bprint.post("/<id>/edit")
def save_edit(id):
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
        equipo_id = request.form.get("equipo_id")
        if (not equipo_id):
            equipo_asignar = equipo.get_one(equipo_id)
            ecuestre.assing_equipo(ecuestre_modificar,equipo_asignar)

        # j_y_a_id = request.form.get("j_y_a_id")
        # if j_y_a_id:
        #     j_y_a_designado = jya.get_jinete_amazona(j_y_a_id)
        #     if j_y_a_designado:
        #         ecuestre.assing_j_y_a(ecuestre_modificar, j_y_a_designado)
        #     else:
        #         flash("Jinete/Amazona no encontrado", "warning")
    except ValueError as e:
        flash(str(e), "danger")

    try:
        equipo_id_a_borrar = request.form.get("equipo_id")
        if equipo_id:
            equipo_designado_borrar = equipo.get_one(equipo_id_a_borrar)
            if equipo_designado_borrar:
                ecuestre.unassing_equipo(ecuestre_modificar, equipo_designado_borrar)
            else:
                flash("Equipo no encontrado", "warning")

        # j_y_a_id_a_borrar = request.form.get("j_y_a_id")
        # if j_y_a_id:
        #     j_y_a_designado_borrar = jya.get_jinete_amazona(j_y_a_id_a_borrar)
        #     if j_y_a_designado_borrar:
        #         ecuestre.unassing_j_y_a(ecuestre_modificar, j_y_a_designado_borrar )
        #     else:
        #         flash("Jinete/Amazona no encontrado", "warning")
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
        ecuestre.edit_ecuestre(id,new_data)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("ecuestre.get_profile", id=id))

    try:
        client = current_app.storage.client
        archivos_a_eliminar = request.form.getlist("archivos_a_eliminar")
        for archivo_id in archivos_a_eliminar:
            archivo = ecuestre.get_archivo(
                archivo_id
            )
            client.remove_object(
                "grupo28", f"{archivo.id}-{archivo.nombre}"
            )
            ecuestre.delete_archivo(archivo_id)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("ecuestre.get_profile", id=id)) 

    flash("Datos guardados con exito.", "success")
    return redirect(url_for("ecuestre.get_profile", id=id))

@bprint.get("/agregar")
def enter_add():
    equipos = Equipo.query.all()
    return render_template("ecuestre/add_ecuestre.html",equipos=equipos)


@bprint.post("/agregar")
def add_ecuestre():
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

        equipo_id = request.form.get("equipo_id")
        if equipo_id:
            equipo_designado = equipo.get_one(equipo_id)
            if equipo_designado:
                ecuestre.assing_equipo(new_ecuestre, equipo_designado)

        # j_y_a_id = request.form.get("j_y_a_id")
        # if j_y_a_id:
        #     j_y_a_designado = jya.get_jinete_amazona(j_y_a_id)
        #     if j_y_a_designado:
        #         ecuestre.assing_j_y_a(new_ecuestre,j_y_a_designado)

        flash("Ecuestre creado con éxito", "success")
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("ecuestre.get_profile", id=new_ecuestre.id))

@bprint.post("/borrar/<id>")
def delete(id):
    try:
        chosen_ecuestre = ecuestre.get_ecuestre(id)
        archivos_asociados = chosen_ecuestre.archivos
        client = current_app.storage.client
        for archivo in archivos_asociados:
            client.remove_object("grupo28",f"{archivo.id}-{archivo.nombre}")
            ecuestre.delete_archivo(archivo.id)
        
        ecuestre.delete_ecuestre(id)

    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("ecuestre.get_profile", id=id))

    flash("Ecuestre borrado con éxito", "success")
    return redirect(url_for("ecuestre.index"))

@bprint.get("/<id>/descargar-archivo")
def download_archivo(id):
    try:
        chosen_archivo = ecuestre.get_archivo(id)
        client = current_app.storage.client
        minio_url = client.presigned_get_object(
            "grupo28", f"/jya/{chosen_archivo.id}-{chosen_archivo.nombre}"
        )
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("ecuestre.get_profile", id=chosen_archivo.ecuestre_id))

    return redirect(minio_url)