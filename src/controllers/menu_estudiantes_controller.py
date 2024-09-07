from flask import render_template, request, redirect, url_for
from src.app import app
from flask_controller import FlaskController
from src.models.estudiantes import Estudiantes, session


class MenuEstudiantes(FlaskController):
    @app.route('/estudiantes')
    def lista_estudiantes():
        estudiantes = session.query(Estudiantes).all()
        return render_template('menu-estudiantes.html', estudiantes=estudiantes)
    
  