from src.core import user
from src.web.controllers import find_user_by_email

def is_authenticated(session):
    return session.get("user") is not None

def check_permission(session, permission):
    user_mail = session.get("user")
    print("MAIL",user_mail)
    usuario = find_user_by_email(user_mail)
    print("user email",usuario)
    permissions = user.get_permissions(usuario)
    print("permisos",permissions)    print(usuario)
    print(permissions)

    return usuario is not None and permission in permissions