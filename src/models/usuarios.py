from sqlalchemy import Column, Integer, String
from src.models import Base
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, current_user
from functools import wraps
from flask import redirect, url_for, flash

bcrypt = Bcrypt()

class Usuario(Base, UserMixin):

    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    nombre_usuario = Column(String(150), unique=True, nullable=False)
    contraseña_hash = Column(String(150), nullable=False)
    rol = Column(String(50), nullable=False)  

    def establecer_contraseña(self, contraseña):
        self.contraseña_hash = bcrypt.generate_password_hash(contraseña).decode('utf-8')

    def verificar_contraseña(self, contraseña):
        return bcrypt.check_password_hash(self.contraseña_hash, contraseña)


def rol_requerido(rol_requerido):
    def decorador(f):
        @wraps(f)
        def decorador_funcion(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Debes iniciar sesión para acceder a esta página.")
                return redirect(url_for("login"))
            elif current_user.rol != rol_requerido:
                flash("No tienes permisos para acceder a esta página.")
                return redirect(url_for("index"))  # Cambia 'index' si deseas otra ruta predeterminada
            return f(*args, **kwargs)
        return decorador_funcion
    return decorador

