from flask import Flask
from src.models import Base, engine, session
from src.models.cursos import inicializar_cursos
from flask_controller import FlaskControllerRegister
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)


register = FlaskControllerRegister(app)
register.register_package('src.controllers')

Base.metadata.create_all(engine)

inicializar_cursos(session)


if __name__ == '__main___':
    app.run(debug=True)