from src.models import Base, session
from sqlalchemy import Column,Integer, Boolean, String, ForeignKey, Date
from sqlalchemy.orm import relationship




class Certificado(Base):
    __tablename__ = 'certificado'
    
    id = Column(Integer(), primary_key=True)
    estudiante_id = Column(Integer, ForeignKey('estudiante.id'), nullable=False)
    archivo_pdf = Column(String(255), nullable=True)  # O puedes usar una ruta de archivo

    estudiante = relationship('Estudiantes', back_populates='certificados')