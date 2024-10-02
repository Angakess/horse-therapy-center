from core.database import db
from core.equipo.equipos import Equipo


def list_equipos():
    equipos = Equipo.query.all()

    return equipos

def create_equipo(**kwargs):
    equipo = Equipo(**kwargs)
    db.session.add(equipo)
    db.session.commit()

    return equipo


