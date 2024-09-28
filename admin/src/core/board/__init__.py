from core.board.users import User
from core.database import db
from core.board.equipos import Equipo
from core.board.roles import Role


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


# esto lo voy a mover, pero no me estaba tomando las rutas
def crate_user(**kwargs):
    existing_user = User.query.filter_by(email=kwargs.get('email')).first()
    
    if existing_user:
        raise ValueError("El correo electrónico ya está registrado")
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()

    return user


def create_role(**kwargs):
    role = Role(**kwargs)
    db.session.add(role)
    db.session.commit()

    return role


def asign_role(user, role):
    user.role = role
    db.session.add(user)
    db.session.commit()