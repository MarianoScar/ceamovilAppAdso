from sqlalchemy import Column, Integer, String, Date
from src.models import Base
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import relationship


class Estudiantes(Base):
    __tablename__ = "estudiantes"    
    id = Column(Integer, primary_key=True)    
    nombre = Column(String(100), nullable=False)
    tipo_identificacion = Column(String(20), nullable=False)
    numero_identificacion = Column(Integer, unique=True, nullable=False)
    telefono = Column(Integer, nullable=False)
    email = Column(String(50), nullable=False)
    fecha_nacimiento = Column(Date)

    
    inscripciones = relationship('Inscripcion', back_populates='estudiante', cascade="all, delete")
    certificados = relationship('Certificado', secondary='inscripcion', viewonly=True) 


    def __init__(self, nombre, tipo_identificacion, numero_identificacion, telefono, email, fecha_nacimiento):
        self.nombre = nombre
        self.tipo_identificacion = tipo_identificacion
        self.numero_identificacion = numero_identificacion
        self.telefono = telefono
        self.email = email
        self.fecha_nacimiento = fecha_nacimiento





   





  
