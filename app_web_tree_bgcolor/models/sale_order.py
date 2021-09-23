# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from datetime import datetime, timedelta

class SaleOrder(models.Model):
    _inherit = "sale.order"

    quotation_alert = fields.Selection([
        ('warning', 'Warning'),
        ('alert', 'Alert'),
    ], string="Quotation Alert", compute='_compute_alert', store=False)
    sale_alert = fields.Selection([
        ('warning', 'Warning'),
        ('alert', 'Alert'),
    ], string="Sale Alert", compute='_compute_alert', store=False)

#    @api.multi
    @api.depends('validity_date', 'commitment_date')
    def _compute_alert(self):
        # quotation 报价期提醒，5天alert红，10天warning黄
        # sale货期提醒，5天alert红，10天warning黄
        time_quotation_alert = timedelta(days=5)
        time_quotation_waring = timedelta(days=10)
        time_sale_alert = timedelta(days=5)
        time_sale_waring = timedelta(days=10)

        for rec in self:
            if rec.state in ('draft', 'sent') and rec.validity_date:
                validity_date = datetime.strptime(str(rec.validity_date), '%Y-%m-%d')
                if validity_date - datetime.now() <= time_quotation_alert:
                    rec.quotation_alert = 'alert'
                elif validity_date - datetime.now() <= time_quotation_waring:
                    rec.quotation_alert = 'warning'

            if rec.commitment_date and rec.state in ('sale', 'done'):
                commitment_date = datetime.strptime(str(rec.commitment_date), '%Y-%m-%d %H:%M:%S')
                if commitment_date - datetime.now() <= time_sale_alert:
                    rec.sale_alert = 'alert'
                elif rec.commitment_date - datetime.now() <= time_sale_waring:
                    rec.sale_alert = 'warning'
