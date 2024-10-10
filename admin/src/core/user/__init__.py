import string

from sqlalchemy import and_, or_
from core.database import db
from core.user.users import User
from core.user.roles import Role


def list_users():
    users = User.query.all()
    return users




def create_user(**kwargs):
    email = kwargs.get('email')
    User.validate_unique_email(email)
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()
    return user

def delete_user(user_id):
    """
    Baja fisica de un usuario del sistema, consultar si no sería mejor una lógica
    """
    
    user = User.query.get(user_id)
    if not user:
        raise ValueError("El usuario no existe")
    if user.system_admin:
        raise ValueError("No puedes eliminar a un usuario administrador del sistema.")
    db.session.delete(user)
    db.session.commit()

def update_user(user_id,**kwargs):
    user = User.query.get(user_id)

    for key, value in kwargs.items():
        if hasattr(user,key):
            setattr(user,key,value)
    
    db.session.commit()
    return user


def search_users(email=None, role=None, active=None, page=1, per_page=25):
    """Funcion que busca usuarios por cualquiera de los 3 parametros recibidos"""
    users_query = User.query
    

    print(f"query search: {email}, role: {role}, active: {active}")

    if email:
        users_query = users_query.filter(User.email.ilike(f"%{email}%"))

    if role:
        users_query = users_query.join(Role).filter(Role.name == role)
    
    if active is not None:
        print(active)
        users_query = users_query.filter(User.enabled == active)

    print(str(users_query)) 

    users = users_query.paginate(page=page, per_page=per_page)

    return users




def create_role(**kwargs):
    role_name = kwargs.get('name')
    Role.validate_role_name(role_name)
    role = Role(**kwargs)
    db.session.add(role)
    db.session.commit()
    return role   


def assign_role(user, role):
    user.role = role
    db.session.add(user)
    db.session.commit()

def delete_role(role_id):
    role = Role.query.get(role_id)
    
    if not role:
        raise ValueError("El rol no existe.")
    
    if role.users:
        raise ValueError("No se puede eliminar el rol porque hay usuarios asociados a él.")
    
    db.session.delete(role)
    db.session.commit()


def unassign_role(user):
    if not user.role:
        raise ValueError("El usuario no tiene rol")
    
    user.role=None
    db.session.add(user)
    db.session.commit()

