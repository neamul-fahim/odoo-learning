from odoo import models, fields, api
import random
from datetime import datetime, timedelta

class SignupRequest(models.Model):
    _name = 'signup.otp.request'
    _description = 'Signup Request'

    email = fields.Char(string='Email', required=True)
    otp = fields.Char(string='OTP', required=True)
    otp_expiration = fields.Datetime(string='OTP Expiration',
                                     default=lambda self: datetime.now() + timedelta(minutes=4))

    @api.model
    def create_otp(self, email):
        existing_request = self.search([('email', '=', email)], limit=1)

        if existing_request:
            otp = str(random.randint(100000, 999999))
            expiration = datetime.now() + timedelta(minutes=4)
            existing_request.write({
                'otp': otp,
                'otp_expiration': expiration,
            })
            signup_request = existing_request
        else:
            otp = str(random.randint(100000, 999999))
            expiration = datetime.now() + timedelta(minutes=4)
            signup_request = self.create({
                'email': email,
                'otp': otp,
                'otp_expiration': expiration,
            })

        self.send_email(signup_request)

        print(f'signup_request----{signup_request.otp}')
        return signup_request



    @api.model
    def send_email(self, signup_request):
        body_html = f"""
          <p>Hello,</p>
          <p>Your OTP for verification is: <strong>{signup_request.otp}</strong></p>
          <p>The OTP will expire on: <strong>{signup_request.otp_expiration}</strong></p>
          <p>If you have any issues, please contact support.</p>
          <p>Best regards,<br>Your Company</p>
          """

        mail_values = {
            'subject': 'Your OTP for Verification',
            'body_html': body_html,
            'email_to': signup_request.email,
            'email_from': 'neamul.bhuiyan@bjitgroup.com',  # Replace with your configured email
        }

        # Create and send the email
        mail = self.env['mail.mail'].create(mail_values)
        mail.send()