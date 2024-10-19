from src.core.bcrypt import bcrypt
from src.core.user import User, Role, RolePermission, Permission

def find_user_by_email(usermail):
    return User.query.filter_by(email = usermail).first()

def check_user(usermail, password):
    '''
    Si el usuario existe y las contraseñas coinciden devuelve el usuario, sino devuelve None
    '''
    usuario = find_user_by_email(usermail)
    if (usuario and bcrypt.check_password_hash(usuario.password,password)):
        return usuario
    else:
        return None
