from core.database import db
from datetime import datetime

class Ecuestre(db.Model):
    __tablename__ = "Ecuestres"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(40), nullable=False)
    fecha_nacimiento = db.Column(db.DateTime, nullable=False)
    sexo = db.Column(db.String(40), nullable=False)
    raza = db.Column(db.String(40), nullable=False)
    pelaje = db.Column(db.String(40), nullable=False)
    sede_asignada = db.Column(db.String(40), nullable=False)
    #entrenadores_conductores
    #tipo_j&a_asignados
    inserted_at = db.Column(db.DateTime, defautl = datetime.now)
    updated_at = db.Column(db.DateTime, default = datetime.now, onupdate = datetime.now)

    def __repr__(self):
        return f'<Nombre "{self.nombre}," Fecha nacimiento "{self.fecha_nacimiento}," Sexo "{self.sexo}," Raza "{self.raza}," Pelaje "{self.pelaje}," Sede Asignada: {self.sede_asignada}>'

def list_ecuestres():
    ecuestres = Ecuestre.query.all()
    return ecuestres

def create_ecuestre(**kwargs):
    ecuestre = Ecuestre(**kwargs)
    db.session.add(ecuestre)
    db.session.commit()
    return ecuestre

def delete_ecuestre(ecuestre):
    db.session.delete(ecuestre)
    db.session.commit()

def ecuestre_by_name(nombre_ecuestre):
    ecuestre = db.select(Ecuestre).filter_by(nombre = nombre_ecuestre)
    return ecuestre