from odoo import models, fields, api

class Partner(models.Model):
    _inherit = "res.partner"
   
    chanel_id = fields.Many2one('res.chanel', string='Canal')
    description = fields.Char(string='Descripción')
    group_id = fields.Many2one('res.group', string='Grupo')
    reference = fields.Char('Referencia')
   
class Chanel(models.Model):
    _name = "res.chanel"
   
    name = fields.Char(string='Nombre')
   
   
class Group(models.Model):
    _name = "res.group"
   
    name = fields.Char(string='Nombre')