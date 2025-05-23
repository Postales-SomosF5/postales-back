from app.extensions import db

class Interes(db.Model):
    __tablename__ = 'intereses'

    id = db.Column(db.Integer, primary_key=True)
    descripcion_castellano = db.Column(db.String(255))
    description_english = db.Column(db.String(255))

    def to_dict(self):
        return {
            'id': self.id,
            'descripcion_castellano': self.descripcion_castellano,
            'description_english': self.description_english
        }
