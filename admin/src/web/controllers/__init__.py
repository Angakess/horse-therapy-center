
users = {
    "pepe": "argento",
    "homero": "simpson"
}

def find_user_by_email_and_password(usermail, password):
    #A ESTO DESP HAY QUE CAMBIARLO CON LA BASE DE DATOS
    print(usermail, password)
    try:
        if users[usermail] == password:
            class User:
                def __init__(self, usermail, password):
                    self.usermail = usermail
                    self.password = password
            user = User(usermail, password)
            return user
        else:
            return None
    except:
        return None
