from src.core import user
from src.web.controllers import find_user_by_email

def is_authenticated(session):
    return session.get("user") is not None

def check_permission(session, permission):
    user_mail = session.get("user")
    usuario = find_user_by_email(user_mail)
    if (usuario.system_admin == True):
        return True
    permissions = user.get_permissions(usuario)

    return usuario is not None and permission in permissions