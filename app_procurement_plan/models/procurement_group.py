# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'

    proc_plan_id = fields.Many2one('procurement.plan', 'Procurement Plan', readonly=True, copy=False)
    # todo: 确定下 origin_type 是否要设置为 procurement.plan

    # 重计追溯
    # todo: 减少依赖后再处理这个 root
    # @api.depends('parent_id', 'sale_id', 'production_id', 'proc_plan_id')
    # def _compute_root(self):
    #     for rec in self:
    #         if rec.parent_id:
    #             rec.root_id = rec.parent_id.root_id
    #         else:
    #             rec.root_id = rec.id
    #
    #         if rec.root_id.proc_plan_id:
    #             rec.root_sale = False
    #             if hasattr(rec, 'root_production'):
    #                 rec.root_production = False
    #         elif rec.root_id.sale_id:
    #             rec.root_sale = rec.root_id.sale_id
    #         else:
    #             rec.root_sale = False
    #
    #         if hasattr(rec, 'root_production') and hasattr(rec, 'production_id'):
    #             if rec.root_id.production_id:
    #                 rec.root_production = rec.root_id.production_id
    #             else:
    #                 rec.root_production = False
    #
    #         if rec.root_id.proc_plan_id:
    #             rec.root_name = rec.root_id.proc_plan_id.name
    #         else:
    #             rec.root_name = rec.root_id.name
