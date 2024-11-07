from sqlalchemy import Column, Integer, String, Date
from src.models import Base, session
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from flask import render_template, request,redirect, url_for, flash


class Instructor(Base, SerializerMixin):
    __tablename__ = "instructor"  
    
    id = Column(Integer, primary_key=True)
    nombre_instructor = Column(String(100), nullable=False)
    tipo_identificacion = Column(String(20), nullable=False)
    numero_identificacion = Column(Integer(), unique=True, nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)  
    telefono = Column(Integer(), nullable=False)
    email = Column(String(50), nullable=False)
    numero_licencia = Column(Integer(), unique=True, nullable=False)

    cursos_impartidos = relationship('InstanciaCurso', back_populates='instructor', lazy=True)





