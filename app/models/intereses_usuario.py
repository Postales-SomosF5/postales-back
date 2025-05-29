#intereses_usuario.py
from app.extensions import db

intereses_usuarios = db.Table(
    'intereses_usuarios',
    db.Column('id_interes', db.Integer, db.ForeignKey('intereses.id'), primary_key=True),
    db.Column('id_usuario', db.Integer, db.ForeignKey('usuarios.id'), primary_key=True),
    db.Column('otros_descripcion', db.String(255))
)

