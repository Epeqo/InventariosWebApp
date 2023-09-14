from flask import Blueprint, render_template, request, jsonify, Flask, request, redirect, url_for, flash
from .models import db, Producto, Factura
import boto3
import pandas as pd
from io import BytesIO
import json

def obtener_credenciales_aws():
    nombre_secreto = "InventariosWeb"
    nombre_region = "us-east-2"
    
    cliente = boto3.client('secretsmanager', region_name=nombre_region)
    respuesta = cliente.get_secret_value(SecretId=nombre_secreto)
    
    if 'SecretString' in respuesta:
        secreto = json.loads(respuesta['SecretString'])
    else:
        raise ValueError("Error al obtener las credenciales de AWS desde el Secret Manager.")
    
    print("Secreto obtenido de AWS:", secreto)
    return secreto

CREDENCIALES_AWS = obtener_credenciales_aws()

# Extraer las claves y valores directamente del diccionario
CLAVE_ACCESO_AWS, CLAVE_SECRETA_AWS = list(CREDENCIALES_AWS.items())[0]
NOMBRE_BUCKET = CREDENCIALES_AWS.get('BUCKET_NAME')
NOMBRE_ARCHIVO = CREDENCIALES_AWS.get('FILE_NAME')

def obtener_excel_desde_s3():
    s3 = boto3.client('s3', aws_access_key_id=CLAVE_ACCESO_AWS, aws_secret_access_key=CLAVE_SECRETA_AWS, region_name='us-east-2')
    obj = s3.get_object(Bucket=NOMBRE_BUCKET, Key=NOMBRE_ARCHIVO)
    datos = obj['Body'].read()

    # Leer las hojas "BASE" y "FACTURAS"
    base_df = pd.read_excel(BytesIO(datos), sheet_name="BASE")
    facturas_df = pd.read_excel(BytesIO(datos), sheet_name="FACTURAS")

    return base_df, facturas_df

main = Blueprint('main', __name__)

@main.route('/test-s3', methods=['GET'])
def test_s3():
    base_df, facturas_df = obtener_excel_desde_s3()
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
    lote_ingresado = request.form.get('lote')
    base_df, _ = obtener_excel_desde_s3()

    # Imprimir las primeras 5 filas de la hoja "BASE" para verificar su contenido
    print(base_df.head())

    # Buscar el lote en la hoja "BASE"
    producto = base_df[base_df['LOTE'] == lote_ingresado]

    # Imprimir el resultado de la busqueda
    print(producto)

    if not producto.empty:
        # Si se encontro el producto, agregarlo a la base de datos y redirigir a la pagina principal
        return redirect(url_for('index'))
    else:
        flash('Lote no encontrado', 'danger')
        return redirect(url_for('index'))

@main.route('/agregar-producto', methods=['POST'])
def agregar_producto():
    datos = request.json
    nuevo_producto = Producto(
        lote=datos.get('lote'),
        nombre=datos.get('nombre'),
        caducidad=datos.get('caducidad'),
        cantidad=datos.get('cantidad'),
        cve_art=datos.get('cve_art')
    )
    
    db.session.add(nuevo_producto)
    db.session.commit()
    
    return jsonify({'mensaje': 'Producto agregado exitosamente'}), 201

@main.route('/verificar-factura', methods=['POST'])
def verificar_factura():
    lote = request.json.get('lote')
    cantidad = request.json.get('cantidad')
    
    factura = Factura.query.filter_by(lote=lote).first()
    
    if factura:
        if factura.cant == cantidad:
            return jsonify({'coincide': True, 'cantidad_correcta': True}), 200
        else:
            return jsonify({'coincide': True, 'cantidad_correcta': False}), 200
    else:
        return jsonify({'coincide': False}), 404


