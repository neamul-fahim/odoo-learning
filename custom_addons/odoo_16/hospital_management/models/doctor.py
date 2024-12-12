
from odoo import models, fields, _

class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Doctor Records'
    _rec_name = 'name'

    name = fields.Char(string='Doctor Name', required=True)
    patient_ids = fields.One2many('hospital.patient', 'doctor_id', string='Patients')
    department_ids = fields.Many2many('hospital.department','doctor_department_rel', 'doctor_id', 'department_id', string="Departments")
    specialty = fields.Char(string='Specialty')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')

    def name_get(self):
        res=[]
        for record in self:
            name = f'{record.name} - {record.specialty}'
            res.append((record.id,name))
        return res

    def redirect_to_profile(self):
        action = {
            'type':'ir.actions.act_url',
            'url':'https://www.odoo.com',
            'target':'new'
        }
        return action