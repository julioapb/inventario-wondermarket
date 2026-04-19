from flask import Flask, render_template, url_for, request, make_response, redirect, Response, Blueprint,send_from_directory

import application
from . import foto_diaria
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

@foto_diaria.route('/foto')
def fotod():
    
    
    return render_template('filtro_foto.html')

@foto_diaria.route('/filtro',methods=['POST','GET'])
def filtrof():
    conexion=obtener_conexion()
    with conexion.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE calculo_foto;")
            conexion.commit()

    fecha = request.form['fecha'] + ' 00:00:00'
    fecha_2 = request.form['fecha_2'] + ' 00:00:00'
    #print(fecha)
    conexion=obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, sku, cant_v, tipo_producto, fecha, estado_2 FROM historial_cargues_ventas WHERE fecha  BETWEEN %s AND %s OR estado_2 = 'PENDIENTE'",(fecha, fecha_2))
        data = result_set = cursor.fetchall()
        print(data)
        for x in data:
            #print(x[1])
            cantidad_v = int(x[2])
            tipo_producto = x[3]
            sku = x[1]
            id_hc = x[0]
            fecha = x[4]
            estado_2=x[5]
    
            if(tipo_producto == 'COMBO'):
                
                conexion=obtener_conexion()
                with conexion.cursor() as cursor:
                    cursor.execute('SELECT sku_indivisible FROM combos WHERE sku_combo = %s',(sku))
                    combos = result_set = cursor.fetchall()

                    for j in combos:
                        sku_padre_2 = j[0]
                        conexion=obtener_conexion()
                        with conexion.cursor() as cursor:
                            cursor.execute('SELECT sku_indivisible, cantidad, sku_padre, descripcion FROM productos WHERE sku_padre = %s',(sku_padre_2))
                            data_2 = result_set = cursor.fetchone()
                            #print(data_2)
                            sku_indivisible =  data_2[0]
                            cantidad_p =  int(data_2[1])
                            descripcion =  data_2[3]
                            total_venta = int(cantidad_p * cantidad_v)
                            #print(descripcion)

                        with conexion.cursor() as cursor:
                            cursor.execute('INSERT INTO calculo_foto (sku_indivisible,descripcion,sku_padre,cant_v,cantidad,total_venta, id_hc, fecha, estado_2) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)',(sku_indivisible,descripcion,sku_padre,cantidad_v,cantidad_p,total_venta,id_hc, fecha, estado_2))
                            conexion.commit()
                        

            
            else:
                sku_padre = x[1]
                
                conexion=obtener_conexion()
                with conexion.cursor() as cursor:
                    cursor.execute('SELECT sku_indivisible, cantidad, sku_padre, descripcion FROM productos WHERE sku_padre = %s',(sku_padre))
                    data_2 = result_set = cursor.fetchone()
                    print(data_2[0])
                    sku_indivisible =  data_2[0]
                    cantidad_p =  int(data_2[1])
                    descripcion =  data_2[3]
                    total_venta = int(cantidad_p * cantidad_v)
                    #print(descripcion)

                    with conexion.cursor() as cursor:
                         cursor.execute('INSERT INTO calculo_foto (sku_indivisible,descripcion,sku_padre,cant_v,cantidad,total_venta, id_hc,fecha, estado_2) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)',(sku_indivisible,descripcion,sku_padre,cantidad_v,cantidad_p,total_venta, id_hc,fecha, estado_2))
                         conexion.commit()

    conexion=obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT cf.id, cf.sku_indivisible, cf.descripcion,cf.cantidad AS Relacion,SUM(cf.total_venta) AS Total_Vendido, i.cantidad AS cantidad_inventario, cf.id_hc, cf.fecha, cf.estado_2,  (SELECT GROUP_CONCAT( concat(proveedor, ' -> ', precio) SEPARATOR ' , ') FROM proveedor where proveedor.sku_indivisible = i.sku_indivisible) as proveedor FROM calculo_foto cf INNER JOIN inventario i ON (cf.sku_indivisible = i.sku_indivisible) GROUP BY cf.sku_indivisible ORDER BY proveedor desc, cf.estado_2 asc;")
        resultado = cursor.fetchall()
        #print(resultado)
    
    return render_template('filtro_foto.html', datos = resultado)


    