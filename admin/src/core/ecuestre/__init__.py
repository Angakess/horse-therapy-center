from core.database import db
from datetime import datetime
from sqlalchemy import asc, desc, or_
from core.relacion_equipo_ecuestre import equipo_ecuestre
from core.jya import JinetesAmazonas
from core.trabajo import Trabajo
from .docs import Docs_Ecuestre


class Ecuestre(db.Model):
    __tablename__ = "Ecuestre"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(40), nullable=False)
    fecha_nacimiento = db.Column(db.DateTime, nullable=False)
    sexo = db.Column(db.String(40), nullable=False)
    raza = db.Column(db.String(40), nullable=False)
    pelaje = db.Column(db.String(40), nullable=False)
    tipo_adquisicion = db.Column(
        db.Enum("Compra", "Donación", name="tipo_adquisicion"), nullable=False
    )
    fecha_ingreso = db.Column(db.DateTime, nullable=False)
    sede_asignada = db.Column(db.String(40), nullable=False)

    equipos = db.relationship(
        "Equipo", secondary=equipo_ecuestre, back_populates="ecuestres", lazy="dynamic"
    )

    j_y_a_id = db.Column(
        db.Integer, db.ForeignKey("JinetesYAmazonas.id", name="fk_ecuestre_jya_id")
    )
    j_y_a = db.relationship("JinetesAmazonas", back_populates="j_y_a")

    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    caballo_trabajo = db.relationship("Trabajo", back_populates="caballo")

    def __repr__(self):
        return f'<Nombre "{self.nombre}," Fecha nacimiento "{self.fecha_nacimiento}," Sexo "{self.sexo}," Raza "{self.raza}," Pelaje "{self.pelaje}," Sede Asignada: {self.sede_asignada}>'

    docs = db.relationship("Docs_Ecuestre", back_populates="ecuestre")

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


def delete_ecuestre(id):
    ecuestre = Ecuestre.query.get(id)
    if ecuestre:
        db.session.delete(ecuestre)
        db.session.commit()
    else:
        pass


def edit_ecuestre(id, data):
    chosen_ecuestre = Ecuestre.query.get(id)
    for key, value in data.items():
        if hasattr(chosen_ecuestre, key):
            setattr(chosen_ecuestre, key, value)
    db.session.commit()


def get_ecuestre(id):
    chosen_ecuestre = Ecuestre.query.get(id)
    return chosen_ecuestre


def list_ecuestres_page(query, page, amount_per_page, order, by, jya):

    sort_column = {
        "nombre": Ecuestre.nombre,
        # "jineteamazona": Ecuestre.j_y_a.trabajo.propuestra_trabajo_institucional,
    }.get(by, Ecuestre.id)

    order_by = asc(sort_column) if order == "asc" else desc(sort_column)
    ecuestres = Ecuestre.query
    print("jinetes", jya)

    if jya:
        ecuestres = (
            ecuestres.join(JinetesAmazonas)
            .join(Trabajo)
            .filter(Trabajo.propuestra_trabajo_institucional == jya)
        )

    if query:
        ecuestres = ecuestres.filter(Ecuestre.nombre.ilike(f"%{query}%"))

    ecuestres = ecuestres.order_by(order_by).paginate(
        page=page, per_page=amount_per_page
    )

    return ecuestres


def ecuestre_by_name(nombre_ecuestre):
    ecuestre = db.select(Ecuestre).filter_by(nombre=nombre_ecuestre)
    return ecuestre


def assing_equipo(ecuestre, equipo):
    if equipo not in ecuestre.equipos:
        ecuestre.equipos.append(equipo)
        db.session.add(ecuestre)
        db.session.commit()
    return ecuestre


def unassing_equipo(ecuestre, equipo):
    if equipo in ecuestre.equipos:
        ecuestre.equipos.remove(equipo)
        db.session.commit()
    else:
        raise ValueError("El equipo no está asociado con este ecuestre.")


def assing_j_y_a(ecuestre, j_y_a):
    ecuestre.j_y_a = j_y_a
    db.session.add(ecuestre)
    db.session.commit()
    return ecuestre


def unassing_j_y_a(ecuestre, j_y_a):
    if j_y_a in ecuestre.j_y_a:
        ecuestre.equipos.remove(j_y_a)
        db.session.commit()
    else:
        raise ValueError("El jinete/amazona no está asociado con este ecuestre.")


def create_archivo(**kwargs):
    archivo = Docs_Ecuestre(**kwargs)
    db.session.add(archivo)
    db.session.commit()
    return archivo


def assign_archivo(ecuestre, archivo):
    ecuestre.docs.append(archivo)
    db.session.add(ecuestre)
    db.session.commit()
    return archivo


def get_archivo(id):
    archivo = Docs_Ecuestre.query.get(id)
    if not archivo:
        raise (ValueError("No se encontró el archivo solicitado"))
    return archivo


def delete_archivo(id):
    archivo = Docs_Ecuestre.query.get(id)
    if not archivo:
        raise (ValueError("No se encontró el archivo solicitado para borrar"))
    else:
        db.session.delete(archivo)
        db.session.commit()


def get_total_ecuestre():
    total = Ecuestre.query.filter().count()
    return total


def contiene_miembro_equipo(ecuestre, equipo_id):
    for equipo in ecuestre.equipos:
        if equipo.id == equipo_id:
            return True
    return False

def get_total_docs(ecuestre_id, query, tipos):
    if tipos:
        total = Docs_Ecuestre.query.filter(
            Docs_Ecuestre.nombre.like(f"%{query}%"),
            Docs_Ecuestre.tipo.in_(tipos),
            Docs_Ecuestre.ecuestre_id == ecuestre_id,
        ).count()
    else:
        total = Docs_Ecuestre.query.filter(
            Docs_Ecuestre.nombre.like(f"%{query}%"),
            Docs_Ecuestre.ecuestre_id == ecuestre_id,
        ).count()

    return total

def list_archivos_page(ecuestre_id, query, order, tipos, by, pag, amount_per_page):

    chosen_ecuestre = Ecuestre.query.get(ecuestre_id)
    if not chosen_ecuestre:
        raise (ValueError("No se encontró el ecuestre solicitado "))

    sort_column = {
        "nombre": Docs_Ecuestre.nombre,
        "inserted_at": Docs_Ecuestre.inserted_at,
    }.get(by, Docs_Ecuestre.id)

    order_by = asc(sort_column) if order == "asc" else desc(sort_column)

    if tipos:
        chosen_archivos = (
            Docs_Ecuestre.query.filter(
                Docs_Ecuestre.nombre.like(f"%{query}%"),
                Docs_Ecuestre.tipo.in_(tipos),
                Docs_Ecuestre.ecuestre_id == ecuestre_id,
            )
            .order_by(order_by)
            .paginate(page=pag, per_page=amount_per_page)
        )
    else:
        chosen_archivos = (
            Docs_Ecuestre.query.filter(
                Docs_Ecuestre.nombre.like(f"%{query}%"),
                Docs_Ecuestre.ecuestre_id == ecuestre_id,
            )
            .order_by(order_by)
            .paginate(page=pag, per_page=amount_per_page)
        )

    return chosen_archivos