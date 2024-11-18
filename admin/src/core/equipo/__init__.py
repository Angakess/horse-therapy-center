from sqlalchemy import String, asc, cast, desc, or_, func
from core.database import db
from .equipo import Equipo
from .archivos import Archivo


def get_total(parametro=""):
    """
    Función que cuenta el total de Equipos (no borrados logicamente)
    Parameters: String parametro, tiene que matchear con nombre o apellido o dni, etc
    Returns: Int total, cantidad de Equipos
    """
    total = Equipo.query.filter(
        or_(
            Equipo.nombre.like(f"%{parametro}%"),
            Equipo.apellido.like(f"%{parametro}%"),
            cast(Equipo.dni, String).like(f"%{parametro}%"),
            Equipo.email.like(f"%{parametro}%"),
            Equipo.puesto.like(f"%{parametro}%"),
        ),
        Equipo.borrado == False,
    ).count()

    return total


def list_equipos_page(query="", page=1, amount_per_page=10, order="asc", by="id"):
    """
    Función que lista una pagina de Equipos segun parametros
    Parameters: query(tring), tiene que matchear con nombre o apellido o dni, etc.
                page(int), pagina deseada.
                amount_per_page(int), cantidad de elementos maximo por pagina.
                order(string "asc" o "desc"), orden del listado.
                by(string "nombre", "apellido" o "fecha"), parametro por el que se ordena la lista.
    Returns: equipos
    """

    sort_column = {
        "nombre": Equipo.nombre,
        "apellido": Equipo.apellido,
        "fecha": Equipo.inserted_at,
    }.get(by, Equipo.id)

    order_by = asc(sort_column) if order == "asc" else desc(sort_column)

    equipos = (
        Equipo.query.filter(
            or_(
                Equipo.nombre.like(f"%{query}%"),
                Equipo.apellido.like(f"%{query}%"),
                cast(Equipo.dni, String).like(f"%{query}%"),
                Equipo.email.like(f"%{query}%"),
                Equipo.puesto.like(f"%{query}%"),
            ),
            Equipo.borrado == False,
        )
        .order_by(order_by)
        .paginate(page=page, per_page=amount_per_page)
    )

    return equipos


def create_equipo(**kwargs):
    """
    Función que crea un Equipo segun parametros
    Parameters: kwargs(parametros para crear user)
    Returns: equipo
    """

    if kwargs.get("fecha_fin") == "":
        kwargs["fecha_fin"] = None
    if kwargs.get("fecha_inicio") == "":
        kwargs["fecha_inicio"] = None

    equipo = Equipo(**kwargs)
    db.session.add(equipo)
    db.session.commit()

    return equipo


def toggle_a(id):
    """
    Función que activa o desactiva un Equipo
    Parameters: id(int)
    Returns: chosen_equipo
    Raises: ValueError si el equipo no se encuentra
    """
    chosen_equipo = Equipo.query.filter_by(id=id, borrado=False).first()

    if not chosen_equipo:
        raise ValueError("No se encontró a la persona seleccionada")
    chosen_equipo.activo = not (chosen_equipo.activo)
    db.session.commit()


def get_one(id):
    """
    Función que obtiene un Equipo por su id.
    Parameters: id(int), id del equipo a buscar.
    Returns: chosen_equipo (objeto Equipo), equipo encontrado.
    Raises: ValueError si el equipo no se encuentra.
    """
    chosen_equipo = Equipo.query.filter_by(id=id, borrado=False).first()

    if not chosen_equipo:
        raise ValueError("No se encontró a la persona seleccionada")

    return chosen_equipo


def edit(id, data):
    """
    Función que edita un Equipo existente con los datos proporcionados.
    Parameters: id(int), id del equipo a editar.
                data(dict), diccionario con los nuevos valores a asignar.
    Raises: ValueError si el equipo no se encuentra.
    """
    chosen_equipo = Equipo.query.filter_by(id=id, borrado=False).first()

    if not chosen_equipo:
        raise ValueError("No se encontró a la persona seleccionada")

    for key, value in data.items():
        if key in ["fecha_inicio", "fecha_fin"] and value == "":
            value = None

        if hasattr(chosen_equipo, key):
            setattr(chosen_equipo, key, value)

    db.session.commit()


def create_archivo(**kwargs):
    """
    Función que crea un nuevo Archivo con los datos proporcionados.
    Parameters: kwargs(diccionario), parámetros para crear el archivo.
    Returns: archivo (objeto Archivo), archivo creado.
    """
    archivo = Archivo(**kwargs)
    db.session.add(archivo)
    db.session.commit()

    return archivo


def assign_archivo(equipo, archivo):
    """
    Función que asigna un archivo a un equipo.
    Parameters: equipo (objeto Equipo), equipo al cual asignar el archivo.
                archivo (objeto Archivo), archivo a asignar.
    Returns: archivo (objeto Archivo), archivo actualizado con la asignación.
    """
    archivo.equipo = equipo
    db.session.add(archivo)
    db.session.commit()

    return archivo


def get_archivo(id):
    """
    Función que obtiene un archivo por su id.
    Parameters: id(int), id del archivo a buscar.
    Returns: archivo (objeto Archivo), archivo encontrado.
    Raises: ValueError si el archivo no se encuentra.
    """
    archivo = Archivo.query.get(id)
    if not archivo:
        raise (ValueError("No se encontró el archivo solicitado"))

    return archivo


def delete_archivo(id):
    """
    Función que elimina un archivo por su id.
    Parameters: id(int), id del archivo a eliminar.
    Raises: ValueError si el archivo no se encuentra.
    """
    archivo = Archivo.query.get(id)
    if not archivo:
        raise (ValueError("No se encontró el archivo solicitado para borrar"))
    else:
        db.session.delete(archivo)
        db.session.commit()


def delete_equipo(id):
    """
    Función que marca un equipo como borrado (borrado lógico).
    Parameters: id(int), id del equipo a borrar.
    Returns: chosen_equipo (objeto Equipo), equipo marcado como borrado.
    Raises: ValueError si el equipo no se encuentra.
    """
    chosen_equipo = Equipo.query.get(id)
    if not chosen_equipo:
        raise ValueError("No se encontró a la persona seleccionada")
    else:
        chosen_equipo.borrado = True
        db.session.commit()

    return chosen_equipo


def list_equipos_apellido_asc():
    """
    Devuelve todos los equipos cargados en la base de datos ordenados por apellido
    """
    equipos = Equipo.query.order_by(Equipo.apellido.asc()).all()
    return equipos


def amount_per_puesto():
    resultados = (
        db.session.query(Equipo.puesto, func.count(Equipo.id).label("cantidad"))
        .filter(
            Equipo.activo == True, Equipo.borrado == False
        )  # Excluir empleados inactivos o borrados
        .group_by(Equipo.puesto)
        .order_by(Equipo.puesto)  # Opcional: ordena por el nombre del puesto
        .all()
    )

    return [{"puesto": puesto, "cant": cantidad} for puesto, cantidad in resultados]


def get_all():
    return Equipo.query.filter(Equipo.activo == True).all()
