from flask import Flask
from src.models import Base, engine, session
from src.models.cursos import inicializar_cursos
from flask_controller import FlaskControllerRegister
import os
from flask_login import LoginManager
from src.models.usuarios import Usuario

app = Flask(__name__)

app.secret_key = os.urandom(24)

usuario_inicial_creado = False

@app.before_request
def crear_usuario_inicial():
    
    usuario = session.query(Usuario).filter_by(nombre_usuario="user").first()
    if usuario is None:
        
        usuario = Usuario(nombre_usuario='user', rol='administrador', es_provisional = True)
        usuario.establecer_contraseña('user')  
        
        session.add(usuario)
        session.commit()
        print(f"Usuario inicial creado: {usuario.nombre_usuario} con contraseña: 'user'")  # Mostrar en consola

register = FlaskControllerRegister(app)
register.register_package('src.controllers')

Base.metadata.create_all(engine)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return session.query(Usuario).get(int(user_id))

inicializar_cursos(session)


if __name__ == '__main___':
    app.run(debug=True)
