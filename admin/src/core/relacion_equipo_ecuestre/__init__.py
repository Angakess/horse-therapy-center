from core.database import db
from sqlalchemy import Table

equipo_ecuestre = db.Table(
    'equipo_ecuestre',
    db.Column('equipo_id', db.Integer, db.ForeignKey('equipos.id'), primary_key=True),
    db.Column('ecuestre_id', db.Integer, db.ForeignKey('Ecuestre.id'), primary_key=True),
)
