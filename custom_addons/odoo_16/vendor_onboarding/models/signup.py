from odoo import models,fields,api
from datetime import datetime, timedelta
import random
from odoo.exceptions import UserError



class Signup(models.Model):
    _name = 'signup'
    _description = 'Vendor signup'

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email', required=True)
    # password = fields.Char(string='Password Hash')
    otp = fields.Char(string='OTP', required=True)
    otp_expiration = fields.Datetime(String='OTP expiration', default=lambda self: datetime.now() + timedelta(minutes=3))


    @api.model
    def create(self,vals):
        """
        Create or update a signup record with OTP and expiration.
        """

        email = vals.get('email')
        name = vals.get('name')
        if not email or not name:
            raise UserError('Required Email and Name')

        record= self.search([('email','=',email)], limit=1)

        if record:
            record.write({
                'otp': str(random.randint(1000, 9999)),
                'otp_expiration': datetime.now() + timedelta(minutes=3)

            })
        else:
            vals['otp'] = str(random.randint(1000, 9999))
            vals['otp_expiration'] = datetime.now() + timedelta(minutes=3)
            record= super(Signup,self).create(vals)

        self.send_email(record)
        return record

    # def set_password(self, record_id, password):
    #     record = self.sudo().browse(record_id)
    #     if not record:
    #         raise UserError("Signup record not found.")
    #
    #     user = self.env['res.users'].sudo().search([('login', '=', record.email)], limit=1)
    #     if not user:
    #         raise UserError("No user found with the given email.")
    #
    #     user.sudo().write({'password': password})

    def send_email(self,record):
        body_html = f"""
                 <p>Hello,</p>
                 <p>Your OTP for verification is: <strong>{record.otp}</strong></p>
                 <p>The OTP will expire on: <strong>{record.otp_expiration}</strong></p>
                 <p>If you have any issues, please contact support.</p>
                 <p>Best regards,<br>Your Company</p>
                 """

        mail_values = {
            'subject': 'Your OTP for Verification',
            'body_html': body_html,
            'email_to': record.email,
            'email_from': 'neamul.bhuiyan@bjitgroup.com',  # Replace with your configured email
        }

        mail=self.env['mail.mail'].create(mail_values)
        mail.send()