from core.database import db

class Trabajo(db.Model):
    __tablename__ = 'TrabajoInstitucion'
    id = db.Column(db.Integer, primary_key=True)
    propuestra_trabajo_institucional = db.Column(db.Enum(
        'Hipoterapia',
        'Monta terapéutica',
        'Deporte Ecuestre Adaptado',
        'Actividades recreativas',
        'Equitación',
        name='propuestra_trabajo_institucional_enum'
    ), nullable=False)

    condicion = db.Column(db.Enum(
        'Regular',
        'De baja',
        name='condicion_enum'
    ), nullable=False)

    sede = db.Column(db.Enum(
        'CASJ',
        'HLP',
        'Otro',
        name='sede_enum'
    ), nullable=False)

    lunes = db.Column(db.Boolean, nullable=False)
    martes =  db.Column(db.Boolean, nullable=False)
    miercoles =  db.Column(db.Boolean, nullable=False)
    jueves =  db.Column(db.Boolean, nullable=False)
    viernes = db.Column(db.Boolean, nullable=False)
    sabado =  db.Column(db.Boolean, nullable=False)
    domingo = db.Column(db.Boolean, nullable=False)

    profesor_terapeuta_id = db.Column(db.Integer, db.ForeignKey("equipos.id"))
    profesor_terapeuta = db.relationship("Equipo", back_populates="profesor_terapeuta_trabajo", foreign_keys=[profesor_terapeuta_id])

    conductor_id = db.Column(db.Integer, db.ForeignKey("equipos.id"))
    conductor = db.relationship("Equipo", back_populates="conductor_trabajo", foreign_keys=[conductor_id])

    auxiliar_pista_id = db.Column(db.Integer, db.ForeignKey("equipos.id"))
    auxiliar_pista = db.relationship("Equipo", back_populates="auxiliar_pista_trabajo", foreign_keys=[auxiliar_pista_id])

    caballo_id = db.Column(db.Integer, db.ForeignKey("Ecuestre.id"))
    caballo = db.relationship("Ecuestre", back_populates="caballo_trabajo")

    j_y_a = db.relationship("JinetesAmazonas", back_populates="trabajo")


def create_trabajo(**kwargs):
    trabajo = Trabajo(**kwargs)
    db.session.add(trabajo)
    db.session.commit()
    return trabajo

def assing_profesor(trabajo,profesor):
    trabajo.profesor_terapeuta = profesor
    db.session.add(trabajo)
    db.session.commit()
    return trabajo

def assing_conductor(trabajo,conductor):
    trabajo.conductor = conductor
    db.session.add(trabajo)
    db.session.commit()
    return trabajo

def assing_auxiliar_pista(trabajo,auxiliar_pista):
    trabajo.auxiliar_pista = auxiliar_pista
    db.session.add(trabajo)
    db.session.commit()
    return trabajo

def assing_caballo(trabajo,caballo):
    trabajo.caballo = caballo
    db.session.add(trabajo)
    db.session.commit()
    return trabajo

def get_trabajo(id):
    trabajo = Trabajo.query.filter_by(id=id).first()
    if not trabajo:
        raise ValueError("No se encontró el trabajo seleccionado")
    return trabajo

def delete_trabajo(id):
    trabajo = Trabajo.query.get(id)
    if trabajo:
        db.session.delete(trabajo)
        db.session.commit()
    else:
        raise ValueError("No se encontro el trabajo a borrar")
    
def edit_trabajo(id, **trabajo_data):
    trabajo = Trabajo.query.get(id)
    if trabajo:
        for key, value in trabajo_data.items():
            setattr(trabajo, key, value)
        db.session.commit()
    else:
        trabajo = create_trabajo(**trabajo_data)
    return trabajo