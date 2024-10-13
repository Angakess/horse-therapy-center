from sqlalchemy import String
from core.database import db


class Archivo(db.Model):
    __tablename__ = "archivos"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    equipo_id = db.Column(db.Integer, db.ForeignKey("equipos.id"))
    equipo = db.relationship("Equipo", back_populates="archivos")
