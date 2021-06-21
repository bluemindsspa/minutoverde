# -*- coding: utf-8 -*-

from odoo import api, fields, models, registry, _
from odoo.exceptions import UserError

PROCUREMENT_PRIORITIES = [('0', 'Not urgent'), ('1', 'Normal'), ('2', 'Urgent'), ('3', 'Very Urgent')]

# 将 odoo 10中功能迁移过来
class ProcurementOrder(models.Model):
    """ Procurement Orders """
    _name = "procurement.order"
    _description = "Procurement"
    _order = 'priority desc, date_planned, id asc'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Text('Description')
    proc_plan_id = fields.Many2one('procurement.plan', 'Procurement Plan', readonly=True)
    origin = fields.Char('Source Document', readonly=True,
                         help="Reference of the document that created this Procurement. This is automatically completed by Sunpop.cn.")
    proc_order_id = fields.Reference(string='Relate Order', selection=[
        ('sale.order', 'Sale'),
        ('mrp.production', 'Manufacture'),
    ], readonly=True)
    sale_order_id = fields.Many2one('sale.order', 'Sale Order', readonly=True)
    sale_line_id = fields.Many2one('sale.order.line', 'Sale Line', readonly=True)
    # These two fields are used for scheduling
    priority = fields.Selection(
        PROCUREMENT_PRIORITIES, string='Priority', default='1',
        required=True, index=True, tracking=1)
    date_planned = fields.Datetime(
        'Scheduled Date', default=fields.Datetime.now,
        required=True, index=True, tracking=1)
    product_id = fields.Many2one(
        'product.product', 'Product',
        readonly=True, required=True)
    product_uom_qty = fields.Float(
        'Quantity',
        digits='Product Unit of Measure',
        readonly=True, required=True, default=1)
    qty_stock = fields.Float(
        'Quantity Stock',
        digits='Product Unit of Measure',
        required=True, default=0, tracking=2)
    qty_buy = fields.Float(
        'Quantity Buy',
        digits='Product Unit of Measure',
        required=True, default=0, tracking=2)
    qty_manufacture = fields.Float(
        'Quantity Manufacture', default=0, tracking=2,
        digits='Product Unit of Measure',
        required=True)
    qty_remain = fields.Float(
        'Quantity Remain',
        digits='Product Unit of Measure',
        compute='_compute_qty'
    )
    product_uom = fields.Many2one(
        'uom.uom', 'Unit of Measure',
        readonly=True, required=True)
    state = fields.Selection([
        ('approved', 'Approved'),
        ('confirmed', 'Confirmed'),
        ('running', 'Running'),
        ('exception', 'Exception'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')], string='Status', default='approved', readonly=True,
        copy=False, required=True, tracking=1)

    company_id = fields.Many2one(related='proc_plan_id.company_id', string='Company', store=True)

    @api.depends('product_uom_qty', 'qty_stock', 'qty_buy', 'qty_manufacture')
    def _compute_qty(self):
        for rec in self:
            rec.qty_remain = rec.product_uom_qty - rec.qty_stock - rec.qty_buy - rec.qty_manufacture

    @api.onchange('product_id')
    def onchange_product_id(self):
        """ Finds UoM of changed product. """
        if self.product_id:
            self.product_uom = self.product_id.uom_id

