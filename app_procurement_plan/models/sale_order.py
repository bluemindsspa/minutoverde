# -*- coding: utf-8 -*-

from odoo import api, fields, models, registry, _


class SaleOder(models.Model):
    _inherit = 'sale.order'

    sale_procurement_step = fields.Selection([
        ('one_step', '1 step,Confirm to Procurement'),
        ('two_steps', '2 steps,Confirm to Plan then Procurement')
    ], string="Procurement Workflow", default='two_steps',
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        help="Set 2 steps to use Procurement Plan to get material supply for the sale order. "
             "Set 1 step to use normal direct Procurement. "
             "You can set for each Sale Order.")

    proc_plan_id = fields.Many2one('procurement.plan', string='Procurement Plan', copy=False, tracking=2)

    def set_proc_plan(self, proc):
        ids = self.filtered(lambda r: r.state == 'sale')
        ids.write({
            'proc_plan_id': proc.id
        })
        for sol in ids.mapped('order_line'):
            # rule = self.env['procurement.group']._get_rule(
            #     sol.product_id, sol.order_partner_id.property_stock_customer, sol._prepare_procurement_values(False))
            # todo: 当前用目录方式，快速得到数量先，后续再用 pg 方法，要找
            vals = self.proc_get_rule(proc, sol.product_id, sol.qty_plan)
            sol.write(vals)

    def proc_get_rule(self, proc, product, qty):
        vals = {
            'qty_manufacture': 0,
            'qty_buy': 0,
            'qty_stock': 0,
            'proc_plan_id': proc.id,
        }
        if proc.manufacture_route_id in product.route_ids + product.route_from_categ_ids:
            vals.update({'qty_manufacture': qty})
        elif proc.buy_route_id in product.route_ids + product.route_from_categ_ids:
            vals.update({'qty_buy': qty})
        else:
            vals.update({'qty_stock': qty})
        return vals

    def clear_proc_plan(self):
        ids = self.filtered(lambda r: r.state == 'sale')
        ids.write({
            'proc_plan_id': False
        })
        ids.order_line.write({
            'proc_plan_id': False
        })

    def action_sale_to_plan(self):
        action = self.env.ref('app_procurement_plan.action_sale_order_to_plan').read()[0]
        return action
