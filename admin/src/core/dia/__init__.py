from core.database import db
from sqlalchemy import String

class Dia(db.Model):
    tablename = 'dia'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(9), nullable = False)

    trabajo_id = db.Column(db.Integer, db.ForeignKey("TrabajoInstitucion.id"))
    trabajo = db.relationship("Trabajo", back_populates="dia")

def create_dia(**kwargs):
    dia = Dia(**kwargs)
    db.session.add(dia)
    db.session.commit()
    return dia