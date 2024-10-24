from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from src.models import Base
from sqlalchemy_serializer import SerializerMixin

class InstanciaCurso(Base, SerializerMixin ):
    __tablename__ = 'instancias_curso'
    
    id = Column(Integer, primary_key=True)
    curso_id = Column(Integer, ForeignKey('cursos.id'), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    
    curso = relationship('Curso', back_populates='instancias')

     # Esta es la relacion con el modelo Inscripciones
    inscripciones = relationship('Inscripcion', back_populates='instancia_curso')
