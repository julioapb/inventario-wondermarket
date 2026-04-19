from flask import Flask, render_template, url_for, request, make_response, redirect, Response, Blueprint, session,flash,jsonify
from . import sesion
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from . bd import obtener_conexion
from datetime import datetime

@sesion.route('/', methods=['GET'])
def index():

    return render_template('inicioSesion.html')


@sesion.route('/login', methods=['GET', 'POST'])
def login():
    conexion=obtener_conexion()
   
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']

        hashed_password = generate_password_hash(password,method='pbkdf2:sha256')
        

        with conexion.cursor() as cursor:
            cursor.execute('SELECT  password FROM usuarios WHERE usuario = %s',(usuario))
            result = cursor.fetchone()

            if result:
                hashed_password_from_database = result[0]
                             
                if check_password_hash(hashed_password_from_database, password):
                    session['usuario']  = usuario
                    
                    #log producto simple
                    usuario = session['usuario']
                    accion = 'Inicio Sesión'
                    sku_indivisible = ''
                    fecha_y_hora_actual = datetime.now()

                    cursor.execute('INSERT INTO log_usuarios (usuario,accion,sku_afectado, fecha) VALUES (%s,%s,%s,%s)',(usuario,accion,sku_indivisible,fecha_y_hora_actual))
                    conexion.commit()

                    return redirect(url_for('inicio.panel'))
                
            flash("Usuario o contraseña incorrectos")
            return redirect(url_for('sesion.index')) 

                                

@sesion.route('/logout', methods=['GET'])
def logout():

    conexion=obtener_conexion()
    
    #log producto simple
    usuario = session['usuario']
    accion = 'Cierre Sesión'
    sku_indivisible = ''
    fecha_y_hora_actual = datetime.now()
    
    with conexion.cursor() as cursor:
        cursor.execute('INSERT INTO log_usuarios (usuario,accion,sku_afectado, fecha) VALUES (%s,%s,%s,%s)',(usuario,accion,sku_indivisible,fecha_y_hora_actual))
        conexion.commit()

    # Eliminar el usuario de la sesión
    session.pop('usuario', None)
    flash("Sesión cerrada exitosamente")
    return redirect(url_for('sesion.index'))