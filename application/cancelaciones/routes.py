from flask import Flask, render_template, url_for, request, make_response, redirect, Response, Blueprint
from . import cancelaciones
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

#funcion cancelacion combos
def cancelacionCombos(sku_combo, cant_v,id):
    
    print(sku_combo)
    print(cant_v)
    conexion_3=obtener_conexion()
    with conexion_3.cursor() as cursor:
        cursor.execute('SELECT cantidad FROM inventario WHERE sku_indivisible = %s',(sku_combo))
        result_set_3 = cursor.fetchone()

        total_en_inv = int(result_set_3[0])

        total = int(total_en_inv) + int(cant_v)

        conexion_4=obtener_conexion()
        with conexion_4.cursor() as cursor:
            cursor.execute("UPDATE inventario SET cantidad = %s WHERE sku_indivisible = %s",(total,sku_combo))
            conexion_4.commit()

    conexion_4=obtener_conexion()
    with conexion_4.cursor() as cursor:
        cursor.execute("UPDATE historial_cargues_ventas SET estado = 1 WHERE id = %s",(id))
        conexion_4.commit()


    return 'hoolq'

@cancelaciones.route('/cancelaciones')
def cancelaciones():

    conexion=obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT * FROM historial_cargues_ventas where estado = 0')
        result_set_10 = cursor.fetchall()

    return render_template('cancelaciones.html', cancelaciones = result_set_10)







