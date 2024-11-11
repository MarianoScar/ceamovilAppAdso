from flask import request, render_template, redirect, url_for, flash
from src.models import session
from src.models.inscripcion import Inscripcion
from src.models.instancia_curso import InstanciaCurso
from src.models.clase import Clase
from src.models.asistencia import Asistencia 
from src.app import app
from src.models.estudiantes import Estudiantes
import re


@app.route('/buscar-estudiante-certificacion',methods=['GET', 'POST'])
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
def menu_certificaciones():

    return render_template('menu-certificaciones.html')




@app.route('/consulta-asistencia/<int:estudiante_id>/<int:instancia_curso_id>')
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
