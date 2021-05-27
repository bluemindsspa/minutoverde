# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt. Ltd. See LICENSE file for full copyright and licensing details.
{
    'name': 'Purchase Order Stages / Purchase Stages',
    'version': '3.1.0',
    'price': 15.0,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'depends': [
        'purchase',
    ],
    'category': 'Purchase/Purchase',
    'summary':  """This app allows you to manage purchase order stages.""",
    'description': """
This app allows you to manage purchase order stages.
purchase stage
purchase order stages
    """,
    'author': 'Probuse Consulting Service Pvt. Ltd.',
    'website': 'www.probuse.com',
    'images': ['static/description/88ps.jpg'],
    'live_test_url': 'https://youtu.be/e2VsFwEzt50',
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_stage_view.xml',
        'views/purchase_view.xml',
    ],
    'installable': True,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
