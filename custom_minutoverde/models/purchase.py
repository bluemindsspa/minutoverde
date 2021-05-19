# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    checklist_line = fields.One2many('purchase.order.checklist', 'order_id', string='Checklist Lines')


class PurchaseOrderChecklist(models.Model):
    _name = 'purchase.order.checklist'
    _description = 'Purchase Order Checklist'
    _order = 'id'

    name = fields.Text(string='Tarea', required=True)
    state = fields.Selection(selection=[
        ('N/A', 'N/A'),
        ('EMP', 'Empezando'),
        ('EJE', 'En ejecucion'),
        ('TER', 'Terminado'),
        ('CAN', 'Cancelado')
    ], string='Estado')
    task_eta = fields.Date('ETA tarea')
    order_id = fields.Many2one('purchase.order', string='Order Reference', index=True, required=True, ondelete='cascade')

