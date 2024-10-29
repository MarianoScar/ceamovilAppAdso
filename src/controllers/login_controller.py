from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from src.models import session
from src.app import app
from src.models.usuarios import Usuario

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre_usuario = request.form['nombre_usuario']
        contraseña = request.form['contraseña']

        usuario = session.query(Usuario).filter_by(nombre_usuario=nombre_usuario).first()

        if usuario and usuario.verificar_contraseña(contraseña):
            login_user(usuario)
            return redirect(url_for('index'))
        flash('Nombre de usuario o contraseña incorrectos')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
