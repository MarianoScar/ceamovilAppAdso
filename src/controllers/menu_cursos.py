from flask import Flask, render_template, request, redirect, flash
from src.models import session
from src.models.cursos import Curso
from src.models.instancia_curso import InstanciaCurso
from src.app import app
from datetime import datetime, timedelta


@app.route('/cursos', methods=['GET'])
def mostrar_instancias():
    instancias = session.query(InstanciaCurso).all()
    
    if instancias:  
        return render_template('menu-cursos.html', instancias=instancias)
    
    else:  
        #flash('Actualmente no se ha abierto un curso. A continuacion puedes abrir uno nuevo.')
        cursos = session.query(Curso).all()
        return render_template('menu-cursos.html', cursos=cursos, mensaje ='NO HAY CURSOS ABIERTOS, VE AL MENU CURSOS Y CREA UNO NUEVO')


@app.route('/crear-cursos', methods=['GET', 'POST'])
def abrir_cursos():
    if request.method == 'POST':
        curso_id = request.form['curso_id']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']
        
        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
            fecha_actual = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            
            # Aqui reviso que la feche de inicio sea mayor que la actual
            if fecha_inicio_dt < fecha_actual:
                flash('Error: La fecha de inicio debe ser igual o posterior a la fecha actual.', 'error')
                return redirect('/cursos')
            
            # Aqui reviso que la fecha final sea posterior a la fecha de inicio
            if fecha_fin_dt <= fecha_inicio_dt:
                flash('Error: La fecha final debe ser posterior a la fecha de inicio.', 'error')
                return redirect('/cursos')
            
            
            diferencia_dias = (fecha_fin_dt - fecha_inicio_dt).days
            
            if diferencia_dias >= 15:
                nueva_instancia = InstanciaCurso(
                    curso_id=curso_id,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin
                )
                
                session.add(nueva_instancia)
                session.commit()
                flash('Curso abierto exitosamente.', 'success')
                return redirect('/cursos')
            else:
                flash(f'Error: Debe haber al menos 15 días entre las fechas. Actualmente hay {diferencia_dias} días.', 'error')
                return redirect('/cursos')
                
        except ValueError:
            flash('Error: Formato de fecha inválido. Use YYYY-MM-DD.', 'error')
            return redirect('/cursos')

    cursos = session.query(Curso).all()  
    return render_template('crear-cursos.html',  cursos=cursos)

