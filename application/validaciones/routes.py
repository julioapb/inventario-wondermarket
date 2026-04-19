from flask import Flask, render_template, url_for, request, make_response, redirect, Response, Blueprint, send_file
from . import validaciones
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
from datetime import date
from datetime import datetime
import subprocess



today = date.today()
fecha_actual = today.strftime("%d-%m-%Y")

def UpdateCantidad(cantidad, id):

    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
            cursor.execute("UPDATE productos SET cantidad = %s WHERE id = %s, ",(cantidad, id))
            conexion.commit()

    return 'ok'


@validaciones.route('/validacionesCantidad')
def validacionesCantidad():
    try:
        
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id_producto, sku_indivisible, sku_padre, cantidad FROM productos WHERE cantidad = 0")
            result_set = cursor.fetchall()
        
        if result_set:
            
            for x in result_set:
                
                cantidad = 1
                id = x[0]

                UpdateCantidad(cantidad, id)
        
            # Convertir tuplas a diccionarios
            columnas = [desc[0] for desc in cursor.description]
            result_set_dict = [dict(zip(columnas, row)) for row in result_set]

            file_path = 'C:\\python\\validacion_cantidad_0_'+fecha_actual+'.txt'
            with open(file_path, 'w') as file:
                for row in result_set_dict:
                    file.write(f"id_producto: {row['id_producto']}, sku_indivisible: {row['sku_indivisible']}, sku_padre: {row['sku_padre']}, cantidad: {row['cantidad']}\n")

            return send_file(file_path, as_attachment=True)
        
        else:
            print('Validación Cantidad sin problemas')
            #return render_template('validaciones.html')

    except Exception as e:
        flash(f"Ha ocurrido un error: {e}", 'error')
        return redirect(url_for('validaciones'))

    return render_template('validaciones.html')



@validaciones.route('/validacionCombos')
def validacionCombos():

    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id_producto, sku_indivisible, sku_padre, cantidad FROM productos WHERE tipo_producto = 'COMBO' and cantidad != 1")
            result_set = cursor.fetchall()
        
        if result_set:
        
            # Convertir tuplas a diccionarios
            columnas = [desc[0] for desc in cursor.description]
            result_set_dict = [dict(zip(columnas, row)) for row in result_set]

            file_path = 'C:\\python\\validacion_combos_diferente_1_'+fecha_actual+'.txt'
            with open(file_path, 'w') as file:
                for row in result_set_dict:
                    file.write(f"id_producto: {row['id_producto']}, sku_indivisible: {row['sku_indivisible']}, sku_padre: {row['sku_padre']}, cantidad: {row['cantidad']}\n")

            return send_file(file_path, as_attachment=True)
        
        else:

            print('Validación Combos sin problemas')
            #return render_template('validaciones.html')
        
    except Exception as e:
        flash(f"Ha ocurrido un error: {e}", 'error')
        return redirect(url_for('validaciones'))

    return render_template('validaciones.html')


@validaciones.route('/validaPrecio0')
def validaPrecio0():

    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id_producto, precio, sku_indivisible, sku_padre,cantidad, tipo_producto FROM productos WHERE  sku_indivisible = sku_padre AND tipo_producto = 'UNITARIO' AND precio = 0.0")
            result_set = cursor.fetchall()
        
        if result_set:
        
            # Convertir tuplas a diccionarios
            columnas = [desc[0] for desc in cursor.description]
            result_set_dict = [dict(zip(columnas, row)) for row in result_set]

            file_path = 'C:\\python\\validacion_precio_0_'+fecha_actual+'.txt'
            with open(file_path, 'w') as file:
                for row in result_set_dict:
                    file.write(f"id_producto: {row['id_producto']}, sku_indivisible: {row['sku_indivisible']}, sku_padre: {row['sku_padre']}, precio: {row['precio']}\n")

            return send_file(file_path, as_attachment=True)
        
        else:

            print('Validación Combos sin problemas')
            #return render_template('validaciones.html')
        
    except Exception as e:
        flash(f"Ha ocurrido un error: {e}", 'error')
        return redirect(url_for('validaciones'))

    return render_template('validaciones.html')

