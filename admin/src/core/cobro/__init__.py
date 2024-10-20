from datetime import datetime
from core.database import db
from sqlalchemy import and_, asc, desc, or_


class MedioDePago(db.Model):
    __tablename__ = "medios_de_pago"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    #cobro = db.relationship("Cobro", back_populates="mediosDePago", lazy = 'dynamic')
    cobros = db.relationship('Cobro', back_populates='medio_pago')

    def __repr__(self):
        return f'<Cobro #{self.id} - Medio: {self.medio_pago.name}>'
    

def create_medio_pago(**kwargs):
    """
    Función que crea un nuevo medio de pago con los datos proporcionados.
    Parameters: kwargs(diccionario), parámetros para crear el medio de pago.
    Returns: medio de pago (objeto Medio de pago), medio de pago creado.
    """

    medio_pago = MedioDePago(**kwargs)
    db.session.add(medio_pago)
    db.session.commit()

    return medio_pago

def get_total_medio():
    """
    Función que obtiene el total de medios de pago
    """
    total = MedioDePago.query.filter().count()

    return total

def list_medio_de_pago():

    mediosDePago = (
        MedioDePago.query.filter()
    )

    return mediosDePago


def get_one_medio(id):
    """
    Función que obtiene un medio de pago por su id.
    Parameters: id(int), id del medio a buscar.
    Returns: chosen_cobro (objeto Cobro), medio encontrado.
    Raises: ValueError si el medio no se encuentra.
    """
    chosen_medio = MedioDePago.query.get(id)

    if not chosen_medio:
        raise ValueError("No se encontró el cobro seleccionado")

    return chosen_medio

class Cobro(db.Model):
    __tablename__ = "cobros"
    id = db.Column(db.Integer, primary_key=True)
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    observaciones = db.Column(db.Text, nullable=False)

    medio_pago_id = db.Column(db.Integer, db.ForeignKey('medios_de_pago.id'), nullable=False)
    medio_pago = db.relationship('MedioDePago', back_populates='cobros')

    #jya que paga
    jya_id = db.Column(db.Integer, db.ForeignKey("JinetesYAmazonas.id"), nullable=False)
    jya = db.relationship('JinetesAmazonas', back_populates='cobros')

    #Miembro del equipo que recibe el dinero
    equipo_id = db.Column(db.Integer, db.ForeignKey("equipos.id"), nullable=False)
    equipo = db.relationship('Equipo', back_populates='cobros')




def create_cobro(**kwargs):
    """
    Función que crea un nuevo Cobro con los datos proporcionados.
    Parameters: kwargs(diccionario), parámetros para crear el cobro.
    Returns: cobro (objeto Cobro), cobro creado.
    """
    if kwargs.get("fecha") == "":
        kwargs["fecha"] = None

    cobro = Cobro(**kwargs)
    db.session.add(cobro)
    db.session.commit()

    return cobro


def list_cobros_page(amount, page, f_min, f_max, order):
    """
    Función que lista cobros paginados según los filtros y parámetros proporcionados.
    Parameters: amount(int), cantidad de cobros por página.
                page(int), número de la página a mostrar.
                f_min(datetime), fecha mínima del filtro.
                f_max(datetime), fecha máxima del filtro.
                tipos(list), lista de tipos de cobro a filtrar.
                order(string "asc" o "desc"), orden del listado.
    Returns: cobros (Paginator), página de cobros.
    """

    order_by_fecha = asc(Cobro.fecha) if order == "asc" else desc(Cobro.fecha)

    cobros = (
        Cobro.query.filter(Cobro.fecha >= f_min, Cobro.fecha <= f_max)
        .order_by(order_by_fecha)
        .paginate(page=page, per_page=amount)
    )

    return cobros


def get_total(f_min, f_max):
    """
    Función que obtiene el total de cobros que cumplen con los filtros proporcionados.
    Parameters: f_min(datetime), fecha mínima del filtro.
                f_max(datetime), fecha máxima del filtro.
    Returns: total (int), cantidad total de cobros.
    """
    total = Cobro.query.filter(Cobro.fecha >= f_min, Cobro.fecha <= f_max).count()

    return total


def get_one(id):
    """
    Función que obtiene un cobro por su id.
    Parameters: id(int), id del cobro a buscar.
    Returns: chosen_cobro (objeto Cobro), cobro encontrado.
    Raises: ValueError si el cobro no se encuentra.
    """
    chosen_cobro = Cobro.query.get(id)

    if not chosen_cobro:
        raise ValueError("No se encontró el cobro seleccionado")

    return chosen_cobro



def edit(id, data):
    """
    Función que edita un cobro existente con los datos proporcionados.
    Parameters: id(int), id del cobro a editar.
                data(dict), diccionario con los nuevos valores a asignar.
    Returns: chosen_cobro (objeto Cobro), cobro actualizado.
    Raises: ValueError si el cobro no se encuentra.
    """
    chosen_cobro = Cobro.query.filter_by(id=id).first()

    if not chosen_cobro:
        raise ValueError("No se encontró el cobro seleccionado")

    for key, value in data.items():
        if key in ["fecha"] and value == "":
            value = None

        if hasattr(chosen_cobro, key):
            setattr(chosen_cobro, key, value)

    db.session.commit()
    return chosen_cobro


def delete_cobro(cobro_id):
    """
    Función que elimina un cobro por su id.
    Parameters: cobro_id(int), id del cobro a eliminar.
    Raises: ValueError si el cobro no se encuentra.
    """
    chosen_cobro = Cobro.query.get(cobro_id)

    if not chosen_cobro:
        raise ValueError("No se encontró el cobro seleccionado")

    db.session.delete(chosen_cobro)
    db.session.commit()

