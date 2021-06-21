# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from datetime import datetime, time

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    proc_plan_id = fields.Many2one('procurement.plan', 'Procurement Plan', readonly=True, copy=False)
