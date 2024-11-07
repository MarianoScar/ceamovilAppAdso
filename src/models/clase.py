from src.models import Base, session
from sqlalchemy import Column,Integer, Boolean, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from src.models.estudiantes import Estudiantes
from src.models.certificado import Certificado
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

CERTIFICADOS_DIR = "certificados"  


class Clase(Base):
    __tablename__ = 'clase'
    
    id = Column(Integer, primary_key=True)
    instancia_curso_id = Column(Integer, ForeignKey('instancia_curso.id'), nullable=False)
    fecha = Column(Date, nullable=False)
    tema = Column(String(100))  
    
    instancia_curso = relationship('InstanciaCurso', back_populates='clases')
    asistencias = relationship('Asistencia', back_populates='clase')



def generar_certificado(estudiante_id, instancia_curso_id):
    from src.models.instancia_curso import InstanciaCurso
    
    estudiante = session.query(Estudiantes).get(estudiante_id)
    instancia_curso = session.query(InstanciaCurso).get(instancia_curso_id)

    # Crear el directorio si no existe
    if not os.path.exists(CERTIFICADOS_DIR):
        os.makedirs(CERTIFICADOS_DIR)

    # Definir el nombre del archivo PDF
    nombre_certificado = f"certificado_{estudiante.nombre.replace(' ', '_')}_{instancia_curso.id}.pdf"
    ruta_certificado = os.path.join(CERTIFICADOS_DIR, nombre_certificado)

    # aca generamos el ( por el momento voy a generar un certificado sencillo, en los proximos commits lo modificamos el formato y el contenido) pdf
    c = canvas.Canvas(ruta_certificado, pagesize=letter)
    c.drawString(100, 750, "Certificado de Finalización")
    c.drawString(100, 730, f"Este certificado se otorga a:")
    c.drawString(100, 710, f"Estudiante: {estudiante.nombre}")
    c.drawString(100, 690, f"Curso: {instancia_curso.curso.tipo}")
    c.drawString(100, 670, f"Fecha de finalización: {instancia_curso.fecha_final}")
    c.drawString(100, 650, "Por haber completado el curso con éxito.")
    c.save()

    
    nuevo_certificado = Certificado(estudiante_id=estudiante_id, archivo_pdf=nombre_certificado)
    session.add(nuevo_certificado)
    session.commit()

    print(f"Certificado generado y guardado en: {ruta_certificado}")