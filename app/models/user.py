from app.extensions import db, bcrypt
from app.models.intereses_usuario import intereses_usuarios  

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    apellido = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)  
    contrasena = db.Column(db.String(200), nullable=False)  
    rol_id = db.Column(db.Integer)
    centro_id = db.Column(db.Integer, db.ForeignKey('centros.id'))
    sector_id = db.Column(db.Integer, db.ForeignKey('sectores.id'))
    refuerzo_linguistico = db.Column(db.Boolean)
    penascal_rol = db.Column(db.String(100))
    fecha_alta = db.Column(db.Date, nullable=True)
    fecha_baja = db.Column(db.Date, nullable=True)
    
    # rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  
    # rol = db.relationship('Rol', backref='usuarios')
    
    
    # intereses = db.relationship(
    #      'Interes',
    #      secondary=intereses_usuarios,
    #      back_populates='usuarios'
    #  )
    
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "intereses": [interes.to_dict() for interes in self.intereses]
        }


 # Relaciones
    centro = db.relationship('Centro', backref='usuarios')
    sector = db.relationship('Sector', backref='usuarios')

    def set_password(self, contrasena):
        self.contrasena = bcrypt.generate_password_hash(contrasena).decode('utf-8')

    def check_password(self, contrasena):
        return bcrypt.check_password_hash(self.contrasena, contrasena)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "rol_id": self.rol_id,
            "centro_id": self.centro_id,
            "centro_nombre": self.centro.nombre if self.centro else None,
            "sector_id": self.sector_id,
            "sector_nombre": self.sector.nombre if self.sector else None,
            "refuerzo_linguistico": self.refuerzo_linguistico,
            "penascal_rol": self.penascal_rol,
            "fecha_alta": self.fecha_alta.isoformat() if self.fecha_alta else None,
            "fecha_baja": self.fecha_baja.isoformat() if self.fecha_baja else None,
        }

