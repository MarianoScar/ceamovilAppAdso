from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from src.models import session
from src.app import app
from src.models.usuarios import Usuario

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        forma = request.form
        nombre_usuario = forma.get('nombre_usuario')
        contraseña = forma.get('contraseña')

        if not nombre_usuario or not contraseña:
            flash('Debe ingresar nombre de usuario y contraseña.')
            return redirect(url_for('login'))

        usuario = session.query(Usuario).filter_by(nombre_usuario=nombre_usuario).first()

        if usuario and usuario.verificar_contraseña(contraseña):
            login_user(usuario)

            # Guardar la página a la que el usuario intentaba acceder
            next_page = request.args.get('next')
            
            if usuario.es_provisional:
                flash("Hola! Estás ingresando con un usuario provisional, debes crear usuario y contraseña nuevos.")
                return render_template('cambiar-usuario-administrador.html', id_usuario=usuario.id)
            else:
                flash('Bienvenido!')
                # Si hay una página siguiente guardada, ir ahí, sino al index
                return redirect(next_page or url_for('index'))
        else:
            flash('Nombre de usuario o contraseña incorrectos')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.')
    return redirect(url_for('login'))