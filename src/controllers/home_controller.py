from flask import render_template
from src.app import app
from flask_controller import FlaskController


class HomeController(FlaskController):
    @app.route("/")
    def index():
        return render_template('index.html')