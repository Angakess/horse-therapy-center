import string

from sqlalchemy import and_, or_
import bcrypt
from core.database import db
from core.user.users import User
from core.user.roles import Permission, Role, RolePermission




PERMISSIONS = {
    "Administración": [
        "users_index",
        "users_activar_usuario",
        "users_edit_user",
        "users_delete_user_controller",
        "users_register_user",
        #"create_user",
        #"update_user",
        #"delete_user",
        #"list_roles",
        #"create_role",
        #"delete_role",
        #"assign_role",
        #"unassign_role",
        "equipo_index",
        "equipo_toggle_activate",
        "equipo_get_profile",
        "equipo_enter_edit",
        "equipo_save_edit",
        "equipo_enter_add",
        "equipo_add_equipo",
        "equipo_download_archivo",
        "equipo_delete",
        "jya_index",
        "jya_get_profile",
        "jya_enter_add",
        "jya_add_jya",
        "jya_delete",
        "jya_enter_edit",
        "jya_save_edit",
        "ecuestre_index",
        "ecuestre_get_profile",
    ],
    "Voluntariado": [
    ],
    "Técnica": [
        "jya_index",
        "jya_get_profile",
        "jya_enter_add",
        "jya_add_jya",
        "jya_delete",
        "jya_enter_edit",
        "jya_save_edit",
        "ecuestre_index",
        "ecuestre_get_profile",
    ],
    "Ecuestre": [
        "jya_index",
        "jya_get_profile",
        "ecuestre_index",
        "ecuestre_get_profile",
        "ecuestre_enter_edit",
        "ecuestre_save_edit",
        "ecuestre_enter_add",
        "ecuestre_add_ecuestre",
        "ecuestre_delete",
    ],
}

def get_permissions(user):
    return PERMISSIONS[user.role.name]

def list_users():
    users = User.query.all()
    return users




def create_user(**kwargs):
    email = kwargs.get('email')
    User.validate_unique_email(email)
    password = kwargs.get('password')
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    kwargs['password'] = hashed_password.decode('utf-8')

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


def search_users(email=None, role=None, active=None, page=1, per_page=25,sort_by='email', order='asc'):
    """Funcion que busca usuarios por cualquiera de los 3 parametros recibidos"""
    users_query = User.query
    

    if email:
        users_query = users_query.filter(User.email.ilike(f"%{email}%"))

    if role:
        users_query = users_query.join(Role).filter(Role.name == role)
    
    if active is not None:
        users_query = users_query.filter(User.enabled == active)

    if sort_by == 'inserted_at':
        users_query = users_query.order_by(User.inserted_at.asc() if order == 'asc' else User.inserted_at.desc())
    else:  
        users_query = users_query.order_by(User.email.asc() if order == 'asc' else User.email.desc())
    
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

def list_roles():
    roles = Role.query.all()
    return roles


def create_permission(name):
    #agregar validación(?
    permission = Permission(name)
    db.session.add(permission)
    db.session.commit()
    return permission



def assign_permission(role, permission):
    permission_role = RolePermission(role,permission)
    db.session.add(permission_role)
    db.session.commit()
