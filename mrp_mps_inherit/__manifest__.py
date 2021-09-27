# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Mrp mps inherit',
    'version': '1.0',
    'category': 'Manufacturing/Manufacturing',
    'sequence': 60,
    'summary': 'Mrp mps inherit',
    'depends': ['mrp_mps'],
    'description': """
Mrp mps inherit
==========================

A;ade dos lineas nuevas en template 
1. Producción Agrícola
2. Compras
""",
    'data': [
        'views/assets.xml',
        'views/product_views.xml'
    ],
    'demo': [
        # 'data/mps_demo.xml',
    ],
    'qweb': [
        'static/src/xml/qweb_templates.xml',
    ],
    'application': False,
    'license': 'OEEL-1',
}
