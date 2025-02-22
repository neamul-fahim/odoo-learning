from odoo import models, fields

class Department(models.Model):
    _name = 'hospital.department'
    _description = 'Department'

    name = fields.Char(string="Department Name", required=True)
    doctor_ids = fields.Many2many(
        'hospital.doctor',            # Target model (Doctor)
        'doctor_department_rel',      # join table name
        'department_id',              # Foreign key to the Department model
        'doctor_id',                  # Foreign key to the Doctor model
        string="Doctors"
    )
    about = fields.Html(string='About')