from app.extensions import db
from datetime import date

class Emparejamiento(db.Model):
    __tablename__ = 'emparejamientos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_a_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    usuario_b_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    fecha_emparejamiento = db.Column(db.Date, default=date.today)
    estado = db.Column(db.Integer, default=1)  # 1 = activo
    fecha_fin = db.Column(db.DateTime, nullable=True)

    usuario_a = db.relationship("Usuario", foreign_keys=[usuario_a_id])
    usuario_b = db.relationship("Usuario", foreign_keys=[usuario_b_id])

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_a_id": self.usuario_a_id,
            "usuario_b_id": self.usuario_b_id,
            "fecha_emparejamiento": str(self.fecha_emparejamiento),
            "estado": self.estado,
            "fecha_fin": self.fecha_fin.isoformat() if self.fecha_fin else None,
            "usuario_a_nombre": self.usuario_a.nombre if self.usuario_a else None,
            "usuario_a_apellido": self.usuario_a.apellido if self.usuario_a else None,
            "usuario_b_nombre": self.usuario_b.nombre if self.usuario_b else None,
            "usuario_b_apellido": self.usuario_b.apellido if self.usuario_b else None

        }
