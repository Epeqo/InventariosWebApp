from . import db


class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lote = db.Column(db.String(100), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)  # Asumo que esto es "PRODUCTOS"
    caducidad = db.Column(db.Date, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    cve_art = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Producto {self.nombre}>"


class Factura(db.Model):
    __tablename__ = 'factura'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    no_factura = db.Column(db.String(100), unique=True, nullable=False)
    marca = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.String(500), nullable=True)
    lote = db.Column(db.String(100), nullable=False)
    cant = db.Column(db.Integer, nullable=False)
    fecha_emision = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<Factura {self.no_factura}>"


