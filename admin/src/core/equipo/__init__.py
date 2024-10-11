from datetime import datetime
from sqlalchemy import String, asc, cast, desc, or_
from core.database import db


class Equipo(db.Model):
    __tablename__ = "equipos"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    dni = db.Column(db.Integer, nullable=False)
    dir = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    localidad = db.Column(db.String(100), nullable=False)
    tel = db.Column(db.Text, nullable=False)
    profesion = db.Column(db.Text, nullable=False)
    puesto = db.Column(db.Text, nullable=False)
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=True)
    contacto_emergencia_nombre = db.Column(db.Text, nullable=False)
    contacto_emergencia_tel = db.Column(db.Text, nullable=False)
    obra_social = db.Column(db.Text, nullable=False)
    num_afiliado = db.Column(db.Text, nullable=False)
    condicion = db.Column(db.Text, nullable=False)
    activo = db.Column(db.Boolean, nullable=False, default=True)
    equipos = db.relationship("Ecuestre", back_populates="equipo")
    inserted_at = db.Column(db.DateTime, nullable=True, default=datetime.now)

    def __repr__(self):
        return f'<Equipo #{self.id} nombre="{self.nombre} {self.apellido}">'


def get_total(parametro):
    total = Equipo.query.filter(
        or_(
            Equipo.nombre.like(f"%{parametro}%"),
            Equipo.apellido.like(f"%{parametro}%"),
            cast(Equipo.dni, String).like(f"%{parametro}%"),
            Equipo.email.like(f"%{parametro}%"),
            Equipo.puesto.like(f"%{parametro}%"),
        )
    ).count()

    return total


def list_equipos_page(query, page, amount_per_page, order, by):

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
            )
        )
        .order_by(order_by)
        .paginate(page=page, per_page=amount_per_page)
    )

    return equipos


def create_equipo(**kwargs):
    equipo = Equipo(**kwargs)
    db.session.add(equipo)
    db.session.commit()

    return equipo


def toggle_a(id):
    chosen_equipo = Equipo.query.get(id)
    chosen_equipo.activo = not (chosen_equipo.activo)
    db.session.commit()


def get_one(id):
    chosen_equipo = Equipo.query.get(id)
    
    return chosen_equipo

def edit(id,data):
    chosen_equipo = Equipo.query.get(id)

    for key, value in data.items():
        if key in ["fecha_inicio", "fecha_fin"] and value == '':
            value = None

        if hasattr(chosen_equipo, key):
            setattr(chosen_equipo, key, value)

    db.session.commit()