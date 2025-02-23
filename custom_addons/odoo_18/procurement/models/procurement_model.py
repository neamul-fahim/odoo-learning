from email.policy import default
from odoo import models, fields, api, _
from odoo.exceptions import UserError


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
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Billing Company'
    )
    order_date = fields.Datetime(string='Order Date', default=fields.Datetime.now, required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled')
    ], string= 'State', default='draft', tracking=True)
    active = fields.Boolean(string='Active', default=True)
    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount', store=True, default=0)
    coo_signature = fields.Binary("COO Signature", groups="procurement.group_coo")
    coo_signed_by = fields.Many2one("res.users", string="COO Signed By", readonly=True, store=True,
                                    compute="_compute_coo_signed_by")

    md_signature = fields.Binary("MD Signature", groups="procurement.group_md")
    md_signed_by = fields.Many2one("res.users", string="MD Signed By", readonly=True, store=True,
                                   compute="_compute_md_signed_by")

    @api.depends('coo_signature')
    def _compute_coo_signed_by(self):
        for order in self:
            if order.coo_signature and not order.coo_signed_by:
                order.coo_signed_by = self.env.user

    @api.depends('md_signature')
    def _compute_md_signed_by(self):
        for order in self:
            if order.md_signature and not order.md_signed_by:
                order.md_signed_by = self.env.user
    def action_confirm(self):
        if self.state != 'draft':
            raise UserError(_('Only Draft states can be Confirmed'))
        self.write({'state': 'confirmed'})

    def action_approve(self):
        if self.state != 'confirmed':
            raise UserError(_('Only Confirmed states can be Approved'))
        self.write({'state': 'approved'})

    def action_complete(self):
        if self.state != 'approved':
            raise UserError(_('Only Approved states can be Completed'))
        self.write({'state': 'completed'})

    def action_cancel(self):
        if self.state not in ('confirmed', 'approved'):
            raise UserError(_('Only Confirmed or Approved states can be Canceled'))
        self.write({'state': 'canceled'})

    @api.depends('order_line_ids.quantity', 'order_line_ids.unit_price')
    def _compute_total_amount(self):
        for order in self:
            order.total_amount = sum(line.quantity * line.unit_price for line in order.order_line_ids)

    @api.depends('total_amount')
    def _compute_big_amount(self):
        for order in self:
            order.big_amount = order.total_amount > 50000

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

    def send_mail_to_vendor(self):
        for order in self:
            email = order.vendor_id.email
            if not email:
                raise UserError(_('Vendor has no email account'))

            body_html = f"""
                <div style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
                    <p>Dear {order.vendor_id.name},</p>

                    <p>We are pleased to inform you that a new <strong>Procurement Order</strong> has been placed.</p>

                    <h3>Order Details:</h3>
                    <ul>
                        <li><strong>Order Reference:</strong> {order.name}</li>
                        <li><strong>Total Amount:</strong> {order.total_amount} Taka</li>
                        <li><strong>Order Date:</strong> {order.order_date}</li>
                    </ul>

                    <p>Please review the order and confirm at your earliest convenience.</p>

                    <p>Best regards,</p>
                    <p><strong>{self.env.user.name}</strong></p>
                    <p><em>Procurement Team</em></p>
                </div>
            """

            mail_values = {
                'subject': _("Procurement Order"),
                'email_to': email,
                'email_from': 'neamul.fahim@gmail.com',
                'body_html':body_html
            }

            mail = self.env['mail.mail'].sudo().create(mail_values)
            mail.send()

class ProcurementOrderLine(models.Model):
    _name = 'procurement.order.line'
    _description = 'Procurement Order Line'


    name = fields.Char(String='Name', related='product_id.name')
    order_id = fields.Many2one(comodel_name='procurement.order', string='Procurement Order', ondelete='cascade')
    product_id = fields.Many2one(comodel_name='product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity', default=1.0, required=True)
    unit_price = fields.Float(string='Unit Price', related='product_id.list_price')
    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount', store=True, default=0)

    @api.depends('quantity', 'unit_price')
    def _compute_total_amount(self):
        for line in self:
            line.total_amount = line.quantity * line.unit_price

    # def name_get(self):
    #     result = []
    #     for record in self:
    #         name = f"{record.product_id.name} - Qty: {record.quantity}"
    #         result.append((record.id, name))
    #     return result