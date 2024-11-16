from datetime import datetime
from core.database import db
from sqlalchemy import and_, asc, desc, or_, String, cast
from core.user.users import User


class EstadoDeContenido(db.Model):
    __tablename__ = "estado_de_contenido"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    contenido = db.relationship('Contenido', back_populates='estado')

    def __repr__(self):
        return f'<Estado #{self.id} - Nombre: {self.name}>'
    

def create_estado(**kwargs):
    """
    Función que crea un nuevo estado con los datos proporcionados.
    Parameters: kwargs(diccionario), parámetros para crear el estado.
    Returns: estado (objeto Estado), estado creado.
    """

    estado = EstadoDeContenido(**kwargs)
    db.session.add(estado)
    db.session.commit()

    return estado

def get_one_estado_by_id(id):
    """
    Función que obtiene un estado por su id.
    Parameters: id(int), id del estado a buscar.
    Returns: estado (objeto Estado), estado encontrado.
    Raises: ValueError si el estado no se encuentra.
    """
    chosen_estado = EstadoDeContenido.query.get(id)

    if not chosen_estado:
        raise ValueError("No se encontró el estado seleccionado")

    return chosen_estado

def get_one_estado_by_name(estado):
    """
    Función que obtiene un estado por su nombre.
    Parameters: estado(string), nombre del estado a buscar.
    Returns: estado (objeto Estado), estado encontrado.
    Raises: ValueError si el estado no se encuentra.
    """
    chosen_estado = EstadoDeContenido.query.filter(EstadoDeContenido.name.ilike(f"{estado}")).first()

    if not chosen_estado:
        raise ValueError("No se encontró el estado seleccionado")

    return chosen_estado

def list_estados():
    """
    Devuelve todos los estados cargados en la base de datos
    """
    estados = (
        EstadoDeContenido.query.filter()
    )

    return estados

class Contenido(db.Model):
    __tablename__ = "contenido"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(30), nullable=False)
    copete = db.Column(db.Text, nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    autor = db.Column(db.String(50), nullable=False)
    fecha_de_publicacion = db.Column(db.DateTime, nullable=True)
    fecha_de_creacion = db.Column(db.DateTime, nullable=False)
    fecha_de_actualizacion = db.Column(db.DateTime, nullable=False)

    autor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    autor = db.relationship('User', back_populates='contenido')

    estado_id = db.Column(db.Integer, db.ForeignKey('estado_de_contenido.id'), nullable=False)
    estado = db.relationship('EstadoDeContenido', back_populates='contenido')


def create_contenido(**kwargs):
    """
    Función que crea un nuevo Contenido con los datos proporcionados.
    Parameters: kwargs(diccionario), parámetros para crear el contenido.
    Returns: contenido (objeto Contenido), contenido creado.
    """
    kwargs["fecha_de_creacion"] = datetime.now()
    kwargs["fecha_de_actualizacion"] = kwargs["fecha_de_creacion"]

    contenido = Contenido(**kwargs)
    db.session.add(contenido)
    db.session.commit()

    return contenido


def list_contenidos_page(amount, page, f_min, f_max, order, query, estados):
    """
    Función que lista contenidos paginados según los filtros y parámetros proporcionados.
    Parameters: amount(int), cantidad de ccontenidos por página.
                page(int), número de la página a mostrar.
                f_min(datetime), fecha mínima de creacion del filtro.
                f_max(datetime), fecha máxima de creacion del filtro.
                order(string "asc" o "desc"), orden del listado.
                medios(list), lista de estados a filtrar.
                query, string por el cual buscar coincidencias en el nombre del autor del contenido.
    Returns: contenidos (Paginator), página de contenidos.
    """

    order_by_fecha = asc(Contenido.fecha_de_creacion) if order == "asc" else desc(Contenido.fecha_de_creacion)

    contenidos = Contenido.query

    contenidos = (
        contenidos.join(User)
    )

    if estados:
        contenidos = (
            contenidos.join(EstadoDeContenido)
        )
    contenidos = contenidos.filter(
        User.alias.ilike(f"%{query}%")
    )
    contenidos = contenidos.filter(
        Contenido.fecha_de_creacion >= f_min, Contenido.fecha_de_creacion <= f_max
    )

    if estados:
        contenidos = contenidos.filter(
            EstadoDeContenido.name.in_(estados)
        )

    contenidos = contenidos.order_by(order_by_fecha).paginate(
        page=page, per_page=amount
    )

    return contenidos


def get_total(f_min, f_max):
    """
    Función que obtiene el total de contenidos que cumplen con los filtros proporcionados.
    Parameters: f_min(datetime), fecha mínima del filtro.
                f_max(datetime), fecha máxima del filtro.
    Returns: total (int), cantidad total de contenidos.
    """
    total = Contenido.query.filter(Contenido.fecha_de_creacion >= f_min, Contenido.fecha_de_creacion <= f_max).count()

    return total


def get_one(id):
    """
    Función que obtiene un contenido por su id.
    Parameters: id(int), id del contenido a buscar.
    Returns: chosen_contenido (objeto Contenido), contenido encontrado.
    Raises: ValueError si el contenido no se encuentra.
    """
    chosen_contenido = Contenido.query.get(id)

    if not chosen_contenido:
        raise ValueError("No se encontró el contenido seleccionado")

    return chosen_contenido


def edit(id, data):
    """
    Función que edita un contenido existente con los datos proporcionados.
    Parameters: id(int), id del contenido a editar.
                data(dict), diccionario con los nuevos valores a asignar.
    Returns: chosen_contenido (objeto Contenido), contenido actualizado.
    Raises: ValueError si el contenido no se encuentra.
    """
    chosen_contenido = Contenido.query.filter_by(id=id).first()

    if not chosen_contenido:
        raise ValueError("No se encontró el contenido seleccionado")
    


    for key, value in data.items():
        if key in ["fecha_de_publicacion"] and value == "":
            value = None

        if hasattr(chosen_contenido, key):
            setattr(chosen_contenido, key, value)

    chosen_contenido.fecha_de_actualizacion = datetime.now()

    db.session.commit()
    return chosen_contenido


def delete_contenido(contenido_id):
    """
    Función que elimina un contenido por su id.
    Parameters: contenido_id(int), id del contenido a eliminar.
    Raises: ValueError si el contenido no se encuentra.
    """
    chosen_contenido = Contenido.query.get(contenido_id)

    if not chosen_contenido:
        raise ValueError("No se encontró el contenido seleccionado")

    db.session.delete(chosen_contenido)
    db.session.commit()

def set_estado(id, estado):
    """
    Esta función setea el valor del estado de contenido
    (identificado por el id) en el el string estado del parámetro estado
    (Si es que existe un estado que se llame así)
    """
    contenido = Contenido.query.get(id)
    if not contenido:
        raise ValueError("No se encontró al contenido seleccionado")

    chosen_estado = get_one_estado_by_name(estado)
    if not chosen_estado:
        raise ValueError("No existe un estado con ese nombre")
        
    contenido.estado = chosen_estado
    if (estado == "Publicado") & (contenido.fecha_de_publicacion == None):
        contenido.fecha_de_publicacion = datetime.now()
    db.session.commit()
    return contenido
