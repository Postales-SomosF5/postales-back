# app/models/sector.py
from app.extensions import db

class Sector(db.Model):
    __tablename__ = 'sectores'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))

    # Relación many-to-many con Centros
    centros = db.relationship('Centro', secondary='centros_sectores', back_populates='sectores')

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre
        }