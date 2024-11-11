from flask import Flask, render_template, request, redirect, flash, url_for
from src.models import session
from src.models.instructores import Instructor
from src.models.cursos import Curso
from src.models.instancia_curso import InstanciaCurso
from src.app import app
from datetime import datetime, timedelta
from src.models.usuarios  import rol_requerido
from flask_login import  login_required



@app.route('/menu-instructores')
@login_required
@rol_requerido(["administrador", "usuario"]) 
def lista_instructores():
    instructores = session.query(Instructor).all()
    return render_template('menu-instructores.html', instructores=instructores)


from datetime import datetime, date
from flask import flash, redirect, url_for, render_template, request

@app.route('/crear-instructor', methods=['GET', 'POST'])
@login_required
@rol_requerido("administrador")
def crear_instructor():
    if request.method == 'POST':
        nombre_instructor = request.form.get('nombre_instructor')
        tipo_identificacion = request.form.get('tipo_identificacion')
        numero_identificacion = request.form.get('numero_identificacion')
        telefono = request.form.get('telefono')
        email = request.form.get('email')
        fecha_nacimiento = request.form.get('fecha_nacimiento')
        numero_licencia = request.form.get('numero_licencia') 

        try:
            
            fecha_nac = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
            
            
            hoy = date.today()
            edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
            
            
            if edad < 18:
                flash('El instructor debe tener al menos 18 años', 'error')
                return redirect(url_for('crear_instructor'))
            
        
            
            
            nuevo_instructor = Instructor(
                nombre_instructor=nombre_instructor,
                tipo_identificacion=tipo_identificacion,
                numero_identificacion=numero_identificacion,
                telefono=telefono,
                email=email,
                fecha_nacimiento=fecha_nacimiento,
                numero_licencia=numero_licencia
            )
            session.add(nuevo_instructor)
            session.commit()

            flash('El instructor fue añadido correctamente', 'success')
            return redirect(url_for('lista_instructores'))
        
        except ValueError:
            
            flash('Formato de fecha de nacimiento inválido. Use YYYY-MM-DD', 'error')
            return redirect(url_for('crear_instructor'))
        
        except Exception as e:
            session.rollback()
            flash(f'Error al registrar el instructor: {str(e)}', 'error')
            return redirect(url_for('crear_instructor'))
    
    return render_template('crear-instructor.html')


@app.route('/editar-instructor/<int:id_instructor>', methods=['GET', 'POST'])
@login_required
@rol_requerido("administrador")
def editar_instructor(id_instructor):
        instructor = session.query(Instructor).get(id_instructor)
        
        if request.method == 'POST':
            
            nombre_instructor = request.form.get('nombre_instructor')
            tipo_identificacion = request.form.get('tipo_identificacion')
            numero_identificacion = request.form.get('numero_identificacion')
            telefono = request.form.get('telefono')
            email = request.form.get('email')
            fecha_nacimiento = request.form.get('fecha_nacimiento')
            numero_licencia = request.form.get('numero_licencia')

            
            instructor.nombre = nombre_instructor
            instructor.tipo_identificacion = tipo_identificacion
            instructor.numero_identificacion = numero_identificacion
            instructor.telefono = telefono
            instructor.email = email
            instructor.fecha_nacimiento = fecha_nacimiento
            instructor.numero_licencia = numero_licencia

            
            session.commit()
            flash('La información se editó correctamente.', 'success')

            
            return redirect(url_for('lista_instructores'))
        
        
        return render_template('editar-instructor.html', instructor=instructor)


@app.route('/eliminar-instructor/<int:id_instructor>', methods=['GET', 'POST'])
@login_required
@rol_requerido("administrador")
def eliminar_instructor(id_instructor):

    if request.method == 'POST':
            
            instructor = session.query(Instructor).get(id_instructor)       
            
            session.delete(instructor)
            session.commit()
            flash('Instructor eliminado correctamente', 'success')
            return redirect(url_for('lista_instructores'))
        

    return redirect(url_for('lista_instructores')) 