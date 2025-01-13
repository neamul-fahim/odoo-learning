from odoo import http
from odoo.addons.portal.controllers.portal import CustomerPortal,pager


# for portal user
class VendorAccountPortal(CustomerPortal):
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
                vendor_count = http.request.env['vendor.details'].sudo().search_count(
                    [('signup_id', '=', signup_record.id)])

            # values['vendor_count'] = vendor_count
            values['vendor_count'] = 1

        if 'vendor_dashboard' in counters:
            vendor_dashboard_count = 1
            values['vendor_dashboard'] = vendor_dashboard_count

        return values


    @http.route('/my/vendor_dashboard', type='http', auth='public', methods=['GET'],website=True)
    def vendor_dashboard(self, **kw):
        return http.request.render("vendor_onboarding.vendor_dashboard_template",
                                   # {
                                   #     'session_info': http.request.env['ir.http'].get_frontend_session_info(),
                                   # }
                                   )



    @http.route('/my/vendor_account', type='http', auth='public', methods=['GET'], website=True)
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
class AllVendorAccountsPortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)

        if 'all_vendor_counts' in counters:

            all_vendor_counts = http.request.env['vendor.details'].sudo().search_count([])

            values['all_vendor_counts'] = 2

        return values

    # @http.route('/my/all_vendor_accounts', type='http', auth='public', methods=['GET'], website=True)
    # def all_vendor_accounts(self, **kw):
    #     vendor_counts = http.request.env['vendor.details'].sudo().search([])
    #     vals={'vendor_counts': vendor_counts,
    #           'page_name': 'all_vendor_accounts',
    #           }
    #     return http.request.render('vendor_onboarding.all_vendor_accounts_portal_tree_view',vals)

    @http.route(['/my/all_vendor_accounts', '/my/all_vendor_accounts/page/<int:page>'], type='http', auth='public',
                methods=['GET'], website=True)
    def all_vendor_accounts(self, page=1, sortby='id', **kw):
        sort_query_list = {
            'id': {'label': 'ID', 'order': 'id desc'},
            'name': {'label': 'Name', 'order': 'name'},
        }

        default_order_by = sort_query_list[sortby]['order']


        total_vendor = http.request.env['vendor.details'].sudo().search_count([])
        page_details = pager(url='/my/all_vendor_accounts',
                             total=total_vendor,
                             page=page,
                             step=3,
                             url_args={'sortby': sortby}
                             )
        vendor_counts = http.request.env['vendor.details'].sudo().search([], limit=3,order=default_order_by, offset=page_details['offset'])
        vals = {'vendor_counts': vendor_counts,
                'page_name': 'all_vendor_accounts',
                'pager': page_details,
                'sortby': sortby,
                'searchbar_sortings': sort_query_list
                }
        return http.request.render('vendor_onboarding.all_vendor_accounts_portal_tree_view', vals)

    @http.route('/my/vendor_account_pending/<int:vendor_id>',type='http', auth='public', methods=['GET'], website=True)
    def vendor_account_pending(self,vendor_id, **kw):

        vendor = http.request.env['vendor.details'].sudo().browse(vendor_id)
        vals={'record': vendor,
              'page_name': 'vendor_account_pending'
              }

        vendors = http.request.env['vendor.details'].search([])
        vendors_ids = vendors.mapped('id')

        vendor_index = vendors_ids.index(vendor_id)

        if vendor_index > 0:
            vals['prev_record'] = f'/my/vendor_account_pending/{vendors_ids[vendor_index-1]}'
        if vendor_index < len(vendors_ids) -1:
            vals['next_record'] = f'/my/vendor_account_pending/{vendors_ids[vendor_index+1]}'

        if not vendor.exists():
            return http.request.not_found()

        # Render the form view template with the vendor data
        return http.request.render('vendor_onboarding.vendor_details_portal_form',vals)
