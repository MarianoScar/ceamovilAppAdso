from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from src.models import Base
from sqlalchemy_serializer import SerializerMixin

class InstanciaCurso(Base, SerializerMixin ):
    __tablename__ = 'instancias_curso'
    
    id = Column(Integer, primary_key=True)
    curso_id = Column(Integer, ForeignKey('cursos.id'), nullable=False)
    instructor_id = Column(Integer, ForeignKey('instructores.id'), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    
    curso = relationship('Curso', back_populates='instancias')

    instructor = relationship('Instructor', back_populates='cursos_impartidos')

    inscripciones = relationship('Inscripcion', back_populates='instancia_curso')




    