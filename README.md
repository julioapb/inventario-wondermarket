# Inventario Wondermarket

Aplicación web desarrollada con **Python y Flask** para la gestión interna del inventario de productos de Wondermarket.

El sistema centraliza procesos operativos como control de productos, movimientos de inventario, ventas, reportes, facturación e integración con WooCommerce, permitiendo mantener actualizado el stock y facilitar tareas administrativas del negocio.

---

## Descripción

Este proyecto fue desarrollado como una solución práctica para gestionar de forma centralizada distintas operaciones del negocio, especialmente relacionadas con:

- control de inventario
- gestión de productos
- registro de ventas
- control de ingresos y salidas
- reportes
- facturación
- sincronización con WooCommerce

Además, incorpora módulos complementarios para sesiones, validaciones, cargas de datos y automatización de tareas operativas.

---

## Funcionalidades principales

- Gestión de productos
- Control de inventario
- Registro de ventas
- Gestión de ingresos y salidas
- Reportes
- Facturación
- Cargas de información
- Validaciones de datos
- Gestión de sesiones y acceso
- Integración con WooCommerce
- Exportación de pedidos a Excel
- Sincronización de stock con tienda online

---

## Tecnologías utilizadas

- **Python**
- **Flask**
- **HTML**
- **Jinja2**
- **WooCommerce API**
- **OpenPyXL**
- **Pandas**
- **SQLAlchemy**

---

## Estructura general del proyecto

El proyecto está organizado de forma modular usando Blueprints de Flask.

### Módulos principales detectados

- `inicio`
- `cargas`
- `productos`
- `inventario`
- `gestion_salidas`
- `cancelaciones`
- `ventas`
- `reportes`
- `combos`
- `facturas`
- `foto_diaria`
- `woo`
- `gestion_ingresos`
- `sesion`
- `registro`
- `validaciones`

---

## Integración con WooCommerce

El sistema incluye una integración con WooCommerce para automatizar procesos como:

- sincronización de stock
- consulta de productos
- exportación de pedidos
- manejo de eventos relacionados con pagos y pedidos

Esto permite conectar la operación interna del inventario con la tienda online y reducir tareas manuales.

---

## Objetivo del proyecto

El objetivo de esta aplicación es mejorar la gestión operativa del negocio mediante una herramienta web interna que facilite el control del inventario y la integración con procesos comerciales y de venta online.

También representa un proyecto práctico de desarrollo backend con Flask aplicado a una necesidad real de negocio.

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/julioapb/inventario-wondermarket.git
cd inventario-wondermarket
