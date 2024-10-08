from core.database import db

class Institucion_escolar(db.Model):
    __tablename__ = 'InstitucionEscolar'
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(40), nullable=False)
    direccion = db.Column(db.Text, nullable=False)
    telefono = db.Column(db.Text, nullable=False)
    grado_actual = db.Column(db.Integer, nullable=False)
    observaciones = db.Column(db.Text, nullable=True)

    j_y_a = db.relationship("JinetesAmazonas", back_populates=("institucion_escolar"))

def create_institucion_escolar(**kwargs):
    institucion_escolar = Institucion_escolar(**kwargs)
    db.session.add(institucion_escolar)
    db.session.commit()
    return institucion_escolar