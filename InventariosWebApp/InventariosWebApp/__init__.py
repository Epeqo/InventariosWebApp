from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventarios.db'  # Usando SQLite para el ejemplo
db = SQLAlchemy(app)
migrate = Migrate(app, db)



