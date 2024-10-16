from sqlalchemy import String
from core.database import db


class Archivo_Ecuestre(db.Model):
    __tablename__ = "archivos_ecuestre"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    ecuestre_id = db.Column(db.Integer, db.ForeignKey("Ecuestre.id"))
    ecuestre = db.relationship("Ecuestre", back_populates="archivos")