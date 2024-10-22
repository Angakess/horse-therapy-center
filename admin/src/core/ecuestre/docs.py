from datetime import datetime
from sqlalchemy import String
from core.database import db


class Docs_Ecuestre(db.Model):
    __tablename__ = "docs_Ecuestre"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.Text, nullable=False)
    inserted_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    es_archivo = db.Column(db.Boolean, default=False, nullable=False)

    ecuestre_id = db.Column(db.Integer, db.ForeignKey("Ecuestre.id"))
    ecuestre = db.relationship("Ecuestre", back_populates="docs")
