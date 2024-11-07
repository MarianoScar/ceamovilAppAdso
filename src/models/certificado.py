from src.models import Base, session
from sqlalchemy import Column,Integer, Boolean, String, ForeignKey, Date
from sqlalchemy.orm import relationship




class Certificado(Base):
    __tablename__ = 'certificado'
    
    id = Column(Integer, primary_key=True)
    inscripcion_id = Column(Integer, ForeignKey('inscripcion.id'), nullable=False) 
    archivo_pdf = Column(String(255), nullable=True) 

    
    inscripcion = relationship('Inscripcion', back_populates='certificado')