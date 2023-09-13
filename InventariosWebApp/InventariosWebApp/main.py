from flask import Blueprint, render_template, request, jsonify
from .models import db, Producto, Factura
import boto3

# Crea un cliente para Secrets Manager
client = boto3.client('secretsmanager', region_name='us-east-1')

def get_secret(secret_name):
    try:
        response = client.get_secret_value(SecretId=secret_name)
        if 'SecretString' in response:
            return response['SecretString']
        else:
            # Si tu secreto es un archivo binario, por ejemplo, un certificado
            return response['SecretBinary']
    except Exception as e:
        print(f"Error al obtener el secreto: {e}")
        return None


main = Blueprint('main', __name__)

@main.route('/')
def index():
    productos = Producto.query.all()
    return render_template('index.html', productos=productos)

@main.route('/buscar-lote', methods=['POST'])
def buscar_lote():
    lote = request.json.get('lote')
    
    producto = Producto.query.filter_by(lote=lote).first()
    
    if producto:
        return jsonify({
            'existe': True,
            'lote': producto.lote,
            'nombre': producto.nombre,
            'caducidad': producto.caducidad,
            'cantidad': producto.cantidad,
            'cve_art': producto.cve_art
        }), 200
    else:
        return jsonify({'existe': False}), 404

@main.route('/agregar-producto', methods=['POST'])
def agregar_producto():
    data = request.json
    nuevo_producto = Producto(
        lote=data.get('lote'),
        nombre=data.get('nombre'),
        caducidad=data.get('caducidad'),
        cantidad=data.get('cantidad'),
        cve_art=data.get('cve_art')
    )
    
    db.session.add(nuevo_producto)
    db.session.commit()
    
    return jsonify({'mensaje': 'Producto agregado exitosamente'}), 201

@main.route('/verificar-factura', methods=['POST'])
def verificar_factura():
    lote = request.json.get('lote')
    cantidad = request.json.get('cantidad')
    
    factura = Factura.query.filter_by(lote=lote).first()  # Asumiendo que tienes un modelo Factura
    
    if factura:
        if factura.cant == cantidad:
            return jsonify({'coincide': True, 'cantidad_correcta': True}), 200
        else:
            return jsonify({'coincide': True, 'cantidad_correcta': False}), 200
    else:
        return jsonify({'coincide': False}), 404



