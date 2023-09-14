from flask import Blueprint, render_template, request, jsonify
from .models import db, Producto, Factura
import boto3
import pandas as pd
from io import BytesIO

s3_client = boto3.client('s3', region_name='us-east-1')
client = boto3.client('secretsmanager', region_name='us-east-1')

def get_excel_from_s3():
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=FILE_NAME)
    data = obj['Body'].read()

    # Leer las hojas "BASE" y "FACTURAS"
    base_df = pd.read_excel(BytesIO(data), sheet_name="BASE")
    facturas_df = pd.read_excel(BytesIO(data), sheet_name="FACTURAS")

    return base_df, facturas_df


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

s3_client = boto3.client('s3', region_name='us-east-1')




main = Blueprint('main', __name__)

@app.route('/test-s3', methods=['GET'])
def test_s3():
    base_df, facturas_df = get_excel_from_s3()
    return jsonify({
        "BASE_columns": list(base_df.columns),
        "BASE_shape": base_df.shape,
        "FACTURAS_columns": list(facturas_df.columns),
        "FACTURAS_shape": facturas_df.shape
    })


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




