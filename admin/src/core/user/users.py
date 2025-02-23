from datetime import datetime
from core.database import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=True)
    enabled = db.Column(db.Boolean, default=True, nullable=False)
    system_admin = db.Column(db.Boolean, default=False, nullable=False)
    inserted_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    role = db.relationship("Role", back_populates="users")

    contenido = db.relationship("Contenido", back_populates="autor")

    def __repr__(self):
        return f'<User #{self.id} email="{self.email}">'

    @staticmethod
    def validate_unique_email(email):
        """
        Valida que el email sea único.
        Parameters: email(string)
        Raises: ValueError si el email ya está en uso.
        """
        if User.query.filter_by(email=email).first() is not None:
            raise ValueError("El correo electrónico ya está registrado")

    def activate_user(self):
        """
        Valida que el usuario pueda ser activado.
        Parameters: self(user)
        Raises: ValueError si el user es sys admin.
        """
        if self.system_admin:
            raise ValueError("El usuario System Admin no puede ser desactivado.")
        self.enabled = True
        db.session.commit()

    def deactivate_user(self):
        """
        Valida que el usuario pueda ser desactivado.
        Parameters: self(user)
        Raises: ValueError si el user es sys admin.
        """
        if self.system_admin:
            raise ValueError("El usuario System Admin no puede ser desactivado.")
        self.enabled = False
        db.session.commit()
