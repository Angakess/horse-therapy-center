from core.database import db
from core.user.users import User
from core.user.roles import Role



def create_user(**kwargs):
    email = kwargs.get('email')
    User.validate_unique_email(email)
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()
    return user


def create_role(**kwargs):
    role = Role(**kwargs)
    db.session.add(role)
    db.session.commit()

    return role   


def assign_role(user, role):
    user.role = role
    db.session.add(user)
    db.session.commit()