from flask import render_template, request, redirect, url_for, flash
from src.app import app
from src.models.estudiantes import Estudiantes
from src.models.instancia_curso import InstanciaCurso
from src.models.inscripcion import Inscripcion
from src.models import session
from src.models.usuarios import rol_requerido
from flask_login import  login_required

@app.route('/registro', methods=['GET', 'POST'])
@login_required
@rol_requerido("administrador")
def registro_estudiante():

    instancias_curso = session.query(InstanciaCurso).all()

    if not instancias_curso:
        #flash('No hay instancias de curso disponibles para inscripción.')
        return render_template('index.html', mensaje = 'No existe un curso abierto aun, debes crear un CURSO nuevo para poder registrar a un estudiante. Por favor ingresa al menu CURSOS en la barra lateral.')
    
    if request.method == 'POST':
        
        nombre = request.form['nombre']
        tipo_identificacion = request.form['tipo_identificacion']
        numero_identificacion = request.form['numero_identificacion']
        telefono = request.form['telefono']
        email = request.form['email']
        fecha_nacimiento = request.form['fecha_nacimiento']
        instancia_curso_id = request.form['instancia_curso'] 

        try:
            
            nuevo_estudiante = Estudiantes(
                nombre=nombre,
                tipo_identificacion=tipo_identificacion,
                numero_identificacion=numero_identificacion,
                telefono=telefono,
                email=email,
                fecha_nacimiento=fecha_nacimiento
            )
            session.add(nuevo_estudiante)
            session.commit()

            # Aqui asociamos al estudiante con la instancia curso
            instancia_curso = session.query(InstanciaCurso).get(instancia_curso_id)
            inscripcion = Inscripcion(estudiante_id=nuevo_estudiante.id, instancia_curso_id=instancia_curso.id)
            session.add(inscripcion)
            session.commit()

            flash('Estudiante registrado con éxito al curso.', 'success')
            return redirect(url_for('lista_estudiantes'))

        except Exception as e:
            session.rollback()
            flash(f'Error al registrar el estudiante: {str(e)}')
            return redirect(url_for('registro_estudiante'))
    
    
    instancias_curso = session.query(InstanciaCurso).all()
    return render_template('registro-alumnos.html', instancias_curso=instancias_curso)
