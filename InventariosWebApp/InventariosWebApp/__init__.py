from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Crear una instancia de SQLAlchemy
db = SQLAlchemy()

def create_app():
    # Crear una instancia de Flask
    app = Flask(__name__)
    
    # Configurar la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventarios.db'
    
    # Inicializar SQLAlchemy con la aplicaci�n Flask
    db.init_app(app)

    # Inicializar Flask-Migrate
    migrate = Migrate(app, db)
    
    # Registrar rutas
    from . import main  # Aseg�rate de que main.py est� en el mismo directorio que __init__.py

    # Retornar la instancia de la aplicaci�n
    return app

# Si necesitas una instancia global de la aplicaci�n (por ejemplo, para un script de ejecuci�n), puedes descomentar la siguiente l�nea:
app = create_app()

from .main import main as main_blueprint
app.register_blueprint(main_blueprint)





