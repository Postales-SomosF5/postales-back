# app/models/centro.py
from app.extensions import db

class Centro(db.Model):
    __tablename__ = 'centros'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))

    # Relación many-to-many con Sectores
    sectores = db.relationship('Sector', secondary='centros_sectores', back_populates='centros')

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'sectores': [sector.to_dict() for sector in self.sectores]  # opcional: incluir sectores en dict
        }