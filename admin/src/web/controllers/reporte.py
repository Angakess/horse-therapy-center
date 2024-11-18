from datetime import datetime
import math
from flask import flash, redirect, render_template, request, url_for
from flask import session, abort
from core import jya
from core import cobro
from core import equipo
from core import ecuestre
from flask import Blueprint
from web.helpers.auth import check_permission, is_authenticated

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

    return render_template(
        "reportes/index.html",
        data_discapacidades=data_discapacidades,
        data_cobros=data_cobros,
        data_puestos=data_puestos,
        data_responsables=data_responsables,
        data_historial=data_historial,
        data_antiguedad=data_antiguedad,
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
