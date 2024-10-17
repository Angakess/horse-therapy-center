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
    if kwargs.get("fecha") == "":
        kwargs["fecha"] = None

    pago = Pago(**kwargs)
    db.session.add(pago)
    db.session.commit()

    return pago


def assign_pago(equipo, pago):
    pago.beneficiario = equipo
    db.session.add(pago)
    db.session.commit()

    return pago


def unassign_pago(pago):
    pago.beneficiario_id = None
    db.session.commit()

    return pago


def list_pagos_page(amount, page, f_min, f_max, tipos, order):

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
    if tipos:
        total = Pago.query.filter(
            Pago.tipo.in_(tipos), Pago.fecha >= f_min, Pago.fecha <= f_max
        ).count()
    else:
        total = Pago.query.filter(Pago.fecha >= f_min, Pago.fecha <= f_max).count()

    return total


def get_one(id):
    chosen_pago = Pago.query.get(id)

    if not chosen_pago:
        raise ValueError("No se encontró el pago seleccionado")

    return chosen_pago


def edit(id, data):
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
    chosen_pago = Pago.query.get(pago_id)

    if not chosen_pago:
        raise ValueError("No se encontró el pago seleccionado")

    db.session.delete(chosen_pago)
    db.session.commit()
