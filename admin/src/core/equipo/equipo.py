from datetime import datetime
from core.database import db
from core.relacion_equipo_ecuestre import equipo_ecuestre


class Equipo(db.Model):
    __tablename__ = "equipos"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    dni = db.Column(db.Integer, nullable=False)
    dir = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    localidad = db.Column(db.String(100), nullable=False)
    tel = db.Column(db.Text, nullable=False)
    profesion = db.Column(db.Text, nullable=False)
    puesto = db.Column(db.Text, nullable=False)
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=True)
    contacto_emergencia_nombre = db.Column(db.Text, nullable=False)
    contacto_emergencia_tel = db.Column(db.Text, nullable=False)
    obra_social = db.Column(db.Text, nullable=False)
    num_afiliado = db.Column(db.Text, nullable=False)
    condicion = db.Column(db.Text, nullable=False)
    activo = db.Column(db.Boolean, nullable=False, default=True)
    borrado = db.Column(db.Boolean, nullable=False, default=False)

    ecuestres = db.relationship(
        "Ecuestre", secondary=equipo_ecuestre, back_populates="equipos", lazy="dynamic"
    )

    profesor_terapeuta_trabajo = db.relationship(
        "Trabajo",
        back_populates="profesor_terapeuta",
        foreign_keys="Trabajo.profesor_terapeuta_id",
    )
    conductor_trabajo = db.relationship(
        "Trabajo", back_populates="conductor", foreign_keys="Trabajo.conductor_id"
    )
    auxiliar_pista_trabajo = db.relationship(
        "Trabajo",
        back_populates="auxiliar_pista",
        foreign_keys="Trabajo.auxiliar_pista_id",
    )

    inserted_at = db.Column(db.DateTime, nullable=True, default=datetime.now)

    archivos = db.relationship("Archivo", back_populates="equipo")

    pagos = db.relationship("Pago", back_populates="beneficiario")

    cobros = db.relationship("Cobro", back_populates="equipo")

    def __repr__(self):
        return f'<Equipo #{self.id} nombre="{self.nombre} {self.apellido}">'
