from turtle import home
from flask import  Flask
from .inicio import inicio
from .cargas import cargas
from .productos import productos
from .inventario import inventario
from .gestion_salidas import gestion_salidas
from .cancelaciones import cancelaciones
from .ventas import ventas
from .reportes import reportes
from .combos import combos
from .facturas import facturas
from .foto_diaria import foto_diaria
from .woo import woo
from .gestion_ingresos import gestion_ingresos
from flask_mail import Mail, Message
from .sesion import sesion
from .registro import registro
from .validaciones import validaciones


miApp = Flask(__name__)


miApp.register_blueprint(inicio)
miApp.register_blueprint(cargas)
miApp.register_blueprint(inventario)
miApp.register_blueprint(productos)
miApp.register_blueprint(gestion_salidas)
miApp.register_blueprint(cancelaciones)
miApp.register_blueprint(ventas)
miApp.register_blueprint(reportes)
miApp.register_blueprint(combos)
miApp.register_blueprint(facturas)
miApp.register_blueprint(foto_diaria)
miApp.register_blueprint(woo)
miApp.register_blueprint(gestion_ingresos)
miApp.register_blueprint(sesion)
miApp.register_blueprint(registro)
miApp.register_blueprint(validaciones)




miApp.config['MAIL_SERVER']='smtp.gmail.com'
miApp.config['MAIL_PORT'] = 465
miApp.config['MAIL_USERNAME'] = 'mercado.maravillas.online@gmail.com'
miApp.config['MAIL_PASSWORD'] = 'vpnvsbphgvakhqdv'
miApp.config['MAIL_USE_TLS'] = False
miApp.config['MAIL_USE_SSL'] = True
mail = Mail(miApp)


miApp.secret_key='mysecretkey'
    

