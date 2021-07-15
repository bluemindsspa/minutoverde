# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = "Product Template"

    family_id = fields.Many2one('product.family', string='Agrupación Familia')
    fam_id = fields.Many2one('product.fam', string="Familia")
    sub_fam_id = fields.Many2one('product.fam', string="Sub Familia")
    categ_fam_id = fields.Many2one('product.categoria.fam', string="Categoría")
    sub_categ_fam_id = fields.Many2one('product.categoria.fam', string="Sub Categoría")
    
class ProductFamily(models.Model):
    _name = 'product.family'
    _description = 'Agrupación Familiar'
   
    name = fields.Char(string='Nombre')

class ProductFam(models.Model):
    _name = 'product.fam'
    _description = 'Familia'
   
    name = fields.Char(string='Nombre')

class ProductCategFam(models.Model):
    _name = 'product.categoria.fam'
    _description = 'Categoría'
   
    name = fields.Char(string='Nombre')