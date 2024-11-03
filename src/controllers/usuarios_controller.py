from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from src.models import session
from src.app import app
from src.models.usuarios import Usuario
from src.models.usuarios import rol_requerido
from flask_login import  login_required


@app.route('/lista-usuarios')
def lista_usuarios():
    usuarios = session.query(Usuario).all()
    if usuarios :

        return render_template('menu-usuarios.html', usuarios=usuarios)
    else:
        flash("La lista de usuarios esta vacia")

    return redirect(url_for('index'))


@app.route('/crear-usuario', methods=['GET', 'POST'])
@login_required
@rol_requerido("administrador")
def crear_usuario():
    if request.method == 'POST':
        nombre_usuario = request.form.get('nombre_usuario')
        contraseña = request.form.get('contraseña')
        rol = request.form.get('rol')
        

        
        if not nombre_usuario or not contraseña:

            flash("El nombre de usuario y la contraseña son requeridos")
            return redirect(url_for('crear_usuario'))

        
        if session.query(Usuario).filter_by(nombre_usuario=nombre_usuario).first():
            flash("El nombre de usuario ya existe. Intenta con otro.")
            return redirect(url_for('crear_usuario'))

        try:
            nuevo_usuario = Usuario(nombre_usuario=nombre_usuario, rol=rol)
            nuevo_usuario.establecer_contraseña(contraseña)

            session.add(nuevo_usuario)
            session.commit()
            flash("Usuario creado exitosamente.", "success")
            return redirect(url_for('lista_usuarios'))
            
        except Exception as e:
            session.rollback()
            flash("Error al crear usuario.")
            print(f"Error: {str(e)}")
            return redirect(url_for('crear_usuario'))
    
    return render_template('crear-usuarios.html')
    


@app.route('/provisional-administrador/<id_usuario>', methods=['GET', 'POST'])
@login_required
@rol_requerido("administrador")
def cambiar_provisional_administrador(id_usuario):
    if request.method == 'POST':
        nombre_usuario = request.form.get('nombre_usuario')
        contraseña = request.form.get('contraseña')

        
        if not nombre_usuario or not contraseña:
            flash("El nombre de usuario y la contraseña son requeridos")
            return redirect(url_for('cambiar_provisional_administrador', id_usuario=id_usuario))

        
        if session.query(Usuario).filter_by(nombre_usuario=nombre_usuario).first():
            flash("El nombre de usuario ya existe. Intenta con otro.")
            return redirect(url_for('cambiar_provisional_administrador', id_usuario=id_usuario))

        try:
            
            usuario = session.query(Usuario).get(id_usuario)
            print(f"Usuario existente encontrado: {usuario.nombre_usuario}, ID: {usuario.id}")
            if not usuario:
                flash("Usuario no encontrado.")
                return redirect(url_for('login'))  

            
            usuario.nombre_usuario = nombre_usuario
            usuario.establecer_contraseña(contraseña)  
            usuario.es_provisional = False

           
            session.commit()
           

            flash("Usuario creado exitosamente.")
            return redirect(url_for('index'))

        except Exception as e:
            session.rollback()
            flash("Error al crear usuario.")
            print(f"Error: {str(e)}")
            return redirect(url_for('cambiar_provisional_administrador', id_usuario=id_usuario))

    
    return render_template('cambiar-usuario-administrador.html')


@app.route('/eliminar-usuario/<int:id_usuario>', methods=['GET', 'POST'])
@login_required
@rol_requerido("administrador")
def eliminar_usuario(id_usuario):

    if request.method == 'POST':
        try:
            usuario = session.query(Usuario).get(id_usuario)
            cantidad_admins = session.query(Usuario).filter_by(rol='administrador').count()

            if usuario.rol == 'administrador' and cantidad_admins <= 1:
                flash('No se puede eliminar el último usuario administrador', 'error')
                return redirect(url_for('lista_usuarios'))
            
            else:
                session.delete(usuario)
                session.commit()
                flash('Usuario eliminado correctamente', 'success')
                return redirect(url_for('lista_usuarios'))
        
            
        except Exception as e:
            flash('Error al eliminar usuario', 'error')
            print(f"Error: {e}")
    return redirect(url_for('lista_usuarios'))        



