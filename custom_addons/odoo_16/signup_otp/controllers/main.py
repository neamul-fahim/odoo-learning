from odoo import http
from odoo.http import request
from datetime import datetime


class SignupController(http.Controller):

    @http.route('/signup_otp', type='http', auth='public', methods=['GET', 'POST'], website=True)
    def handle_signup(self, **kw):
        if request.httprequest.method == 'POST':
            email = kw.get('email')
            if email:
                print(f'email--{email}')
                # Create an OTP and store it with an expiration time
                signup_request = request.env['signup.otp.request'].create_otp(email)
                # Redirect to the OTP verification page
                print(f'signup request------{signup_request.otp}')
                return request.render('signup_otp.otp_verification_page', {
                    'signup_request_id': signup_request.id,
                })
        return request.render('signup_otp.signup_page')

    @http.route('/verify_otp', type='http', auth='public', methods=['POST'], website=True)
    def verify_otp(self, **kw):
        otp = kw.get('otp')
        signup_request_id = int(kw.get('signup_request_id'))
        signup_request = request.env['signup.otp.request'].sudo().browse(signup_request_id)

        if signup_request.otp == otp and datetime.now() <= signup_request.otp_expiration:
            # OTP is valid and not expired
            return request.render('signup_otp.welcome_page')
        else:
            # OTP is invalid or expired
            return request.render('signup_otp.otp_verification_page', {
                'error': 'Invalid or expired OTP. Please try again.',
                'signup_request_id': signup_request_id,
            })
