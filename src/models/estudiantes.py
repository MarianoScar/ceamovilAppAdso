from sqlalchemy import Column, Integer, String, Date, Enum
from src.models import Base, session
import enum
from sqlalchemy_serializer import SerializerMixin

class Curso(enum.Enum):
    MOTO = "Moto"
    AUTOMOVIL = "Automovil"
    CAMION = "Camion"

class Estudiantes(Base, SerializerMixin):
    __tablename__ = "estudiantes"    
    id = Column(Integer, primary_key=True)    
    nombre = Column(String(100), unique=False, nullable=False)
    tipo_identificacion = Column(String(20), unique=False, nullable=False)
    numero_identificacion = Column(Integer(), unique=True, nullable=False)
    #direccion = Column(String(300), unique=False, nullable=False)
    telefono = Column(Integer(), unique=False, nullable=False)
    email = Column(String(50), unique=False, nullable=False)
    curso = Column(Enum(Curso), nullable=False)
    fecha_nacimiento = Column(Date)

    def __init__(self, nombre, tipo_identificacion, numero_identificacion, telefono, email, curso, fecha_nacimiento):
        self.nombre = nombre
        self.tipo_identificacion = tipo_identificacion
        self.numero_identificacion = numero_identificacion
        #self.direccion = direccion
        self.telefono = telefono
        self.email = email
        self.curso = curso
        self.fecha_nacimiento = fecha_nacimiento

    def agregar_estudiante(estudiante):
        estudiante = session.add(estudiante)
        session.commit()
        return estudiante
    
    def obtener_estudiante():
        estudiante = session.query(Estudiantes).all()
        return estudiante    
    
    def obtener_estudiante_por_id(id):
        estudiante = session.query(Estudiantes).get(id)
        return estudiante.to_dict() if estudiante else None
