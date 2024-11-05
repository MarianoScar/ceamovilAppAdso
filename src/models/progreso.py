""" from src.models import Base, session
from sqlalchemy import Column,Integer, Boolean, String, ForeignKey, Date
from sqlalchemy.orm import relationship




class ProgresoDiario(Base):
    __tablename__ = 'progreso_diario'
    
    id = Column(Integer(), primary_key=True)
    estudiante_id = Column(Integer(), ForeignKey('estudiante.id'), nullable=False)
    instancia_curso_id =Column(Integer(), ForeignKey('instancia_curso.id'), nullable=False)
    fecha = Column(Date, nullable=False)
    completado = Column(Boolean, default=False, nullable=False)

    estudiante = relationship('Estudiante', backref='progresos_diarios')
    instancia_curso = relationship('InstanciaCurso', backref='progresos_diarios')

    
    """