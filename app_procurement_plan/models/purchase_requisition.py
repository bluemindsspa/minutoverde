# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta
from odoo import fields, models, api, _
from odoo.addons.purchase_stock.models.stock_rule import StockRule


class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    proc_plan_id = fields.Many2one('procurement.plan', 'Procurement Plan', readonly=True, copy=False)

    def _prepare_tender_values(self, product_id, product_qty, product_uom, location_id, name, origin, company_id, values):
        res = super(PurchaseRequisition, self)._prepare_tender_values(product_id, product_qty, product_uom, location_id, name, origin, company_id, values)
        if values.get('group_id', False):
            pg = values.get('group_id', False)
            if pg and pg.proc_plan_id:
                res.update({
                    'proc_plan_id': pg.proc_plan_id.id,
                    'origin': pg.proc_plan_id.name
                })
        return res

