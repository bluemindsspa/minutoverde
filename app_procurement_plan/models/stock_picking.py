# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    proc_plan_id = fields.Many2one('procurement.plan', 'Procurement Plan', readonly=True)

