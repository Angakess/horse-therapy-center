from core.database import db
from datetime import datetime

class JinetesAmazonas(db.Model):
    __tablename__ = 'JinetesYAmazonas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(40), nullable=False)
    apellido = db.Column(db.String(40), nullable=False)
    dni = db.Column(db.Integer, nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    fecha_nacimiento = db.Column(db.DateTime, nullable=False)
    lugar_nacimiento = db.Column(db.Text, nullable=False)
    domicilio_actual = db.Column(db.Text, nullable=False)
    telefono_actual = db.Column(db.Text, nullable=False)
    contacto_emergencia = tel = db.Column(db.Text, nullable=False)
    tel = db.Column(db.Text, nullable=False)
    becado = tel = db.Column(db.Boolean, nullable=False)
    porcentaje_beca = tel = db.Column(db.Double, nullable=False)
    profesionales_atienden = db.Column(db.Text, nullable=False)
    j_y_a = db.relationship("Ecuestre", back_populates=("j_y_a"))

def list_jinetes_amazonas():
    jinetes_amazonas = JinetesAmazonas.query.all()
    return jinetes_amazonas

def create_jinetes_amazonas(**kwargs):
    jinetes_amazonas = JinetesAmazonas(**kwargs)
    db.session.add(jinetes_amazonas)
    db.session.commit()
    return jinetes_amazonas

def delete_jinetes_amazonas(jinetes_amazonas):
    db.session.delete(jinetes_amazonas)
    db.session.commit()

def jinetes_amazonas_by_name(nombre_jinetes_amazonas):
    jinetes_amazonas = db.select(JinetesAmazonas).filter_by(nombre = nombre_jinetes_amazonas)
    return jinetes_amazonas

def jinetes_amazonas_by_apellido(apellido_jinetes_amazonas):
    jinetes_amazonas = db.select(JinetesAmazonas).filter_by(apellido = apellido_jinetes_amazonas)
    return jinetes_amazonas

def jinetes_amazonas_by_dni(dni_jinetes_amazonas):
    jinetes_amazonas = db.select(JinetesAmazonas).filter_by(dni = dni_jinetes_amazonas)
    return jinetes_amazonas

def jinetes_amazonas_by_profesionales(profesionales_jinetes_amazonas):
    jinetes_amazonas = db.select(JinetesAmazonas).filter_by(profesionales = profesionales_jinetes_amazonas)
    return jinetes_amazonas