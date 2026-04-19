from ast import dump
import datetime
from operator import index
from socket import IPV6_DONTFRAG
import time
from flask import Flask, render_template, url_for, request, make_response, redirect, Response, Blueprint
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
from flask_mail import Mail, Message

gestion_salidas = Blueprint('gestion_salidas',__name__, template_folder='templates')

from . import gestion_salidas

gestion_salidas.secret_key='mysecretkey'

from . import routes