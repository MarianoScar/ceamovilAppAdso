from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import relationship
from src.models import Base

class Inscripcion(Base, SerializerMixin):
    __tablename__ = 'inscripciones'
    
    id = Column(Integer, primary_key=True)
    estudiante_id = Column(Integer, ForeignKey('estudiantes.id'), nullable=False)
    instancia_curso_id = Column(Integer, ForeignKey('instancias_curso.id'), nullable=False)
    
    # Esta es la relacion con el modelo  Estudiante
    estudiante = relationship('Estudiantes', back_populates='inscripciones')

    # Esta es la relacion con el modelo InstanciaCurso
    instancia_curso = relationship('InstanciaCurso', back_populates='inscripciones')
