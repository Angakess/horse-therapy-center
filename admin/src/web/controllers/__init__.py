from src.core.bcrypt import bcrypt

users = {
    "pepe": bcrypt.generate_password_hash("argento").decode("utf-8"),
    "homero": bcrypt.generate_password_hash("simpson").decode("utf-8")
}

def user_exists(usermail):
    try:
        asd = users[usermail]
        print(asd)
        return True
    except:
        return False
    

def find_user_by_email(usermail, password):
    #A ESTO DESP HAY QUE CAMBIARLO CON LA BASE DE DATOS
    if user_exists(usermail):
        class User:
            def __init__(self, usermail, password):
                self.usermail = usermail
                self.password = password
        user = User(usermail, users[usermail])
        return user
    else:
        return None

def check_user(usermail, password):
    user = find_user_by_email(usermail, password)
    #checkeo la contraseña usando bcrypt para hashearla
    if (user and bcrypt.check_password_hash(user.password,password)):
        return user
    else:
        return None
