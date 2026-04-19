from flask import Flask, render_template, url_for, request, make_response, redirect, Response, Blueprint, session
import application
from . import combos
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
#Vista combos agrupados
@combos.route('/combos_2')
def combosget():
    
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, sku_combo, nombre_combo, sku_indivisible FROM combos GROUP BY id, sku_combo, nombre_combo, sku_indivisible")
        result_set = cursor.fetchall()

    return render_template('combos.html', combos = result_set)

#editar combo parte 1 

#editar combo parte 1 
@combos.route('/edit_combo/<id>')
def get_combo(id):
    conexion=obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT sku_combo, sku_indivisible FROM combos WHERE id = %s',(id))
        data = result_set = cursor.fetchall()

        sku_combo = data[0][0]

    conexion=obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT id, sku_combo, nombre_combo, sku_indivisible, cantidad FROM combos WHERE sku_combo = %s',(sku_combo))
        data = result_set = cursor.fetchall()
    return render_template('edit_combo.html', id_combo = id, combos = result_set)
#fin editar combos


#editar combo por item
@combos.route('/edit_item_combo/<id>')
def get_items(id):
    conexion=obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT id, sku_combo, nombre_combo,sku_indivisible, cantidad FROM combos WHERE id = %s',(id))
        data = result_set = cursor.fetchall()

    return render_template('edit_item_combo.html', item = data, id = id)

#ACTUALIZA COMBO ITEM PARTE 2
@combos.route('/update_item/<id>', methods=['POST'])
def update_item(id):

        id = request.form['id']
        nombre_combo = request.form['nombre_combo']
        sku_combo = request.form['sku_combo']
        sku_indivisible = request.form['sku_indivisible']
        cantidad = request.form['cantidad']
        tipo_producto = 'COMBO'

        conexion=obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("UPDATE combos SET nombre_combo = %s, sku_combo = %s, sku_indivisible = %s, cantidad = %s WHERE id = %s",(nombre_combo, sku_combo, sku_indivisible,cantidad ,id ))
            conexion.commit()
        
        #log producto simple
        usuario = session['usuario']
        accion = 'Actualiza combo'
        fecha_y_hora_actual = datetime.now()

        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO log_usuarios (usuario,accion,sku_afectado,sku_indivisible, tipo_producto, fecha) VALUES (%s,%s,%s,%s,%s,%s)',(usuario,accion,sku_combo,sku_combo,tipo_producto,fecha_y_hora_actual))
            conexion.commit()

        flash("Combo actualizado correctamente")
        return redirect(request.referrer)
        #return redirect(url_for('combos.combosget'))

#eliminar combo general
@combos.route('/delete_combo/<id>')
def d_combo(id):

    print(id) 

    conexion=obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT sku_combo FROM combos WHERE id = %s',(id))
        sku_combo = cursor.fetchone()

    conexion_2=obtener_conexion()
    with conexion_2.cursor() as cursor:
        cursor.execute("DELETE FROM combos WHERE id = %s", id)
        conexion_2.commit()
    
    #log producto simple
    usuario = session['usuario']
    accion = 'Elimina combo'
    fecha_y_hora_actual = datetime.now()
    tipo_producto = 'COMBO'

    with conexion.cursor() as cursor:
        cursor.execute('INSERT INTO log_usuarios (usuario,accion,sku_afectado,sku_indivisible, tipo_producto, fecha) VALUES (%s,%s,%s,%s,%s,%s)',(usuario,accion,sku_combo,sku_combo,tipo_producto,fecha_y_hora_actual))
        conexion.commit()
    
    flash("Combo eliminado correctamente")
    return redirect(request.referrer)
#fin eliminar combo general

#eliminar combo item 
@combos.route('/delete_item_combo/<id>')
def d_i_combo(id):
    print(id)
    conexion_2=obtener_conexion()
    with conexion_2.cursor() as cursor:
        cursor.execute("DELETE FROM combos WHERE id = %s", id)
        conexion_2.commit()
    
    flash("PROVEEDOR ELIMINADO CORRECTAMENTE")
    return redirect(url_for('combos.combosget'))
#fin eliminar combo intem

#Nuevo item combo
@combos.route('/new_item/<id>', methods=['POST'])
def new_item(id):
        
        
        nombre_combo = request.form['nombre_combo']
        sku_combo = request.form['sku_combo']
        sku_indivisible = request.form['sku_indivisible']
        cantidad = request.form['cantidad']
        tipo_producto = 'COMBO'

        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO combos (nombre_combo,sku_combo,sku_indivisible,cantidad) VALUES (%s,%s,%s,%s)",(nombre_combo,sku_combo,sku_indivisible,cantidad))
            conexion.commit()

        #log producto simple
        usuario = session['usuario']
        accion = 'Nuevo Item Combo'
        fecha_y_hora_actual = datetime.now()

        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO log_usuarios (usuario,accion,sku_afectado,sku_indivisible, tipo_producto, fecha) VALUES (%s,%s,%s,%s,%s,%s)',(usuario,accion,sku_combo,sku_indivisible,tipo_producto,fecha_y_hora_actual))
            conexion.commit()
    
        return redirect(url_for('combos.combosget'))
#return "PROVEEDOR ACTUALIZADO CORRECTAMENTE"

#funcion combo
@combos.route('/combo', methods=['POST','GET'])
def combo():
    
    recibe_sku_combo = request.form['sku_combo']
    sku_combo = recibe_sku_combo.strip()

    recibe_nombre_sku_combo = request.form['nombre_combo']
    nombre_sku_combo = recibe_nombre_sku_combo.strip()

    #sku_combo = request.form['sku_combo']
    #nombre_sku_combo = request.form['nombre_combo']

    sku = request.form.getlist('sku[]')
    cantidad = request.form.getlist('cantidad[]')
                
    #nombre del combo
    #nombre_sku_combo = request.form['nombre_sku_combo']

    #print(valor)
    #valida que el combo no exista
    conexion=obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT sku_combo FROM combos WHERE sku_combo = %s', sku_combo)
        result_set = cursor.fetchone()
        if(result_set):
            flash("SKU_COMBO EXISTENTE")
            return redirect(request.referrer)
        else:
            print('ok_2')    
        #TERMINA VALIDACION SKU_COMBO
        
        
        #VALIDACION SKUS_INDIVISIBLES
        contador=0
        rep = []
        for x in sku:
            #print(x)
            x_limpio = x.strip()

            cursor.execute('SELECT sku_indivisible FROM productos WHERE sku_indivisible = %s',x_limpio)
            result_set_2 = cursor.fetchone()
            if(result_set_2):
                print('ok')
            else:
                rep.append(x_limpio)
                contador = contador + 1
        #TERMINA VALIDACION SKUS_INDIVISIBLES

        #VALIDACION ANTES DE GUARDAR 
        if(len(rep)== 0):
            print('entra')
            #guardar en bd
           
            # guardar en productos y en inventario
            
            tipo_producto = 'COMBO'
            conexion=obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute('INSERT INTO productos (sku_indivisible, sku_padre, nombre,descripcion, tipo_producto) VALUES (%s,%s,%s,%s,%s)',(sku_combo,sku_combo,nombre_sku_combo,nombre_sku_combo, tipo_producto))
                conexion.commit()

    
            conexion=obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute('INSERT INTO inventario (sku_indivisible, sku) VALUES (%s,%s)',(sku_combo, sku_combo))
                conexion.commit()
            total = 0
            total_precio = 0

            for elemento1, elemento2 in zip(sku, cantidad):
                sku = elemento1 
                cantidad = elemento2

                elemento1_limpio = elemento1.strip()
                elemento2_limpio = elemento2.strip()


                conexion = obtener_conexion()
                with conexion.cursor() as cursor:
                    cursor.execute("INSERT INTO combos (nombre_combo,sku_combo,sku_indivisible, cantidad) VALUES (%s,%s,%s,%s)",(nombre_sku_combo,sku_combo,elemento1_limpio, elemento2_limpio))
                    conexion.commit()

                total += calculaComboPeso(elemento1_limpio,sku_combo)
                total_precio += calculaComboPrecio(elemento1_limpio, sku_combo)
            
            fecha_caducidad = CalculaFecha(sku_combo)
            
            
            with conexion.cursor() as cursor:
                cursor.execute("UPDATE productos SET peso = %s, precio = %s, fecha_caducidad = %s, cantidad = %s  WHERE sku_padre = %s",(total, total_precio,fecha_caducidad, 1 ,sku_combo))
                conexion.commit()

            cantidad_minima = CalculaCantidad(sku_combo)

            with conexion.cursor() as cursor:
                cursor.execute("UPDATE inventario SET cantidad = %s  WHERE sku_indivisible = %s",(cantidad_minima, sku_combo))
                conexion.commit()

            #log producto simple
            usuario = session['usuario']
            accion = 'Crear Combo'
            fecha_y_hora_actual = datetime.now()
            
            with conexion.cursor() as cursor:
                cursor.execute('INSERT INTO log_usuarios (usuario,accion,sku_afectado,sku_indivisible, tipo_producto, fecha) VALUES (%s,%s,%s,%s,%s,%s)',(usuario,accion,sku_combo,sku_combo,tipo_producto,fecha_y_hora_actual))
                conexion.commit()

            flash("PRODUCTO CREADO CORRECTAMENTE")
            return redirect(url_for('combos.combosget'))
        else:
            print(rep)
            flash("SKU no se encuentra en la BD")
            return redirect(url_for('combos.combosget'))


#### tarea programada

@combos.route('/actualizacionCombos', methods=['POST','GET'])
def actualizacionCombos():
    
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT sku_indivisible, sku_combo FROM combos GROUP BY sku_combo')
        result_set_4 = cursor.fetchall()
        
        #print(result_set_4)
        contador = 0
        for y in result_set_4:

            sku_combos = y[1]

            with conexion.cursor() as cursor:
                cursor.execute('SELECT SUM(c.cantidad * p.peso) AS peso_total FROM combos c INNER JOIN productos p ON(c.sku_indivisible = p.sku_padre) WHERE c.sku_combo = %s',(sku_combos))
                result_set_6 = cursor.fetchone()
                #print(result_set_6[0], sku_combos)

            with conexion.cursor() as cursor:
                cursor.execute('SELECT SUM(c.cantidad * p.precio) AS precio_total FROM combos c INNER JOIN productos p ON(c.sku_indivisible = p.sku_padre) WHERE c.sku_combo = %s',(sku_combos))
                result_set_7 = cursor.fetchone()
            
                #print(result_set_7[0], sku_combos)
            
            with conexion.cursor() as cursor:
                cursor.execute('SELECT MIN(p.fecha_caducidad) AS fecha_caducidad FROM combos c INNER JOIN productos p ON(c.sku_indivisible = p.sku_padre) WHERE c.sku_combo = %s',(sku_combos))
                result_set_8 = cursor.fetchone()

                #print(result_set_8[0], sku_combos)

            cantidad_ratio = 1

            with conexion.cursor() as cursor:
                cursor.execute("UPDATE productos SET peso = %s, precio = %s, cantidad = %s, fecha_caducidad = %s WHERE sku_padre = %s",(result_set_6[0], result_set_7[0], cantidad_ratio ,result_set_8[0],sku_combos))
                conexion.commit()

            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute('SELECT MIN(i.cantidad) FROM combos  c INNER JOIN inventario i ON(c.sku_indivisible = i.sku_indivisible) WHERE c.sku_combo = %s',(sku_combos))
                result_set_9 = cursor.fetchone()

            cantidad_minima = result_set_9[0]
            print(cantidad_minima, sku_combos)
            with conexion.cursor() as cursor:
                cursor.execute("UPDATE inventario SET cantidad = %s  WHERE sku_indivisible = %s",(cantidad_minima, sku_combos))
                conexion.commit()
            
        
    flash("ACTUALIZACIÓN DE COMBOS REALIZADA CON EXITO")
    return redirect(url_for('combos.combosget'))


### funcines calculos combos
def calculaComboPeso(elemento1,sku_combo):

    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT sku_indivisible, cantidad FROM combos WHERE sku_indivisible = %s and  sku_combo = %s',(elemento1,sku_combo))
        result_set_4 = cursor.fetchone()

        cantidad = result_set_4[1]

    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT peso FROM productos WHERE sku_padre = %s',(elemento1))
        result_set_4 = cursor.fetchone()

        peso = result_set_4[0]

    total = peso * cantidad

    return total

def calculaComboPrecio(elemento1,sku_combo):

    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT sku_indivisible, cantidad FROM combos WHERE sku_indivisible = %s and  sku_combo = %s',(elemento1,sku_combo))
        result_set_4 = cursor.fetchone()

        cantidad = result_set_4[1]

    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT precio FROM productos WHERE sku_padre = %s',(elemento1))
        result_set_4 = cursor.fetchone()

        precio = result_set_4[0]

    total_precio = precio * cantidad

    return total_precio

def CalculaFecha(sku_combo):

    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT MIN(p.fecha_caducidad) FROM combos  c INNER JOIN productos p ON(c.sku_indivisible = p.sku_padre) WHERE c.sku_combo = %s',(sku_combo))
        result_set_4 = cursor.fetchone()

        fecha_minima = result_set_4[0]

    return fecha_minima

def CalculaCantidad(sku_combo):

    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT MIN(i.cantidad) FROM combos  c INNER JOIN inventario i ON(c.sku_indivisible = i.sku_indivisible) WHERE c.sku_combo = %s',(sku_combo))
        result_set_4 = cursor.fetchone()

        cantidad_minima = result_set_4[0]

    return cantidad_minima