# -*- coding: utf-8 -*-

from odoo import api, fields, models, registry, _
from odoo.exceptions import UserError

# stock.warehouse 中，有定义各种操作,即 m2o 的 stock.rule
# todo: 增加个直接取库存的规则，其实就是什么都没有的规则。但是要显性处理，避免被其它低排序覆盖。
# mto_pull_id, 执行 mto 的规则
# buy_pull_id, 采购
# manufacture_pull_id，制造拉
# manufacture_mto_pull_id，制造MTO
# pbm_mto_pull_id，先领料再制造MTO
# sam_rule_id，先领料，再制造，再储存

PLAN_READONLY_STATES = {
    'draft': [('readonly', False)],
    'approved': [('readonly', True)],
    'running': [('readonly', True)],
    'done': [('readonly', True)],
    'cancel': [('readonly', True)],
}

PROC_READONLY_STATES = {
    'draft': [('readonly', False)],
    'approved': [('readonly', False)],
    'running': [('readonly', True)],
    'done': [('readonly', True)],
    'cancel': [('readonly', True)],
}

class ProcurementPlan(models.Model):
    _name = 'procurement.plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Sale Procurement Plan'
    _order = "id desc"
    _check_company_auto = True

    @api.model
    def _get_default_manufacture_route_id(self):
        domain = [('proc_plan_type', '=', 'manufacture'), '|', ('company_id', '=', False), ('company_id', '=', self.env.company.id)]
        route = self.env['stock.location.route'].with_user(1).search(domain, limit=1)
        if not route:
            route = self.env.ref('mrp.route_warehouse0_manufacture', raise_if_not_found=False)
        return route

    @api.model
    def _get_default_buy_route_id(self):
        domain = [('proc_plan_type', '=', 'buy'), '|', ('company_id', '=', False), ('company_id', '=', self.env.company.id)]
        route = self.env['stock.location.route'].with_user(1).search(domain, limit=1)
        if not route:
            route = self.env.ref('purchase_stock.route_warehouse0_buy', raise_if_not_found=False)
        return route
    
    @api.model
    def _get_default_stock_route_id(self):
        domain = [('proc_plan_type', '=', 'stock'), '|', ('company_id', '=', False), ('company_id', '=', self.env.company.id)]
        route = self.env['stock.location.route'].with_user(1).search(domain, limit=1)
        if not route:
            route = self.env.ref('app_stock_mts_else_mto.route_warehouse0_pull_mts', raise_if_not_found=False)
        return route

    name = fields.Char('Reference', index=True, required=True, readonly=True, default=lambda self: _('New'))
    # 停用，使用 so 中设置
    # warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse', index=True, default=_get_default_warehouse_id, states=PLAN_READONLY_STATES)
    # 用路线处理
    manufacture_route_id = fields.Many2one('stock.location.route', 'Route Manufacture', default=_get_default_manufacture_route_id,
                                           states=PLAN_READONLY_STATES, ondelete='set null')
    buy_route_id = fields.Many2one('stock.location.route', 'Route Buy', default=_get_default_buy_route_id,
                                   states=PLAN_READONLY_STATES, ondelete='set null')
    stock_route_id = fields.Many2one('stock.location.route', 'Route Take from Stock', default=_get_default_stock_route_id,
                                     states=PLAN_READONLY_STATES, ondelete='set null')
    purchase_type_id = fields.Many2one('purchase.requisition.type', string='Agreement Type',
                                       states=PLAN_READONLY_STATES, ondelete='set null',
                                       default=lambda self: self._app_get_m2o_default('purchase_type_id'))
    sale_order_ids = fields.One2many('sale.order', 'proc_plan_id', string='Sale Orders to Plan', check_company=True, states=PLAN_READONLY_STATES,
                                     ondelete='set null')
    sale_order_count = fields.Integer(string='Sale Count', compute='_compute_procurement_count', store=True)
    procurement_ids = fields.One2many('sale.order.line', 'proc_plan_id', 'Sale Order Lines',
                                      states=PROC_READONLY_STATES,
                                      domain="[('product_id.type', 'in', ('consu', 'product'))]")
    procurement_count = fields.Integer(string='Procurements Count', compute='_compute_procurement_count', store=True)
    # draft，可改
    # approved, 单头确认不可改，明细可改
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('running', 'Running'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')], string='Status', default='draft',
        copy=False, required=True, tracking=1, readonly=True)

    # 工作流处理
    date_approved = fields.Datetime('approved Date', readonly=True, index=True, copy=False)
    user_approved = fields.Many2one('res.users', string='approved By', readonly=True, index=True, tracking=2)
    note = fields.Char(string="Note")
    # begin：关联单据
    purchase_requisition_ids = fields.One2many('purchase.requisition', 'proc_plan_id', string='Purchase Agreement', copy=False, readonly=True)
    purchase_requisition_count = fields.Integer('Number of Purchase Agreements', compute='_compute_purchase_requisition_count')

    purchase_order_ids = fields.One2many('purchase.order', 'proc_plan_id', string='Purchases', copy=False, readonly=True)
    purchase_order_count = fields.Integer('Number of Purchase Order', compute='_compute_purchase_order_count')

    mrp_production_ids = fields.One2many('mrp.production', 'proc_plan_id', string='Productions', copy=False, readonly=True)
    mrp_production_count = fields.Integer('Number of Manufacturing Orders', compute='_compute_mrp_production_count')
    # end: 关联单据

    qty_plan_total = fields.Float(
        'Qty Plan Total',
        digits='Product Unit of Measure', copy=False, store=True, tracking=2,
        compute='_compute_qty_total')
    qty_remain_total = fields.Float(
        'Qty Remain Total',
        digits='Product Unit of Measure', copy=False, store=True, tracking=2,
        compute='_compute_qty_total')
    qty_manufacture_total = fields.Float(
        'Qty Manufacture Total',
        digits='Product Unit of Measure', copy=False, store=True, tracking=2,
        compute='_compute_qty_total')
    qty_buy_total = fields.Float(
        'Qty Buy Total',
        digits='Product Unit of Measure', copy=False, store=True, tracking=2,
        compute='_compute_qty_total')
    qty_stock_total = fields.Float(
        'Qty Stock Total',
        digits='Product Unit of Measure', copy=False, store=True, tracking=2,
        compute='_compute_qty_total')
    
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company, states=PLAN_READONLY_STATES)


    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code('procurement.plan') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('procurement.plan') or _('New')
        return super(ProcurementPlan, self).create(vals)

    @api.depends('state', 'procurement_ids', 'procurement_ids.qty_plan', 'procurement_ids.qty_remain', 
                 'procurement_ids.qty_manufacture', 'procurement_ids.qty_buy', 'procurement_ids.qty_stock')
    def _compute_qty_total(self):
        for rec in self:
            rec.qty_plan_total = sum(rec.procurement_ids.mapped("qty_plan"))
            rec.qty_remain_total = sum(rec.procurement_ids.mapped("qty_remain"))
            rec.qty_manufacture_total = sum(rec.procurement_ids.mapped("qty_manufacture"))
            rec.qty_buy_total = sum(rec.procurement_ids.mapped("qty_buy"))
            rec.qty_stock_total = sum(rec.procurement_ids.mapped("qty_stock"))

    @api.depends('state', 'sale_order_ids', 'procurement_ids.product_uom_qty')
    def _compute_procurement_count(self):
        for rec in self:
            rec.procurement_count = len(rec.procurement_ids)
            rec.sale_order_count = len(rec.sale_order_ids)

    @api.depends('state', 'purchase_requisition_ids')
    def _compute_purchase_requisition_count(self):
        for rec in self:
            rec.purchase_requisition_count = len(rec.purchase_requisition_ids)

    @api.depends('state', 'purchase_order_ids')
    def _compute_purchase_order_count(self):
        for rec in self:
            rec.purchase_order_count = len(rec.purchase_order_ids)

    @api.depends('state', 'mrp_production_ids')
    def _compute_mrp_production_count(self):
        for rec in self:
            rec.mrp_production_count = len(rec.mrp_production_ids)

    def action_approved(self):
        # if not self.user_has_groups('app_procurement_plan.group_proc_plan_manager'):
        #     raise UserError(_("Only Procurement Plan Manager can Approved the Plan."))
        ids = self.filtered(lambda r: r.state == 'draft')
        for plan in ids:
            plan.sale_order_ids.set_proc_plan(plan)
        return ids.write({
            'state': 'approved',
            'date_approved': fields.Datetime.now(),
            'user_approved': self.env.user.id,
        })

    def action_running(self):
        if not self.user_has_groups('app_procurement_plan.group_proc_plan_manager'):
            raise UserError(_("Only Procurement Plan Manager can Run the Plan."))
        ids = self.filtered(lambda r: r.state == 'approved')
        for p in ids:
            # 检查是否有没处理的
            if not p.procurement_ids:
                raise UserError(_("No Item to Plan."))
            if any(r.qty_remain != 0.0 for r in p.procurement_ids):
                raise UserError(_("You must plan all the line to Run the Plan. And All Qty Remain must equal to 0."))
            # 必须用原生补货组，每个 so 一个补货组
            # todo:  全部不用 mto, 在此处理生成 采购/生产 补货
            p.procurement_ids.with_context(procurement_plan_running=True)._action_launch_stock_rule()
        return ids.write({
            'state': 'running',
        })

    def action_done(self):
        ids = self.filtered(lambda r: r.state == 'running')
        return ids.write({
            'state': 'done',
        })

    # todo 取消所有相关单据操作
    def action_cancel(self):
        for rec in self:
            if rec.state not in ['draft', 'approved']:
                raise UserError(_("The Plan can not to be cancel once Running."))
        ids = self.filtered(lambda s: s.state in ['draft', 'approved'])
        return ids.write({'state': 'cancel'})

    # 重置，只有取消的才可重置
    def action_draft(self):
        for rec in self:
            if rec.state not in ['cancel']:
                raise UserError(_("You should cancel the Plan if you want to reset to draft."))
        ids = self.filtered(lambda s: s.state == 'cancel')
        for plan in ids:
            plan.sale_order_ids.clear_proc_plan()
        return ids.write({
            'state': 'draft',
            'sale_order_ids': False,
            'date_approved': False,
            'user_approved': False,
        })

    # 只有取消后才可删除
    def unlink(self):
        for rec in self:
            if rec.state != 'cancel':
                raise UserError(_('You must cancel the Plan before you can delete it.'))
        return super(ProcurementPlan, self).unlink()


    def action_view_pr(self):
        self.ensure_one()
        action = self.env.ref('purchase_requisition.action_purchase_requisition').read()[0]
        action['context'] = dict(self._context, create=False)
        # choose the view_mode accordingly
        if not self.purchase_requisition_count or self.purchase_requisition_count > 1:
            action['domain'] = [('proc_plan_id', '=', self.id)]
        elif self.purchase_requisition_count == 1:
            action['views'] = [(False, 'form')]
            action['res_id'] = self.purchase_requisition_ids[0].id
        return action

    def action_view_po(self):
        self.ensure_one()
        action = self.env.ref('purchase.purchase_rfq').read()[0]
        action['context'] = dict(self._context, create=False)
        if not self.purchase_order_count or self.purchase_order_count > 1:
            action['domain'] = [('proc_plan_id', '=', self.id)]
        elif self.purchase_order_count == 1:
            action['views'] = [(False, 'form')]
            action['res_id'] = self.purchase_order_ids[0].id
        return action

    def action_view_mo(self):
        self.ensure_one()
        action = self.env.ref('mrp.mrp_production_action').read()[0]
        action['context'] = dict(self._context, create=False)
        if not self.mrp_production_count or self.mrp_production_count > 1:
            action['domain'] = [('proc_plan_id', '=', self.id)]
        elif self.mrp_production_count == 1:
            action['views'] = [(self.env.ref('mrp.mrp_production_form_view').id, 'form')]
            action['res_id'] = self.mrp_production_ids[0].id
        return action


