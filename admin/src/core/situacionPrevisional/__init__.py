from core.database import db

class Situacion_previsional(db.Model):
    __tablename__ = 'situacion_previsional'
    id = db.Column(db.Integer, primary_key=True)
    obra_social = db.Column(db.Text, nullable=False)
    nroafiliado = db.Column(db.Integer, nullable=False)
    curatela =  db.Column(db.Boolean, nullable=False)
    observaciones = db.Column(db.Text, nullable=True)
    j_y_a = db.relationship("JinetesAmazonas", back_populates=("situacion_previsional"))\
    
def create_situacion_previsional(**kwargs):
    situacion_previsional = Situacion_previsional(**kwargs)
    db.session.add(situacion_previsional)
    db.session.commit()
    return situacion_previsional

def get_situacion_previsional(id):
    choosed_situacion_previsional = Situacion_previsional.query.filter_by(id=id).first()
    if not choosed_situacion_previsional:
        raise ValueError("No se encontró la situación previsional seleccionada")
    return choosed_situacion_previsional

def delete_situacion_previsional(id):
    situacion_previsional = Situacion_previsional.query.get(id)
    if situacion_previsional:
        db.session.delete(situacion_previsional)
        db.session.commit()
    else:
        raise ValueError("No se encontro la situación previsional a borrar")
