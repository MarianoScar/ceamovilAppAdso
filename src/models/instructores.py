from sqlalchemy import Column, Integer, String, Date
from src.models import Base, session
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from flask import render_template, request,redirect, url_for, flash


class Instructor(Base, SerializerMixin):
    __tablename__ = "instructores"
    id = Column(Integer, primary_key=True)
    nombre_instructor = Column(String(100), unique=False, nullable=False)
    tipo_identificacion = Column(String(20), unique=False, nullable=False)
    numero_identificacion = Column(Integer(), unique=True, nullable=False)
    fecha_nacimiento = Column(Integer(), nullable=False)
    telefono = Column(Integer(), unique=False, nullable=False)
    email = Column(String(50), unique=False, nullable=False)
    numero_licencia = Column(Integer(), unique=True, nullable=False)


    cursos_impartidos = relationship('InstanciaCurso', back_populates='instructor', lazy=True)




