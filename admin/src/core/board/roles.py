from datetime import datetime
from core.database import db


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user = db.relationship("User", secondary="role")
    
    def __repr__(self):
        return f'<User #{self.id} email="{self.email}">'
