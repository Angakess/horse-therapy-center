from core.database import db
from core.board.equipos import Equipo


def list_issues():
    issues = [
        {
        "id": 1,
        "title": "Issue 1",
        "status": "Nuevo",
        }
    ]
    return issues

def list_equipos():
    equipos = Equipo.query.all()

    return equipos

def create_equipo(**kwargs):
    equipo = Equipo(**kwargs)
    db.session.add(equipo)
    db.session.commit()

    return equipo


