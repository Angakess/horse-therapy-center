from flask import current_app, redirect, render_template, request, url_for, flash
from core import ecuestre, equipo, jya
from flask import Blueprint

bprint = Blueprint("ecuestre", __name__, url_prefix="/ecuestre")


@bprint.get("/")
def index():
    amount_per_page = 10
    query = request.args.get("query", "")
    order = request.args.get("order", "asc")
    by = request.args.get("by", "")
    page = int(request.args.get("pag", "1"))

    total = ecuestre.list_ecuestres(query)
    ecuestres = ecuestre.list_ecuestres_page(query, page, amount_per_page, order, by)

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
    try:
        chosen_ecuestre = ecuestre.get_ecuestre(id)
        return render_template(
            "ecuestre/profile_editing.html",
            info=chosen_ecuestre,
            # archivos=chosen_ecuestre.archivos,
        )
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(
            url_for(
                "ecuestre/profile.html",
                info=chosen_ecuestre,
                # archivos=chosen_ecuestre.archivos,
            )
        )

@bprint.post("/<id>/edit")
def save_edit(id):
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
    
    ecuestre.edit_ecuestre(id,new_data)

    return redirect(url_for("ecuestre.get_profile", id=id))

@bprint.get("/agregar")
def enter_add():
    return render_template("ecuestre/add_ecuestre.html")


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

        j_y_a_id = request.form.get("j_y_a_id")
        if j_y_a_id:
            j_y_a_designado = jya.get_jinete_amazona(j_y_a_id)
            if j_y_a_designado:
                ecuestre.assing_j_y_a(new_ecuestre,j_y_a_designado)

        flash("Ecuestre creado con éxito", "success")
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("ecuestre.get_profile", id=new_ecuestre.id))

@bprint.post("/borrar")
def delete():
    chosen_id = request.form["id"]
    try:
        chosen_ecuestre = ecuestre.get_ecuestre(chosen_id)
        # archivos_asociados = chosen_ecuestre.archivos
        client = current_app.storage.client
        # for archivo in archivos_asociados:
        #     client.remove_object("grupo28",f"{archivo.id}-{archivo.nombre}")
        #     ecuestre.delete_archivo(archivo.id)
        
        ecuestre.delete_ecuestre(chosen_id)

    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("ecuestre.get_profile", id=chosen_id))

    flash("Ecuestre borrado con éxito", "success")
    return redirect(url_for("ecuestre.index"))