from core.database import db
from sqlalchemy import Enum

class Familiar_tutor(db.Model):
    __tablename__ = 'FamiliarOTutor'
    id = db.Column(db.Integer, primary_key = True)
    parentesco = db.Column(db.Text, nullable = False)
    nombre = db.Column(db.Text, nullable = False)
    apellido = db.Column(db.Text, nullable = False)
    dni = db.Column(db.Integer, nullable = False)
    domicilio_actual = db.Column(db.Text, nullable = False)
    celular_actual = db.Column(db.Text, nullable = False)
    email = db.Column(db.Text, nullable = False)
    nivel_escolaridad = db.Column(db.Enum(
        'Primario',
        'Secundario',
        'Terciario',
        'Universitario',
        name='nivel_escolaridad'
    ), nullable = False)
    actividad_ocupacion = db.Column(db.Text, nullable = False)

    j_y_a_id = db.Column(db.Integer, db.ForeignKey("JinetesYAmazonas.id"))
    j_y_a = db.relationship("JinetesAmazonas", back_populates=("parentesco_tutor"))

def create_parentesco_tutor(**kwargs):
    parentesco_tutor = Familiar_tutor(**kwargs)
    db.session.add(parentesco_tutor)
    db.session.commit()
    return parentesco_tutor

def get_responsable(id):
    responsable = Familiar_tutor.query.filter_by(id=id).first()
    if not responsable:
        raise ValueError("No se encontró al responsable seleccionado")
    return responsable

def delete_responsable(id):
    responsable = Familiar_tutor.query.get(id)
    if responsable:
        db.session.delete(responsable)
        db.session.commit()
    else:
        raise ValueError("No se encontro responsable a borrar")
    
def existe(dni):
    return Familiar_tutor.query.filter_by(dni=dni).first()
