from datetime import datetime
from core.database import db
from sqlalchemy import asc, desc


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


def list_pagos_page(amount, page):
    pagos = Pago.query.filter().paginate(page=page, per_page=amount)

    return pagos


def get_total():
    total = Pago.query.filter().count()

    return total

def edit():
    pass


def delete_pago():
    pass
