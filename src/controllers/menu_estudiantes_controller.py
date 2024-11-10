from flask import render_template, request,redirect, url_for, flash
from src.app import app
from src.models import session
from src.models.estudiantes import Estudiantes
from flask_controller import FlaskController  
import re
from src.models.usuarios import rol_requerido
from flask_login import  login_required





@app.route('/estudiantes')
def lista_estudiantes():
    estudiantes = session.query(Estudiantes).all()
    return render_template('menu-estudiantes.html', estudiantes=estudiantes)

@app.route('/buscar', methods=['GET', 'POST'])
def buscar_estudiante():
    if request.method == 'POST':
        busqueda = request.form['busqueda']  

        
        if re.search(r'[^a-zA-Z0-9]', busqueda):
            return render_template('tabla-estudiantes.html', mensaje='La búsqueda debe ser por nombre o número de cédula sin caracteres especiales.')

        
        if busqueda.isdigit():
            estudiantes = session.query(Estudiantes).filter(
                Estudiantes.numero_identificacion.ilike(f'%{busqueda}%')
            ).all()
        else:
            estudiantes = session.query(Estudiantes).filter(
                Estudiantes.nombre.ilike(f'%{busqueda}%')
            ).all()

        
        if estudiantes:
            return render_template('tabla-estudiantes.html', estudiantes=estudiantes)
        else:
            flash("No se encontro ningun resultado", "error")
            return redirect(url_for('buscar_estudiante'))
            

    
    return render_template('menu-estudiantes.html')
    

        
@app.route('/editar-estudiante/<int:id_estudiante>', methods=['GET', 'POST'])
@login_required
@rol_requerido("administrador")
def editar_estudiante(id_estudiante):
        estudiante = session.query(Estudiantes).get(id_estudiante)
        
        if request.method == 'POST':
            
            nombre = request.form['nombre']
            tipo_identificacion = request.form['tipo_identificacion']
            numero_identificacion = request.form['numero_identificacion']
            telefono = request.form['telefono']
            email = request.form['email']
            fecha_nacimiento = request.form['fecha_nacimiento']

            
            estudiante.nombre = nombre
            estudiante.tipo_identificacion = tipo_identificacion
            estudiante.numero_identificacion = numero_identificacion
            estudiante.telefono = telefono
            estudiante.email = email
            estudiante.fecha_nacimiento = fecha_nacimiento

            
            session.commit()
            flash('La información se editó correctamente.', 'success')

            
            return redirect(url_for('lista_estudiantes'))
        
        
        return render_template('editar-estudiante.html', estudiante=estudiante)

    

@app.route('/eliminar-estudiante/<int:id_estudiante>', methods=['POST'])
@login_required
@rol_requerido("administrador")
def eliminar_estudiante(id_estudiante):
    
    estudiante = session.query(Estudiantes).get(id_estudiante)
    if estudiante:
        session.delete(estudiante)
        session.commit()
        flash('Estudiante eliminado exitosamente.','success')

    else:
        flash('Estudiante no encontrado.')
    
    
    return redirect(url_for('lista_estudiantes'))    
            
