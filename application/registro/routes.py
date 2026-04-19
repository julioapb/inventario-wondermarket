from flask import Flask, render_template, url_for, request, make_response, redirect, Response, Blueprint,send_from_directory, send_file
import application
from . import registro
from ast import dump
import datetime
from operator import index
from socket import IPV6_DONTFRAG
import time
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import flask
from flask.helpers import flash
from numpy import append
import sqlalchemy
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
import pymysql
from . bd import obtener_conexion
import json
import mysql.connector
from mysql import connector
import pandas as pd
import csv
import sqlite3
import xlrd
import io
from io import BytesIO
import xlwt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import pandas as pd

@registro.route('/registroUsuario')
def registroUsuario():
    
    return render_template('registro.html')


@registro.route('/ingreso_usuario',methods=['GET', 'POST'])
def ingreso_usuario():
    conexion=obtener_conexion()

    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']

        hashed_password = generate_password_hash(password,method='pbkdf2:sha256')

        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO usuarios (usuario, password, fecha) VALUES (%s, %s,%s)', (usuario, hashed_password, datetime.now()))
            conexion.commit()
    
    flash("Usuario creado correctamente")
    return redirect(url_for('inicio.panel')) 

def obtenerUsuarios():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT usuario FROM log_usuarios GROUP BY usuario')
        data_usuarios_1 = cursor.fetchall()
    
    return data_usuarios_1

@registro.route('/log_usuario', methods=['GET', 'POST'])
def logUsuario():
    
    data_usuarios_1= obtenerUsuarios()

    return render_template('log_usuario.html', data_usuarios_1 = data_usuarios_1)




@registro.route('/procesa_consulta_log', methods=['GET', 'POST'])
def procesaConsultaLog():
    conexion = obtener_conexion()
    usuario = request.form.get('usuario_log', '')
    sku_indivisible = request.form.get('sku_indivisible_log', '')
    sku = request.form.get('sku_log', '')
    accion = request.form.get('accion_log', '')
    fecha_1 = request.form.get('fecha_log_1', '')
    fecha_2 = request.form.get('fecha_log_2', '')
    tipo_filtro_log = request.form.get('tipo_filtro_log', '')
    exportar_excel = request.form.get('exportar_excel', '')

    fecha_1_final = fecha_1 + ' 00:00:00' if fecha_1 else ''
    fecha_2_final = fecha_2 + ' 23:59:59' if fecha_2 else ''

    data = []
    data_usuarios_1 = []

    query = ''
    params = ()

    if tipo_filtro_log == '1':
        data_usuarios_1= obtenerUsuarios()

        if fecha_1:
            query = 'SELECT * FROM log_usuarios WHERE usuario = %s AND fecha >= %s AND fecha <= %s'
            params = (usuario, fecha_1_final, fecha_2_final)
        else:
            query = 'SELECT * FROM log_usuarios WHERE usuario = %s'
            params = (usuario,)

    elif tipo_filtro_log == '2':
        data_usuarios_1= obtenerUsuarios()
        if fecha_1:
            query = 'SELECT * FROM log_usuarios WHERE sku_afectado = %s AND fecha >= %s AND fecha <= %s'
            params = (sku_indivisible, fecha_1_final, fecha_2_final)
        else:
            query = 'SELECT * FROM log_usuarios WHERE sku_afectado = %s'
            params = (sku_indivisible,)

    elif tipo_filtro_log == '3':
        data_usuarios_1= obtenerUsuarios()
        if fecha_1:
            query = 'SELECT * FROM log_usuarios WHERE sku_indivisible = %s AND fecha >= %s AND fecha <= %s'
            params = (sku, fecha_1_final, fecha_2_final)
        else:
            query = 'SELECT * FROM log_usuarios WHERE sku_indivisible = %s'
            params = (sku,)

    elif tipo_filtro_log == '4':
        data_usuarios_1= obtenerUsuarios()
        if fecha_1:
            query = 'SELECT * FROM log_usuarios WHERE accion = %s AND fecha >= %s AND fecha <= %s'
            params = (accion, fecha_1_final, fecha_2_final)
        else:
            query = 'SELECT * FROM log_usuarios WHERE accion = %s'
            params = (accion,)

    if query:
        with conexion.cursor() as cursor:
            cursor.execute(query, params)
            data = cursor.fetchall()

    # Si el usuario quiere exportar los datos a Excel
    if exportar_excel:
        df = pd.DataFrame(data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Log Usuarios')
        output.seek(0)

        return send_file(output, download_name='log_usuarios.xlsx', as_attachment=True)

    # Devolver la respuesta renderizando la plantilla
    return render_template('log_usuario.html', data=data, data_usuarios_1=data_usuarios_1)