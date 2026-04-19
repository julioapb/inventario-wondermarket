from flask import Flask, render_template, url_for, request, make_response, redirect, Response, Blueprint,send_from_directory
from woocommerce import API
import application
from . import gestion_ingresos
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
import requests
import mysql.connector
from mysql import connector
import pandas as pd
import csv
import sqlite3
import xlrd
import io
import xlwt


#inicio
@gestion_ingresos.route('/ing')
def gestion_ing():

    return render_template('ingresos.html')

#reestablece la tabla cargue_ingresos
@gestion_ingresos.route('/eliminaIngresos')
def eliminaTabla():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('TRUNCATE TABLE cargue_ingresos')
        conexion.commit()

    with conexion.cursor() as cursor:
        cursor.execute('TRUNCATE TABLE qty_ingreso_antes')
        conexion.commit()

    flash("TABLA REESTABLECIDA CORRECTAMENTE",'success')
    return render_template('ingresos.html')  


#cargue tabla ingresos
@gestion_ingresos.route('/cargue_ingresos')
def cargueIngresos():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT sku_indivisible FROM cargue_ingresos')
        valida_cargue_e = result_set = cursor.fetchall()

        if(valida_cargue_e):
            flash("Existe un cargue en la base de datos, por favor validar", 'error')
            return render_template('ingresos.html')
        
        else:

            db = 'inventario'
            table = 'cargue_ingresos'
            path = "C:/python/cargas_ingresos.xlsm"
            url = "mysql+mysqlconnector://root:@localhost/"
            engine = create_engine(url + db)
            df = pd.read_excel(path)
            df.to_sql(name = table, con = engine, if_exists='append', index= False)

            flash("INGRESOS CARGADOS CORRECTAMENTE", 'success')
            return render_template('ingresos.html')

#valida la existencia de los sku para ingresar
@gestion_ingresos.route('/valida_ingreso')
def validaIngreso():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT sku_indivisible FROM cargue_ingresos')
        cargue_ingresos = result_set = cursor.fetchall()
        #print(cargue_ingresos)
        no_existe = []
        for x in cargue_ingresos:
            sku_validate = x[0]
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute('SELECT sku_indivisible FROM productos WHERE sku_indivisible = %s',(sku_validate))
                producto_existe = cursor.fetchall()
                
            if(producto_existe):
                print('ok')
            else:
                no_existe.append(sku_validate)

        no_existentes = len(no_existe)

        if(no_existentes > 0):
            flash("SKU INEXISTENTE POR FAVOR VALIDAR",'error')
            return render_template('validacion.html',array_sku = no_existe)
        else:
            flash("EL CARGUE INGRESADO ES CORRECTO", 'success')
            return render_template('ingresos.html')

#gestion ingresos
@gestion_ingresos.route('/calculo_ingresos')
def calculaIng():
    
    #trae la informacion de a tabla cargue_ingresos
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT sku_indivisible, qty_ingreso, precio, proveedor, fecha_vencimiento, orden, fecha_recibido FROM cargue_ingresos')
        cargue_ingresos = result_set = cursor.fetchall()

        for x in cargue_ingresos:
            sku_indivisible_c = x[0]
            qty_ingreso = x[1] 
            precio_c = x[2]
            proveedor_c = x[3]
            orden_c = x[5]
            fecha_recibido = x[6]
            fecha_vencimiento_c = x[4]
            print(fecha_recibido)
            #validacion repetidos
            
            with conexion.cursor() as cursor:
                cursor.execute('SELECT * FROM historial_ingresos WHERE sku_indivisible = %s AND proveedor = %s AND fecha_recibido = %s',(sku_indivisible_c,proveedor_c, fecha_recibido))
                data_validacion = cursor.fetchall()
            if(data_validacion):
                qty_inventario = cantidadInventario()
                data_ingreso_antes = datsaIngresoAntes()
                flash("SE ENCONTRO UN REGISTRO REPETIDO EN EL HISTORIAL POR FAVOR REVISAR")
                return render_template('ingresos.html', qty_inventario = qty_inventario, data_ingreso_antes = data_ingreso_antes)
            
            else:
                
                #trae la informacion de qty y precio de las tablas inventario y precios
                with conexion.cursor() as cursor:
                    cursor.execute('SELECT i.cantidad, p.precio, p.fecha_caducidad  FROM productos p INNER JOIN inventario i ON(p.sku_padre = i.sku_indivisible) WHERE i.sku_indivisible = %s',sku_indivisible_c)
                    data_inventario = cursor.fetchall()

                    for j in data_inventario:
                        qty_base = j[0]
                        precio_b = j[1]  
                        fecha_caducidad_b = j[2]

                    qty_final = int(qty_base) + int(qty_ingreso)
                    #actualiza la cantidad en la tabla invemtario
                    
                    with conexion.cursor() as cursor:
                        cursor.execute('UPDATE inventario SET cantidad = %s WHERE sku_indivisible = %s', (qty_final, sku_indivisible_c) )
                        conexion.commit()

                        qty_inventario = cantidadInventario()
                        data_ingreso_antes = datsaIngresoAntes()

        guardaHistorial()
        data_calculada = dataCalculada()
        
        #ojo hacer pruebas
        eliminaTabla()
        flash("INGRESOS CALCULADOS CORRECTAMENTE",'success')
        return render_template('ingresos.html', qty_inventario = qty_inventario, data_ingreso_antes = data_ingreso_antes, data_calculada = data_calculada)


#identifica proveedores repetidos y los elimina
@gestion_ingresos.route('/p')
def funcioP():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT sku_indivisible, proveedor, id FROM cargue_ingresos')
        cargue_ingresos_p = cursor.fetchall()
        
        for x in cargue_ingresos_p:
            
            sku_indivisible_c = x[0]
            proveedor_c = x[1]
            id_c = x[2]

            #Selecciona sku y id de proveedor donde sku_cargue y el proveedor_cargue sea igual al de la bd
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute("SELECT sku_indivisible, id FROM proveedor WHERE sku_indivisible = %s AND proveedor = %s",(sku_indivisible_c, proveedor_c))
                cargue_rep = cursor.fetchall()

                #print(cargue_rep, len(cargue_rep))
                #SI HAY MAS DE UNA COMBINACION SKU PROVEEDOR ELIMINA LO ELIMINA
                if(len(cargue_rep) > 1):
                    for y in cargue_rep:
                        print(y[1], y[0])

                        conexion = obtener_conexion()
                        with conexion.cursor() as cursor:
                            cursor.execute("DELETE FROM proveedor WHERE id = %s",(y[1]))
                            conexion.commit()
                
                else:
                        print('ok no repetido')            

        return  render_template('validacion_repetidos.html')

#pone la P a los sku_indivisibles del cargue ingreso que tengan un solo porveedor
def ponerP():

    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT sku_indivisible, proveedor, id, precio, orden FROM cargue_ingresos')
        cargue_ingresos_p = cursor.fetchall()

    for x in cargue_ingresos_p:

        orden_2 = x[4]
        sku_indivisible = x[0]
        orden = 'P'
        precio = x[3]
        proveedor = x[1]

        if(orden_2 == 'P'):
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute('UPDATE productos SET precio = %s WHERE sku_padre = %s',(precio,sku_indivisible))
                conexion.commit()

            #borra la P del sku
            p_vacia = ''
            print('funcion2 ',p_vacia, sku_indivisible)
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute("UPDATE proveedor SET orden = %s WHERE sku_indivisible = %s", (p_vacia, sku_indivisible))
                conexion.commit()
            #Pone la P al propveddor que la tiene en el cargue
            print('funcion3 ', orden, sku_indivisible, proveedor)
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute("UPDATE proveedor SET orden = %s WHERE sku_indivisible = %s AND proveedor = %s", (orden, sku_indivisible, proveedor))
                conexion.commit()

        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT * FROM proveedor WHERE sku_indivisible = %s',(sku_indivisible))
            cantidad_proveedores = cursor.fetchone()
        
        cantidad_proveedores_def = cursor.rowcount
        
        if(cantidad_proveedores_def == 1):
            print(cantidad_proveedores_def,'--',sku_indivisible)
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute('UPDATE proveedor SET orden = %s WHERE sku_indivisible = %s',(orden,sku_indivisible))
                conexion.commit()
            
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute('UPDATE productos SET precio = %s WHERE sku_padre = %s',(precio,sku_indivisible))
                conexion.commit()

    return 'ok'


#actualiza o inserta segun sea el caso 
#ESTA ES LA ACTUAL TOCA DESACTIVARLA PARA HACER UNA NUEVA Y PRBAR
@gestion_ingresos.route('/controlp')
def controlap():

    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT sku_indivisible, proveedor, id, precio, orden FROM cargue_ingresos')
        cargue_ingresos_p = cursor.fetchall()
        
        #print(cargue_ingresos_p)

        for x in cargue_ingresos_p:
            
            sku_indivisible_c = x[0]
            proveedor_c = x[1]
            id_c = x[2]
            precio_c = x[3]
            orden_c = x[4]

            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute("SELECT sku_indivisible, id, orden FROM proveedor WHERE sku_indivisible = %s AND proveedor = %s",(sku_indivisible_c, proveedor_c))
                cargue_rep_2 = cursor.fetchall()
                #print(cargue_rep_2)
                cantidad_registros = cursor.rowcount
                
                for y in cargue_rep_2:
                    id_proveedor = y[1]
                    orden_proveedor = y[2]

                if(cantidad_registros == 0):

                    conexion = obtener_conexion()
                    with conexion.cursor() as cursor:
                        cursor.execute("INSERT INTO proveedor (sku_indivisible, proveedor, precio) VALUES (%s, %s,%s)", (sku_indivisible_c, proveedor_c, precio_c))
                        conexion.commit()

                elif(cantidad_registros == 1):
                    
                    if(orden_proveedor == 'P'):
                        print('actualiza tambien en productos', sku_indivisible_c, id_proveedor, orden_proveedor, precio_c)
                        #Actualiza el precio del proveedor al que viene en el cargue en la tabla proveedor
                        print('funcion1 ',precio_c, id_proveedor)
                        conexion = obtener_conexion()
                        with conexion.cursor() as cursor:
                            cursor.execute("UPDATE proveedor SET precio = %s WHERE id = %s", (precio_c, id_proveedor))
                            conexion.commit()
                        #borra la P del sku
                        p_vacia = ''
                        print('funcion2 ',p_vacia, sku_indivisible_c)
                        conexion = obtener_conexion()
                        with conexion.cursor() as cursor:
                            cursor.execute("UPDATE proveedor SET orden = %s WHERE sku_indivisible = %s", (p_vacia, sku_indivisible_c))
                            conexion.commit()
                        #Pone la P al propveddor que la tiene en el cargue
                        print('funcion3 ', orden_proveedor, sku_indivisible_c, proveedor_c)
                        conexion = obtener_conexion()
                        with conexion.cursor() as cursor:
                            cursor.execute("UPDATE proveedor SET orden = %s WHERE sku_indivisible = %s AND proveedor = %s", (orden_proveedor, sku_indivisible_c, proveedor_c))
                            conexion.commit()
                        #Actualiza el precio del producto en la tabla productos, con el precio que trae el cargue
                        print('funcion4 ', precio_c, sku_indivisible_c)
                        conexion = obtener_conexion()
                        with conexion.cursor() as cursor:
                            cursor.execute("UPDATE productos SET precio = %s WHERE sku_padre = %s", (precio_c, sku_indivisible_c))
                            conexion.commit()

                    else:
                        print('Solo actualiza en proveedor', sku_indivisible_c, id_proveedor, orden_proveedor)
                        conexion = obtener_conexion()
                        with conexion.cursor() as cursor:
                            cursor.execute("UPDATE proveedor SET precio = %s WHERE id = %s", (precio_c, id_proveedor))
                            conexion.commit()
                    
                elif(cantidad_registros > 1):
                    print('solo deja 1 elimina',cantidad_registros, sku_indivisible_c, id_proveedor)
                    
                    conexion = obtener_conexion()
                    with conexion.cursor() as cursor:
                        cursor.execute("SELECT id, sku_indivisible FROM proveedor WHERE sku_indivisible = %s AND proveedor = %s",(sku_indivisible_c, proveedor_c))
                        proveedores_repetidos = cursor.fetchall()
                        
                    print(cantidad_registros)
                    cantidad = cantidad_registros
                    
                    for u in proveedores_repetidos:
                        id_eliminar = u[0]

                        print(id_eliminar)
                        conexion = obtener_conexion()
                        with conexion.cursor() as cursor:
                            cursor.execute("DELETE FROM proveedor WHERE id = %s", (id_eliminar))
                            conexion.commit()

                    print(sku_indivisible_c,proveedor_c, precio_c, 'este inserta')
                    conexion = obtener_conexion()
                    with conexion.cursor() as cursor:
                        cursor.execute("INSERT INTO proveedor (sku_indivisible, proveedor, precio, orden) VALUES (%s, %s, %s, %s)", (sku_indivisible_c, proveedor_c, precio_c, orden_c))
                        conexion.commit()
         
        
        ponerP()    
        fechaVencimiento()

        
        data_ingreso_antes = datsaIngresoAntes()

        with conexion.cursor() as cursor:
            cursor.execute("SELECT SUM(qty_ingreso) FROM cargue_ingresos")
            qty_ingreso = cursor.fetchone()

            qty_cargue_ingreso = int(qty_ingreso[0])

            qty_inventario_total = cantidadInventario()

            qty_final = qty_cargue_ingreso + qty_inventario_total

            print(qty_cargue_ingreso, qty_inventario_total, qty_final)
        
        fecha_hora_actual = datetime.now()

        try:
            with conexion.cursor() as cursor:
                cursor.execute("INSERT INTO qty_ingreso_antes (qty_carga, qty_inventario, qty_final, fecha) VALUES (%s, %s, %s, %s)", (qty_cargue_ingreso, qty_inventario_total, qty_final, fecha_hora_actual))
                conexion.commit()

        except pymysql.err.IntegrityError as e:
            if e.args[0] == 1062:
                print("Error de integridad: Entrada duplicada")
                flash("Error de integridad: Entrada duplicada",'error')
                return render_template('ingresos.html', data_ingreso_antes = data_ingreso_antes)
                # Manejar la excepción según tus necesidades
            else:
                # Otras excepciones de IntegrityError
                flash("Error de integridad:", e)
                print("Error de integridad:", e,'error')
                return render_template('ingresos.html', data_ingreso_antes = data_ingreso_antes)
        except Exception as e:
            flash("Otro tipo de excepción:", e)
            print("Otro tipo de excepción:", e)
            return render_template('ingresos.html', data_ingreso_antes = data_ingreso_antes)
        finally:
            conexion.close()

        data_calculada = dataCalculada()

        flash("ACTUALIZACIÓN DE PROVEEDORES CORRECTA",'success')
        return render_template('ingresos.html', data_ingreso_antes = data_ingreso_antes, data_calculada = data_calculada)

def datsaIngresoAntes():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM qty_ingreso_antes")
            data_ingreso_antes = cursor.fetchall()
    
    return data_ingreso_antes

def cantidadInventario():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT SUM(cantidad) FROM inventario")
        qty_inventario = cursor.fetchone()

        qty = int(qty_inventario[0])

        return  qty


def fechaVencimiento():

    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT c.sku_indivisible, c.fecha_vencimiento, p.fecha_caducidad FROM `cargue_ingresos` c INNER JOIN productos p ON(c.sku_indivisible = p.sku_padre)')
        fechas_caducidad = cursor.fetchall()
        
        for i in fechas_caducidad:
            
            sku_indivisible, fecha_cargue_str, fecha_producto_str = i[0], str(i[1]), str(i[2])

            # Manejo del valor 'None'
            if fecha_cargue_str and fecha_producto_str and fecha_cargue_str != '0000-00-00' and fecha_producto_str != '0000-00-00':
                try:
                    fecha_cargue = datetime.strptime(fecha_cargue_str, "%Y-%m-%d").date()
                    fecha_producto = datetime.strptime(fecha_producto_str, "%Y-%m-%d").date()
                    print(fecha_cargue, fecha_producto)
                    if fecha_cargue > fecha_producto:
                        print(fecha_cargue, sku_indivisible, 'estos')
                                                
                        conexion = obtener_conexion()
                        with conexion.cursor() as cursor:
                            cursor.execute("UPDATE productos SET fecha_caducidad = %s WHERE sku_padre = %s", (fecha_cargue,sku_indivisible))
                            conexion.commit()

                        
                    elif fecha_cargue < fecha_producto:
                        print('nada')
                    else:
                        print('nada iguales')

                except ValueError:
                    print(f'Error al convertir fechas para SKU {sku_indivisible}')
            else:
                print('Nada para SKU', sku_indivisible)

    return 'ok'


   
@gestion_ingresos.route('/gestion_ingresos')
def gestionIngresos():

    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT hi.id, hi.sku_indivisible, hi.qty_ingreso, hi.fecha, hi.precio,hi.proveedor ,hi.fecha_factura, hi.fecha_recibido, hi.fecha_vencimiento, hi.observaciones, p.descripcion, p.fecha_caducidad FROM historial_ingresos hi INNER JOIN productos p ON(hi.sku_indivisible = p.sku_padre) ORDER BY hi.fecha_recibido DESC")
        ingresos_bd = cursor.fetchall()

    return render_template('gestion_ingresos.html', ingresos = ingresos_bd)


def guardaHistorial():

    db = 'inventario'
    table = 'historial_ingresos'
    path = "C:/python/cargas_ingresos.xlsm"
    url = "mysql+mysqlconnector://root:@localhost/"
    engine = create_engine(url + db)
    df = pd.read_excel(path)
    df.to_sql(name = table, con = engine, if_exists='append', index= False)

    return 'guarda historial'


def dataCalculada():

    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT ci.sku_indivisible, p.descripcion, ci.qty_ingreso, i.cantidad, i.cantidad + ci.qty_ingreso AS total FROM cargue_ingresos ci INNER JOIN inventario i ON(ci.sku_indivisible = i.sku_indivisible)INNER JOIN productos p ON(ci.sku_indivisible =  p.sku_padre)')
        data_calculada = cursor.fetchall()

    return data_calculada


@gestion_ingresos.route('/proveedor_p')
def proveedorP():

    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT id, sku_indivisible, proveedor, orden FROM cargue_ingresos')
        cargue_ingresos_p = cursor.fetchall()

        #print(cargue_ingresos_p)
        
    for x in cargue_ingresos_p:
        sku_indivisible = x[1]
        proveedor = x[2]
        orden = x[3]
        orden_bd = 'P'
        if(orden == 'P'):
            print('entra')
            with conexion.cursor() as cursor:
                cursor.execute('SELECT * FROM proveedor WHERE sku_indivisible = %s and orden = %s and proveedor = %s', (sku_indivisible, orden_bd, proveedor))
                validaproveedorp = cursor.fetchall()

            print(validaproveedorp)

    return 'hola P'



  
    

