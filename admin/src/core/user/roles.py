from datetime import datetime
from core.database import db


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    users = db.relationship("User", back_populates="role")
    role_permissions = db.relationship('RolePermission', back_populates='role')


    def __repr__(self):
        return f'<Role #{self.id} name="{self.name}">'
    
    VALID_ROLES = {"Técnica", "Ecuestre", "Voluntariado", "Administración"}

    @staticmethod
    def validate_role_name(name):
        """Valida que el nombre del rol esté en la lista de roles permitidos."""
        if name not in Role.VALID_ROLES:
            raise ValueError(f"El rol '{name}' no es valido. Los roles permitidos son: {', '.join(Role.VALID_ROLES)}.")



class RolePermission(db.Model):
    __tablename__ = 'role_permissions'
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True)
    role = db.relationship("Role", back_populates="role_permissions")

    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
    permission = db.relationship("Permission", back_populates="role_permissions")

    def __init__(self, role_id, permission_id):
        self.role_id= role_id
        self.permission_id= permission_id

class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    role_permissions = db.relationship('RolePermission', back_populates='permission')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Permission #{self.id} name="{self.name}">'
