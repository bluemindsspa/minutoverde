# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_custom_move_fields(self):
        # 注意，到了生产，每个补货组 pg 就是自己，不会源于上有游，故 proc_plan_id 会特殊处理，根据 group_id.proc_plan_id 来设定
        fields = super(StockRule, self)._get_custom_move_fields()
        fields += ['proc_plan_id']
        return fields

    @api.model
    def _run_buy(self, procurements):
        # 使用 plan后，如果是合并至pr，那么应该没有 补货组 pg，因为是多个 sale 合并了
        p = procurements
        return super(StockRule, self)._run_buy(procurements)

    def _prepare_purchase_order(self, company_id, origins, values):
        res = super(StockRule, self)._prepare_purchase_order(company_id, origins, values)
        values = values[0]
        proc_plan_id = values.get('proc_plan_id', False)
        if not proc_plan_id and values.get('group_id', False):
            proc_plan = values.get('group_id', False).proc_plan_id
            proc_plan_id = proc_plan.id if proc_plan else False
            origin = proc_plan.name if proc_plan else False

        if proc_plan_id:
            res.update({
                'proc_plan_id': proc_plan_id,
                'origin': origin
            })
        return res

    def _prepare_mo_vals(self, product_id, product_qty, product_uom, location_id, name, origin, company_id, values, bom):
        res = super(StockRule, self)._prepare_mo_vals(product_id, product_qty, product_uom, location_id, name, origin, company_id, values, bom)
        proc_plan_id = values.get('proc_plan_id', False)
        if not proc_plan_id and values.get('group_id', False):
            proc_plan = values.get('group_id', False).proc_plan_id
            proc_plan_id = proc_plan.id if proc_plan else False
            origin = proc_plan.name if proc_plan else False

        if proc_plan_id:
            res.update({
                'proc_plan_id': proc_plan_id,
                'origin': origin
            })
        return res
