import string

from sqlalchemy import and_, or_
import bcrypt
from core.database import db
from core.user.users import User
from core.user.roles import Permission, Role, RolePermission


def get_permissions(user):
    user_role = user.role.name
    a = (
        db.session.query(Permission.name)
        .join(RolePermission)
        .join(Role)
        .filter(Role.name == user_role)
        .all()
    )
    flat_permisos = tuple(item for sublist in a for item in sublist)
    return flat_permisos


def list_users():
    """Función que devuelve una lista de usuarios"""
    users = User.query.all()
    return users


def create_user(**kwargs):
    """
    Función que crea un usuario válido y hashea su contraseña
    Parameters: kwargs(parametros para crear user)
    Returns: user
    Raises: ValueError propagado por validate_unique_email si el mail no es único
    """
    email = kwargs.get("email")
    User.validate_unique_email(email)
    password = kwargs.get("password")
    if password:
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        kwargs["password"] = hashed_password.decode("utf-8")

    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()
    return user


def delete_user(user_id):
    """
    Función que realiza baja física de un usuario del sistema
    Parameters: user_id(int)
    Raises: ValueError si el usuario no existe o es sys_admin
    """

    user = User.query.get(user_id)
    if not user:
        raise ValueError("El usuario no existe")
    if user.system_admin:
        raise ValueError("No puedes eliminar a un usuario administrador del sistema.")
    db.session.delete(user)
    db.session.commit()


def update_user(user_id, **kwargs):
    """
    Función que realiza una actualización del usuario
    Parameters: kwargs(parametros a modificar de user), user_id(int)
    Returns: user
    """
    user = User.query.get(user_id)

    for key, value in kwargs.items():
        if hasattr(user, key):
            setattr(user, key, value)

    db.session.commit()
    return user


def search_users(
    email=None,
    role=None,
    active=None,
    page=1,
    per_page=25,
    sort_by="email",
    order="asc",
):
    """
    Función que busca usuarios por 3 parametros(mail,role y active) pagina y ordena el resultado
    Parameters: email(string), role(string), active(string), page(int), per_page(int), sort_by(string), order(string)
    Returns: users
    """
    users_query = User.query

    if email:
        users_query = users_query.filter(User.email.ilike(f"%{email}%"))

    if role:
        users_query = users_query.join(Role).filter(Role.name == role)

    if active is not None:
        users_query = users_query.filter(User.enabled == active)

    if sort_by == "inserted_at":
        users_query = users_query.order_by(
            User.inserted_at.asc() if order == "asc" else User.inserted_at.desc()
        )
    else:
        users_query = users_query.order_by(
            User.email.asc() if order == "asc" else User.email.desc()
        )

    users = users_query.paginate(page=page, per_page=per_page)

    return users


def create_role(**kwargs):
    """
    Función que crea un rol válido
    Parameters: kwargs(parametros para crear rol)
    Returns: rol
    Raises: ValueError propagado por validate_role_name si el role no está permitido
    """
    role_name = kwargs.get("name")
    Role.validate_role_name(role_name)
    role = Role(**kwargs)
    db.session.add(role)
    db.session.commit()
    return role


def assign_role(user, role):
    """Funcion que asigna un rol a un usuario ya validados"""
    user.role = role
    db.session.add(user)
    db.session.commit()


def delete_role(role_id):
    """
    Función que borra un rol fisicamente
    Parameters: role_id(int)
    Raises: ValueError si el rol no existe o tiene usuarios asociados
    """
    role = Role.query.get(role_id)

    if not role:
        raise ValueError("El rol no existe.")

    if role.users:
        raise ValueError(
            "No se puede eliminar el rol porque hay usuarios asociados a él."
        )

    db.session.delete(role)
    db.session.commit()


def unassign_role(user):
    """
    Funcion que desasigna un rol a un usuario
    Raise: ValueError si el usuario no tiene rol
    """
    if not user.role:
        raise ValueError("El usuario no tiene rol")

    user.role = None
    db.session.add(user)
    db.session.commit()


def list_roles():
    """'Función que devuelve una lista de roles"""
    roles = Role.query.all()
    return roles


def create_permission(name):
    # agregar validación(?
    permission = Permission(name)
    db.session.add(permission)
    db.session.commit()
    return permission


def assign_permission(role, permission):
    permission_role = RolePermission(role, permission)
    db.session.add(permission_role)
    db.session.commit()
