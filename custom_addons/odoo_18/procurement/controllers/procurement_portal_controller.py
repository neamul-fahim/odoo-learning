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

    @http.route(['/procurement_order/report/pdf/<int:order_id>'], type='http', auth="public", website=True)
    def procurement_order_report_pdf(self, order_id, **kwargs):
        # Load the procurement order with sudo() to bypass record rules.
        order = request.env['procurement.order'].sudo().browse(order_id)
        if not order.exists() or order.state != 'approved':
            return request.not_found()

        # Retrieve the report action record using sudo() on the environment.
        report_action = request.env.ref('procurement.action_procurement_order_report').sudo()
        # Render the PDF report.
        pdf, _ = report_action._render_qweb_pdf(report_action.report_name, [order_id])

        # Set response headers to force the browser to download the PDF.
        headers = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(pdf)),
            ('Content-Disposition', 'attachment; filename="procurement_order_%s.pdf"' % order_id),
        ]
        return request.make_response(pdf, headers=headers)

