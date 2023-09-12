"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

import InventariosWebApp.views

from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Inventarios.db'
db = SQLAlchemy(app)



