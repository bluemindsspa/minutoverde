# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api

class CustomPurchaseOrderStage(models.Model):
    _name = 'custom.purchase.order.stage'
    _description = 'Purchase Order Stages'

    name = fields.Char(
        string='Name',
        required=True,
    )
    sequence = fields.Integer(
    	string='Sequence',
    )
            
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: