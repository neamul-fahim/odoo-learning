from odoo import http
from datetime import datetime, timedelta


class VendorDetailsController(http.Controller):
    @http.route('/vendor_details_form', methods=['GET', 'POST'], auth='public', type='http')
    def vendor_details_form(self, **kw):
        if http.request.httprequest.method == 'POST':

            vals = {'signup_id': kw.get('record_id'),
                    'name': kw.get('name'),
                    'contact_number': kw.get('contact_number'),
                    'address': kw.get('address'),
                    'company_name': kw.get('company_name')}

            record = http.request.env['vendor.details'].sudo().create(vals)
            print(f'vendor details----------------{record}')
            # return http.request.render('vendor_onboarding.welcome')
            return http.request.redirect('/my')

        if http.request.httprequest.method == 'GET':
            pass