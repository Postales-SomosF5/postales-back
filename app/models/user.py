from app.extensions import db, bcrypt

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    apellido = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)  
    contrasena = db.Column(db.String(200), nullable=False)  
    rol_id = db.Column(db.Integer)
    centro_id = db.Column(db.Integer)
    sector_id = db.Column(db.Integer)
    refuerzo_linguistico = db.Column(db.Boolean)
    penascal_rol = db.Column(db.String(100))
    fecha_alta = db.Column(db.Date, nullable=True)
    fecha_baja = db.Column(db.Date, nullable=True)
    # rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  
    # rol = db.relationship('Rol', backref='usuarios')


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
            "sector_id": self.sector_id,
            "refuerzo_linguistico": self.refuerzo_linguistico,
            "penascal_rol": self.penascal_rol,
            "fecha_alta": self.fecha_alta.isoformat() if self.fecha_alta else None,
            "fecha_baja": self.fecha_baja.isoformat() if self.fecha_baja else None,
        }

