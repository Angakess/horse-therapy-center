from core.database import db
from sqlalchemy import Enum
from sqlalchemy import asc
from sqlalchemy import desc
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
    contacto_emergencia = db.Column(db.Text, nullable=False)
    tel = db.Column(db.Text, nullable=False)
    becado = db.Column(db.Boolean, nullable=False)
    porcentaje_beca = db.Column(db.Double, nullable=False)
    profesionales_atienden = db.Column(db.Text, nullable=False)
    certificado_discapacidad = db.Column(db.Boolean, nullable=False)
    asignacion_familiar = db.Column(db.Boolean, nullable=False)

    tipo_asignacion_familiar = db.Column(db.Enum(
        'Universal por hijo',
        'Universal por hijo con discapacidad',
        'Ayuda escolar anual',
        name='tipo_asignacion_familiar'
    ), nullable=True)

    beneficiario_pension = db.Column(db.Boolean, nullable=False)
    beneficiario_pension_tipo = db.Column(db.Enum(
        'Provincial',
        'Nacional',
        name='beneficiario_pension_tipo'
    ), nullable=True)

    discapacidad = db.Column(db.Enum(
        'ECNE',
        'Lesión post-traumática',
        'Mielomeningocele',
        'Esclerosis Múltiple',
        'Escoliosis Leve',
        'Secuelas de ACV',
        'Discapacidad Intelectual',
        'Trastorno del Espectro Autista',
        'Trastorno del Aprendizaje',
        'Trastorno por Déficit de Atención/Hiperactividad',
        'Trastorno de la Comunicación',
        'Trastorno de Ansiedad',
        'Síndrome de Down',
        'Retraso Madurativo',
        'Psicosis',
        'Trastorno de Conducta',
        'Trastornos del ánimo y afectivos',
        'Trastorno Alimentario',
        'OTRO',
        name='discapacidad'
    ), nullable=True)

    otra_discapacidad = db.Column(db.Text, nullable=True)
    tipo_discapacidad = db.Column(db.Enum(
        'Mental',
        'Motora',
        'Sensorial',
        'Visceral',
        name='tipo_discapacidad'
    ), nullable=True)

    j_y_a = db.relationship("Ecuestre", back_populates="j_y_a")

    situacion_previsional_id = db.Column(db.Integer, db.ForeignKey("situacion_previsional.id"))
    situacion_previsional = db.relationship("Situacion_previsional", back_populates="j_y_a")

    institucion_escolar_id = db.Column(db.Integer, db.ForeignKey("InstitucionEscolar.id"))
    institucion_escolar = db.relationship("Institucion_escolar", back_populates="j_y_a")

    parentesco_tutor = db.relationship("Familiar_tutor", back_populates="j_y_a", lazy = 'dynamic')

    trabajo_id = db.Column(db.Integer, db.ForeignKey("TrabajoInstitucion.id"))
    trabajo = db.relationship("Trabajo", back_populates="j_y_a")


def list_jinetes_amazonas():
    jinetes_amazonas = JinetesAmazonas.query.all()
    return jinetes_amazonas

def list_jinetes_amazonas_nombre_asc():
    jinetes_amazonas = JinetesAmazonas.query.order_by(asc(JinetesAmazonas.nombre)).all()
    return jinetes_amazonas

def list_jinetes_amazonas_nombre_desc():
    jinetes_amazonas = JinetesAmazonas.query.order_by(desc(JinetesAmazonas.nombre)).all()
    return jinetes_amazonas

def list_jinetes_amazonas_apellido_asc():
    jinetes_amazonas = JinetesAmazonas.query.order_by(asc(JinetesAmazonas.apellido)).all()
    return jinetes_amazonas

def list_jinetes_amazonas_apellido_desc():
    jinetes_amazonas = JinetesAmazonas.query.order_by(desc(JinetesAmazonas.apellido)).all()
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

def assing_situacion_previsional(jya,situacion_previsional):
    jya.situacion_previsional = situacion_previsional
    db.session.add(jya)
    db.session.commit()
    return jya

def assing_institucion_escolar(jya,institucion_escolar):
    jya.institucion_escolar = institucion_escolar
    db.session.add(jya)
    db.session.commit()
    return jya

def assing_parentesco_tutor(jya,parentesco_tutor):
    jya.parentesco_tutor.append(parentesco_tutor)
    db.session.add(jya)
    db.session.commit()
    return jya

def assing_trabajo(jya,trabajo):
    jya.trabajo = trabajo
    db.session.add(jya)
    db.session.commit()
    return jya