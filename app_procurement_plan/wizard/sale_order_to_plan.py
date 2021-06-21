# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError


class SaleOrderToPlan(models.TransientModel):
    _name = 'sale.order.to.plan'
    _description = 'Sale order to Plan Wizard.'

    create_new = fields.Boolean(string='New Procurement Plan', default=True)
    plan_id = fields.Many2one('procurement.plan', string='Procurement Plan', domain=[('state', '=', 'draft')])
    so_ids = fields.Many2many('sale.order', string='Selected Sale Orders', readonly=True)

    @api.model
    def default_get(self, fields):
        result = super(SaleOrderToPlan, self).default_get(fields)
        active_ids = self._context.get('active_ids') or self._context.get('active_id')
        so_ids = self.env['sale.order'].browse(active_ids)\
            .filtered(lambda r: r.sale_procurement_step == 'two_steps' and r.state == 'sale' and not r.proc_plan_id).ids
        if so_ids:
            result['so_ids'] = so_ids
        return result

    def attach_plan(self):
        self.ensure_one()
        if not self.so_ids:
            raise UserError(_("Please select a Confirmed sale order which not planned."))
        if self.create_new:
            plan_id = self.plan_id.create({})
        else:
            plan_id = self.plan_id
        if not plan_id:
            raise UserError(_("Please select a Procurement Plan."))

        self.so_ids.write({'proc_plan_id': plan_id.id})

        action = self.env.ref('app_procurement_plan.action_procurement_plan').read()[0]
        action['views'] = [(self.env.ref('app_procurement_plan.procurement_plan_form_view').id, 'form')]
        action['res_id'] = plan_id.id
        return action



