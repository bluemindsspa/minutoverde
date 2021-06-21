# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class StockMove(models.Model):
    _inherit = "stock.move"
    
    proc_plan_id = fields.Many2one('procurement.plan', 'Procurement Plan', index=True)

    # 处理合并发货
    @api.model
    def _prepare_merge_moves_distinct_fields(self):
        distinct_fields = super(StockMove, self)._prepare_merge_moves_distinct_fields()
        distinct_fields.append('proc_plan_id')
        return distinct_fields
