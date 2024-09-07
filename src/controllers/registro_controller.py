from flask import render_template, request, redirect, url_for
from src.app import app
from flask_controller import FlaskController
from src.models.estudiantes import Estudiantes, Curso, session

class RegistroController(FlaskController):
    
    @app.route('/registro', methods=['GET', 'POST'])
    def registro():
        if request.method == 'POST':
            
            nombre = request.form['nombre']
            tipo_identificacion = request.form['tipo_identificacion']
            numero_identificacion = request.form['numero_identificacion']
            #direccion = request.form['direccion']
            telefono = request.form['telefono']
            email = request.form['email']
            curso = request.form['curso']
            fecha_nacimiento = request.form['fecha_nacimiento']

            
            nuevo_estudiante = Estudiantes(
                nombre=nombre,
                tipo_identificacion=tipo_identificacion,
                numero_identificacion=numero_identificacion,
                #direccion=direccion,
                telefono=telefono,
                email=email,
                curso=Curso[curso],  
                fecha_nacimiento=fecha_nacimiento
            )
            
            
            session.add(nuevo_estudiante)
            session.commit()

            return redirect(url_for('lista_estudiantes'))  

       
        return render_template('registro-alumnos.html')
        

