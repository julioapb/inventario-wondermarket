from flask import Flask, render_template, url_for, request, make_response, redirect, Response, Blueprint
from . import reportes
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

today = str(date.today())

@reportes.route('/report')
def report():
    
    return render_template('reportes.html')

#DESCARGAR REPORTE 1 Inventario
@reportes.route('/download_report')
def download_report():
    
    conexion=obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT i.id as id, i.sku_indivisible as sku_indivisible, p.nombre as nombre,i.cantidad as cantidad, i.inventario_en_proceso as inv_proceso, i.inventario_en_proceso + i.cantidad  as total, i.estado as estado FROM inventario i inner JOIN productos p ON(i.sku_indivisible = p.sku_indivisible)where p.sku_indivisible = p.sku_padre")
        result_set = cursor.fetchall()

        output = io.BytesIO()
        workbook = xlwt.Workbook()
        sh = workbook.add_sheet('Report')

        sh.write(0, 0, 'id')
        sh.write(0, 1, 'sku_indivisible')
        sh.write(0, 2, 'nombre')
        sh.write(0, 3, 'cantidad')
        sh.write(0, 4, 'inv_proceso')
        sh.write(0, 5, 'total')
        sh.write(0, 6, 'estado')
        
        idx = 0
        for row in result_set:
            sh.write(idx+1, 0, int(row[0]))
            sh.write(idx+1, 1, str(row[1]))
            sh.write(idx+1, 2, str(row[2]))
            sh.write(idx+1, 3, int(row[3]))
            sh.write(idx+1, 4, int(row[4]))
            sh.write(idx+1, 5, int(row[5]))
            sh.write(idx+1, 6, int(row[6]))
           
            idx += 1
        
        workbook.save(output)
        output.seek(0)

        return Response(output, mimetype="aplication/ms-excel", headers={"Content-Disposition":"attachment;filename=rep_inventario_" + today +".xls"})
#FIN  REPORTE

#REPORTE PRODUCTOS
@reportes.route('/download_report_2')
def download_report_2():
    conexion=obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("select id_producto, sku_indivisible, sku_padre as sku, ean, nombre, cantidad as relacion, fecha_caducidad, descripcion, precio, tipo_producto, localizacion, promocion, sku_transitorio, valoracion, peso, cant_trans, impuesto FROM productos")
        result_set = cursor.fetchall()

        output = io.BytesIO()
        workbook = xlwt.Workbook()
        sh = workbook.add_sheet('Report')

        sh.write(0, 0, 'id_producto')
        sh.write(0, 1, 'sku_indivisible')
        sh.write(0, 2, 'sku')
        sh.write(0, 3, 'ean')
        sh.write(0, 4, 'nombre')
        sh.write(0, 5, 'relacion')
        sh.write(0, 6, 'fecha_caducidad')
        sh.write(0, 7, 'descripcion')
        sh.write(0, 8, 'precio')
        sh.write(0, 9, 'tipo_producto')
        sh.write(0, 10,'localizacion')
        sh.write(0, 11,'promocion')
        sh.write(0, 12,'sku_transitorio')
        sh.write(0, 13,'valoracion')
        sh.write(0, 14,'peso')
        sh.write(0, 15,'cant_trans')
        sh.write(0, 16,'impuesto')

        idx = 0
        for row in result_set:
            sh.write(idx+1, 0, int(row[0]))
            sh.write(idx+1, 1, str(row[1]))
            sh.write(idx+1, 2, str(row[2]))
            sh.write(idx+1, 3, str(row[3]))
            sh.write(idx+1, 4, str(row[4]))
            sh.write(idx+1, 5, int(row[5]))
            sh.write(idx+1, 6, str(row[6]))
            sh.write(idx+1, 7, str(row[7]))
            sh.write(idx+1, 8, float(row[8]))
            sh.write(idx+1, 9, str(row[9]))
            sh.write(idx+1, 10, str(row[10]))
            sh.write(idx+1, 11, str(row[11]))
            sh.write(idx+1, 12, str(row[12]))
            sh.write(idx+1, 13, str(row[13]))
            sh.write(idx+1, 14, str(row[14]))
            sh.write(idx+1, 15, str(row[15]))
            sh.write(idx+1, 16, str(row[16]))
           
            idx += 1
        
        workbook.save(output)
        output.seek(0)

        return Response(output, mimetype="aplication/ms-excel", headers={"Content-Disposition":"attachment;filename=rep_productos_"+ today +".xls"})
#FIN REPORTE PRODUCTOS

#REPORTE PEDIDOS
@reportes.route('/download_report_3')
def download_report_3():
    conexion=obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT order_id, sku, cant_v, fecha, estado as cancelaciones FROM historial_cargues_ventas")
        result_set = cursor.fetchall()

        output = io.BytesIO()
        workbook = xlwt.Workbook()
        sh = workbook.add_sheet('Report')

        sh.write(0, 0, 'order_id')
        sh.write(0, 1, 'sku')
        sh.write(0, 2, 'cant_v')
        sh.write(0, 3, 'fecha')
        sh.write(0, 4, 'cancelaciones')
        
        idx = 0
        for row in result_set:
            sh.write(idx+1, 0, str(row[0]))
            sh.write(idx+1, 1, str(row[1]))
            sh.write(idx+1, 2, int(row[2]))
            sh.write(idx+1, 3, str(row[3]))
            sh.write(idx+1, 4, int(row[4]))
           
            idx += 1
        
        workbook.save(output)
        output.seek(0)

        return Response(output, mimetype="aplication/ms-excel", headers={"Content-Disposition":"attachment;filename=rep_pedidos_"+ today +".xls"})
#FIN REPORTE PEDIDOS

#REPORTE FOTO DIARIA
@reportes.route('/download_report_4')
def download_report_4():
    conexion=obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT cf.id as id, cf.sku_indivisible as sku_indivisible, cf.descripcion as nombre, cf.cantidad AS Relacion,SUM(cf.total_venta) AS Total_Vendido, i.cantidad AS cantidad_inventario, cf.fecha as fecha, cf.estado_2 as estado,  (SELECT GROUP_CONCAT( concat(proveedor, ' -> ', precio) SEPARATOR ' , ') FROM proveedor where proveedor.sku_indivisible = i.sku_indivisible) as proveedor FROM calculo_foto cf INNER JOIN inventario i ON (cf.sku_indivisible = i.sku_indivisible) GROUP BY cf.sku_indivisible ORDER BY proveedor desc, cf.estado_2 asc;")
        result_set = cursor.fetchall()

        output = io.BytesIO()
        workbook = xlwt.Workbook()
        sh = workbook.add_sheet('Report')

        sh.write(0, 0, 'id')
        sh.write(0, 1, 'sku_indivisible')
        sh.write(0, 2, 'nombre')
        sh.write(0, 3, 'Relacion')
        sh.write(0, 4, 'Total_Vendido')
        sh.write(0, 5, 'cantidad_inventario')
        sh.write(0, 6, 'fecha')
        sh.write(0, 7, 'estado')
        sh.write(0, 8, 'proveedor')
        
        idx = 0
        for row in result_set:
            sh.write(idx+1, 0, int(row[0]))
            sh.write(idx+1, 1, str(row[1]))
            sh.write(idx+1, 2, str(row[2]))
            sh.write(idx+1, 3, int(row[3]))
            sh.write(idx+1, 4, int(row[4]))
            sh.write(idx+1, 5, int(row[5]))
            sh.write(idx+1, 6, str(row[6]))
            sh.write(idx+1, 7, str(row[7]))
            sh.write(idx+1, 8, str(row[8]))
           
            idx += 1
        
        workbook.save(output)
        output.seek(0)

        return Response(output, mimetype="aplication/ms-excel", headers={"Content-Disposition":"attachment;filename=rep_foto_diaria_"+ today +".xls"})
#FIN REPORTE FOTO DIARIA

#REPORTE SKU X PROVEEDOR
@reportes.route('/download_report_5')
def download_report_5():
    conexion=obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT h.sku_indivisible as SKU,(SELECT GROUP_CONCAT( concat(proveedor,' ',precio,' ', orden, ' ') ORDER BY orden desc SEPARATOR ',') as Proveedor FROM proveedor where proveedor.sku_indivisible = h.sku) as proveedor FROM inventario h INNER JOIN proveedor p ON (h.sku_indivisible = p.sku_indivisible)")
        result_set = cursor.fetchall()

        output = io.BytesIO()
        workbook = xlwt.Workbook()
        sh = workbook.add_sheet('Report')

        sh.write(0, 0, 'SKU')
        sh.write(0, 1, 'Proveedor')
        


        idx = 0
        for row in result_set:
            sh.write(idx+1, 0, str(row[0]))
            sh.write(idx+1, 1, str(row[1]))
           
            idx += 1
        
        workbook.save(output)
        output.seek(0)

        return Response(output, mimetype="aplication/ms-excel", headers={"Content-Disposition":"attachment;filename=rep_proveedor_"+ today +".xls"})
#FIN REPORTE SKU X PROVEEDOR

#REPORTE COMBOS
@reportes.route('/download_report_6')
def download_report_6():
    conexion=obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT sku_combo, nombre_combo, sku_indivisible FROM combos")
        result_set = cursor.fetchall()

        output = io.BytesIO()
        workbook = xlwt.Workbook()
        sh = workbook.add_sheet('Report')

        sh.write(0, 0, 'sku_combo')
        sh.write(0, 1, 'nombre_combo')
        sh.write(0, 2, 'sku_indivisible')
        
  
        idx = 0
        for row in result_set:
            sh.write(idx+1, 0, str(row[0]))
            sh.write(idx+1, 1, str(row[1]))
            sh.write(idx+1, 2, str(row[2]))
           
            idx += 1
        
        workbook.save(output)
        output.seek(0)

        return Response(output, mimetype="aplication/ms-excel", headers={"Content-Disposition":"attachment;filename=rep_combos_"+ today +".xls"})
#FIN REPORTE COMBOS

#REPORTE DIARIO CALCULADO
@reportes.route('/download_report_7', methods=['POST'])
def download_repo():

    conexion=obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE calculo")
        conexion.commit()

    #hola
    fecha_1 = request.form['fecha_1'] + ' 00:00:00'
    fecha_2 = request.form['fecha_2'] + ' 00:00:00'
    print(fecha_1)
    print(fecha_2)
    conexion=obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT h.sku AS 'sku historial',p.sku_indivisible, p.sku_padre, h.order_id, h.cant_v, h.fecha, h.estado_2, p.cantidad, h.tipo_producto, p.descripcion, (SELECT  GROUP_CONCAT( concat(orden,proveedor, precio) SEPARATOR ',') FROM proveedor where proveedor.sku_indivisible = p.sku_indivisible ORDER BY orden desc) as proveedor FROM `historial_cargues_ventas` h INNER JOIN productos p ON(h.sku = p.sku_padre) WHERE h.fecha BETWEEN %s AND %s ORDER BY h.fecha;", (fecha_1, fecha_2))
        result_set = cursor.fetchall()
        
        for j in result_set:
            #print(j[1])
            sku_indivisible = j[1]
            sku_padre = j[2]
            
            sku_historial = j[0]
           
            
            order_id = j[3]
            cantidad_vendida = int(j[4])
            fecha = j[5]
            estado_2 = j[6]
            cantidad = int(j[7])
            tipo_producto = j[8]
            nombre_corto = j[9]

            proveedor = j[10]

            #print(sku_historial, sku_indivisible, sku_padre, order_id, cantidad_vendida, fecha, estado_2, cantidad, tipo_producto)
            #print(sku_indivisible)
            #tipo producto COMBO
            if (tipo_producto == 'COMBO'):
               with conexion.cursor() as cursor:
                     cursor.execute("SELECT sku_indivisible  FROM combos WHERE sku_combo = %s", (sku_indivisible))
                     result_set_5 = cursor.fetchall()
                     
                     for i in result_set_5:
                        sku_com = i[0]

                        with conexion.cursor() as cursor:
                            cursor.execute("SELECT p.sku_indivisible, p.sku_padre, p.cantidad, i.sku_indivisible, i.cantidad, p.descripcion  FROM productos p INNER JOIN inventario i ON(p.sku_padre = i.sku_indivisible) WHERE p.sku_padre = %s", (sku_com))
                            result_set_7 = cursor.fetchall()

                            sku_indivisible_combo = result_set_7[0][0]
                            sku_padre_combo = result_set_7[0][1]
                            cantidad_combo = result_set_7[0][2]
                            sku_indivisible_inv = result_set_7[0][3]
                            cantidad_inv_combo = result_set_7[0][4]
                            nombre_corto_combo = result_set_7[0][5]

                        
                        print(sku_indivisible, '1')
                        with conexion.cursor() as cursor:
                            cursor.execute("INSERT INTO calculo (sku_historial, sku_indivisible,nombre_corto ,sku_padre, order_id, cantidad_vendida, cantidad,cantidad_inventario, fecha,estado_2, tipo_producto, proveedor ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s, %s,%s, %s)",(sku_indivisible_combo,sku_indivisible_inv, nombre_corto_combo, sku_padre_combo, order_id, cantidad_vendida, cantidad_combo,cantidad_inv_combo, fecha,estado_2, tipo_producto, proveedor ))
                            conexion.commit()

            #tipo producto NORMAL
            else:
                
                conexion=obtener_conexion()
                with conexion.cursor() as cursor:
                     cursor.execute("SELECT cantidad  FROM inventario WHERE sku_indivisible = %s", (sku_indivisible))
                     result_set_6 = cursor.fetchone()
                    
                     print(sku_indivisible, '2')
                     with conexion.cursor() as cursor:
                        cursor.execute("INSERT INTO calculo (sku_historial, sku_indivisible, nombre_corto,sku_padre, order_id, cantidad_vendida, cantidad,cantidad_inventario, fecha,estado_2, tipo_producto, proveedor ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s, %s,%s, %s)",(sku_historial, sku_indivisible,nombre_corto, sku_padre, order_id, cantidad_vendida, cantidad,result_set_6[0], fecha,estado_2, tipo_producto, proveedor ))
                        conexion.commit()

                     

        conexion=obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT sku_indivisible from calculo")
            result_set_12 = cursor.fetchall()

        conexion=obtener_conexion()
        with conexion.cursor() as cursor:
            #cursor.execute("SELECT id, sku_historial, sku_indivisible,nombre_corto,sku_padre, order_id,cantidad_vendida, cantidad, cantidad_inventario, fecha, estado_2, tipo_producto, proveedor, SUM(cantidad_vendida) AS cantidad_vendida FROM calculo group by sku_indivisible ORDER BY fecha")
            #cursor.execute("SELECT  sku_indivisible,nombre_corto, cantidad_inventario, SUM(cantidad_vendida * cantidad) AS cantidad_vendida,proveedor, nombre_2 FROM calculo group by sku_indivisible ORDER BY fecha")
            cursor.execute("SELECT c.sku_indivisible , p.descripcion, c.cantidad_inventario, SUM(c.cantidad_vendida * c.cantidad) AS cantidad_vendida, c.proveedor FROM calculo c INNER JOIN productos p ON(c.sku_indivisible = p.sku_padre) group by c.sku_indivisible ORDER BY c.fecha")
            result_set_12 = cursor.fetchall()
     
        output = io.BytesIO()
        workbook = xlwt.Workbook()
        sh = workbook.add_sheet('Report')

        #sh.write(0, 0, 'id')
        #sh.write(0, 1, 'sku_historial')
        sh.write(0, 0, 'sku_indivisible')
        sh.write(0, 1, 'nombre_corto')
        #sh.write(0, 4, 'sku_padre')
        #sh.write(0, 5, 'order_id')
        #sh.write(0, 2, 'cantidad_vendida')
        #sh.write(0, 7, 'cantidad')
        sh.write(0, 2, 'cantidad_inventario')
        #sh.write(0, 9, 'fecha')
        #sh.write(0, 10, 'estado_2')
        #sh.write(0, 11, 'tipo_producto')
        sh.write(0, 3, 'cantidad_vendida')
        sh.write(0, 4, 'proveedor')
              
        idx = 0
        for row in result_set_12:
            sh.write(idx+1, 0, str(row[0]))
            sh.write(idx+1, 1, str(row[1]))
            sh.write(idx+1, 2, int(row[2]))
            sh.write(idx+1, 3, int(row[3]))
            sh.write(idx+1, 4, str(row[4]))
                 
            idx += 1
        
        workbook.save(output)
        output.seek(0)

        return Response(output, mimetype="aplication/ms-excel", headers={"Content-Disposition":"attachment;filename=rep_consolidado_"+ today +".xls"})     
#FIN REPORTE DIARIO CALCULADO

# REPORTE DIARIO SIN CALCULAR
@reportes.route('/download_report_8')
def download_report_8():
    conexion=obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT sku_historial, sku_indivisible, nombre_corto, order_id, cantidad_vendida, cantidad, cantidad_inventario, fecha, estado_2, tipo_producto, proveedor  FROM calculo")
        result_set = cursor.fetchall()

        output = io.BytesIO()
        workbook = xlwt.Workbook()
        sh = workbook.add_sheet('Report')

        sh.write(0, 0, 'sku_historial')
        sh.write(0, 1, 'sku_indivisible')
        sh.write(0, 2, 'nombre_corto')
        sh.write(0, 3, 'order_id')
        sh.write(0, 4, 'cantidad_vendida')
        sh.write(0, 5, 'cantidad')
        sh.write(0, 6, 'cantidad_inventario')
        sh.write(0, 7, 'fecha')
        sh.write(0, 8, 'estado_2')
        sh.write(0, 9, 'tipo_producto')
        sh.write(0, 10, 'proveedor')
        
  
        idx = 0
        for row in result_set:
            sh.write(idx+1, 0, str(row[0]))
            sh.write(idx+1, 1, str(row[1]))
            sh.write(idx+1, 2, str(row[2]))
            sh.write(idx+1, 3, str(row[3]))
            sh.write(idx+1, 4, int(row[4]))
            sh.write(idx+1, 5, int(row[5]))
            sh.write(idx+1, 6, int(row[6]))
            sh.write(idx+1, 7, str(row[7]))
            sh.write(idx+1, 8, str(row[8]))
            sh.write(idx+1, 9, str(row[9]))
            sh.write(idx+1, 10, str(row[10]))
           
            idx += 1
        
        workbook.save(output)
        output.seek(0)

        return Response(output, mimetype="aplication/ms-excel", headers={"Content-Disposition":"attachment;filename=rep_diario_sin_calcular_"+ today +".xls"})
#FIN REPORTE DIARIO SIN CALCULAR
                     
@reportes.route('/grafica2', methods=['POST','GET'])
def grafic2():

   
    return render_template('grafico_2.html')        

@reportes.route('/grafica', methods=['POST','GET'])
def grafic():
    
    sku = request.form['sku_indivisible']
    #sku = 'KOH-KAE_115GE_X1'
    fecha_1 = request.form['fecha_1']
    fecha_2 = request.form['fecha_2']

    conexion=obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT  SUM(cant_v) AS Ventas FROM desglose_historial_ventas WHERE sku_indivisible = %s AND fecha BETWEEN %s AND %s",(sku, fecha_1, fecha_2))
        result_set_ventas = cursor.fetchone()

    print(result_set_ventas)

    conexion=obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT  SUM(qty_ingreso) AS Ingresos FROM historial_ingresos WHERE sku_indivisible = %s AND fecha BETWEEN %s AND %s",(sku, fecha_1, fecha_2))
        result_set_ingresos = cursor.fetchone()
            
        ingresos = result_set_ingresos[0] if result_set_ingresos[0] is not None else 0

        ventas = result_set_ventas[0] if result_set_ventas[0] is not None else 0

        print(int(ingresos))
        print(int(ventas))

        diferencia = int(ingresos) - int(ventas)

    return render_template('grafico_2.html', ingresos = int(ingresos), ventas = ventas, sku = sku, fecha_1 = fecha_1, fecha_2 = fecha_2, diferencia = diferencia)
                     


@reportes.route('/backup_bd')
def realizar_backup():

    fecha = datetime.today().strftime('%Y_%m_%d_%H_%M')

    respaldo = "C:\\Users\\Supervisor\\Desktop\\respaldo_"+str(fecha)+".sql"

    pathBase = "C:\\xampp\\mysql\\bin\\mysqldump.exe"

    try:

        os.popen(pathBase+" -u 'root' inventario > "+ respaldo)
        print("BASE OK"+respaldo)

        return "la buena"
    
    except:
        print("paila")
        exit

            