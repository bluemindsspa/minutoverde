# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from dateutil import relativedelta
from odoo.exceptions import UserError, ValidationError

from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

class Route(models.Model):
    _inherit = 'stock.location.route'

    proc_plan_type = fields.Selection([
        ('stock', 'Take from Stock'),
        ('buy', 'Buy'),
        ('manufacture', 'Manufacture'),
        ('push', 'Push to Stock Location')
    ], string='Plan Type')

    # 一种安排只能有一个路线
    @api.constrains("proc_plan_type", "company_id")
    def _check_proc_plan_type(self):
        for rec in self:
            if rec.search_count([
                    ('company_id', '=', rec.company_id.id),
                    ('proc_plan_type', '=', rec.proc_plan_type),
                    ('proc_plan_type', '!=', False)]) > 1:
                raise ValidationError(_("You can only assign one Procurement Route to one Plan Type."))

    @api.onchange('sale_selectable')
    def onchange_sale_selectable(self):
        if not self.sale_selectable:
            self.proc_plan_type = False
