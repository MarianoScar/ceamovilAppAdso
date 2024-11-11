from flask import render_template
from src.app import app
from flask_controller import FlaskController
from src.models.usuarios  import rol_requerido
from flask_login import  login_required


class HomeController(FlaskController):
    @app.route("/index")
    @login_required
    @rol_requerido(["administrador", "usuario"]) 
    
    def index():
        return render_template('index.html')
    