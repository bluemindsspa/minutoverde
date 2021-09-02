# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta


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
    estimated_date = fields.Date(string='Fecha Estimada')
    contenedor_count = fields.Integer(string="Cant. Contenedores", store=True, compute='_compute_contenedor')

    @api.model
    def retrieve_dashboard(self):
        """ This function returns the values to populate the custom dashboard in
            the purchase order views.
        """
        self.check_access_rights('read')

        result = {
            'all_to_send': 0,
            'all_waiting': 0,
            'all_late': 0,
            'all_container': 0,
            'my_to_send': 0,
            'my_waiting': 0,
            'my_late': 0,
            'my_container': 0,
            'all_avg_order_value': 0,
            'all_avg_days_to_purchase': 0,
            'all_total_last_7_days': 0,
            'all_sent_rfqs': 0,
            'company_currency_symbol': self.env.company.currency_id.symbol
        }

        one_week_ago = fields.Datetime.to_string(fields.Datetime.now() - relativedelta(days=7))
        # This query is brittle since it depends on the label values of a selection field
        # not changing, but we don't have a direct time tracker of when a state changes
        query = """SELECT COUNT(1)
                       FROM mail_tracking_value v
                       LEFT JOIN mail_message m ON (v.mail_message_id = m.id)
                       JOIN purchase_order po ON (po.id = m.res_id)
                       WHERE m.create_date >= %s
                         AND m.model = 'purchase.order'
                         AND m.message_type = 'notification'
                         AND v.old_value_char = 'RFQ'
                         AND v.new_value_char = 'RFQ Sent'
                         AND po.company_id = %s;
                    """

        self.env.cr.execute(query, (one_week_ago, self.env.company.id))
        res = self.env.cr.fetchone()
        result['all_sent_rfqs'] = res[0] or 0

        # easy counts
        po = self.env['purchase.order']
        result['all_to_send'] = po.search_count([('state', '=', 'draft')])
        result['my_to_send'] = po.search_count([('state', '=', 'draft'), ('user_id', '=', self.env.uid)])
        result['all_waiting'] = po.search_count([('state', '=', 'sent'), ('date_order', '>=', fields.Datetime.now())])
        result['my_waiting'] = po.search_count(
            [('state', '=', 'sent'), ('date_order', '>=', fields.Datetime.now()), ('user_id', '=', self.env.uid)])
        result['all_late'] = po.search_count(
            [('state', 'in', ['draft', 'sent', 'to approve']), ('date_order', '<', fields.Datetime.now())])
        all_purchases = po.search([('date_order', '<=', fields.Datetime.now())])
        result['all_container'] = sum(purch.contenedor_count for purch in all_purchases)
        result['my_late'] = po.search_count(
            [('state', 'in', ['draft', 'sent', 'to approve']), ('date_order', '<', fields.Datetime.now()),
             ('user_id', '=', self.env.uid)])
        my_purchases = po.search([('user_id', '=', self.env.uid),('date_order', '<=', fields.Datetime.now())])
        result['my_container'] = sum(purch.contenedor_count for purch in my_purchases)

        # Calculated values ('avg order value', 'avg days to purchase', and 'total last 7 days') note that 'avg order value' and
        # 'total last 7 days' takes into account exchange rate and current company's currency's precision. Min of currency precision
        # is taken to easily extract it from query.
        # This is done via SQL for scalability reasons
        query = """SELECT AVG(COALESCE(po.amount_total / NULLIF(po.currency_rate, 0), po.amount_total)),
                              AVG(extract(epoch from age(po.date_approve,po.create_date)/(24*60*60)::decimal(16,2))),
                              SUM(CASE WHEN po.date_approve >= %s THEN COALESCE(po.amount_total / NULLIF(po.currency_rate, 0), po.amount_total) ELSE 0 END),
                              MIN(curr.decimal_places)
                       FROM purchase_order po
                       JOIN res_company comp ON (po.company_id = comp.id)
                       JOIN res_currency curr ON (comp.currency_id = curr.id)
                       WHERE po.state in ('purchase', 'done')
                         AND po.company_id = %s
                    """
        self._cr.execute(query, (one_week_ago, self.env.company.id))
        res = self.env.cr.fetchone()
        result['all_avg_order_value'] = round(res[0] or 0, res[3])
        result['all_avg_days_to_purchase'] = round(res[1] or 0, 2)
        result['all_total_last_7_days'] = round(res[2] or 0, res[3])

        return result

    @api.depends('order_line', 'order_line.contenedor_name')
    def _compute_contenedor(self):
        for record in self:
            qty = 0
            if record.order_line:
                contenedores = record.order_line.mapped('contenedor_name')
                for contenedor in contenedores:
                    if contenedor:
                        qty += 1
            record.contenedor_count = qty



class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    contenedor_name = fields.Char('N° DE CONT')
    contrato_name = fields.Char('Contrato')

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

