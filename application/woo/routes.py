from flask import render_template, request, jsonify, flash
from woocommerce import API
from . import woo
import stripe
import os
import requests
import openpyxl
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
from .bd import obtener_conexion

# =========================
# CONFIGURACIÓN SEGURA
# =========================

STRIPE_ENDPOINT_SECRET = os.getenv("STRIPE_ENDPOINT_SECRET")

WC_CONSUMER_KEY = os.getenv("WC_CONSUMER_KEY")
WC_CONSUMER_SECRET = os.getenv("WC_CONSUMER_SECRET")

MIRAVIA_APP_KEY = os.getenv("MIRAVIA_APP_KEY")
MIRAVIA_APP_SECRET = os.getenv("MIRAVIA_APP_SECRET")
MIRAVIA_ACCESS_TOKEN = os.getenv("MIRAVIA_ACCESS_TOKEN")


# =========================
# RUTAS
# =========================

@woo.route('/integracion')
def integra():
    return render_template('tienda.html')


# =========================
# SINCRONIZAR INVENTARIO
# =========================

@woo.route('/woocommerce')
def sincronizaInventario():

    wcapi = API(
        url='https://wondermarket.es',
        consumer_key=WC_CONSUMER_KEY,
        consumer_secret=WC_CONSUMER_SECRET,
        wp_api=True,
        version='wc/v3',
        query_string_auth=True
    )

    page = 1

    for _ in range(201):

        productos = wcapi.get("products", params={"per_page": 10, 'page': page}).json()
        page += 1

        for x in productos:
            sku = x['sku']
            product_id = x['id']

            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute(
                    "SELECT sku_indivisible, sku_padre, cantidad FROM productos WHERE sku_padre = %s",
                    (sku,)
                )
                result = cursor.fetchone()

                if result:
                    sku_indivisible, _, relacion = result

                    with conexion.cursor() as cursor2:
                        cursor2.execute(
                            "SELECT cantidad FROM inventario WHERE sku_indivisible = %s",
                            (sku_indivisible,)
                        )
                        inv = cursor2.fetchone()

                        if inv:
                            qty_bd = int(inv[0])

                            if relacion > 1:
                                qty_bd = int(qty_bd / relacion)

                            wcapi.put(f'products/{product_id}', {
                                "stock_quantity": qty_bd
                            })

    return render_template('tienda.html')


# =========================
# WEBHOOK STRIPE
# =========================

@woo.route('/webhookWoocomerce', methods=['POST', 'GET'])
def webhookwoocomerce():

    if request.method == 'POST':
        payload = request.get_data(as_text=True)
        sig_header = request.headers.get('Stripe-Signature')

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, STRIPE_ENDPOINT_SECRET
            )
        except Exception:
            return jsonify(success=False), 400

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            print('Pago recibido:', session['id'])

        return jsonify(success=True), 200

    return 'OK', 200


# =========================
# WEBHOOK MIRAVIA
# =========================

@woo.route('/webhook', methods=['GET'])
def webhook():

    url = 'https://api.miravia.com/v2/product/get'

    headers = {
        'Authorization': f'Bearer {MIRAVIA_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

    params = {
        'product_id': '1357296984086901',
        'page_size': '10'
    }

    response = requests.get(url, headers=headers, params=params)

    return response.json()


# =========================
# EXPORTAR PEDIDOS A EXCEL
# =========================

@woo.route('/pedidos')
def pedidosWonder():

    wcapi = API(
        url='https://wondermarket.es',
        consumer_key=WC_CONSUMER_KEY,
        consumer_secret=WC_CONSUMER_SECRET,
        wp_api=True,
        version='wc/v3',
        query_string_auth=True
    )

    workbook = openpyxl.Workbook()
    sheet = workbook.active

    sheet.append(['Pedido', 'Estado', 'Email', 'Total'])

    page = 1

    while True:
        pedidos = wcapi.get("orders", params={"per_page": 30, 'page': page}).json()

        if not pedidos:
            break

        for order in pedidos:
            sheet.append([
                order['id'],
                order['status'],
                order['billing']['email'],
                order['total']
            ])

        page += 1

    nombre = f"pedidos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    workbook.save(nombre)

    return f"Archivo generado: {nombre}"