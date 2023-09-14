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
    
    # Inicializar SQLAlchemy con la aplicacion Flask
    db.init_app(app)

    # Inicializar Flask-Migrate
    migrate = Migrate(app, db)
    
    # Registrar rutas
    from . import main  # Asegurate de que main.py este en el mismo directorio que __init__.py

    # Retornar la instancia de la aplicacion
    return app

# Si necesitas una instancia global de la aplicacion (por ejemplo, para un script de ejecucion), puedes descomentar la siguiente linea:
app = create_app()

from .main import main as main_blueprint
app.register_blueprint(main_blueprint)





