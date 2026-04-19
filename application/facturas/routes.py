from flask import Flask, render_template, url_for, request, make_response, redirect, Response, Blueprint,send_from_directory

import application
from . import facturas
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

#inventario - facturas por gestionar
@facturas.route('/invent_facturas')
def invent_facturas():
    conexion=obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT * FROM facturacion WHERE tipo_ingreso = %s',('en_progrso'))
        result_set = cursor.fetchall()
        #print(result_set)
    
    return render_template('inv_facturas.html',productos = result_set)