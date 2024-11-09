from flask import render_template, request, redirect, flash,url_for
from src.models import session
from src.models.cursos import Curso
from src.models.instructores import Instructor
from src.models.instancia_curso import InstanciaCurso
from src.app import app
from datetime import datetime, timedelta
from src.models.usuarios  import rol_requerido
from flask_login import  login_required


@app.route('/cursos', methods=['GET'])
def mostrar_instancias():
    instancias = session.query(InstanciaCurso).all()
    instructores = session.query(Instructor).all() 

    if not instructores:
        flash('Error: No hay instructores disponibles, debe haber instructores registrados para poder abrir un curso nuevo.', 'error')
        return redirect(url_for('crear_instructor'))
    
    
    if instancias:  
        return render_template('menu-cursos.html', instancias=instancias, instructores=instructores)
    
    else:  
        #flash('Actualmente no se ha abierto un curso. A continuacion puedes abrir uno nuevo.')
        cursos = session.query(Curso).all()
        return render_template('crear-cursos.html', cursos=cursos, instructores=instructores)
    
    


@app.route('/crear-cursos', methods=['GET', 'POST'])
@login_required
@rol_requerido("administrador")
def abrir_cursos():
    instructores = session.query(Instructor).all()    

    if not instructores:
        flash('Error: No hay instructores disponibles, debe haber instructores registrados para poder abrir un curso nuevo.', 'error')
        return redirect(url_for('mostrar_instancias'))

    if request.method == 'POST':
        curso_id = request.form['curso_id']
        fecha_inicio = request.form['fecha_inicio']
        instructor_id = request.form['instructor_id']
        
        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')  
            fecha_actual = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            fecha_fin_dt = fecha_inicio_dt + timedelta(days=15)
            
            if fecha_inicio_dt < fecha_actual:
                flash('Error: La fecha de inicio debe ser igual o posterior a la fecha actual.', 'error')
                return redirect('/cursos')
            
            if fecha_fin_dt <= fecha_inicio_dt:
                flash('Error: La fecha final debe ser posterior a la fecha de inicio.', 'error')
                return redirect('/cursos')
            
            diferencia_dias = (fecha_fin_dt - fecha_inicio_dt).days

            if diferencia_dias >= 15:
                nueva_instancia = InstanciaCurso(
                    curso_id=curso_id,
                    fecha_inicio=fecha_inicio_dt,  # Usa el objeto datetime en lugar del string
                    instructor_id=instructor_id
                )
                
                session.add(nueva_instancia)
                session.commit()
                nueva_instancia.programar_clases()
                flash('Curso abierto exitosamente.', 'success')
                return redirect('/cursos')
            else:
                flash(f'Error: Debe haber al menos 15 días entre las fechas. Actualmente hay {diferencia_dias} días.', 'error')
                return redirect('/cursos')
                
        except ValueError:
            flash('Error: Formato de fecha inválido. Use YYYY-MM-DD.', 'error')
            return redirect('/cursos')

    cursos = session.query(Curso).all()  
    return render_template('crear-cursos.html', cursos=cursos, instructores=instructores)


