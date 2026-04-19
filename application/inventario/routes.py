from flask import Flask, render_template, url_for, request, make_response, redirect, Response, Blueprint
from . import inventario
from ast import dump
from datetime import datetime
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

#muestra inventario
@inventario.route('/invent_general')
def invent_general():
    conexion=obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT i.id, i.sku_indivisible, p.descripcion,i.cantidad, i.inventario_en_proceso, i.inventario_en_proceso + i.cantidad  as total, i.estado FROM inventario i inner JOIN productos p ON(i.sku_indivisible = p.sku_indivisible)where p.sku_indivisible = p.sku_padre')
        result_set = cursor.fetchall()
        #print(result_set)
    
    return render_template('inv_general.html',productos = result_set)

#editar inventario
@inventario.route('/editInventario/<id>')
def get_inv(id):

    conexion=obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT sku_indivisible, cantidad, inventario_en_proceso FROM inventario WHERE id = %s',(id))
        data = result_set = cursor.fetchall()
        
    return render_template('edit_inventario.html', data = data)

#actualiza inventario
@inventario.route('/updateInvGral/<id>', methods=['POST'])
def update_inventario(id):

        cantidad = request.form['cantidad']
        cantidad_en_proceso = request.form['cantidad_en_proceso']
        
        conexion=obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("UPDATE inventario SET cantidad = %s, inventario_en_proceso = %s WHERE sku_indivisible = %s",(cantidad,cantidad_en_proceso, id))
            conexion.commit()
    
        return render_template('inv_general.html')

@inventario.route('/ingreso_inventario_2', methods=['POST', 'GET'])
def ingreso_inventario():
    conexion_12=obtener_conexion()
    with conexion_12.cursor() as cursor:
        cursor.execute("SELECT nombre_proveedor FROM lista_proveedor")
        result_set_12 = cursor.fetchall()

    if request.method == 'POST':
        sku_2 = request.form['sku_indivisible']
        #print(sku_2)
        cantidad = request.form['cantidad']
        tipo_ingreso = request.form['tipo_ingreso']
        no_factura = request.form['no_factura']
    
        if tipo_ingreso == 'fisico':
            campo = 'cantidad'
            conexion_3=obtener_conexion()
            with conexion_3.cursor() as cursor:
                cursor.execute('SELECT cantidad FROM inventario WHERE sku_indivisible = %s',(sku_2))
                data_3 = result_set = cursor.fetchone()
                cantidad_tabla = data_3[0]
                total = int(cantidad_tabla) + int(cantidad)
                print(total)
                cursor.execute("UPDATE inventario SET cantidad = %s WHERE sku_indivisible = %s",(total,sku_2))
                conexion_3.commit()
                
            #guarda_factura
            conexion_5=obtener_conexion()
            with conexion_5.cursor() as cursor:
                cursor.execute('INSERT INTO facturacion (sku_indivisible,cantidad,tipo_ingreso,no_factura,estado) VALUES (%s,%s,%s,%s,%s)',(sku_2,cantidad,tipo_ingreso,no_factura,1))
                conexion_5.commit()

        elif tipo_ingreso == 'en_progrso':
            campo = 'inventario_en_proceso'
            conexion_4=obtener_conexion()
            with conexion_4.cursor() as cursor:
                cursor.execute('SELECT inventario_en_proceso FROM inventario WHERE sku_indivisible = %s',(sku_2))
                data_4 = result_set = cursor.fetchone()
                cantidad_tabla_2 = data_4[0]
                total_2 = int(cantidad_tabla_2) + int(cantidad)
                print(total_2)
                cursor.execute("UPDATE inventario SET inventario_en_proceso = %s WHERE sku_indivisible = %s",(total_2,sku_2))
                conexion_4.commit()

            #guarda_factura
            conexion_6=obtener_conexion()
            with conexion_6.cursor() as cursor:
                cursor.execute('INSERT INTO facturacion (sku_indivisible,cantidad,tipo_ingreso,no_factura,estado) VALUES (%s,%s,%s,%s,%s)',(sku_2,cantidad,tipo_ingreso,no_factura,1))
                conexion_6.commit()
        
    return render_template('gestion_3.html', proveedores = result_set_12)

#Metodo para guardar el historial diario del inventario4
@inventario.route('/guardar_inventario_actual')
def guardarHistorialInventario():
    
    conexion =obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE historial_inventario SET activo = 0")
        conexion.commit()

    conexion =obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT sku_indivisible, cantidad FROM inventario")
        inventario  = cursor.fetchall()
        
        fecha  = datetime.now().date()
        
        for x in inventario:
            
            sku_indivisible = x[0]
            cantidad = x[1]
            activo = 1

            with conexion.cursor() as cursor:
                cursor.execute('INSERT INTO historial_inventario (sku_indivisible,cantidad,fecha, activo) VALUES (%s,%s,%s, %s)',(sku_indivisible,cantidad,fecha, activo))
                conexion.commit()
            
    flash("Historial Guardado correctamente",'success')
    return render_template('inv_general.html') 
