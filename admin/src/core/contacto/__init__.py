from datetime import datetime
from core.database import db

class Consulta(db.Model):
    __tablename__ = "consulta"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    nya = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100),nullable=False)
    cuerpo = db.Column(db.Text,nullable=False)
    fecha = db.Column(db.DateTime,default=datetime.now, nullable=False)
    estado = db.Column(db.Enum("Pendiente", "Resuelta", name="estado"), nullable=True)
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

def list_consultas():
    consultas = Consulta.query.all()
    return consultas

def search_consultas( estado=None, page=1, per_page=25, order='asc'):
    '''
        Función que busca consultas por el parametro estado, pagina y ordena el resultado
        Parameters: estado(string),  page(int), per_page(int),  order(string)
        Returns: consultas
    '''
    consulta_query = Consulta.query
    
    if estado:
        consulta_query = consulta_query.filter(Consulta.estado == estado)

    consulta_query = consulta_query.order_by(Consulta.fecha.asc() if order == 'asc' else Consulta.fecha.desc())

    consultas = consulta_query.paginate(page=page, per_page=per_page)

    return consultas

def delete_consulta(id):
    '''
        Función que realiza baja física de un usuario del sistema
        Parameters: user_id(int)
        Raises: ValueError si el usuario no existe o es sys_admin
    '''
    consulta = Consulta.query.get(id)
    if not consulta:
        raise ValueError("La consulta no existe")
    if consulta.estado=="Pendiente":
        raise ValueError("No se puede eliminar una consulta pendiente")
    
    db.session.delete(consulta)
    db.session.commit()
    


def get_one(id):
    """
    Función que obtiene una Consulta por su id.
    Parameters: id(int), id de la consulta a buscar.
    Returns: query (objeto Consulta), consulta encontrada.
    Raises: ValueError si el equipo no se encuentra.
    """
    query = Consulta.query.filter_by(id=id).first()

    if not query:
        raise ValueError("No se encontró la consulta seleccionada")

    return query



def edit(id, data):
    """
    Función que edita una Consulta existente con los datos proporcionados.
    Parameters: id(int), id de la consulta a editar.
                data(dict), diccionario con los nuevos valores a asignar.
    Raises: ValueError si la consulta no se encuentra.
    """
    query = Consulta.query.filter_by(id=id).first()

    if not query:
        raise ValueError("No se encontró la consulta seleccionada")

    for key, value in data.items():
        if hasattr(query, key):
            setattr(query, key, value)

    db.session.commit()
