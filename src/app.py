from flask import Flask
from src.models import Base, engine, session
from src.models.cursos import inicializar_cursos
from src.models.usuarios import crear_usuario_inicial
from flask_controller import FlaskControllerRegister
import os
from flask_login import LoginManager
from src.models.usuarios import Usuario

app = Flask(__name__)

app.secret_key = os.urandom(24)

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

crear_usuario_inicial()


if __name__ == '__main__':
    app.run(debug=True)
