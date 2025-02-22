from odoo import models, fields, api

class PatientBill(models.Model):
    _name = 'hospital.patient.bill'
    _description = 'Patient Bill'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 'patient_id'

    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    currency_id = fields.Many2one('res.currency',string='Currency', default=56)
    billable_amount = fields.Monetary(string='Billable Amount', currency_field='currency_id', required=True, help="Sum of all billable items")
    discount = fields.Float(string='Discount (%)', default=0.0, help="Discount applied to the billable amount")
    total_amount = fields.Float(compute='_compute_total_amount', inverse='_set_total_amount', store=True)
    is_paid = fields.Boolean(string='Paid', default=False, help="Indicates whether the bill is paid")
    priority_bill = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Priority bill")
    bill_state = fields.Selection([
        ('draft', 'Draft'),
        ('in_process', 'In process'),
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid')], string="Bill status", default='draft', required=True)

    @api.depends('billable_amount','discount')
    def _compute_total_amount(self):
        for bill in self:
            bill.total_amount = bill.billable_amount - (bill.billable_amount * (bill.discount/100))

    def _set_total_amount(self):
        for bill in self:
            bill.discount =  ((bill.billable_amount - bill.total_amount) / bill.billable_amount) * 100

    def action_mark_as_paid(self):
        """Marks the selected bills as paid."""
        for bill in self:
            bill.is_paid = True
            bill.bill_state = 'paid'

    def action_print_report(self):
        self.ensure_one()  # Ensure only one record is selected
        return self.env.ref('hospital_management.action_patient_bill_report').report_action(self)

    def unpaid_bill(self):
        for bill in self:
            bill.bill_state = 'unpaid'