from sqlalchemy import Column, Integer, String, Boolean
from src.models import Base, session
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
    es_provisional = Column(Boolean, default=False)

    def establecer_contraseña(self, contraseña):
        self.contraseña_hash = bcrypt.generate_password_hash(contraseña).decode('utf-8')

    def verificar_contraseña(self, contraseña):
        return bcrypt.check_password_hash(self.contraseña_hash, contraseña)
    

def crear_usuario_inicial():
   
    usuario_no_provisional = session.query(Usuario).filter(Usuario.es_provisional.is_(False)).first()
    
  
    usuario_provisional = session.query(Usuario).filter(Usuario.es_provisional.is_(True)).first()
    
    if usuario_no_provisional is None and usuario_provisional is None:
        
        usuario = Usuario(nombre_usuario='provisional', rol='administrador', es_provisional=True)
        usuario.establecer_contraseña('provisional')
        session.add(usuario)
        session.commit()
        print(f"Se ha creado un usuario inicial: {usuario.nombre_usuario} , contraseña : provisional")
    elif usuario_provisional is not None:
        print("Ya existe un usuario provisional")


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

