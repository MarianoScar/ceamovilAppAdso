from flask import render_template, request,redirect, url_for, flash
from src.app import app
from src.models.estudiantes import Estudiantes, session
from flask_controller import FlaskController  


class MenuEstudiantes(FlaskController):
    
    @app.route('/estudiantes')
    def lista_estudiantes():
        estudiantes = session.query(Estudiantes).all()
        return render_template('menu-estudiantes.html', estudiantes=estudiantes)

    @app.route('/buscar', methods=['GET', 'POST'])
    def buscar_estudiante():
        if request.method == 'POST':
            # tomo los datos del formulario
            criterio_nombre = request.form.get('criterio_nombre')  
            criterio_numero_identificacion = request.form.get('criterio_numero_identificacion') 
            busqueda = request.form['busqueda']  # Valor de la barra de búsqueda

            # Verificamos qué criterio escogio el usuario
            if criterio_nombre and busqueda:
                
                estudiantes = session.query(Estudiantes).filter(
                    Estudiantes.nombre.ilike(f'%{busqueda}%')
                ).all()
            elif criterio_numero_identificacion and busqueda:
                
                estudiantes = session.query(Estudiantes).filter(
                    Estudiantes.numero_identificacion.ilike(f'%{busqueda}%')
                ).all()
            else:
                estudiantes = None

            # Si se encuentra al estudiante, se muestra la info
            if estudiantes:
                return render_template('tabla-estudiantes.html', estudiantes=estudiantes)
            else:
                return render_template('tabla-estudiantes.html', mensaje='No se encontraron resultados.')

        # Si es GET, mostrar el formulario de búsqueda
        return render_template('menu-estudiantes.html')
    
    @app.route('/editar-estudiante/<int:id_estudiante>', methods=['GET', 'POST'])
    def editar_estudiante(id_estudiante):
        if request.method == 'POST':
            # Retrieve form data
            nombre = request.form['nombre']
            tipo_identificacion = request.form['tipo_identificacion']
            numero_identificacion = request.form['numero_identificacion']
            telefono = request.form['telefono']
            email = request.form['email']
            curso = request.form['curso']
            fecha_nacimiento = request.form['fecha_nacimiento']
            
            # Update the student in the database
            
            estudiante = session.query(Estudiantes).get(id_estudiante)
            estudiante.nombre = nombre
            estudiante.tipo_identificacion = tipo_identificacion
            estudiante.numero_identificacion = numero_identificacion
            estudiante.telefono = telefono
            estudiante.email = email
            estudiante.curso = curso
            estudiante.fecha_nacimiento = fecha_nacimiento
            # Save changes to the database
            session.commit()
            flash('La informacion se edito correctamente.')

            
            # Redirect the user to the list of students
            return redirect(url_for('lista_estudiantes'))
        
        # If GET, show the edit form
        estudiante = session.query(Estudiantes).get(id_estudiante)
        return render_template('editar-estudiante.html', estudiante=estudiante)

    @app.route('/eliminar-estudiante/<int:id_estudiante>', methods=['POST'])
    def eliminar_estudiante(id_estudiante):
        # Obtener el estudiante por ID
        estudiante = session.query(Estudiantes).get(id_estudiante)
        if estudiante:
            session.delete(estudiante)
            session.commit()
            flash('Estudiante eliminado exitosamente.')

        else:
             flash('Estudiante no encontrado.')
        
        # Redirigir a la lista de estudiantes
        return redirect(url_for('lista_estudiantes'))    
            
