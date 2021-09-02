from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    contenedor_count = fields.Integer(string="Cant. Contenedores", store=True, compute='_compute_contenedor', default=0)

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

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    contenedor_name = fields.Char('N° DE CONT')
    box_per_container = fields.Float(string="Cont. aprox.", compute='_compute_container_approximate')

    @api.depends('product_id', 'product_uom_qty')
    def _compute_container_approximate(self):
        for line in self:
            qty = 0.0
            if line.product_id:
                qty = line.product_uom_qty / line.product_id.box_per_container if line.product_id.box_per_container else 0.0
            line.box_per_container = qty

