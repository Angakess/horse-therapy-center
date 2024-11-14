from datetime import datetime
from core.database import db

class Consulta(db.Model):
    __tablename__ = "consulta"
    id = db.Column(db.Integer, primary_key=True)
    nya = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100),nullable=False)
    cuerpo = db.Column(db.Text,nullable=False)
    fecha = db.Column(db.DateTime,default=datetime.now, nullable=False)
    estado = db.Column(db.Enum("Pendiente", "Resuelta", name="estado"), nullable=False)
    desc = db.Column(db.Text,nullable=True)

    def __repr__(self):
        return f'<Consulta #{self.id} email="{self.email} estado {self.estado}">'

    
def create_consulta(**kwargs):
    """
    Función que crea una nueva consulta con los datos proporcionados.
    Parameters: kwargs(diccionario), parámetros para crear la consulta.
    Returns: consulta (objeto Consulta), consulta creada.
    """
 
    consulta = Consulta(**kwargs)
    db.session.add(consulta)
    db.session.commit()

    return consulta


def delete_consulta(id):
    """
    Función que elimina un pago por su id.
    Parameters: pago_id(int), id del pago a eliminar.
    Raises: ValueError si el pago no se encuentra.
    """
    consulta = Consulta.query.get(id)

    if not consulta:
        raise ValueError("No se encontró la consulta seleccionada")

    db.session.delete(consulta)
    db.session.commit()

