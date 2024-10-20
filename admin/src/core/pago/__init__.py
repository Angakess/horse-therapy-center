from datetime import datetime
from core.database import db
from sqlalchemy import and_, asc, desc, or_


class Pago(db.Model):
    __tablename__ = "pagos"
    id = db.Column(db.Integer, primary_key=True)
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    tipo = db.Column(db.Text, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    beneficiario_id = db.Column(db.Integer, db.ForeignKey("equipos.id"), nullable=True)
    beneficiario = db.relationship("Equipo", back_populates="pagos")


def create_pago(**kwargs):
    """
    Función que crea un nuevo Pago con los datos proporcionados.
    Parameters: kwargs(diccionario), parámetros para crear el pago.
    Returns: pago (objeto Pago), pago creado.
    """
    if kwargs.get("fecha") == "":
        kwargs["fecha"] = None

    pago = Pago(**kwargs)
    db.session.add(pago)
    db.session.commit()

    return pago


def assign_pago(equipo, pago):
    """
    Función que asigna un pago a un equipo.
    Parameters: equipo (objeto Equipo), equipo al cual asignar el pago.
                pago (objeto Pago), pago a asignar.
    Returns: pago (objeto Pago), pago actualizado con la asignación.
    """
    pago.beneficiario = equipo
    db.session.add(pago)
    db.session.commit()

    return pago


def unassign_pago(pago):
    """
    Función que desasigna un pago de un equipo.
    Parameters: pago (objeto Pago), pago a desasignar.
    Returns: pago (objeto Pago), pago actualizado sin beneficiario.
    """
    pago.beneficiario_id = None
    db.session.commit()

    return pago


def list_pagos_page(amount, page, f_min, f_max, tipos, order):
    """
    Función que lista pagos paginados según los filtros y parámetros proporcionados.
    Parameters: amount(int), cantidad de pagos por página.
                page(int), número de la página a mostrar.
                f_min(datetime), fecha mínima del filtro.
                f_max(datetime), fecha máxima del filtro.
                tipos(list), lista de tipos de pago a filtrar.
                order(string "asc" o "desc"), orden del listado.
    Returns: pagos (Paginator), página de pagos.
    """

    order_by_fecha = asc(Pago.fecha) if order == "asc" else desc(Pago.fecha)

    if tipos:
        pagos = (
            Pago.query.filter(
                Pago.tipo.in_(tipos), Pago.fecha >= f_min, Pago.fecha <= f_max
            )
            .order_by(order_by_fecha)
            .paginate(page=page, per_page=amount)
        )
    else:
        pagos = (
            Pago.query.filter(Pago.fecha >= f_min, Pago.fecha <= f_max)
            .order_by(order_by_fecha)
            .paginate(page=page, per_page=amount)
        )

    return pagos


def get_total(f_min, f_max, tipos):
    """
    Función que obtiene el total de pagos que cumplen con los filtros proporcionados.
    Parameters: f_min(datetime), fecha mínima del filtro.
                f_max(datetime), fecha máxima del filtro.
                tipos(list), lista de tipos de pago a filtrar.
    Returns: total (int), cantidad total de pagos.
    """
    if tipos:
        total = Pago.query.filter(
            Pago.tipo.in_(tipos), Pago.fecha >= f_min, Pago.fecha <= f_max
        ).count()
    else:
        total = Pago.query.filter(Pago.fecha >= f_min, Pago.fecha <= f_max).count()

    return total


def get_one(id):
    """
    Función que obtiene un pago por su id.
    Parameters: id(int), id del pago a buscar.
    Returns: chosen_pago (objeto Pago), pago encontrado.
    Raises: ValueError si el pago no se encuentra.
    """
    chosen_pago = Pago.query.get(id)

    if not chosen_pago:
        raise ValueError("No se encontró el pago seleccionado")

    return chosen_pago


def edit(id, data):
    """
    Función que edita un Pago existente con los datos proporcionados.
    Parameters: id(int), id del pago a editar.
                data(dict), diccionario con los nuevos valores a asignar.
    Returns: chosen_pago (objeto Pago), pago actualizado.
    Raises: ValueError si el pago no se encuentra.
    """
    chosen_pago = Pago.query.filter_by(id=id).first()

    if not chosen_pago:
        raise ValueError("No se encontró el pago seleccionado")

    for key, value in data.items():
        if key in ["fecha"] and value == "":
            value = None

        if hasattr(chosen_pago, key):
            setattr(chosen_pago, key, value)

    db.session.commit()
    return chosen_pago


def delete_pago(pago_id):
    """
    Función que elimina un pago por su id.
    Parameters: pago_id(int), id del pago a eliminar.
    Raises: ValueError si el pago no se encuentra.
    """
    chosen_pago = Pago.query.get(pago_id)

    if not chosen_pago:
        raise ValueError("No se encontró el pago seleccionado")

    db.session.delete(chosen_pago)
    db.session.commit()
