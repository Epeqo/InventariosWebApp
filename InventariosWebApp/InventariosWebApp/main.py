from flask import Blueprint, render_template
from .models import db, Producto

main = Blueprint('main', __name__)

@main.route('/')
def index():
    productos = Producto.query.all()
    return render_template('index.html', productos=productos)


