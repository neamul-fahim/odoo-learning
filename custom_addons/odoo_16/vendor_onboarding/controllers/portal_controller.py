from odoo import http
from odoo.addons.portal.controllers import portal


# for portal user
class VendorAccountPortal(portal.CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)

        if 'vendor_count' in counters:
            user = http.request.env.user
            vendor_count = 0
            # Get the current user's email
            user_email = http.request.env.user.login

            # Find the corresponding signup record
            signup_record = http.request.env['signup'].sudo().search([('email', '=', user_email)], limit=1)

            if signup_record:
                # Count the vendor.details records linked to this signup record
                vendor_count = http.request.env['vendor.details'].sudo().search_count(
                    [('signup_id', '=', signup_record.id)])

            values['vendor_count'] = vendor_count

        if 'vendor_dashboard' in counters:
            vendor_dashboard_count = 1
            values['vendor_dashboard'] = vendor_dashboard_count

        return values


    @http.route('/my/vendor_dashboard', type='http', auth='public', methods=['GET'],website=True)
    def vendor_dashboard(self, **kw):
        return http.request.render("vendor_onboarding.vendor_dashboard_template")



    @http.route('/my/vendor_account', type='http', auth='public', methods=['GET'])
    def vendor_account(self,**kw):
        # Fetch the record from the model
        email = http.request.env.user.login
        signup_record = http.request.env['signup'].sudo().search([('email', '=', email)], limit=1)
        if not signup_record:
            return http.request.not_found()

        vendor_details_record = http.request.env['vendor.details'].sudo().search([('signup_id', '=', signup_record.id)], limit=1)

        if not vendor_details_record:
            return http.request.not_found()

        return http.request.render('vendor_onboarding.vendor_details_portal_form',{'record':vendor_details_record})



# for internal user
class AllVendorAccountsPortal(portal.CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)

        if 'all_vendor_counts' in counters:

            all_vendor_counts = http.request.env['vendor.details'].sudo().search_count([])

            values['all_vendor_counts'] = all_vendor_counts

        return values

    @http.route('/my/all_vendor_accounts', type='http', auth='public', methods=['GET'], website=True)
    def all_vendor_accounts(self, **kw):
        vendor_counts = http.request.env['vendor.details'].sudo().search([])
        return http.request.render('vendor_onboarding.all_vendor_accounts_portal_tree_view',{'vendor_counts':vendor_counts})

    @http.route('/my/vendor_account_pending/<int:vendor_id>',type='http', auth='public', methods=['GET'], website=True)
    def vendor_account_pending(self,vendor_id, **kw):

        print(f"vendor id ==== {vendor_id}")
        vendor = http.request.env['vendor.details'].sudo().browse(vendor_id)

        if not vendor.exists():
            return http.request.not_found()

        # Render the form view template with the vendor data
        return http.request.render('vendor_onboarding.vendor_details_portal_form',{'record':vendor})
