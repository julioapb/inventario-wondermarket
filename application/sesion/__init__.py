from flask import Flask, render_template, url_for, request, make_response, redirect, Response, Blueprint


sesion = Blueprint('sesion', __name__, template_folder='templates')

from . import routes