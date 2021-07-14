# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = "Product Template"

    family_id = fields.Many2one('product.family', string='Agrupación Familia')

class ProductFamily(models.Model):
    _name = 'product.family'
    _description = 'Agrupación Familiar'
   
    name = fields.Char(string='Nombre')