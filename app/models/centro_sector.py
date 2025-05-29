# app/models/centros_sectores.py
from app.extensions import db

centros_sectores = db.Table(
    'centros_sectores',
    db.Column('centro_id', db.Integer, db.ForeignKey('centros.id'), primary_key=True),
    db.Column('sector_id', db.Integer, db.ForeignKey('sectores.id'), primary_key=True)
)