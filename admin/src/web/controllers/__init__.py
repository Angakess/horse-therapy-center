from src.core.bcrypt import bcrypt
from src.core.user import User

def check_user(usermail, password):
    '''
    Si el usuario existe y las contraseñas coinciden devuelve el usuario, sino devuelve None
    '''
    usuario = User.query.filter_by(email = usermail).first()
    if (usuario and bcrypt.check_password_hash(usuario.password,password)):
        return usuario
    else:
        return None
