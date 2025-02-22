from odoo import http
from datetime import datetime, timedelta


class SignupController(http.Controller):
    @http.route('/signup', type='http', auth='public', methods=['GET', 'POST'])
    def handle_signup(self, **kw):
        if http.request.httprequest.method=='POST':
            email = kw.get('email')
            name = kw.get('name')

            vals={'email':email,
                  'name': name,
                  }
            if email:
                record = http.request.env['signup'].sudo().create(vals)
                return http.request.render('vendor_onboarding.otp_page',{
                    'email':record.email,'record_id': record.id })

        return http.request.render('vendor_onboarding.signup_page')

    @http.route('/otp_verification', type='http', auth='public', methods=['POST'])
    def otp_verification(self, **kw):
        otp = kw.get('otp-code')
        record_id = int(kw.get('record_id'))
        email = kw.get('email')
        print(f'otp = {otp} record_id = {record_id}')

        record = http.request.env['signup'].sudo().browse(record_id)
        if record and record.otp == otp and datetime.now() <= record.otp_expiration:
            portal_group_id = http.request.env.ref('base.group_portal').sudo().id

            user = http.request.env['res.users'].sudo().create({
                'login': record.email,
                'name': record.name,
                'groups_id': [(6, 0, [portal_group_id])],  # Correct format for groups_id
            })

            return http.request.render('vendor_onboarding.set_password',{
                'user_id':user.id,
                'record_id': record.id,
            })
        else:
            return http.request.render('vendor_onboarding.otp_page',{
                'error': 'Invalid or expired OTP. Please try again.',
                'email': email,
                'record_id': record_id,
            })

    @http.route('/set_password', type='http', auth='public', methods=['POST'])
    def set_password(self, **kw):
        password = kw.get('password')
        user_id = kw.get('user_id')
        record_id = kw.get('record_id')

        if not password or not user_id:
            return http.request.render('vendor_onboarding.set_password', {
                'error': 'Password or record ID missing',
                'user_id': user_id,
            })

        try:
            user_id = int(user_id)
        except ValueError:
            return http.request.render('vendor_onboarding.set_password', {
                'error': 'Invalid record ID',
                'user_id': user_id,
            })

        user = http.request.env['res.users'].sudo().browse(user_id)
        if user.exists():
            user.write({'password':password})
            return http.request.render('vendor_onboarding.vendor_details_wizard_template', {
                'record_id': record_id,
            })
        else:
            return http.request.render('vendor_onboarding.set_password', {
                'error': 'Record not found',
                'user_id': user_id,
            })

