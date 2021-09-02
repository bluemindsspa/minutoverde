# -*- coding: utf-8 -*-
{
    'name': "Custom Minuto Verde",

    'summary': """
        """,

    'description': """
Adecuaciones varias a solicitud
===============================

Se crea una lengüeta en módulo de compras llamada Checklist

En esta lengüeta se crea un line de 3 columnas:
-----------------------------------------------

* Actividad: Campo de lista (tri) para incorporar el nombre de alguna actividad (Busca/ crea-editar)
* Estado: Campo selector (N/A, Empezado, En ejecución, Terminado, Cancelado)
* ETA Actividad: campo de fecha

""",

    'author': "Blueminds",
    'website': "blueminds.cl",
    'contributors': ["Boris Silva <silvaboris@gmail.com>"],

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Purchase',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase', 'sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/purchase_data.xml',
        'views/purchase_view.xml',
        'views/sale_order_views.xml',
        'views/product_template_view.xml',
        'views/res_partner_view.xml',
    ],

    'qweb': [
        'static/src/xml/purchase_dashboard.xml',
    ],
}
