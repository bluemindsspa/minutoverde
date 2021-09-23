# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class SupplierInfo(models.Model):
	_inherit = 'product.supplierinfo'
	_description = "Supplier Pricelist"

	incoterm = fields.Many2one('purchase.order', string="Incoterm")
