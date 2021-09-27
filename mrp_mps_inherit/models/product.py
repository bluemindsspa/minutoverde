from odoo import api, fields, models 

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    week_analysis = fields.Integer(string='Semanas de Analisis', help='Cantidad de semanas de analisis para el stock de seguridad implementado en el Programa Maestro de Produccion')