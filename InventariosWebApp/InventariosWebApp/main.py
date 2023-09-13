from flask import render_template
from . import app, db
from .models import Producto

@app.route('/')
def index():
    productos = Producto.query.all()
    return render_template('index.html', productos=productos)

