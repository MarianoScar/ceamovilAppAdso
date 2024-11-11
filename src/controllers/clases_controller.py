from flask import request, render_template, redirect, url_for, flash
from src.models import session
from src.models.inscripcion import Inscripcion
from src.models.instancia_curso import InstanciaCurso
from src.models.clase import Clase
from src.models.asistencia import Asistencia 
from src.app import app



@app.route('/instancia-curso/<int:instancia_curso_id>', methods=['GET'])
def ver_clases(instancia_curso_id):
   
    instancia_curso = session.query(InstanciaCurso).get(instancia_curso_id)
    clases = session.query(Clase).filter_by(instancia_curso_id=instancia_curso_id).all()

    if not instancia_curso:
        flash("La instancia de curso no existe.", "error")
        return redirect(url_for('mostrar_instancias'))

    return render_template('ver-clases.html', instancia_curso=instancia_curso, clases=clases)




@app.route('/clase/<int:clase_id>', methods=['GET'])
def mostrar_asistencia(clase_id):
    
    clase = session.query(Clase).get(clase_id)

    if not clase:
        flash("La clase no existe.", "error")
        return redirect(url_for('mostrar_instancias'))

    
    inscripciones = session.query(Inscripcion).filter_by(instancia_curso_id=clase.instancia_curso_id).all()
    estudiantes = [inscripcion.estudiante for inscripcion in inscripciones]

    return render_template('marcar-asistencia.html', clase=clase, estudiantes=estudiantes)



@app.route('/clase-asistencia/<int:clase_id>', methods=['POST'])
def guardar_asistencia(clase_id):
    presente_data = request.form.getlist('presente')  # Lista con los IDs de estudiantes marcados como presentes
    
    clase = session.query(Clase).get(clase_id)
    inscripciones = session.query(Inscripcion).filter_by(instancia_curso_id=clase.instancia_curso_id).all()

    estudiantes_duplicados = []  # Para guardar los estudiantes con asistencia duplicada

    for inscripcion in inscripciones:
        # Chequear si el estudiante ya tiene un registro de asistencia para esta clase
        asistencia_existente = session.query(Asistencia).filter_by(
            inscripcion_id=inscripcion.id,
            clase_id=clase_id
        ).first()

        # Si ya tiene un registro, agregar a duplicados y continuar al siguiente estudiante
        if asistencia_existente:
            estudiantes_duplicados.append(inscripcion.estudiante.nombre)
            continue

        # Registrar asistencia solo si no existe aún
        presente = str(inscripcion.estudiante.id) in presente_data  # Verificar si el estudiante está en la lista de presentes
        asistencia = Asistencia(
            inscripcion_id=inscripcion.id,
            clase_id=clase_id,
            presente=presente
        )
        session.add(asistencia)

    session.commit()  # Guardar todos los registros en una sola operación de commit

    # Mensajes flash dependiendo de si hubo duplicados o no
    if estudiantes_duplicados:
        flash(f'YA se hizo el registro de asistencia para esta clase, no es posible ingresar la asistencia nuevamente.', 'warning')
    else:
        flash('Asistencia registrada correctamente.', 'success')

    return redirect(url_for('ver_clases', instancia_curso_id=clase.instancia_curso_id))









