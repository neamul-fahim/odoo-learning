
from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'Patient Records'

    # Personal information
    name = fields.Char(string='Name', required=True, tracking=True)
    image_1920 = fields.Binary(string='Profile Picture')
    profile_pic_file_name = fields.Char(string='File Name (pro_pic)')
    current_prescriptions = fields.Many2many('ir.attachment', string='Current Prescriptions')
    patient_sequence = fields.Char(string='Patient Sequence', required=True, readonly=True, default='New', tracking=True)
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', context="{'no_open': True, 'no_create': True}", tracking=True) # 'no_open': True: This 'context' key is typically used to prevent the linked records from being opened directly from the dropdown in the form view. 'no_create': True: This 'context' key prevents users from being able to create new hospital.doctor records directly from the dropdown.
    doctor_phone = fields.Char(related='doctor_id.phone', string='Doctor Phone Number')
    age = fields.Integer(string='Age', compute = '_compute_age', store=True) # store parameter in a computed field indicates whether the computed value should be stored in the database or not.
    date_of_birth = fields.Date(string='Date Of Birth', tracking=True, default= fields.Date.context_today)
    date_of_birth_with_time = fields.Datetime(string='Date Of Birth (with time)', tracking=True, default= fields.Datetime.now)
    gender  = fields.Selection(
        selection=[
            ('male','Male'),
            ('female','Female'),
            ('others','Others'),
    ],
        string='Gender',
        tracking=True
    )

    # address
    address = fields.Char(string='Address', tracking=True)

    # previous medical history
    pre_medical_history = fields.Text(string='Previous Medical History', tracking=True)

    # others
    is_staff = fields.Boolean(string='Is Staff', tracking=True)
    active = fields.Boolean(default=True, help='active is a default field name that activates archive and unarchive option under Action')
    notes = fields.Text(string='Notes', tracking=True)

    @api.model_create_multi
    def create(self,vals_list):
        for val in vals_list:
            if val.get('patient_sequence','New') == 'New':
                val['patient_sequence'] = self.env['ir.sequence'].next_by_code('hospital_management.hospital.patient') or 'New'
            name_parts = val['name'].split(' ')
            # capitalizes name and adds 'San' at the end of the name
            val['name'] = ' '.join([string.capitalize() for string in name_parts]) + ' San'

        patients=super(HospitalPatient,self).create(vals_list)

        for patient in patients:
            patient.create_patient_bill()  # Call the function to create the bill

        return patients

    def create_patient_bill(self):
        for patient in self:
            # Logic to determine billable amount and other details
            bill_vals = {
                'patient_id': patient.id,
                'currency_id': 56,  # You can set this dynamically or use a default value
                'billable_amount': 100.0,
                # Set the billable amount logic here (you can use default or calculated value)
                'discount': 0.0,  # Default discount, you can modify this as needed
                'is_paid': False,  # Set it to False by default
            }

            # Create the bill record
            self.env['hospital.patient.bill'].create(bill_vals)

    @api.onchange('address')
    def _onchange_age(self):
        if self.address and self.address.lower() == 'hospital':
            self.is_staff = True
        else:
            self.is_staff = False

    @api.depends('date_of_birth')
    def _compute_age(self):
        for record in self:
            if record.date_of_birth:
                today = datetime.today()
                dob = record.date_of_birth
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                record.age = age
            else:
                record.age = 0

    @api.constrains('name', 'age')
    def _check_if_name_has_number(self):
        for record in self:
            if record.name and any(char.isdigit() for char in record.name):
                raise ValidationError(_("Name can't contain digit"))

            if record.age <0:
                raise ValidationError(_("That Age is Unrealistic"))

