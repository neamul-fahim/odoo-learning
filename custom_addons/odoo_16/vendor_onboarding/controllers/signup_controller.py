from odoo import http
from datetime import datetime, timedelta

class SignupController(http.Controller):
    @http.route('/signup', type='http', auth='public', methods=['GET', 'POST'])
    def handle_signup(self, **kw):
        if http.request.httprequest.method=='POST':
            email = kw.get('email')
            vals={'email':email}
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
            return http.request.render('vendor_onboarding.vendor_details_wizard_template',{
                'record_id':record_id})
        else:
            return http.request.render('vendor_onboarding.otp_page',{
                'error': 'Invalid or expired OTP. Please try again.',
                'email': email,
                'record_id': record_id,
            })

    @http.route('/vendor_details_form', methods=['GET','POST'], auth='public', type='http')
    def vendor_details_form(self, **kw):
        if http.request.httprequest.method=='POST':
            vals={}
            vals['signup_id'] = kw.get('record_id')
            vals['name'] = kw.get('name')
            vals['contact_number'] = kw.get('contact_number')
            vals['address'] = kw.get('address')
            vals['company_name'] = kw.get('company_name')

            record = http.request.env['vendor.details'].sudo().create(vals)
            return http.request.render('vendor_onboarding.welcome')
        if http.request.httprequest.method=='GET':
            pass