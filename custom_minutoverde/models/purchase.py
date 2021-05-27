# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    checklist_line = fields.One2many('purchase.order.checklist', 'order_id', string='Checklist Lines')
    oc_sap = fields.Char('Nº OC SAP')
    imports = fields.Boolean('Importaciones')
    awb_bl = fields.Char('AWB o B/L')
    cont_nbr = fields.Char('N° DE CONT')
    cia_id = fields.Many2one('purchase.order.cia', string='CIA')
    mn_id = fields.Many2one('purchase.order.mn', string='M/N')
    arrival_port_id = fields.Many2one('purchase.order.arrivalport', string='Puerto de Arribo')
    planned_wh_id = fields.Many2one('purchase.order.plannedwh', string='Bodega Planificada')
    warehouse_id = fields.Many2one('purchase.order.warehouse', string='Bodega')


class PurchaseOrderCia(models.Model):
    _name = 'purchase.order.cia'
    _description = 'CIA'

    name = fields.Text(string='CIA', required=True)


class PurchaseOrderMn(models.Model):
    _name = 'purchase.order.mn'
    _description = 'M/N'

    name = fields.Text(string='M/N', required=True)


class PurchaseOrderArrivalPort(models.Model):
    _name = 'purchase.order.arrivalport'
    _description = 'Puerto de Arribo'

    name = fields.Text(string='Puerto de Arribo', required=True)


class PurchaseOrderPlannedWh(models.Model):
    _name = 'purchase.order.plannedwh'
    _description = 'Bodega Planificada'

    name = fields.Text(string='Bodega Planificada', required=True)


class PurchaseOrderWarehouse(models.Model):
    _name = 'purchase.order.warehouse'
    _description = 'Bodega'

    name = fields.Text(string='Bodega', required=True)


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

