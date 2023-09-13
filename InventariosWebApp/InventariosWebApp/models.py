from . import db


class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(100), unique=True, nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    descripcion = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f"<Producto {self.codigo}>"

