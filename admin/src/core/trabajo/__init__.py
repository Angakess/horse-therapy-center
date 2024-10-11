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

    dia = db.Column(db.Enum(
        'Lunes',
        'Martes',
        'Miércoles',
        'Jueves',
        'Viernes',
        'Sábado',
        'Domingo',
        name='dia_enum'
    ), nullable=False)

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