# -*- coding: utf-8 -*-

from odoo import api, fields, models, registry, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_compare
from odoo.exceptions import UserError

PROCUREMENT_PRIORITIES = [('0', 'Not urgent'), ('1', 'Normal'), ('2', 'Urgent'), ('3', 'Very Urgent')]

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    proc_plan_id = fields.Many2one(related='order_id.proc_plan_id', store=True)
    group_id = fields.Many2one('procurement.group', 'Procurement Group')

    # These two fields are used for scheduling
    priority = fields.Selection(
        PROCUREMENT_PRIORITIES, string='Priority', default='1', copy=False,
        required=True, index=True, tracking=1)
    # 数量    product_uom_qty 是总数，product_uom 是单位
    qty_plan = fields.Float(
        'Qty Plan',
        digits='Product Unit of Measure', copy=False, store=True,
        compute='_compute_qty_plan')
    qty_remain = fields.Float(
        'Qty Remain',
        digits='Product Unit of Measure', copy=False, store=True,
        compute='_compute_qty_plan')
    qty_manufacture = fields.Float(
        'Qty Manufacture',
        digits='Product Unit of Measure', default=0, required=True, copy=False, tracking=2)
    qty_buy = fields.Float(
        'Qty Buy',
        digits='Product Unit of Measure', default=0, required=True, copy=False, tracking=2)
    qty_stock = fields.Float(
        'Qty Stock',
        digits='Product Unit of Measure', default=0, required=True, copy=False, tracking=2)
    proc_state = fields.Selection([
        ('approved', 'Approved'),
        ('confirmed', 'Confirmed'),
        ('running', 'Running'),
        ('exception', 'Exception'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')], string='Status', default='approved', required=True, readonly=True, copy=False, tracking=1)

    # 要处理的数量，便于更改
    def _get_qty_plan(self):
        self.ensure_one()
        return self.product_uom_qty

    @api.depends('product_uom_qty', 'qty_stock', 'qty_buy', 'qty_manufacture')
    def _compute_qty_plan(self):
        for rec in self:
            qty_plan = rec._get_qty_plan()
            rec.qty_plan = qty_plan
            rec.qty_remain = qty_plan - rec.qty_stock - rec.qty_buy - rec.qty_manufacture

    # 调整，还是每个 so 生成一个 pg，要不无法处理好发货单
    def _prepare_procurement_group_vals(self):
        # todo: 后续在 pr 中处理合并
        res = super(SaleOrderLine, self)._prepare_procurement_group_vals()
        if self.order_id.sale_procurement_step == 'two_steps' and self.order_id.proc_plan_id:
            # 正常情况不传 sale_id，
            res.update({
                'proc_plan_id': self.order_id.proc_plan_id.id,
            })
            # 增加采购类型，处理是否安装 app_purchase_requisition
            if self.order_id.proc_plan_id and self.order_id.proc_plan_id.purchase_type_id and hasattr(self.env['procurement.group'], 'purchase_type_id'):
                res.update({
                    'purchase_type_id': self.order_id.proc_plan_id.purchase_type_id.id,
                })
        return res 

    # 处理指定数量的补货请求，初始值
    def _action_launch_stock_rule(self, previous_product_uom_qty=False):
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        procurements = []
        # 全局判断只从第一个处理，便于批量
        if self and not self[0].order_id.sale_procurement_step == 'two_steps':
            return super(SaleOrderLine, self)._action_launch_stock_rule(previous_product_uom_qty)
        elif self._context.get('procurement_plan_running', False):
            for line in self:            
                if line.state != 'sale' or not line.product_id.type in ('consu', 'product'):
                    continue
                qty = line._get_qty_procurement(previous_product_uom_qty)
                # todo: 数量与 stock.move 的传递，当前只处理 proc 一次                
                # 处理增量，可不管
                if float_compare(qty, line.qty_plan, precision_digits=precision) >= 0:
                    continue

                group_id = line._get_procurement_group()
                if not group_id:
                    group_id = self.env['procurement.group'].create(line._prepare_procurement_group_vals())
                    line.order_id.procurement_group_id = group_id
                else:
                    # 每处理一次，就将 move_type 等参数设置为新的，避免 pr 之前被取消
                    updated_vals = {}
                    if group_id.partner_id != line.order_id.partner_shipping_id:
                        updated_vals.update({'partner_id': line.order_id.partner_shipping_id.id})
                    if group_id.move_type != line.order_id.picking_policy:
                        updated_vals.update({'move_type': line.order_id.picking_policy})
                    if updated_vals:
                        group_id.write(updated_vals)

                procurements += line._get_procurements_by_type(group_id, 'manufacture')
                procurements += line._get_procurements_by_type(group_id, 'buy')
                procurements += line._get_procurements_by_type(group_id, 'stock')
            if procurements:
                self.env['procurement.group'].run(procurements)
            return True

    def _get_procurements_by_type(self, group_id, type):
        values = self._prepare_procurement_values(group_id=group_id)
        self.ensure_one()
        procurements = []
        route_ids = self.proc_plan_id[('%s_route_id' % type)]
        # todo: 暂时当生产或者采购，强制MTO。 注意，如果是从库存补货，一定不能强制MTO，因为会触发相关 采购或者生产
        if type in ['manufacture', 'buy']:
            route_mto = self.order_id.warehouse_id.mto_pull_id.route_id
            route_ids += route_mto
        values.update({
            'route_ids': route_ids,
        })
        product_qty = self[('qty_%s' % type)]

        line_uom = self.product_uom
        quant_uom = self.product_id.uom_id
        product_qty, procurement_uom = line_uom._adjust_uom_quantities(product_qty, quant_uom)
        procurements.append(self.env['procurement.group'].Procurement(
            self.product_id, product_qty, procurement_uom,
            self.order_id.partner_shipping_id.property_stock_customer,
            self.name, self.order_id.name, self.order_id.company_id, values))
        return procurements

    def _prepare_procurement_values(self, group_id=False):
        res = super(SaleOrderLine, self)._prepare_procurement_values(group_id)
        if group_id and group_id.proc_plan_id:
            res.update({
                'proc_plan_id': group_id.proc_plan_id.id,
            })
        return res
