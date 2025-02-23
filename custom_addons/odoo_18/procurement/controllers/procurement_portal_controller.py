from odoo.addons.portal.controllers.portal import CustomerPortal,pager
from odoo import http
from odoo.http import request

class ProcurementModulePortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)

        if 'procurement_order_count' in counters:
            user = request.env.user

            # Count quotations belonging to the current user
            procurement_order_count = request.env['procurement.order'].sudo().search_count([('vendor_id', '=', user.id)])
            print(f'procurement_order_count---  {procurement_order_count}')
            values['procurement_order_count'] = procurement_order_count
        return values


    @http.route(['/my/procurement_orders', '/my/procurement_orders/page/<int:page>'], type='http', auth='user', methods=['GET'],
                website=True)
    def procurement_orders(self, page=1, sortby='id', **kw):
        # Define sort options
        sort_query_list = {
            'id': {'label': 'ID', 'order': 'id desc'},
            'state': {'label': 'State', 'order': 'state'},
            'total_amount': {'label': 'Total', 'order': 'total_amount desc'},
        }
        default_order_by = sort_query_list[sortby]['order']

        # Check if the user has admin permissions
        user = request.env.user

        domain = [('vendor_id', '=', user.id)]

        # Get total count and fetch paginated records
        procurement_order_count = request.env['procurement.order'].sudo().search_count(domain)
        page_details = pager(
            url='/my/procurement_orders',
            total=procurement_order_count,
            page=page,
            step=10,
            url_args={'sortby': sortby},
        )
        procurement_orders = request.env['procurement.order'].sudo().search(
            domain, limit=10, order=default_order_by, offset=page_details['offset']
        )

        # Prepare data for rendering
        vals = {
            'procurement_orders': procurement_orders,
            'page_name': 'procurement_orders',
            'pager': page_details,
            'sortby': sortby,
            'searchbar_sortings': sort_query_list,
        }
        return request.render('procurement.procurement_order_tree_view_portal', vals)

    @http.route('/my/procurement_order/<int:order_id>', type='http', auth='public', methods=['GET'], website=True)
    def procurement_order(self, order_id, **kw):
        user = request.env.user
        order = http.request.env['procurement.order'].sudo().browse(order_id)
        if not order.exists():
            return http.request.not_found()
        vals = {
            'procurement_order': order,
            'page_name': 'procurement_order',
        }
        domain = [('vendor_id', '=', user.id)]
        orders = http.request.env['procurement.order'].sudo().search(domain)
        order_ids = orders.mapped('id')

        order_index = order_ids.index(order_id)

        if order_index > 0:
            vals['prev_record'] = f'/my/procurement_order/{order_ids[order_index - 1]}'
        if order_index < len(order_ids) - 1:
            vals['next_record'] = f'/my/procurement_order/{order_ids[order_index + 1]}'

        return http.request.render('procurement.procurement_order_form_view_portal', vals)


    # @http.route('/sale_order/new', type='http', auth='user', website=True)
    # def sale_order_form(self, **kwargs):
    #     customers = request.env['res.partner'].sudo().search([])
    #     products = request.env['product.product'].sudo().search([])
    #     return request.render('sales_module_portal.sale_order_create_update_form_view', {
    #         'customers': customers,
    #         'products': products
    #     })
    #
    # @http.route('/sale_order/create', type='http', auth='user', methods=['POST'], website=True, csrf=True)
    # def create_sale_order(self, **post):
    #     customer_id = int(post.get('customer_id'))
    #     product_ids = request.httprequest.form.getlist('product_ids[]')
    #     # product_ids = post.get('product_ids[]', [])
    #
    #     print(f'product==============={product_ids}')
    #     if not product_ids:
    #         return request.redirect('/sale_order/failure')
    #
    #     # Convert product_ids to integers and handle quantities
    #     order_lines = []
    #     for product_id in product_ids:
    #         product_id = int(product_id)
    #         quantity = int(post.get(f'quantity_{product_id}', 1))  # Get quantity for each product
    #
    #         order_line_values = (0, 0, {
    #             'product_id': product_id,
    #             'product_uom_qty': quantity,
    #             'price_unit': request.env['product.product'].sudo().browse(product_id).list_price
    #         })
    #
    #         order_lines.append(order_line_values)
    #
    #     # Create the sale order
    #     sale_order = request.env['sale.order'].sudo().create({
    #         'partner_id': customer_id,
    #         'order_line': order_lines,
    #     })
    #
    #     return request.redirect(f'/my/sale_order/{sale_order.id}')
    #
    # # @http.route('/sale_order/success', type='http', auth='user', website=True)
    # # def sale_order_success(self):
    # #     return request.render('sales_module_portal.sale_order_success')
    #
    # @http.route('/sale_order/update_state', type='http', auth='user', methods=['POST'], website=True, csrf=True)
    # def update_sale_order_state(self, **post):
    #     order_id = int(post.get('order_id'))
    #     new_state = post.get('new_state')
    #     # Fetch the sale order using the provided order_id
    #     sale_order = request.env['sale.order'].sudo().browse(order_id)
    #
    #     # Check if the order exists
    #     if not sale_order:
    #         return request.redirect('/sale_order/error')
    #
    #     # Check if the new_state is valid
    #     valid_states = ['draft', 'sent', 'sale', 'cancel']
    #     if new_state not in valid_states:
    #         return request.redirect('/sale_order/error')
    #
    #     # Update the state of the sale order
    #     sale_order.write({'state': new_state})
    #     sale_order_record = http.request.env['sale.order'].sudo().browse(order_id)
    #     if not sale_order_record.exists():
    #         return http.request.not_found()
    #     vals = {
    #         'doc': sale_order_record,
    #         'page_name': 'sale_order',
    #     }
    #
    #     # Redirect back to the quotations page or show success message
    #     return http.request.render('sales_module_portal.sale_order_portal_form_view', vals)
