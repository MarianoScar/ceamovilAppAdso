from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.models import Base
from datetime import datetime

class Inscripcion(Base):
    __tablename__ = 'inscripcion'
    
    id = Column(Integer, primary_key=True)
    estudiante_id = Column(Integer, ForeignKey('estudiantes.id'), nullable=False)
    instancia_curso_id = Column(Integer, ForeignKey('instancia_curso.id'), nullable=False)
    fecha_inscripcion = Column(DateTime, default=datetime.utcnow)
    
    estudiante = relationship('Estudiantes', back_populates='inscripciones')
    instancia_curso = relationship('InstanciaCurso', back_populates='inscripciones')
    asistencias = relationship('Asistencia', back_populates='inscripcion')
    
   
    certificado = relationship('Certificado', uselist=False, back_populates='inscripcion')
