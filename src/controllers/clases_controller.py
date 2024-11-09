from flask import request, render_template, redirect, url_for, flash
from src.models import session
from src.models.inscripcion import Inscripcion
from src.models.instancia_curso import InstanciaCurso
from src.models.clase import Clase
from src.models.asistencia import Asistencia 
from src.app import app



@app.route('/instancia-curso/<int:instancia_curso_id>', methods=['GET'])
def ver_clases(instancia_curso_id):
    # Obtener todas las clases de la instancia de curso
    instancia_curso = session.query(InstanciaCurso).get(instancia_curso_id)
    clases = session.query(Clase).filter_by(instancia_curso_id=instancia_curso_id).all()

    if not instancia_curso:
        flash("La instancia de curso no existe.", "error")
        return redirect(url_for('mostrar_instancias'))

    return render_template('ver-clases.html', instancia_curso=instancia_curso, clases=clases)




@app.route('/clase/<int:clase_id>', methods=['GET'])
def mostrar_asistencia(clase_id):
    # Obtener la clase específica
    clase = session.query(Clase).get(clase_id)

    if not clase:
        flash("La clase no existe.", "error")
        return redirect(url_for('mostrar_instancias'))

    # Obtener estudiantes inscritos en la instancia de curso de la clase
    inscripciones = session.query(Inscripcion).filter_by(instancia_curso_id=clase.instancia_curso_id).all()
    estudiantes = [inscripcion.estudiante for inscripcion in inscripciones]

    return render_template('marcar-asistencia.html', clase=clase, estudiantes=estudiantes)



@app.route('/clase/<int:clase_id>', methods=['POST'])
def guardar_asistencia(clase_id):
    presente_data = request.form.getlist('presente')  # Lista de IDs de estudiantes presentes

    # Obtener la clase y la instancia de curso
    clase = session.query(Clase).get(clase_id)
    inscripciones = session.query(Inscripcion).filter_by(instancia_curso_id=clase.instancia_curso_id).all()

    for inscripcion in inscripciones:
        presente = str(inscripcion.estudiante.id) in presente_data
        asistencia = Asistencia(
            inscripcion_id=inscripcion.id,
            clase_id=clase_id,
            presente=presente
        )
        session.add(asistencia)

    session.commit()
    flash('Asistencia registrada correctamente.', 'success')
    return redirect(url_for('menu_cursos.ver_clases', instancia_curso_id=clase.instancia_curso_id))





'''

@app.route('/asistencia', methods=['POST'])
def marcar_asistencia():
   
    inscripcion_id = request.form.get('inscripcion_id')
    clase_id = request.form.get('clase_id')
    presente = request.form.get('presente') == 'on' 

    # Crear instancia de Asistencia
    asistencia = Asistencia(inscripcion_id=inscripcion_id, clase_id=clase_id, presente=presente)
    session.add(asistencia)
    session.commit()

    # Confirmar éxito
    flash('Asistencia registrada correctamente.', 'success')
    return redirect(url_for('index'))

'''

'''@app.route('/verificar_finalizacion/<int:estudiante_id>/<int:instancia_curso_id>', methods=['GET'])
def verificar_finalizacion_route(estudiante_id, instancia_curso_id):
    try:
        verificar_finalizacion(estudiante_id, instancia_curso_id)
        flash('Verificación de finalización realizada. Si cumple con los requisitos, el certificado ha sido generado.', 'success')  
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')  

    return redirect(url_for('index'))  
'''