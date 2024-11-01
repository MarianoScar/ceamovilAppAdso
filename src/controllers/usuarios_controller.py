from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from src.models import session
from src.app import app
from src.models.usuarios import Usuario


@app.route('/lista-usuarios')
def lista_usuarios():
    usuarios = session.query(Usuario).all()
    return render_template('menu-usuarios.html', usuarios=usuarios)



@app.route('/crear-usuario', methods=['GET', 'POST'])
def crear_usuario():
    if request.method == 'POST':
        nombre_usuario = request.form.get('nombre_usuario')
        contraseña = request.form.get('contraseña')
        rol = request.form.get('rol')
        

        # Validaciones básicas
        if not nombre_usuario or not contraseña:

            flash("El nombre de usuario y la contraseña son requeridos")
            return redirect(url_for('crear_usuario'))

        # Verificar si el usuario ya existe
        if session.query(Usuario).filter_by(nombre_usuario=nombre_usuario).first():
            flash("El nombre de usuario ya existe. Intenta con otro.")
            return redirect(url_for('crear_usuario'))

        try:
            nuevo_usuario = Usuario(nombre_usuario=nombre_usuario, rol=rol)
            nuevo_usuario.establecer_contraseña(contraseña)

            session.add(nuevo_usuario)
            session.commit()
            flash("Usuario creado exitosamente.")
            return redirect(url_for('index'))
            
        except Exception as e:
            session.rollback()
            flash("Error al crear usuario.")
            print(f"Error: {str(e)}")
            return redirect(url_for('crear_usuario'))
    
    return render_template('crear-usuarios.html')
    


@app.route('/provisional-administrador', methods=['GET', 'POST'])
def cambiar_provisional_administrador():
    if request.method == 'POST':
        nombre_usuario = request.form.get('nombre_usuario')
        contraseña = request.form.get('contraseña')
                

        # Validaciones básicas
        if not nombre_usuario or not contraseña:

            flash("El nombre de usuario y la contraseña son requeridos")
            return redirect(url_for('cambiar_provisional_administrador'))

        # Verificar si el usuario ya existe
        if session.query(Usuario).filter_by(nombre_usuario=nombre_usuario).first():
            flash("El nombre de usuario ya existe. Intenta con otro.")
            return redirect(url_for('cambiar_provisional_administrador'))

        try:
            nuevo_usuario = Usuario(nombre_usuario=nombre_usuario, rol="administrador", es_provisional=False)
            nuevo_usuario.establecer_contraseña(contraseña)

            session.add(nuevo_usuario)
            session.commit()
            flash("Usuario creado exitosamente.")
            return redirect(url_for('index'))
            
        except Exception as e:
            session.rollback()
            flash("Error al crear usuario.")
            print(f"Error: {str(e)}")
            return redirect(url_for('cambiar_provisional_administrador'))
    
    return render_template('cambiar-usuario-administrador.html')


@app.route('/eliminar-usuario/<int:id_usuario>', methods=['POST'])
def eliminar_usuario(id_usuario):

    usuario = session.query(Usuario).get(id_usuario)

    if usuario: 
        session.delete(usuario)
        session.commit()
        flash('Usuario eliminado correctamente', 'success')

    else:
        flash('Usuario no encontrado')

    return redirect(url_for('lista_usuarios'))        
