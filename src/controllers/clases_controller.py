from flask import request, render_template, redirect, url_for, flash
from src.models import session
from src.models.estudiantes import Estudiantes
from src.models.instancia_curso import InstanciaCurso
from src.models.clase import Clase
from src.models.asistencia import Asistencia 
from src.app import app

@app.route('/asistencia', methods=['POST'])
def marcar_asistencia():
    
    estudiante_id = request.form.get('estudiante_id')
    clase_id = request.form.get('clase_id')
    presente = request.form.get('presente')

    
    asistencia = Asistencia(estudiante_id=estudiante_id, clase_id=clase_id, presente=presente)
    session.add(asistencia)
    session.commit()

    flash('Asistencia registrada correctamente.', 'success')  
    return redirect(url_for('index')) 

@app.route('/verificar_finalizacion/<int:estudiante_id>/<int:instancia_curso_id>', methods=['GET'])
def verificar_finalizacion_route(estudiante_id, instancia_curso_id):
    try:
        verificar_finalizacion(estudiante_id, instancia_curso_id)
        flash('Verificación de finalización realizada. Si cumple con los requisitos, el certificado ha sido generado.', 'success')  
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')  

    return redirect(url_for('index'))  