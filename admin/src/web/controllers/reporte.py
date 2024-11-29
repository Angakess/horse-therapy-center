from datetime import datetime
import math
from flask import (
    flash,
    redirect,
    render_template,
    request,
    url_for,
    send_file,
    current_app,
)
from flask import session, abort
from core import jya
from core import cobro
from core import equipo
from core import ecuestre
from core import trabajo
from flask import Blueprint
from web.helpers.auth import check_permission, is_authenticated
import os

bprint = Blueprint("reporte", __name__, url_prefix="/reporte")


@bprint.get("/")
def index():
    if not is_authenticated(session):
        return abort(401)

    if not check_permission(session, "reporte_index"):
        return abort(403)

    data_discapacidades = get_data_discapacidades()
    data_cobros = get_data_cobros()
    data_puestos = get_data_puestos()
    data_responsables = get_data_responsables()
    data_historial = get_data_historial()
    data_antiguedad = get_data_antiguedad()
    data_deudas = get_data_deudas()
    data_propuestas = get_data_propuestas()

    return render_template(
        "reportes/index.html",
        data_discapacidades=data_discapacidades,
        data_cobros=data_cobros,
        data_puestos=data_puestos,
        data_responsables=data_responsables,
        data_historial=data_historial,
        data_antiguedad=data_antiguedad,
        data_deudas=data_deudas,
        data_propuestas=data_propuestas,
    )


def get_data_discapacidades():
    cant_mental = jya.count_discapacidad("Mental")
    cant_motora = jya.count_discapacidad("Motora")
    cant_sensorial = jya.count_discapacidad("Sensorial")
    cant_visceral = jya.count_discapacidad("Visceral")
    cant_sin = jya.count_discapacidad(None)

    labels = [
        f"Mental: {cant_mental}",
        f"Motora: {cant_motora}",
        f"Sensorial: {cant_sensorial}",
        f"Visceral: {cant_visceral}",
        f"N/A: {cant_sin}",
    ]

    return {
        "cants": [cant_mental, cant_motora, cant_sensorial, cant_visceral, cant_sin],
        "labels": labels,
    }


def get_data_cobros():
    monto_por_mes = cobro.amount_per_month()
    mes_actual = datetime.now().month
    totales = [0] * mes_actual

    for i in monto_por_mes:
        mes = int(i["mes"])
        totales[mes - 1] = i["total"]

    return totales


def get_data_puestos():
    cant_por_puesto = equipo.amount_per_puesto()

    puestos = [
        "Administrativo/a",
        "Terapeuta",
        "Conductor",
        "Auxiliar de pista",
        "Herrero",
        "Veterinario",
        "Entrenador de Caballos",
        "Domador",
        "Profesor de Equitación",
        "Docente de Capacitación",
        "Auxiliar de mantenimiento",
        "Otro",
    ]

    # Crear lista de diccionarios con cantidad inicial en 0
    data = [{"puesto": puesto, "cant": 0} for puesto in puestos]

    for i in cant_por_puesto:
        for item in data:
            if item["puesto"] == i["puesto"]:
                item["cant"] = i["cant"]
                break

    return data


def get_data_responsables():
    pros = equipo.get_all()
    pros.sort(key=lambda p: p.ecuestres.count(), reverse=True)

    return pros


def get_data_historial():
    caballos = ecuestre.list_ecuestres()
    caballos.sort(key=lambda c: c.fecha_ingreso, reverse=True)

    return caballos


def get_data_antiguedad():
    fecha_actual = datetime.now()

    empleados = equipo.get_all()
    empleados.sort(key=lambda e: e.fecha_inicio)

    return [
        {
            "info": e,
            "antiguedad": math.floor((fecha_actual - e.fecha_inicio).days / 365),
        }
        for e in empleados
    ]


def get_data_deudas():
    adeudados = jya.list_jinete_amazona_deuda()

    return adeudados


def get_data_propuestas():
    ranking_propuestas = [
        {"nombre": "Hipoterapia", "cant": 0},
        {"nombre": "Monta terapéutica", "cant": 0},
        {"nombre": "Deporte Ecuestre Adaptado", "cant": 0},
        {"nombre": "Actividades recreativas", "cant": 0},
        {"nombre": "Equitación", "cant": 0},
    ]

    for prop in ranking_propuestas:
        prop["cant"] = trabajo.get_propuestas_cant_solicitadas(prop["nombre"])

    return ranking_propuestas


@bprint.get("/download-adeudados")
def download_adeudados():
    adeudados = jya.list_jinete_amazona_deuda()

    if len(adeudados) == 0:
        return "No data to download."

    csv_data = "Nombre,Teléfono,Domicilio\n"
    for adeudado in adeudados:
        csv_data += f'"{adeudado.nombre} {adeudado.apellido}","{adeudado.telefono_actual}","{adeudado.domicilio_actual}"\n'

    file_path = os.path.join(current_app.static_folder, "adeudados.csv")
    with open(file_path, "w") as csv_file:
        csv_file.write(csv_data)

    return send_file(file_path, as_attachment=True, download_name="adeudados.csv")


@bprint.get("/download-propuestas")
def download_propuestas():
    ranking_propuestas = get_data_propuestas()

    csv_data = "Ranking,Propuesta,Cantidad de jinetes/amazonas\n"

    ranking_propuestas.sort(key=lambda x: x["cant"], reverse=True)

    for index, prop in enumerate(ranking_propuestas, start=1):
        csv_data += f'{index},"{prop["nombre"]}",{prop["cant"]}\n'

    file_path = os.path.join(current_app.static_folder, "ranking-propuestas.csv")
    with open(file_path, "w") as csv_file:
        csv_file.write(csv_data)

    return send_file(
        file_path, as_attachment=True, download_name="ranking-propuestas.csv"
    )


@bprint.get("/download-historial")
def download_historial():
    caballos = get_data_historial()

    csv_data = "Nombre,Fecha,Sede,Tipo de adquisición\n"

    caballos.sort(key=lambda c: c.fecha_ingreso, reverse=True)

    for caballo in caballos:
        csv_data += f'"{caballo.nombre}","{caballo.fecha_ingreso.strftime('%d/%m/%Y')}","{caballo.sede_asignada}","{caballo.tipo_adquisicion}"\n'

    file_path = os.path.join(current_app.static_folder, "historial-caballos.csv")
    with open(file_path, "w") as csv_file:
        csv_file.write(csv_data)

    return send_file(
        file_path, as_attachment=True, download_name="historial-caballos.csv"
    )


@bprint.get("/download-antiguedad")
def download_antiguedad():
    empleados = get_data_antiguedad()

    csv_data = "Nombre,Cantidad de años,Fecha de ingreso\n"

    for empleado in empleados:
        csv_data += f'"{empleado["info"].nombre} {empleado["info"].apellido}",{empleado["antiguedad"]},"{empleado["info"].fecha_inicio.strftime("%d/%m/%Y")}"\n'

    file_path = os.path.join(current_app.static_folder, "antiguedad-empleados.csv")
    with open(file_path, "w") as csv_file:
        csv_file.write(csv_data)

    return send_file(
        file_path, as_attachment=True, download_name="aniguedad-empleados.csv"
    )
