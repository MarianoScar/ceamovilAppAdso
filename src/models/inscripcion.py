
from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import relationship
from src.models import Base, session
from datetime import datetime, timedelta
from src.models.clase import Clase


class Inscripcion(Base):
    __tablename__ = 'inscripcion'
    
    id = Column(Integer(), primary_key=True)
    estudiante_id = Column(Integer(), ForeignKey('estudiante.id'), nullable=False)
    instancia_curso_id = Column(Integer(), ForeignKey('instancia_curso.id'), nullable=False)
    fecha_inscripcion = Column(DateTime, default=datetime.utcnow)
    
    estudiante = relationship('Estudiante', back_populates='inscripciones')
    instancia_curso = relationship('InstanciaCurso', back_populates='inscripciones')
    asistencias = relationship('Asistencia', back_populates='inscripcion')
    certificado = relationship('Certificado', uselist=False, back_populates='inscripcion')