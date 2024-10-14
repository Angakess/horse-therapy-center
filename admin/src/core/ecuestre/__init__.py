from core.database import db
from datetime import datetime
from sqlalchemy import asc, desc

class Ecuestre(db.Model):
    __tablename__ = 'Ecuestre'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(40), nullable=False)
    fecha_nacimiento = db.Column(db.DateTime, nullable=False)
    sexo = db.Column(db.String(40), nullable=False)
    raza = db.Column(db.String(40), nullable=False)
    pelaje = db.Column(db.String(40), nullable=False)
    tipo_adquisicion = db.Column(db.Enum(
        'Compra',
        'Donación',
        name = 'tipo_adquisicion'
    ), nullable=False)
    fecha_ingreso = db.Column(db.DateTime, nullable=False)
    sede_asignada = db.Column(db.String(40), nullable=False)

    equipo_id = db.Column(db.Integer, db.ForeignKey("equipos.id", name="fk_ecuestre_equipo_id"))
    equipo = db.relationship("Equipo", back_populates="equipos")

    j_y_a_id = db.Column(db.Integer, db.ForeignKey("JinetesYAmazonas.id", name="fk_ecuestre_jya_id"))
    j_y_a = db.relationship("JinetesAmazonas", back_populates="j_y_a")

    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    caballo_trabajo = db.relationship("Trabajo", back_populates="caballo")


    def __repr__(self):
        return f'<Nombre "{self.nombre}," Fecha nacimiento "{self.fecha_nacimiento}," Sexo "{self.sexo}," Raza "{self.raza}," Pelaje "{self.pelaje}," Sede Asignada: {self.sede_asignada}>'

def list_ecuestres():
    ecuestres = Ecuestre.query.all()
    return ecuestres

def list_ecuestres_nombre_asc():
    ecuestres = Ecuestre.query.order_by(asc(Ecuestre.nombre)).all()
    return ecuestres 

def list_ecuestres_nombre_desc():
    ecuestres = Ecuestre.query.order_by(desc(Ecuestre.nombre)).all()
    return ecuestres    

def list_ecuestres_fecha_nacimiento_asc():
    ecuestres = Ecuestre.query.order_by(asc(Ecuestre.fecha_nacimiento)).all()
    return ecuestres    

def list_ecuestres_fecha_nacimiento_desc():
    ecuestres = Ecuestre.query.order_by(desc(Ecuestre.fecha_nacimiento)).all()
    return ecuestres

def list_ecuestres_fecha_ingreso_asc():
    ecuestres = Ecuestre.query.order_by(asc(Ecuestre.fecha_ingreso)).all()
    return ecuestres    

def list_ecuestres_fecha_ingreso_desc():
    ecuestres = Ecuestre.query.order_by(desc(Ecuestre.fecha_ingreso)).all()
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

def assing_equipo(ecuestre, equipo):
    ecuestre.equipo = equipo
    db.session.add(ecuestre)
    db.session.commit()
    return ecuestre

def assing_j_y_a(ecuestre, j_y_a):
    ecuestre.j_y_a = j_y_a
    db.session.add(ecuestre)
    db.session.commit()
    return ecuestre