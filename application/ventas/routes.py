from http.client import PRECONDITION_REQUIRED
from flask import Flask, render_template, url_for, request, make_response, redirect, Response, Blueprint
from . import ventas
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

@ventas.route('/gestion_cargas')
def gestion_cargas():
    
    conexion=obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT h.id, h.order_id, h.sku, h.nombre_corto_sku, h.cant_v,p.cantidad,h.cant_v * p.cantidad as total_vendido,h.destinatario, h.fecha, h.estado_2, p.sku_indivisible, p.sku_padre, p.nombre, p.tipo_producto, p.descripcion FROM `historial_cargues_ventas` h INNER JOIN productos p ON(h.sku = p.sku_padre) ORDER BY h.id desc LIMIT 1000;")
        #cursor.execute("SELECT h.id, h.order_id, h.sku, h.nombre_corto_sku, h.cant_v,p.cantidad,h.cant_v * p.cantidad as total_vendido,h.destinatario, h.fecha, h.estado_2, p.sku_indivisible, p.sku_padre, p.nombre, p.tipo_producto, p.descripcion FROM `historial_cargues_ventas` h INNER JOIN productos p ON(h.sku = p.sku_padre) LEFT JOIN (SELECT case when estado_2 = 'PENDIENTE' THEN 1 ELSE 2 END loco,estado_2 FROM historial_cargues_ventas) t  ON (h.estado_2 =t.estado_2) ORDER BY t.loco")
        result_set = cursor.fetchall()

    return render_template('gestion_cargas.html', cargas = result_set)

@ventas.route('/actualiza_venta/<id>', methods=['POST'])
def actualiza_venta(id):

    date = time.strftime("%x")
    #date = (datetime.today().strftime('%Y-%m-%d'))

    estado = request.form['estado_2']
    sku = request.form['sku']
    sku_indivisible = request.form['sku_indivisible']
    cantidad_v = request.form['cantidad_v']
    tipo_producto = request.form['tipo_producto']
    order_id = request.form['order_id']
    
    if(tipo_producto=='COMBO'):
        
        if(estado == 'CANCELADO POR EL CLIENTE'):
            
            #aca hay que poner el estado toca hacer iagual que en el normal
            #ok
            
            conexion=obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute("SELECT sku_indivisible FROM combos WHERE sku_combo = %s",(sku))
                result_set_2 = cursor.fetchall()
                #relacion: es la cantidad de unidades del producto
                #ok
            for x in result_set_2:
                sku_indivisible_2 = (x[0])
               
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT sku_padre, cantidad FROM productos WHERE sku_padre = %s",(sku_indivisible_2))
                    result_set_3 = cursor.fetchall()

                    sku_c = result_set_3[0][0]
                    relacion = result_set_3[0][1]
                    

                with conexion.cursor() as cursor:
                    cursor.execute("SELECT cantidad FROM inventario WHERE sku = %s",(sku_indivisible_2))
                    result_set_5 = cursor.fetchall()

                cantidad_inv_c = result_set_5[0][0]
                
                total = (int(cantidad_v) * int(relacion)) + int(cantidad_inv_c)

                #actualiza el inventario combos
                conexion=obtener_conexion()
                with conexion.cursor() as cursor:
                    cursor.execute("UPDATE inventario SET cantidad = %s WHERE sku = %s", (total,sku_indivisible_2))
                    conexion.commit()
                
                #update historial cargues ventas

                #actualiza el estado en historial cargues
                conexion=obtener_conexion()
                with conexion.cursor() as cursor:
                    cursor.execute("UPDATE historial_cargues_ventas SET estado_2 = %s WHERE id = %s",('CANCELADO POR EL CLIENTE', id))
                    conexion.commit()

                #LOG COMBOS
                conexion = obtener_conexion()
                with conexion.cursor() as cursor:
                    cursor.execute("INSERT INTO log (accion,fecha,sku_indivisible, order_id, usuario) VALUES (%s,%s,%s,%s,%s)",('CANCELACION COMBO', date ,sku_c, order_id,'USER'))
                    conexion.commit()

        elif(estado == 'REEMBOLSO'):
             #aca hay que poner el estado toca hacer iagual que en el normal
            
            conexion=obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute("SELECT sku_indivisible FROM combos WHERE sku_combo = %s",(sku))
                result_set_2 = cursor.fetchall()
                #relacion: es la cantidad de unidades del producto
            
            for x in result_set_2:
                sku_indivisible_2 = (x[0])
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT sku_padre, cantidad FROM productos WHERE sku_padre = %s",(sku_indivisible_2))
                    result_set_3 = cursor.fetchall()

                    sku_c = result_set_3[0][0]
                    relacion = result_set_3[0][1]

                with conexion.cursor() as cursor:
                    cursor.execute("SELECT cantidad FROM inventario WHERE sku = %s",(sku_indivisible_2))
                    result_set_5 = cursor.fetchall()

                cantidad_inv_c = result_set_5[0][0]

                total = (int(cantidad_v) * int(relacion)) + int(cantidad_inv_c)

                #actualiza el inventario combos
                conexion=obtener_conexion()
                with conexion.cursor() as cursor:
                    cursor.execute("UPDATE inventario SET cantidad = %s WHERE sku = %s", (total,sku_indivisible_2))
                    conexion.commit()
                #LOG COMBOS
                conexion = obtener_conexion()
                with conexion.cursor() as cursor:
                    cursor.execute("INSERT INTO log (accion,fecha,sku_indivisible, order_id,usuario) VALUES (%s,%s,%s,%s,%s)",('REEMBOLSO', date ,sku_c, order_id,'USER'))
                    conexion.commit()

                #actualiza el estado en historial cargues
                conexion=obtener_conexion()
                with conexion.cursor() as cursor:
                    cursor.execute("UPDATE historial_cargues_ventas SET estado_2 = %s WHERE id = %s",('REEMBOLSO', id))
                    conexion.commit()

        elif(estado == 'PROCESADO'):
            
            conexion=obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute("UPDATE historial_cargues_ventas SET estado_2 = %s WHERE id = %s",('PROCESADO', id))
                conexion.commit()
            
            
            conexion=obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute("SELECT sku_indivisible FROM combos WHERE sku_combo = %s",(sku))
                result_set_2 = cursor.fetchall()
                #relacion: es la cantidad de unidades del producto
            
            for x in result_set_2:
                sku_indivisible_2 = (x[0])
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT sku_padre, cantidad FROM productos WHERE sku_padre = %s",(sku_indivisible_2))
                    result_set_3 = cursor.fetchall()

                    sku_c = result_set_3[0][0]


                with conexion.cursor() as cursor:
                    cursor.execute("INSERT INTO log (accion,fecha,sku_indivisible, order_id ,usuario) VALUES (%s,%s,%s,%s,%s)",('PROCESADO', date ,sku_c, order_id,'USER'))
                    conexion.commit()

        elif(estado == 'PENDIENTE'):
            #actualiza el estado en historial cargues
            conexion=obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute("UPDATE historial_cargues_ventas SET estado_2 = %s WHERE id = %s",('PENDIENTE', id))
                conexion.commit()
            
            
            conexion=obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute("SELECT sku_indivisible FROM combos WHERE sku_combo = %s",(sku))
                result_set_2 = cursor.fetchall()
                #relacion: es la cantidad de unidades del producto
            
            for x in result_set_2:
                sku_indivisible_2 = (x[0])
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT sku_padre, cantidad FROM productos WHERE sku_indivisible = %s",(sku_indivisible_2))
                    result_set_3 = cursor.fetchall()

                    sku_c = result_set_3[0][0]


                with conexion.cursor() as cursor:
                    cursor.execute("INSERT INTO log (accion,fecha,sku_indivisible, order_id ,usuario) VALUES (%s,%s,%s,%s,%s)",('PENDIENTE', date ,sku_c, order_id,'USER'))
                    conexion.commit()

    else:
        
        if(estado == 'CANCELADO POR EL CLIENTE'):
            
            conexion=obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute("SELECT cantidad FROM productos WHERE sku_padre = %s",(sku))
                result_set_2 = cursor.fetchone()
               
                relacion = result_set_2[0]
                print(sku_indivisible)
            conexion=obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute("SELECT cantidad FROM inventario WHERE sku = %s",(sku_indivisible))
                result_set = cursor.fetchone()
                print(result_set)
                #cantidad_inv: es la cantidad de unidades del producto en el inventario
                cantidad_inv = result_set[0]

            #total: suma de los productos que se habian descontado
            total = (int(cantidad_v) * int(relacion)) + int(cantidad_inv)

            #actualiza el inventario
            conexion=obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute("UPDATE inventario SET cantidad = %s WHERE sku_indivisible = %s", (total,sku_indivisible))
                conexion.commit()

            #actualiza el estado en historial cargues
            conexion=obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute("UPDATE historial_cargues_ventas SET estado_2 = %s WHERE id = %s",('CANCELADO POR EL CLIENTE', id))
                conexion.commit()

            #log
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute("INSERT INTO log (accion,fecha,sku_indivisible,order_id ,usuario) VALUES (%s,%s,%s,%s,%s)",('CAMBIO ESTADO CANCELADO POR CLIENTE', date ,sku_indivisible, order_id ,'USER'))
                conexion.commit()
           
        
        elif(estado == 'REEMBOLSO'):
            print(sku_indivisible)
            conexion=obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute("SELECT cantidad FROM productos WHERE sku_padre = %s",(sku))
                result_set_2 = cursor.fetchone()
                #relacion: es la cantidad de unidades del producto
                relacion = result_set_2[0]

            conexion=obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute("SELECT cantidad FROM inventario WHERE sku = %s",(sku_indivisible))
                result_set = cursor.fetchone()
                #cantidad_inv: es la cantidad de unidades del producto en el inventario
                cantidad_inv = result_set[0] 

            #total: suma de los productos que se habian descontado

           

            total = (int(cantidad_v) * int(relacion)) + int(cantidad_inv)
            print(total)
            #actualiza el inventario
            conexion=obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute("UPDATE inventario SET cantidad = %s WHERE sku = %s", (total,sku_indivisible))
                conexion.commit()

            #actualiza el estado en historial cargues
            conexion=obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute("UPDATE historial_cargues_ventas SET estado_2 = %s WHERE id = %s",('REEMBOLSO', id))
                conexion.commit()

            #log
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute("INSERT INTO log (accion,fecha,sku_indivisible,order_id ,usuario) VALUES (%s,%s,%s,%s,%s)",('REEMBOLSO', date ,sku_indivisible, order_id,'USER'))
                conexion.commit()

        elif(estado == 'PROCESADO'):
            #actualiza el estado en historial cargues
            conexion=obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute("UPDATE historial_cargues_ventas SET estado_2 = %s WHERE id = %s",('PROCESADO', id))
                conexion.commit()

            estad= 'PROCESADO'
            usu = 'USUARIO'

            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute("INSERT INTO log (accion,fecha,sku_indivisible, order_id,usuario) VALUES (%s,%s,%s,%s,%s)",(estad, date ,sku_indivisible, order_id,usu))
                conexion.commit()
            
        elif(estado == 'PENDIENTE'):
            #actualiza el estado en historial cargues
            conexion=obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute("UPDATE historial_cargues_ventas SET estado_2 = %s WHERE id = %s",('PENDIENTE', id))
                conexion.commit()

            #log
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute("INSERT INTO log (accion,fecha,sku_indivisible, order_id,usuario) VALUES (%s,%s,%s,%s,%s)",('PENDIENTE', date ,sku_indivisible, order_id,'USER'))
                conexion.commit()
    
    return redirect(url_for('ventas.gestion_cargas'))
