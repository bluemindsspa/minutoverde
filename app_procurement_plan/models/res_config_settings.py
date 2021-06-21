# -*- coding: utf-8 -*-

from odoo import models, api, fields, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    default_sale_procurement_step = fields.Selection(string="Default Sale Procurement Workflow", related='company_id.default_sale_procurement_step',
        readonly=False, default_model="sale.order",
        help="Set 2 steps to use Procurement Plan to get material supply for the sale order. "
             "Set 1 step to use normal direct Procurement. "
             "You can set for each Sale Order.")


