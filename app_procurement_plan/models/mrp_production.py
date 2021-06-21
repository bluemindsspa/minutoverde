# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, registry, _

import logging
_logger = logging.getLogger(__name__)

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    proc_plan_id = fields.Many2one('procurement.plan', 'Procurement Plan', readonly=True, copy=False)

    @api.model
    def _prepare_procurement_group_vals(self, values):
        # 注意，由于每个 生产的 pg 都是自己，故生产相关的参数要通过此处传递
        res = super(MrpProduction, self)._prepare_procurement_group_vals(values)
        res.update({'proc_plan_id': values.get('proc_plan_id', False)})
        return res

    def _get_finished_move_value(self, product_id, product_uom_qty, product_uom, operation_id=False, byproduct_id=False):
        # plan 值传递至下游
        res = super(MrpProduction, self)._get_finished_move_value(product_id, product_uom_qty, product_uom, operation_id=False, byproduct_id=False)
        res.update({
            'proc_plan_id': self.proc_plan_id.id if self.proc_plan_id else False,
        })
        return res
