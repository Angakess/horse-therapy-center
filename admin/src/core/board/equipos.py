from datetime import datetime
from core.database import db


class Equipo(db.Model):
    __tablename__ = 'equipos'
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
    contacto_emergencia = db.Column(db.Text, nullable=False)
    obra_social = db.Column(db.Text, nullable=False)
    num_afiliado = db.Column(db.Text, nullable=False)
    condicion = db.Column(db.Text, nullable=False)
    activo = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<Equipo #{self.id} nombre="{self.nombre} {self.apellido}">'
