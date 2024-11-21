from core.bcrypt import bcrypt
from core.user import User, Role, RolePermission, Permission


def find_user_by_email(usermail):
    user = User.query.filter_by(email=usermail).first()
    if user.role_id == 5:
        raise ValueError("La cuenta sigue en estado de revisión")
    return user


def check_user(usermail, password):
    """
    Si el usuario existe y las contraseñas coinciden devuelve el usuario, sino devuelve None
    """
    usuario = find_user_by_email(usermail)
    if (not usuario) or (
        not (
            usuario.password and bcrypt.check_password_hash(usuario.password, password)
        )
    ):
        raise ValueError("Usuario y/o contraseña incorrecta")
    return usuario
