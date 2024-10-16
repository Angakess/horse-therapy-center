from sqlalchemy import String, asc, cast, desc, or_
from core.database import db
from .equipo import Equipo
from .archivos import Archivo


def get_total(parametro=""):
    total = Equipo.query.filter(
        or_(
            Equipo.nombre.like(f"%{parametro}%"),
            Equipo.apellido.like(f"%{parametro}%"),
            cast(Equipo.dni, String).like(f"%{parametro}%"),
            Equipo.email.like(f"%{parametro}%"),
            Equipo.puesto.like(f"%{parametro}%"),
        ),
        Equipo.borrado == False
    ).count()

    return total


def list_equipos_page(query="", page=1, amount_per_page=10, order="asc", by="id"):
    sort_column = {
        "nombre": Equipo.nombre,
        "apellido": Equipo.apellido,
        "fecha": Equipo.inserted_at,
    }.get(by, Equipo.id)

    order_by = asc(sort_column) if order == "asc" else desc(sort_column)

    equipos = (
        Equipo.query.filter(
            or_(
                Equipo.nombre.like(f"%{query}%"),
                Equipo.apellido.like(f"%{query}%"),
                cast(Equipo.dni, String).like(f"%{query}%"),
                Equipo.email.like(f"%{query}%"),
                Equipo.puesto.like(f"%{query}%"),
            ),
            Equipo.borrado == False
        )
        .order_by(order_by)
        .paginate(page=page, per_page=amount_per_page)
    )

    return equipos


def create_equipo(**kwargs):
    if kwargs.get("fecha_fin") == "":
        kwargs["fecha_fin"] = None
    if kwargs.get("fecha_inicio") == "":
        kwargs["fecha_inicio"] = None

    equipo = Equipo(**kwargs)
    db.session.add(equipo)
    db.session.commit()

    return equipo


def toggle_a(id):
    chosen_equipo = Equipo.query.filter_by(id=id, borrado=False).first()

    if not chosen_equipo:
        raise ValueError("No se encontró a la persona seleccionada")
    chosen_equipo.activo = not (chosen_equipo.activo)
    db.session.commit()


def get_one(id):
    chosen_equipo = Equipo.query.filter_by(id=id, borrado=False).first()

    if not chosen_equipo:
        raise ValueError("No se encontró a la persona seleccionada")

    return chosen_equipo


def edit(id, data):
    chosen_equipo = Equipo.query.filter_by(id=id, borrado=False).first()


    if not chosen_equipo:
        raise ValueError("No se encontró a la persona seleccionada")

    for key, value in data.items():
        if key in ["fecha_inicio", "fecha_fin"] and value == "":
            value = None

        if hasattr(chosen_equipo, key):
            setattr(chosen_equipo, key, value)

    db.session.commit()


def create_archivo(**kwargs):
    archivo = Archivo(**kwargs)
    db.session.add(archivo)
    db.session.commit()

    return archivo


def assign_archivo(equipo, archivo):
    archivo.equipo = equipo
    db.session.add(archivo)
    db.session.commit()

    return archivo


def get_archivo(id):
    archivo = Archivo.query.get(id)
    if not archivo:
        raise(ValueError("No se encontró el archivo solicitado"))

    return archivo


def delete_archivo(id):
    archivo = Archivo.query.get(id)
    if not archivo:
        raise(ValueError("No se encontró el archivo solicitado para borrar"))
    else:
        db.session.delete(archivo)
        db.session.commit()


def delete_equipo(id):
    chosen_equipo = Equipo.query.get(id)
    if not chosen_equipo:
        raise ValueError("No se encontró a la persona seleccionada")
    else:
        chosen_equipo.borrado = True
        db.session.commit()

    return chosen_equipo