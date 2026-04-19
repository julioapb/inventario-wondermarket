from flask import Flask, render_template, url_for, request, make_response, redirect, Response, Blueprint, session
from . import inicio
from application import productos
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
from datetime import datetime

@inicio.route('/panel', methods=['GET'])
def panel():

    return render_template('inicio.html')


#@inicio.route('/', methods=['GET'])
@inicio.route('/add_product', methods=['POST','GET'])
def add_product():
    if request.method == 'POST':
        #se aplica strip() para quitar espacios en blanco
        recibe_sku_indivisible = request.form['sku_indivisible']
        sku_indivisible = recibe_sku_indivisible.strip()

        recibe_sku_padre = request.form['sku_padre']
        sku_padre = recibe_sku_padre.strip()

        ean = request.form['ean']
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        impuesto = request.form['impuesto']
        descripcion = request.form['descripcion']
        fecha_caducidad = request.form['fecha_caducidad']
        precio = request.form['precio']
        localizacion = request.form['localizacion']
        promocion = request.form['promocion']
        sku_transitorio = request.form['sku_transitorio']
        valoracion = request.form['valoracion']
        peso = request.form['peso']
        cant_trans = request.form['cant_trans']

        if precio:
            print('precio')
        else:
            precio = 0.0
            print(precio)

        if peso:
            print('precio')
        else:
            peso = 0.0
            print(peso)

  
        if(sku_indivisible == sku_padre):
            
            tipo_producto = 'UNITARIO'
            
            conexion=obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute('SELECT sku_padre FROM productos WHERE sku_padre = %s', sku_padre)
                result_set = cursor.fetchone()

                if(result_set):
                    
                    flash(f'{sku_indivisible} PRODUCTO EXISTENTE VALIDE SKU EN PRODUCTOS', 'error')
                    
                else:
                    with conexion.cursor() as cursor:
                        cursor.execute('INSERT INTO productos (sku_indivisible,sku_padre,ean,nombre,cantidad,impuesto,fecha_caducidad,descripcion,estado, precio, tipo_producto,localizacion, promocion, sku_transitorio, valoracion, peso, cant_trans) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(sku_indivisible,sku_padre,ean,nombre,cantidad,impuesto,fecha_caducidad,descripcion,1,precio, tipo_producto,localizacion, promocion, sku_transitorio, valoracion,peso,cant_trans))
                        conexion.commit()

                    #log producto simple
                    usuario = session['usuario']
                    accion = 'Crear producto simple'
                    fecha_y_hora_actual = datetime.now()
                    
                    with conexion.cursor() as cursor:
                        cursor.execute('INSERT INTO log_usuarios (usuario,accion,sku_afectado,sku_indivisible, tipo_producto, fecha) VALUES (%s,%s,%s,%s,%s,%s)',(usuario,accion,sku_indivisible,sku_padre,tipo_producto,fecha_y_hora_actual))
                        conexion.commit()
                    
                    with conexion.cursor() as cursor:
                        cursor.execute('SELECT sku_indivisible FROM inventario WHERE sku_indivisible = %s', sku_indivisible)
                        result_inven = cursor.fetchone()
                    
                    if(result_inven):
                        print('paila')
                        
                    else:
                        with conexion.cursor() as cursor:
                            cursor.execute('INSERT INTO inventario (sku_indivisible,sku,cantidad,inventario_en_proceso,estado) VALUES (%s,%s,%s,%s,%s)',(sku_indivisible,sku_padre,0,0,0))
                            conexion.commit()

                        session['usuario']
                    flash(f'EL PRODUCTO {sku_indivisible} fue creado con éxito', 'success')
            
            return redirect(url_for('inicio.panel'))
        
        elif(sku_indivisible != sku_padre):

            
            
            tipo_producto = 'PACK'
            #precio = round(float(precio) * int(cantidad),2)
            conexion=obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute('SELECT * FROM productos WHERE sku_indivisible = %s', sku_indivisible)
                valida_existencia_sku = cursor.fetchone()
            
            if valida_existencia_sku:

                if(precio == ''):
                    precio = float(precio) * int(cantidad)
                
                with conexion.cursor() as cursor:
                    cursor.execute('SELECT fecha_caducidad, precio, localizacion, peso, valoracion FROM productos WHERE sku_padre = %s', sku_padre)
                    data_sku = cursor.fetchone()

                    if data_sku:
                        fecha_caducidad, precio, localizacion, peso, valoracion = data_sku

                        print(fecha_caducidad, precio, localizacion, peso, valoracion )

                conexion=obtener_conexion()
                with conexion.cursor() as cursor:
                    cursor.execute('SELECT sku_padre FROM productos WHERE sku_padre = %s', sku_padre)
                    result_set = cursor.fetchone()

                    if(result_set):
                        flash("PRODUCTO EXISTENTE VALIDE SKU EN PRODUCTOS")
                        
                    else:
                        print(impuesto)
                        cursor.execute('INSERT INTO productos (sku_indivisible,sku_padre,ean,nombre,cantidad,impuesto,fecha_caducidad,descripcion,estado, precio, tipo_producto,localizacion, promocion, sku_transitorio, valoracion, peso, cant_trans) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(sku_indivisible,sku_padre,ean,nombre,cantidad,impuesto,fecha_caducidad,descripcion,1,precio, tipo_producto,localizacion, promocion, sku_transitorio, valoracion,peso,cant_trans))
                        conexion.commit()

                        #log producto simple
                        usuario = session['usuario']
                        accion = 'Crear producto pack'
                        fecha_y_hora_actual = datetime.now()
                        
                        with conexion.cursor() as cursor:
                            cursor.execute('INSERT INTO log_usuarios (usuario,accion,sku_afectado,sku_indivisible, tipo_producto, fecha) VALUES (%s,%s,%s,%s,%s,%s)',(usuario,accion,sku_indivisible,sku_padre,tipo_producto,fecha_y_hora_actual))
                            conexion.commit()

                        with conexion.cursor() as cursor:
                            cursor.execute('SELECT sku_indivisible FROM inventario WHERE sku_indivisible = %s', sku_indivisible)
                            result_inven = cursor.fetchone()
                        
                        if(result_inven):
                            print('paila')
                            
                        else:
                            cursor.execute('INSERT INTO inventario (sku_indivisible,sku,cantidad,inventario_en_proceso,estado) VALUES (%s,%s,%s,%s,%s)',(sku_indivisible,sku_padre,0,0,0))
                            #conexion.commit()

                            session['usuario']
                        flash(f'EL PRODUCTO {sku_indivisible} fue creado con éxito', 'success')
            else:
                flash(f'{sku_indivisible} NO EXISTE EN LA BD VALIDAR', 'error')
            
            return redirect(url_for('inicio.panel'))
            #fecha_caducidad, coste * cantidad, impuesto, localizacion, peso * cantidad, valoracion

     