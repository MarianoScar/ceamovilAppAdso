from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.models import Base, session


class Curso(Base, SerializerMixin):
    __tablename__ = 'cursos'
    
    id = Column(Integer, primary_key=True)
    nombre_curso = Column(String(50), nullable=False, unique=True)
    duracion_dias = Column(Integer, nullable=False)

    # Esta es la relacion con la clase InstanciaCurso
    instancias = relationship("InstanciaCurso", back_populates="curso")

def inicializar_cursos(session):

    #  Verificamos di existen los cursos
    if session.query(Curso).count() == 0:

        # Si no existen los inicializamos
        curso1 = Curso(nombre_curso="Moto", duracion_dias=15)
        curso2 = Curso(nombre_curso="Automovil", duracion_dias=15)
        curso3 = Curso(nombre_curso="Camion", duracion_dias=15)

        session.add_all([curso1, curso2, curso3])
        session.commit()
        print("Cursos inicializados")
    else:
        print("Los cursos ya están inicializados.")

    
        
        
