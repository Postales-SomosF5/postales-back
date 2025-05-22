from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    contrasena = Column(String(255), nullable=False)
    rol_id = Column(Integer, ForeignKey('roles.id'))
    centro_id = Column(Integer, ForeignKey('centros.id'))
    sector_id = Column(Integer, ForeignKey('sectores.id'))
    refuerzo_linguistico = Column(Boolean, default=False)
    penascal_rol = Column(String(100))
    fecha_alta = Column(Date)
    fecha_baja = Column(Date)
