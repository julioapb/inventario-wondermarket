from flask import Flask, render_template, url_for, request, make_response, redirect, Response, Blueprint,send_from_directory
import application
from . import cargas
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
import xlwt

@cargas.route('/cargas')
def carga():
    
    return render_template('cargas.html')

@cargas.route('/cargar_productos')
def cargar_productos():
  
    db = 'inventario'
    table = 'productos'
    path = "C:/python/cargar_productos.xlsx"
    
    url = "mysql+mysqlconnector://root:@localhost/"
    engine = create_engine(url +db)
    df = pd.read_excel(path)
    print("read ok")
    df.to_sql(name = table, con = engine, if_exists='append', index= False)

    conexion=obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT sku_indivisible, sku_padre FROM productos")
        result_set = cursor.fetchall()

        for x in result_set:
            sku_padre = x[1]
            sku_indivisible = x[0]

            if(sku_padre == sku_indivisible):
                cantidad = 0
                cantidad_inventario = 0
                estado = 0
                cursor.execute("SELECT sku FROM inventario WHERE sku = %s", sku_padre)
                result_set_2 = cursor.fetchone()

                if(result_set_2):
                    print('ok')
                else:
                    cursor.execute('INSERT INTO inventario (sku_indivisible,sku,cantidad,inventario_en_proceso,estado) VALUES (%s,%s,%s,%s,%s)',(sku_padre,sku_padre,cantidad_inventario,cantidad,estado))
                    conexion.commit()

    return render_template('home.html')


#@cargas.route("/", methods=['POST', 'GET'])
def upload_file():
 # renderiamos la plantilla "formulario.html"
 return render_template('formulario.html')

@cargas.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname (__file__) # La ruta donde se encuentra el archivo actual
        upload_path = os.path.join (basepath, 'C:\python', secure_filename (f.filename)) #Nota: Si no hay una carpeta, debe crearla primero, de lo contrario se le preguntará que no existe tal ruta
        f.save(upload_path)
        return redirect(url_for('cargas.carga'))
    return render_template('cargas.html')

    






