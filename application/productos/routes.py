from flask import Flask, render_template, url_for, request, make_response, redirect, Response, Blueprint, session
from . import productos
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

#muestra productos
#se reemplaza por vista-productos
@productos.route('/product')
def product():
    
    conexion=obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT p.id_producto, p.sku_padre, p.sku_indivisible,p.cantidad, p.descripcion, i.cantidad + i.inventario_en_proceso as cantidad_total,p.precio, p.impuesto,p.fecha_caducidad,(SELECT GROUP_CONCAT( concat(proveedor, ' -> ', precio) SEPARATOR ' , ') FROM proveedor where proveedor.sku_indivisible = p.sku_padre AND) as proveedor,p.localizacion, p.promocion, p.sku_transitorio, p.valoracion, p.peso, p.cant_trans from productos p INNER JOIN inventario i ON (p.sku_indivisible = i.sku_indivisible) WHERE i.sku_indivisible = p.sku_indivisible ")
        result_set = cursor.fetchall()
    
    return render_template('product.html', productos = result_set)

#vista actual 23-02-2024
#vista productod con filtro
@productos.route('/vista-productos')
def vistaProductos():
    #sku_indivisible = request.form['sku_indivisible']
    print('hola')

    return render_template('productos.html')

@productos.route('/procesaBbusquedaProductos', methods=['POST'])
def procesaBbusquedaProductos():

    sku_indivisible_filtro = request.form['sku_indivisible_filtro']
    sku_filtro = request.form['sku_filtro']
    nombre_filtro = request.form['nombre_filtro']
    proveedor_filtro = request.form['proveedor_filtro']
    fecha_vencimiento_filtro = request.form['fecha_vencimiento_filtro']
    
    if(sku_indivisible_filtro):

        conexion=obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT p.id_producto, p.sku_padre, p.sku_indivisible,p.cantidad, p.descripcion, i.cantidad + i.inventario_en_proceso as cantidad_total,p.precio, p.impuesto,p.fecha_caducidad,(SELECT GROUP_CONCAT( concat(proveedor, ' -> ', precio) SEPARATOR ' , ') FROM proveedor where proveedor.sku_indivisible = p.sku_padre) as proveedor,p.localizacion, p.promocion, p.sku_transitorio, p.valoracion, p.peso, p.cant_trans from productos p INNER JOIN inventario i ON (p.sku_indivisible = i.sku_indivisible) WHERE i.sku_indivisible = p.sku_indivisible AND p.sku_indivisible = %s", (sku_indivisible_filtro))
            data = result_set = cursor.fetchall()

            print(data)

        return render_template('productos.html', productos = data)
    
    elif(sku_filtro):
        conexion=obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT p.id_producto, p.sku_padre, p.sku_indivisible,p.cantidad, p.descripcion, i.cantidad + i.inventario_en_proceso as cantidad_total,p.precio, p.impuesto,p.fecha_caducidad,(SELECT GROUP_CONCAT( concat(proveedor, ' -> ', precio) SEPARATOR ' , ') FROM proveedor where proveedor.sku_indivisible = p.sku_padre) as proveedor,p.localizacion, p.promocion, p.sku_transitorio, p.valoracion, p.peso, p.cant_trans from productos p INNER JOIN inventario i ON (p.sku_indivisible = i.sku_indivisible) WHERE i.sku_indivisible = p.sku_indivisible AND p.sku_padre = %s", (sku_filtro))
            data = result_set = cursor.fetchall()

            print(data)

        return render_template('productos.html', productos = data)
    
    elif(nombre_filtro):

        
        conexion=obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT p.id_producto, p.sku_padre, p.sku_indivisible,p.cantidad, p.descripcion, i.cantidad + i.inventario_en_proceso as cantidad_total,p.precio, p.impuesto,p.fecha_caducidad,(SELECT GROUP_CONCAT( concat(proveedor, ' -> ', precio) SEPARATOR ' , ') FROM proveedor where proveedor.sku_indivisible = p.sku_padre) as proveedor,p.localizacion, p.promocion, p.sku_transitorio, p.valoracion, p.peso, p.cant_trans from productos p INNER JOIN inventario i ON (p.sku_indivisible = i.sku_indivisible) WHERE i.sku_indivisible = p.sku_indivisible AND p.descripcion REGEXP %s", (nombre_filtro))
            data = result_set = cursor.fetchall()

            print(data)

        return render_template('productos.html', productos = data)
    
    elif(proveedor_filtro):
        conexion=obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT p.id_producto, p.sku_padre, p.sku_indivisible, p.cantidad, p.descripcion, i.cantidad + i.inventario_en_proceso as cantidad_total, p.precio, p.impuesto, p.fecha_caducidad, (SELECT GROUP_CONCAT( CONCAT(proveedor, ' -> ', precio) SEPARATOR ' , ') FROM proveedor WHERE proveedor.sku_indivisible = p.sku_padre) as proveedor, p.localizacion, p.promocion, p.sku_transitorio, p.valoracion, p.peso, p.cant_trans FROM productos p INNER JOIN inventario i ON p.sku_indivisible = i.sku_indivisible WHERE  (SELECT GROUP_CONCAT( CONCAT(proveedor, ' -> ', precio) SEPARATOR ' , ') FROM proveedor WHERE  proveedor.sku_indivisible = p.sku_padre ) LIKE %s", ('%'+proveedor_filtro+'%'))
            data = result_set = cursor.fetchall()

            print(data)

        return render_template('productos.html', productos = data)
    
    elif(fecha_vencimiento_filtro):
        conexion=obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT p.id_producto, p.sku_padre, p.sku_indivisible,p.cantidad, p.descripcion, i.cantidad + i.inventario_en_proceso as cantidad_total,p.precio, p.impuesto,p.fecha_caducidad,(SELECT GROUP_CONCAT( concat(proveedor, ' -> ', precio) SEPARATOR ' , ') FROM proveedor where proveedor.sku_indivisible = p.sku_padre) as proveedor,p.localizacion, p.promocion, p.sku_transitorio, p.valoracion, p.peso, p.cant_trans from productos p INNER JOIN inventario i ON (p.sku_indivisible = i.sku_indivisible) WHERE i.sku_indivisible = p.sku_indivisible AND p.fecha_caducidad = %s",(fecha_vencimiento_filtro))
            data = result_set = cursor.fetchall()

            print(data)

        return render_template('productos.html', productos = data)

   
    

#EDITAR PRODUCTO
@productos.route('/edit/<id>')
def get_product(id):

    conexion=obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT * FROM productos WHERE id_producto = %s',(id))
        data = result_set = cursor.fetchall()
        
        sku = data[0][2]

    conexion_2=obtener_conexion()
    with conexion_2.cursor() as cursor:
        cursor.execute('SELECT * FROM proveedor WHERE sku_indivisible = %s',(sku))
        data_2 = result_set = cursor.fetchall()
    
    conexion_2=obtener_conexion()
    with conexion_2.cursor() as cursor:
        cursor.execute('SELECT * FROM lista_proveedor order by nombre_proveedor desc')
        data_3 = result_set = cursor.fetchall()
        
    return render_template('edit_product.html', product = data[0], proveedor = data_2, lista = data_3)

#ACTUALIZA PRODUCTO
@productos.route('/update/<id>', methods=['POST'])
def update_product(id):

        sku_indivisible = request.form['sku_indivisible']
        sku_padre = request.form['sku_padre']
        ean = request.form['ean']
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        impuesto = request.form['impuesto']
        fecha_caducidad = request.form['fecha_caducidad']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        localizacion = request.form['localizacion']
        promocion = request.form['promocion']
        promocion = request.form['promocion']
        sku_transitorio = request.form['sku_transitorio']
        valoracion = request.form['valoracion']
        peso = request.form['peso']
        cant_trans = request.form['cant_trans']
        tipo_producto = request.form['tipo_producto']


        conexion=obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("UPDATE productos SET sku_indivisible = %s, sku_padre = %s, ean=%s, nombre=%s, cantidad=%s, impuesto=%s, fecha_caducidad=%s, descripcion=%s, precio=%s,localizacion = %s, promocion = %s, sku_transitorio = %s, valoracion = %s, peso = %s, cant_trans = %s WHERE sku_padre = %s",(sku_indivisible,sku_padre, ean, nombre, cantidad, impuesto, fecha_caducidad, descripcion, precio, localizacion, promocion,sku_transitorio, valoracion,peso, cant_trans,sku_padre))
            conexion.commit()

        #log producto simple
        usuario = session['usuario']
        accion = 'Actualiza producto'
        fecha_y_hora_actual = datetime.now()

        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO log_usuarios (usuario,accion,sku_afectado,sku_indivisible, tipo_producto, fecha) VALUES (%s,%s,%s,%s,%s,%s)',(usuario,accion,sku_indivisible,sku_padre,tipo_producto,fecha_y_hora_actual))
            conexion.commit()
                    
        return render_template('productos.html')



#eliminar producto
@productos.route('/delete/<id>')
def deleteProduct(id):

    conexion=obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT sku_indivisible, sku_padre, tipo_producto FROM productos WHERE id_producto = %s',(id))
        data = result_set = cursor.fetchall()
        
        sku_indivisible = data[0][0]
        sku = data[0][1]
        tipo_producto = data[0][2]
        
        if(tipo_producto != 'COMBO'):

            if(sku == sku_indivisible):
                
                with conexion.cursor() as cursor:
                    cursor.execute("DELETE FROM productos WHERE sku_indivisible = %s", sku_indivisible)
                    conexion.commit()

                with conexion.cursor() as cursor:
                    cursor.execute("DELETE FROM inventario WHERE sku_indivisible = %s", sku_indivisible)
                    conexion.commit()
                
                #log producto simple
                usuario = session['usuario']
                accion = 'Elimina producto'
                fecha_y_hora_actual = datetime.now()
                
                with conexion.cursor() as cursor:
                    cursor.execute('INSERT INTO log_usuarios (usuario,accion,sku_afectado,sku_indivisible, tipo_producto, fecha) VALUES (%s,%s,%s,%s,%s,%s)',(usuario,accion,sku_indivisible,sku,tipo_producto,fecha_y_hora_actual))
                    conexion.commit()
                    
                
                flash("Producto eliminado correctamente")
                return redirect(url_for('productos.vistaProductos'))
            
            else:
                with conexion.cursor() as cursor:
                    cursor.execute("DELETE FROM productos WHERE sku_padre = %s", sku)
                    conexion.commit()

                #log producto simple
                usuario = session['usuario']
                accion = 'Elimina producto'
                fecha_y_hora_actual = datetime.now()
                
                with conexion.cursor() as cursor:
                    cursor.execute('INSERT INTO log_usuarios (usuario,accion,sku_afectado,sku_indivisible, tipo_producto, fecha) VALUES (%s,%s,%s,%s,%s,%s)',(usuario,accion,sku_indivisible,sku,tipo_producto,fecha_y_hora_actual))
                    conexion.commit()

                flash("Producto eliminado correctamente")
                return redirect(url_for('productos.vistaProductos'))

        elif(tipo_producto == 'COMBO'):
            
            with conexion.cursor() as cursor:
                cursor.execute("DELETE FROM productos WHERE sku_indivisible = %s", sku_indivisible)
                conexion.commit()

            with conexion.cursor() as cursor:
                cursor.execute("DELETE FROM inventario WHERE sku_indivisible = %s", sku_indivisible)
                conexion.commit()
            
            with conexion.cursor() as cursor:
                cursor.execute("DELETE FROM combos WHERE sku_combo = %s", sku_indivisible)
                conexion.commit()
            #log producto simple
            usuario = session['usuario']
            accion = 'Elimina producto'
            fecha_y_hora_actual = datetime.now()

            with conexion.cursor() as cursor:
                    cursor.execute('INSERT INTO log_usuarios (usuario,accion,sku_afectado,sku_indivisible, tipo_producto, fecha) VALUES (%s,%s,%s,%s,%s,%s)',(usuario,accion,sku_indivisible,sku,tipo_producto,fecha_y_hora_actual))
                    conexion.commit()

            flash("Producto eliminado correctamente")
            return redirect(url_for('productos.vistaProductos'))

    #EDITAR PROVEEDOR

@productos.route('/edit_proveedor/<id>')
def edit_proveedor(id):

    conexion=obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT * FROM proveedor WHERE id = %s',(id))
        data = result_set = cursor.fetchall()
        
    return render_template('edit_proveedor.html', proveedor = data)
#FIN EDITAR PROVEEDOR
#eliminar proveedor
@productos.route('/delete_proveedor/<id>')
def get_proveedor(id):
    
    conexion_2=obtener_conexion()
    with conexion_2.cursor() as cursor:
        cursor.execute("DELETE FROM proveedor WHERE id = %s", id)
        conexion_2.commit()
    
    #log elimina proveedor
    usuario = session['usuario']
    accion = 'Elimina proveedor'
    tipo_producto = 'N/A'
    sku_indivisible = id
    fecha_y_hora_actual = datetime.now()

    with conexion_2.cursor() as cursor:
        cursor.execute('INSERT INTO log_usuarios (usuario,accion,sku_afectado,sku_indivisible, tipo_producto, fecha) VALUES (%s,%s,%s,%s,%s,%s)',(usuario,accion,sku_indivisible,sku_indivisible,tipo_producto,fecha_y_hora_actual))
        conexion_2.commit()
    
    flash("PROVEEDOR ELIMINADO CORRECTAMENTE")
    #return render_template('edit/<id>')
    return redirect(request.referrer)

#ACTUALIZA PROVEEDOR
@productos.route('/update_proveedor/<id>', methods=['POST'])
def update_proveedor(id):

        id = request.form['id']
        precio = request.form['precio']
        orden = request.form['orden']
        
        conexion=obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("UPDATE proveedor SET precio = %s , orden= %s WHERE id = %s",(precio,orden,id))
            conexion.commit()
        
        #log producto simple
        usuario = session['usuario']
        accion = 'Edita proveedor'
        sku_indivisible = id
        fecha_y_hora_actual = datetime.now()
        tipo_producto = 'UNITARIO'

        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO log_usuarios (usuario,accion,sku_afectado,sku_indivisible, tipo_producto, fecha) VALUES (%s,%s,%s,%s,%s,%s)',(usuario,accion,sku_indivisible,sku_indivisible,tipo_producto,fecha_y_hora_actual))
            conexion.commit()
    
        #return render_template('inv_general.html')
        flash("Proveedor editado correctamente")
        return redirect(request.referrer)

@productos.route('/ajax-proveedor', methods=['POST','GET'])
def ajax_proveedor():
    
    sku_indivisible_2=request.form['sku_indivisible_2']
    proveedor=request.form['proveedor']
    precio=request.form['precio']
    
    conexion=obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('INSERT INTO proveedor (sku_indivisible, proveedor,precio) VALUES (%s,%s,%s)',(sku_indivisible_2,proveedor,precio))
        conexion.commit()
    
    #log producto simple
    usuario = session['usuario']
    accion = 'Crea proveedor'
    fecha_y_hora_actual = datetime.now()
    tipo_producto = 'UNITARIO'

    with conexion.cursor() as cursor:
        cursor.execute('INSERT INTO log_usuarios (usuario,accion,sku_afectado,sku_indivisible, tipo_producto, fecha) VALUES (%s,%s,%s,%s,%s,%s)',(usuario,accion,sku_indivisible_2,sku_indivisible_2,tipo_producto,fecha_y_hora_actual))
        conexion.commit()

    response = { 'status': 200, 'proveedor': proveedor, 'id': 1}

    return json.dumps(response)

@productos.route('/precios')
def calculaPrecios():
    
    conexion=obtener_conexion()
    #se desactiva por indicación de Edu 
    #with conexion.cursor() as cursor:
        #cursor.execute('SELECT COUNT(DISTINCT order_id) AS total_order_id FROM historial_cargues_ventas WHERE MONTH(fecha) = MONTH(DATE_SUB(NOW(), INTERVAL 1 MONTH)) AND YEAR(fecha) = YEAR(DATE_SUB(NOW(), INTERVAL 1 MONTH))')
        #no_pedidos_mes_anterior = cursor.fetchone()

    #pedidos_mes_anterior = (no_pedidos_mes_anterior[0])
    
    pedidos_mes_anterior = 1725
    
    with conexion.cursor() as cursor:
        cursor.execute('SELECT sku_indivisible, sku_padre, tipo_producto, precio, cantidad, impuesto FROM productos')
        productos = cursor.fetchall()

        combo = 0
        normales = 0
        packs = 0
        total_iva = 0

        #constantes
        embalaje = round(0.5 + (450/(50*23)),2)
        personal = round(1000 / int(pedidos_mes_anterior),2)
        otros_costes = round(1000 /int(pedidos_mes_anterior),2)

        for x in productos:

            sku = x[0]
            sku_indivisible = x[1]
            tipo_producto = x[2]
            coste = x[3]
            relacion = x[4]
            impuesto = x[5]
            iva_combo = []
            coste_combo = []
            iva = 0
            #print(sku_indivisible)
            #combos
            if(tipo_producto == 'COMBO'):
                
                with conexion.cursor() as cursor:
                    cursor.execute('SELECT c.sku_combo, p.sku_indivisible, p.sku_padre,p.cantidad ,p.impuesto, p.precio FROM combos c INNER JOIN productos p ON(c.sku_indivisible = p.sku_padre) WHERE sku_combo = %s',(sku_indivisible))
                    combos = cursor.fetchall()

                    for j in combos:

                        coste_c = j[5]
                        impuesto = int(j[4])

                        iva = float(round(impuesto / 100 * float(coste_c),2))
                        iva_combo.append(iva)
                        coste_combo.append(coste_c)
                    
                    total_iva_combo = float(round(sum(iva_combo),2))
                    coste_total_combo = float(round(sum(coste_combo),2))

                    precio_bruto = round(total_iva_combo,2) + round(coste_total_combo,2)

                    pva = round(coste_total_combo,2) + round(total_iva_combo,2) + round(embalaje,2) + round(personal,2) + round(otros_costes,2)

                    if(pva < 5 ):

                        pva_final = pva
                    
                    elif(pva >= 5 and pva <= 15 ):

                        pva_final = pva + 1.5
                    
                    elif(pva > 15 and pva <= 25):

                        pva_final = pva + 4

                    elif(pva > 25 ):
                        pva_final = pva + 15

                    
                    pva_neto = round(pva_final / (1+(impuesto/100)),2)
                    iva_venta = round(float(pva_final) - float(pva_neto),2)
                                
                    with conexion.cursor() as cursor:
                        cursor.execute('INSERT INTO precios (sku,sku_indivisible,tipo_producto, coste, iva, impuesto,precio_bruto,embalaje,personal,otros_costes,pedidos_mes_anterior,pva, pva_neto, iva_venta) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(sku,sku_indivisible,tipo_producto,coste_total_combo, total_iva_combo,impuesto,precio_bruto,embalaje,personal,otros_costes,pedidos_mes_anterior ,pva_final,pva_neto, iva_venta))
                        conexion.commit()   

            elif(tipo_producto == 'UNITARIO'):
                
                iva = float(round(impuesto / 100 * float(coste),2))
                precio_bruto = float(coste) + float(iva)
                pva = round(float(coste) + float(iva) + float(embalaje) + float(personal) + float(otros_costes),2)

                if(pva < 5 ):

                    pva_final = pva
                    
                elif(pva >= 5 and pva <= 15 ):

                    pva_final = pva + 1.5
                
                elif(pva > 15 and pva <= 25):

                    pva_final = pva + 4

                elif(pva > 25 ):

                    pva_final = pva + 15

                pva_neto = round(pva_final / (1+(impuesto/100)),2)
                iva_venta = round(float(pva_final) - float(pva_neto),2)
                #print(precio,impuesto, iva, pva)
                #print(sku_padre)
                #print(round(coste,2), round(iva,2), round(embalaje,2),round(personal,2), round(otros_costes,2) )

                with conexion.cursor() as cursor:
                    cursor.execute('INSERT INTO precios (sku,sku_indivisible,tipo_producto, coste, iva, impuesto,precio_bruto,embalaje,personal,otros_costes,pedidos_mes_anterior,pva, pva_neto, iva_venta) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(sku,sku_indivisible,tipo_producto,coste, iva,impuesto ,precio_bruto,embalaje,personal,otros_costes,pedidos_mes_anterior,pva_final, pva_neto, iva_venta))
                    conexion.commit()

            elif(tipo_producto == 'PACK'):
                
                precio_total = float(coste) * int(relacion)

                iva = float(round(impuesto / 100 * float(coste),2))
                precio_bruto = float(coste) + float(iva)
                #print(precio,impuesto, iva, pva)
                pva = round(float(coste) + float(iva) + float(embalaje) + float(personal) + float(otros_costes),2)

                if(pva < 5 ):

                    pva_final = pva
                    
                elif(pva >= 5 and pva <= 15 ):

                    pva_final = pva + 1.5
                
                elif(pva > 15 and pva <= 25):

                    pva_final = pva + 4

                elif(pva > 25 ):
                    
                    pva_final = pva + 15


                pva_neto = round(pva_final / (1+(impuesto/100)),2)
                iva_venta = round(float(pva_final) - float(pva_neto),2)
                print(pva_final - pva_neto)
                #print(sku_padre)
                #print(round(coste,2), round(iva,2), round(embalaje,2),round(personal,2), round(otros_costes,2) )
                
                with conexion.cursor() as cursor:
                    cursor.execute('INSERT INTO precios (sku,sku_indivisible,tipo_producto, coste, iva, impuesto,precio_bruto,embalaje,personal,otros_costes,pedidos_mes_anterior,pva, pva_neto, iva_venta) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(sku,sku_indivisible,tipo_producto,coste, iva,impuesto ,precio_bruto,embalaje,personal,otros_costes,pedidos_mes_anterior,pva_final, pva_neto, iva_venta))
                    conexion.commit()

    return 'precios'

@productos.route('/validaPrecioMinimo')
def validaPrecioMinimo():

    try:
        conexion=obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute('SELECT id, coste, pva, sku_indivisible, tipo_producto FROM precios WHERE coste != 0')
            data_precios = cursor.fetchall()
            #print(data_precios)

            for x in data_precios:
                id = x[0]
                coste = x[1]
                precio_minimo = round(x[1] * 1.5,2)
                pva = x[2]
                sku_indivisible = x[3]
                tipo_producto = x[4]

                #print(precio_minimo, pva)

                if(precio_minimo < pva):

                    print(id,coste, ' - ', precio_minimo,' - ',pva, ' - ', sku_indivisible)

                else:

                    with conexion.cursor() as cursor:
                        cursor.execute('UPDATE precios SET pva = %s WHERE id = %s',(precio_minimo, id))
                        conexion.commit()

        return 'hola'
    
    except Exception as e:

         # Manejar la excepción aquí, por ejemplo, imprimir un mensaje de error
        print("Ocurrió un error al ejecutar la consulta:", e)
        flash("Ocurrió un error al ejecutar la consulta:", e)
        return redirect(url_for('excepcion_precio.excepcion')) 
        # También puedes revertir la transacción si es necesario
        conexion.rollback()

    finally:

        conexion.close()

#sE CREO PARA REALIZAR LA ACTUALIZACION MASIVA DE EL CALCULO DE LOS PRECIOS DE LOS PACKS CON RESPECTO AL PRECIO DEL PRODUCTO UNICO
@productos.route('/calculoPack')
def calculoPack():

    conexion=obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT sku_indivisible, sku_padre, cantidad, tipo_producto FROM productos WHERE tipo_producto = 'PACK'")
        data_packs = cursor.fetchall()

        for x in data_packs:
            #print(x[0], '-' ,x[1])
            sku_indivisible = x[0]
            sku_padre = x[1]
            cantidad = x[2]
            tipo_producto = x[3]
            with conexion.cursor() as cursor:
                cursor.execute("SELECT precio FROM productos WHERE sku_padre = %s", (sku_indivisible))
                data_precio = cursor.fetchall()

            for j in data_precio:
                
                precio_pack = round(float(j[0]) * int(cantidad),2)

                print(sku_indivisible,'-' ,sku_padre, '-',str(j[0]), '-', str(cantidad), '-' , str(precio_pack), '-', tipo_producto)

                with conexion.cursor() as cursor:
                    cursor.execute("UPDATE productos SET precio = %s  WHERE sku_padre = %s",(precio_pack,sku_padre))
                    conexion.commit()

    return 'hola'