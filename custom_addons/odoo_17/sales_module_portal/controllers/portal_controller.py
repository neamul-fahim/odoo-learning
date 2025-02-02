from odoo.addons.portal.controllers.portal import CustomerPortal,pager

# from odoo.addons.sale.controllers.portal import CustomerPortal, pager
from odoo import http
from odoo.http import request

class Sales_module_Portal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)

        if 'quotation_count_portal' in counters:
            # user = request.env.user
            # partner = user.partner_id
            #
            # # Count quotations belonging to the current user
            # quotation_count = request.env['sale.order'].search_count([
            #     ('partner_id', '=', partner.id),
            #     ('state', 'in', ['draft', 'sent'])
            # ])

            values['quotation_count_portal'] = 1
        return values


    @http.route(['/my/all_sales', '/my/all_sales/page/<int:page>'], type='http', auth='user', methods=['GET'],
                website=True)
    def all_sales(self, page=1, sortby='id', **kw):
        # Define sort options
        sort_query_list = {
            'id': {'label': 'ID', 'order': 'id desc'},
        }
        default_order_by = sort_query_list[sortby]['order']

        # Check if the user has admin permissions
        user = request.env.user
        is_admin = user.has_group('sales_team.group_sale_manager')  # Adjust the group ID if needed
        has_all_docs_access = user.has_group('sales_team.group_sale_salesman_all_leads')

        # Define domain based on user permissions
        if is_admin or has_all_docs_access:
            domain = []
        else:
            domain = [('user_id', '=', user.id)]  # Filter sales related to the logged-in user

        # Get total count and fetch paginated records
        total_sales = request.env['sale.order'].sudo().search_count(domain)
        page_details = pager(
            url='/my/all_sales',
            total=total_sales,
            page=page,
            step=3,
            url_args={'sortby': sortby},
        )
        sale_counts = request.env['sale.order'].sudo().search(
            domain, limit=3, order=default_order_by, offset=page_details['offset']
        )

        # Prepare data for rendering
        vals = {
            'quotations': sale_counts,
            'page_name': 'all_sales',
            'pager': page_details,
            'sortby': sortby,
            'searchbar_sortings': sort_query_list,
        }
        return request.render('sales_module_portal.all_sales_order_portal_tree_view', vals)

    @http.route('/my/sale_order/<int:order_id>', type='http', auth='public', methods=['GET'], website=True)
    def sale_order(self, order_id, **kw):

        # vendor = http.request.env['sale.order'].sudo().browse(order_id)
        sale_order_record = http.request.env['sale.order'].sudo().browse(order_id)
        vals = {'doc': sale_order_record,
                'page_name': 'vendor_account_pending'
                }

        sale_order_records = http.request.env['sale.order'].search([])
        sale_order_records_ids = sale_order_records.mapped('id')

        sale_order_record_index = sale_order_records_ids.index(order_id)

        if sale_order_record_index > 0:
            vals['prev_record'] = f'/my/sale_order/{sale_order_records_ids[sale_order_record_index - 1]}'
        if sale_order_record_index < len(sale_order_records_ids) - 1:
            vals['next_record'] = f'/my/sale_order/{sale_order_records_ids[sale_order_record_index + 1]}'

        if not sale_order_record.exists():
            return http.request.not_found()

        # Render the form view template with the vendor data
        return http.request.render('sales_module_portal.sale_order_portal_form_view', vals)


    @http.route('/sale_order/new', type='http', auth='user', website=True)
    def sale_order_form(self, **kwargs):
        customers = request.env['res.partner'].search([])
        products = request.env['product.product'].search([])
        return request.render('sales_module_portal.sale_order_create_update_form_view', {
            'customers': customers,
            'products': products
        })

    @http.route('/sale_order/create', type='http', auth='user', methods=['POST'], website=True, csrf=True)
    def create_sale_order(self, **post):
        customer_id = int(post.get('customer_id'))
        product_id = int(post.get('product_id'))
        quantity = int(post.get('quantity'))

        order_line_values = [(0, 0, {
            'product_id': product_id,
            'product_uom_qty': quantity,
            'price_unit': request.env['product.product'].browse(product_id).list_price
        })]

        sale_order = request.env['sale.order'].create({
            'partner_id': customer_id,
            'order_line': order_line_values,
        })

        return request.redirect('/sale_order/success')

    @http.route('/sale_order/success', type='http', auth='user', website=True)
    def sale_order_success(self):
        return request.render('sales_module_portal.sale_order_success')

    @http.route('/sale_order/update_state', type='http', auth='user', methods=['POST'], website=True, csrf=True)
    def update_sale_order_state(self, **post):
        order_id = int(post.get('order_id'))
        new_state = post.get('new_state')
        print(f'========================{order_id} {new_state}')
        # Fetch the sale order using the provided order_id
        sale_order = request.env['sale.order'].browse(order_id)

        # Check if the order exists
        if not sale_order:
            return request.redirect('/sale_order/error')

        # Check if the new_state is valid
        valid_states = ['draft', 'sent', 'sale']
        if new_state not in valid_states:
            return request.redirect('/sale_order/error')

        # Update the state of the sale order
        sale_order.write({'state': new_state})

        # Redirect back to the quotations page or show success message
        # return request.redirect('/my/quotations')