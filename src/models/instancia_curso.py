from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import relationship
from src.models import Base, session
from datetime import datetime, timedelta 





TEMAS_CLASES = [
    "Introducción y normas básicas",
    "Señalización vial",
    "Seguridad y equipos obligatorios",
    "Documentación y requisitos",
    "Mantenimiento básico del vehículo",
    "Conducción en ciudad",
    "Conducción en carretera",
    "Estacionamiento y maniobras",
    "Condiciones climáticas adversas",
    "Conducción defensiva",
    "Ley de tránsito y multas",
    "Uso de tecnología en la conducción",
    "Responsabilidad del conductor",
    "Emergencias y primeros auxilios",
    "Examen y revisión final"
]


class InstanciaCurso(Base):
    __tablename__ = 'instancia_curso'
    
    id = Column(Integer(), primary_key=True)
    curso_id = Column(Integer(), ForeignKey('curso.id'), nullable=False)
    instructor_id = Column(Integer(), ForeignKey('instructor.id'), nullable=True)
    fecha_inicio = Column(Date, nullable=False)
    fecha_final = Column(Date, nullable=False)
    
    curso = relationship('Curso', back_populates='instancias') 
    instructor = relationship('Instructor', back_populates='cursos_impartidos')  
    inscripciones = relationship('Inscripcion', back_populates='instancia_curso', cascade="all, delete-orphan")
    clases = relationship('Clase', back_populates='instancia_curso', cascade="all, delete-orphan")

    def __init__(self, curso_id, fecha_inicio, instructor_id=None):
        self.curso_id = curso_id
        self.fecha_inicio = fecha_inicio
        self.instructor_id = instructor_id
        self.fecha_final = self.fecha_inicio + timedelta(days=14)  # Calcular la fecha final

    def programar_clases(self):
        from src.models.clase import Clase
        for i in range(15):
            fecha_clase = self.fecha_inicio + timedelta(days=i)
            tema = TEMAS_CLASES[i]
            clase = Clase(instancia_curso_id=self.id, fecha=fecha_clase, tema=tema)
            session.add(clase)
            session.commit()  # Mover el commit aquí para que se realice después de agregar todas las clases










