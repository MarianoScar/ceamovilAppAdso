from flask import request, render_template, redirect, url_for, flash, send_from_directory
from src.models import session
from datetime import datetime
from src.models.inscripcion import Inscripcion
from src.models.instancia_curso import InstanciaCurso
from src.models.clase import Clase
from src.models.asistencia import Asistencia 
from src.app import app
from src.models.estudiantes import Estudiantes
import re
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from src.models.usuarios  import rol_requerido
from flask_login import  login_required



@app.route('/buscar-estudiante-certificacion',methods=['GET', 'POST'])
@login_required
@rol_requerido(["administrador", "usuario"])  
def buscar_estudiante_certificacion():
    if request.method == 'POST':
        busqueda = request.form['busqueda']  

        
        if re.search(r'[^a-zA-Z0-9]', busqueda):
            return render_template('menu-certificaciones.html', mensaje='La búsqueda debe ser por nombre o número de cédula sin caracteres especiales.')

        
        if busqueda.isdigit():
            estudiantes = session.query(Estudiantes).filter(
                Estudiantes.numero_identificacion.ilike(f'%{busqueda}%')
            ).all()
        else:
            estudiantes = session.query(Estudiantes).filter(
                Estudiantes.nombre.ilike(f'%{busqueda}%')
            ).all()

        
        if estudiantes:
            return render_template('tabla-estudiante-certificacion.html', estudiantes=estudiantes)
        else:
            flash("No se encontro ningun resultado", "error")
            return redirect(url_for('buscar_estudiante_certificacion'))
            

    
    return render_template('menu-certificaciones.html')


@app.route('/menu-certificaciones',methods=['GET', 'POST'])
@login_required
@rol_requerido(["administrador", "usuario"]) 
def menu_certificaciones():

    return render_template('menu-certificaciones.html')




@app.route('/consulta-asistencia/<int:estudiante_id>/<int:instancia_curso_id>')
@login_required
@rol_requerido(["administrador", "usuario"])  
def consulta_asistencia(estudiante_id, instancia_curso_id):
    estudiante = session.query(Estudiantes).get(estudiante_id)
    instancia_curso = session.query(InstanciaCurso).get(instancia_curso_id)
    clases = session.query(Clase).filter_by(instancia_curso_id=instancia_curso_id).all()

    # Obtener asistencia para cada clase del estudiante
    asistencias = {}
    for clase in clases:
        asistencia = session.query(Asistencia).filter_by(
            inscripcion_id=estudiante_id,
            clase_id=clase.id
        ).first()
        asistencias[clase] = "Presente" if asistencia and asistencia.presente else "Ausente"

    return render_template('consulta-asistencia.html', estudiante=estudiante, instancia_curso=instancia_curso, asistencias=asistencias)




@app.route('/generar-certificado/<int:estudiante_id>/<int:instancia_curso_id>')
@login_required
@rol_requerido("administrador") 
def generar_certificado(estudiante_id, instancia_curso_id):
    estudiante = session.query(Estudiantes).get(estudiante_id)
    instancia_curso = session.query(InstanciaCurso).get(instancia_curso_id)
    clases = session.query(Clase).filter_by(instancia_curso_id=instancia_curso_id).all()

   
    asistencias = session.query(Asistencia).filter_by(inscripcion_id=estudiante_id).filter(
        Asistencia.clase_id.in_([clase.id for clase in clases])
    ).all()
    clases_asistidas = sum(1 for asistencia in asistencias if asistencia.presente)

    
    if clases_asistidas == len(clases):

        if not os.path.exists('certificados'):
            os.makedirs('certificados')


        # Generar el certificado como archivo PDF
        nombre_archivo = f"certificado_{estudiante_id}_{instancia_curso_id}.pdf"
        ruta_archivo = os.path.join("certificados", nombre_archivo)
        
        # Crear el PDF con ReportLab
        c = canvas.Canvas(ruta_archivo, pagesize=A4)
        width, height = A4
        
        # Título del certificado
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(width / 2, height - 100, "Certificado de Finalización")
        
        # Información del estudiante y curso
        c.setFont("Helvetica", 12)
        c.drawString(100, height - 150, f"Nombre del Estudiante: {estudiante.nombre}")
        c.drawString(100, height - 180, f"Curso: {instancia_curso.curso.nombre_curso}")
        
        # Texto de finalización del curso
        c.drawString(100, height - 210, "Este certificado confirma la finalización del curso con éxito.")
        
        # Fecha de emisión
        c.drawString(100, height - 250, "Fecha de Emisión:")
        c.drawString(250, height - 250, datetime.now().strftime("%Y-%m-%d"))
        
        # Guardar el archivo PDF
        c.save()
        
        flash('Certificado generado exitosamente.', 'success')
        return redirect(url_for('descargar_certificado', filename=nombre_archivo))
    else:
        flash('El estudiante no cumple con el 100% de asistencia necesario para certificar.', 'warning')
        return redirect(url_for('consulta_asistencia', estudiante_id=estudiante_id, instancia_curso_id=instancia_curso_id))
    

@app.route('/descargar-certificados/<filename>')
@login_required
@rol_requerido("administrador") 
def descargar_certificado(filename):
    return send_from_directory("certificados", filename, as_attachment=True)
