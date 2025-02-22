from odoo import models, fields, api

class ProcurementOrder(models.Model):
    _name = 'procurement.order'
    _description = 'Procurement Order Model'

    name = fields.Char(string='Order Reference', required=True)
    order_line_ids = fields.One2many(comodel_name='procurement.order.line', inverse_name='order_id', string='Order Lines')
    vendor_id = fields.Many2one(
        comodel_name='res.users',
        string='Vendor',
        domain=lambda self: self._get_portal_user_domain()
    )
    order_date = fields.Datetime(string='Order Date', default=fields.Datetime.now, required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled')
    ], string= 'State', default='draft', tracking=True, readonly=True)
    active = fields.Boolean(string='Active', default=True)

    @api.model_create_multi
    def create(self, vals_list):
        """Override create method to handle order lines properly in batch"""

        order_lines_map = {}  # Dictionary to store order-line mappings
        for idx, vals in enumerate(vals_list):
            order_lines_map[idx] = vals.pop('order_line_ids', [])  # Extract order lines and store them

        orders = super(ProcurementOrder, self).create(vals_list)  # Batch create orders

        order_lines_to_create = []  # List to store order lines for batch creation
        for idx, order in enumerate(orders):
            for line_data in order_lines_map.get(idx, []):
                if isinstance(line_data, (list, tuple)) and len(line_data) == 3:
                    line_values = line_data[2]  # Extract actual field values
                    line_values['order_id'] = order.id  # Assign order ID
                    order_lines_to_create.append(line_values)  # Collect for batch creation

        if order_lines_to_create:
            self.env['procurement.order.line'].create(order_lines_to_create)  # Batch create order lines

        return orders

    @api.model
    def _get_portal_user_domain(self):
        portal_group_id = self.env.ref('base.group_portal').id
        return [('groups_id', 'in', [portal_group_id])]



class ProcurementOrderLine(models.Model):
    _name = 'procurement.order.line'
    _description = 'Procurement Order Line'


    name = fields.Char(String='Name', related='product_id.name')
    order_id = fields.Many2one(comodel_name='procurement.order', string='Procurement Order', ondelete='cascade')
    product_id = fields.Many2one(comodel_name='product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity', default=1.0, required=True)
    unit_price = fields.Float(string='Unit Price', related='product_id.list_price')


    # def name_get(self):
    #     result = []
    #     for record in self:
    #         name = f"{record.product_id.name} - Qty: {record.quantity}"
    #         result.append((record.id, name))
    #     return result