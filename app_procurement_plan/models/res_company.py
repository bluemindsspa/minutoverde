# -*- coding: utf-8 -*-

from odoo import models, api, fields, _


class ResCompany(models.Model):
    _inherit = 'res.company'

    default_sale_procurement_step = fields.Selection([
        ('one_step', '1 step,Confirm to Procurement'),
        ('two_steps', '2 steps,Confirm to Plan then Procurement')
    ], string="Default Sale Procurement Workflow", default='two_steps',
        help="Set 2 steps to use Procurement Plan to get material supply for the sale order. "
             "Set 1 step to use normal direct Procurement. "
             "You can set for each Sale Order.")

