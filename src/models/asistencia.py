from src.models import Base, session
from sqlalchemy import Column,Integer, Boolean, String, ForeignKey, Date
from sqlalchemy.orm import relationship




class Asistencia(Base):
    __tablename__ = 'asistencia'
    
    id = Column(Integer, primary_key=True)
    inscripcion_id = Column(Integer, ForeignKey('inscripcion.id'), nullable=False)
    clase_id = Column(Integer, ForeignKey('clase.id'), nullable=False)
    presente = Column(Boolean, default=False)
    
    inscripcion = relationship('Inscripcion', back_populates='asistencias')
    clase = relationship('Clase', back_populates='asistencias')

