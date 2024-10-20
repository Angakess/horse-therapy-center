from sqlalchemy import String
from core.database import db


class Archivo_JineteAmazonas(db.Model):
    __tablename__ = "archivos_JineteAmazonas"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    JineteAmazonas_id = db.Column(db.Integer, db.ForeignKey("JinetesYAmazonas.id"))
    JineteAmazonas = db.relationship("JinetesAmazonas", back_populates="archivos")