from app.extensions import db

class Centro(db.Model):
    __tablename__ = 'centros'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre
        }
